"""
Neural network modules for GNN-SAC.

Contains:
- GNNBackbone: Graph neural network that processes game state graphs
- Actor: Stochastic policy network with continuous turn/thrust/shoot
- TwinCritics: Twin Q-networks for SAC value estimation
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATv2Conv
from typing import Tuple, Optional
import math


class GNNBackbone(nn.Module):
    """
    Graph neural network that produces a player state embedding.

    Architecture:
    - Projects player and asteroid nodes to a common hidden dimension
    - Applies multiple GATv2Conv layers for message passing (asteroid -> player)
    - Extracts the player node embedding as the state representation

    GATv2Conv is used because it supports edge attributes and has been shown
    to be more expressive than the original GAT for certain tasks.
    """

    def __init__(
        self,
        player_dim: int = 5,
        asteroid_dim: int = 3,
        edge_dim: int = 7,
        hidden_dim: int = 64,
        num_layers: int = 2,
        dropout: float = 0.0,
        heads: int = 4,
    ):
        """
        Initialize the GNN backbone.

        Args:
            player_dim: Dimension of player node features.
            asteroid_dim: Dimension of asteroid node features.
            edge_dim: Dimension of edge features.
            hidden_dim: Hidden dimension for all layers.
            num_layers: Number of GNN message passing layers.
            dropout: Dropout probability.
            heads: Number of attention heads for GATv2Conv.
        """
        super().__init__()

        self.player_dim = player_dim
        self.asteroid_dim = asteroid_dim
        self.edge_dim = edge_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.dropout = dropout
        self.heads = heads

        # Project all nodes to same dimension
        self.player_proj = nn.Linear(player_dim, hidden_dim)
        self.asteroid_proj = nn.Linear(asteroid_dim, hidden_dim)

        # GNN layers with multi-head attention
        # Each layer outputs hidden_dim (using concat=False to average heads)
        self.gnn_layers = nn.ModuleList([
            GATv2Conv(
                hidden_dim,
                hidden_dim,
                heads=heads,
                edge_dim=edge_dim,
                add_self_loops=False,
                concat=False,  # Average heads instead of concatenating
            )
            for _ in range(num_layers)
        ])

        # Layer normalization for stability
        self.layer_norms = nn.ModuleList([
            nn.LayerNorm(hidden_dim)
            for _ in range(num_layers)
        ])

    def forward(
        self,
        player_feat: torch.Tensor,
        asteroid_feat: torch.Tensor,
        edge_index: torch.Tensor,
        edge_attr: torch.Tensor,
    ) -> torch.Tensor:
        """
        Forward pass through the GNN.

        Args:
            player_feat: [batch_size, player_dim] - Player node features
            asteroid_feat: [total_asteroids, asteroid_dim] - Asteroid node features
            edge_index: [2, total_edges] - Edge indices (asteroid_local_idx -> player_batch_idx)
            edge_attr: [total_edges, edge_dim] - Edge features

        Returns:
            player_embedding: [batch_size, hidden_dim] - State embedding for actor/critic
        """
        batch_size = player_feat.size(0)

        # Project to hidden dim
        h_player = F.relu(self.player_proj(player_feat))  # [batch_size, hidden_dim]

        if asteroid_feat.size(0) == 0:
            # No asteroids - just return projected player features
            return h_player

        h_asteroid = F.relu(self.asteroid_proj(asteroid_feat))  # [total_asteroids, hidden_dim]

        # Concatenate nodes: players first (indices 0 to batch_size-1),
        # then asteroids (indices batch_size to batch_size + total_asteroids - 1)
        x = torch.cat([h_player, h_asteroid], dim=0)

        # Adjust edge_index: asteroid source indices need to be offset by batch_size
        # edge_index[0] = asteroid local indices -> add batch_size
        # edge_index[1] = player batch indices -> already correct
        adjusted_edge_index = edge_index.clone()
        adjusted_edge_index[0] = adjusted_edge_index[0] + batch_size

        # Message passing with residual connections
        for i, (gnn, ln) in enumerate(zip(self.gnn_layers, self.layer_norms)):
            x_new = gnn(x, adjusted_edge_index, edge_attr)
            x_new = F.relu(x_new)

            # Residual connection
            x = x + x_new
            x = ln(x)

            if self.dropout > 0 and self.training:
                x = F.dropout(x, p=self.dropout, training=self.training)

        # Extract player embeddings (first batch_size nodes)
        player_embedding = x[:batch_size]

        return player_embedding


class Actor(nn.Module):
    """
    Stochastic policy network for SAC.

    Outputs:
    - Turn: Squashed Gaussian distribution -> [-1, 1]
    - Thrust: Squashed Gaussian distribution -> [0, 1]
    - Shoot: Squashed Gaussian distribution -> [0, 1]

    The squashing correction (tanh for turn, sigmoid for thrust) is applied
    to compute proper log probabilities for the entropy bonus.
    """

    def __init__(
        self,
        state_dim: int = 64,
        hidden_dim: int = 256,
        log_std_min: float = -20.0,
        log_std_max: float = 2.0,
    ):
        """
        Initialize the actor network.

        Args:
            state_dim: Dimension of the state embedding from GNN.
            hidden_dim: Hidden dimension for the MLP.
            log_std_min: Minimum log standard deviation (for numerical stability).
            log_std_max: Maximum log standard deviation.
        """
        super().__init__()

        self.log_std_min = log_std_min
        self.log_std_max = log_std_max

        # Shared MLP backbone
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )

        # Turn head: outputs mean and log_std for Gaussian
        self.turn_mean = nn.Linear(hidden_dim, 1)
        self.turn_log_std = nn.Linear(hidden_dim, 1)

        # Thrust head: outputs mean and log_std for Gaussian
        self.thrust_mean = nn.Linear(hidden_dim, 1)
        self.thrust_log_std = nn.Linear(hidden_dim, 1)

        # Shoot head: outputs mean and log_std for Gaussian (squashed to [0, 1])
        self.shoot_mean = nn.Linear(hidden_dim, 1)
        self.shoot_log_std = nn.Linear(hidden_dim, 1)

    def forward(
        self,
        state: torch.Tensor,
        deterministic: bool = False,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Sample actions from the policy.

        Args:
            state: [batch_size, state_dim] - State embedding from GNN.
            deterministic: If True, use mean actions (for evaluation).

        Returns:
            action: [batch_size, 3] - Actions [turn, thrust, shoot]
                   turn in [-1, 1], thrust in [0, 1], shoot in [0, 1]
            log_prob: [batch_size, 1] - Log probability of the action
        """
        h = self.net(state)

        # === Turn (squashed Gaussian -> [-1, 1]) ===
        turn_mean = self.turn_mean(h)
        turn_log_std = torch.clamp(self.turn_log_std(h), self.log_std_min, self.log_std_max)
        turn_std = torch.exp(turn_log_std)

        # === Thrust (squashed Gaussian -> [0, 1]) ===
        thrust_mean = self.thrust_mean(h)
        thrust_log_std = torch.clamp(self.thrust_log_std(h), self.log_std_min, self.log_std_max)
        thrust_std = torch.exp(thrust_log_std)

        # === Shoot (squashed Gaussian -> [0, 1]) ===
        shoot_mean = self.shoot_mean(h)
        shoot_log_std = torch.clamp(self.shoot_log_std(h), self.log_std_min, self.log_std_max)
        shoot_std = torch.exp(shoot_log_std)

        if deterministic:
            # Use mean actions
            turn = torch.tanh(turn_mean)
            thrust = torch.sigmoid(thrust_mean)
            shoot = torch.sigmoid(shoot_mean)
            log_prob = torch.zeros(state.size(0), 1, device=state.device)
        else:
            # Sample from distributions
            turn_dist = torch.distributions.Normal(turn_mean, turn_std)
            turn_sample = turn_dist.rsample()  # Reparameterization trick
            turn = torch.tanh(turn_sample)

            thrust_dist = torch.distributions.Normal(thrust_mean, thrust_std)
            thrust_sample = thrust_dist.rsample()
            thrust = torch.sigmoid(thrust_sample)

            shoot_dist = torch.distributions.Normal(shoot_mean, shoot_std)
            shoot_sample = shoot_dist.rsample()
            shoot = torch.sigmoid(shoot_sample)

            # === Compute log probabilities with squashing correction ===
            # For tanh squashing: log_prob = log_prob_gaussian - log(1 - tanh^2(x))
            # For sigmoid squashing: log_prob = log_prob_gaussian - log(sigmoid(x) * (1 - sigmoid(x)))

            # Turn log prob
            log_prob_turn = turn_dist.log_prob(turn_sample)
            log_prob_turn = log_prob_turn - torch.log(1 - turn.pow(2) + 1e-6)

            # Thrust log prob
            log_prob_thrust = thrust_dist.log_prob(thrust_sample)
            log_prob_thrust = log_prob_thrust - torch.log(thrust * (1 - thrust) + 1e-6)

            # Shoot log prob
            log_prob_shoot = shoot_dist.log_prob(shoot_sample)
            log_prob_shoot = log_prob_shoot - torch.log(shoot * (1 - shoot) + 1e-6)

            # Sum log probs (assuming independence)
            log_prob = log_prob_turn + log_prob_thrust + log_prob_shoot

        # Concatenate actions
        action = torch.cat([turn, thrust, shoot], dim=-1)

        return action, log_prob


class TwinCritics(nn.Module):
    """
    Twin Q-networks for SAC.

    Uses two independent Q-networks to reduce overestimation bias.
    The minimum of the two Q-values is used for the Bellman target.
    """

    def __init__(
        self,
        state_dim: int = 64,
        action_dim: int = 3,
        hidden_dim: int = 256,
    ):
        """
        Initialize the twin critics.

        Args:
            state_dim: Dimension of the state embedding from GNN.
            action_dim: Dimension of the action vector (3: turn, thrust, shoot).
            hidden_dim: Hidden dimension for the MLPs.
        """
        super().__init__()

        # Q1 network
        self.q1 = nn.Sequential(
            nn.Linear(state_dim + action_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

        # Q2 network
        self.q2 = nn.Sequential(
            nn.Linear(state_dim + action_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(
        self,
        state: torch.Tensor,
        action: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Compute Q-values for both critics.

        Args:
            state: [batch_size, state_dim] - State embedding.
            action: [batch_size, action_dim] - Action vector.

        Returns:
            q1: [batch_size, 1] - Q-value from first critic.
            q2: [batch_size, 1] - Q-value from second critic.
        """
        x = torch.cat([state, action], dim=-1)
        return self.q1(x), self.q2(x)

    def q1_forward(self, state: torch.Tensor, action: torch.Tensor) -> torch.Tensor:
        """Compute Q-value from Q1 only (for actor loss)."""
        x = torch.cat([state, action], dim=-1)
        return self.q1(x)
