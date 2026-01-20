import math
from typing import Dict, Tuple

import torch
import torch.nn as nn
import torch.optim as optim

from training.config.sac import SACConfig
from training.methods.sac.networks import GNNBackbone, Actor, TwinCritics


class SACLearner:
    """Minimal SAC learner for GNN-based state embeddings."""
    def __init__(self, device: torch.device, config: SACConfig):
        self.device = device
        self.config = config

        self.gnn = GNNBackbone(
            player_dim=5,
            asteroid_dim=3,
            edge_dim=7,
            hidden_dim=config.GNN_HIDDEN_DIM,
            num_layers=config.GNN_NUM_LAYERS,
            dropout=config.GNN_DROPOUT,
            heads=config.GNN_HEADS,
        ).to(device)

        self.actor = Actor(
            state_dim=config.GNN_HIDDEN_DIM,
            hidden_dim=config.ACTOR_HIDDEN_DIM,
        ).to(device)

        self.critics = TwinCritics(
            state_dim=config.GNN_HIDDEN_DIM,
            action_dim=3,
            hidden_dim=config.CRITIC_HIDDEN_DIM,
        ).to(device)

        self.target_critics = TwinCritics(
            state_dim=config.GNN_HIDDEN_DIM,
            action_dim=3,
            hidden_dim=config.CRITIC_HIDDEN_DIM,
        ).to(device)
        self.target_critics.load_state_dict(self.critics.state_dict())
        self.target_critics.eval()

        self.actor_optimizer = optim.Adam(
            list(self.gnn.parameters()) + list(self.actor.parameters()),
            lr=config.ACTOR_LR
        )
        self.critic_optimizer = optim.Adam(self.critics.parameters(), lr=config.CRITIC_LR)

        self.auto_entropy = config.AUTO_ENTROPY
        if self.auto_entropy:
            self.log_alpha = torch.tensor(
                math.log(config.INIT_ALPHA),
                dtype=torch.float32,
                requires_grad=True,
                device=device
            )
            self.alpha_optimizer = optim.Adam([self.log_alpha], lr=config.ALPHA_LR)
            self.target_entropy = config.TARGET_ENTROPY
        else:
            self.log_alpha = torch.tensor(math.log(config.INIT_ALPHA), device=device)
            self.alpha_optimizer = None
            self.target_entropy = None

        self.grad_clip = config.GRAD_CLIP_NORM

    @property
    def alpha(self) -> torch.Tensor:
        return self.log_alpha.exp()

    def select_action(
        self,
        graph_tensors: Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor],
        deterministic: bool = False
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Select action from the current policy."""
        self.gnn.eval()
        self.actor.eval()

        with torch.no_grad():
            player_feat, asteroid_feat, edge_index, edge_attr = graph_tensors
            state = self.gnn(player_feat, asteroid_feat, edge_index, edge_attr)
            action, log_prob = self.actor(state, deterministic=deterministic)

        self.gnn.train()
        self.actor.train()
        return action, log_prob

    def update(
        self,
        batch: Tuple[
            torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor,
            torch.Tensor, torch.Tensor,
            torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor,
            torch.Tensor
        ],
    ) -> Dict[str, float]:
        """Run one SAC update step."""
        (
            obs_player,
            obs_asteroid,
            obs_edge_index,
            obs_edge_attr,
            actions,
            rewards,
            next_player,
            next_asteroid,
            next_edge_index,
            next_edge_attr,
            dones,
        ) = batch

        # Compute state embeddings for critic update (detach to avoid double-backprop through GNN)
        state = self.gnn(obs_player, obs_asteroid, obs_edge_index, obs_edge_attr).detach()

        with torch.no_grad():
            next_state = self.gnn(next_player, next_asteroid, next_edge_index, next_edge_attr)
            next_action, next_log_prob = self.actor(next_state, deterministic=False)
            target_q1, target_q2 = self.target_critics(next_state, next_action)
            target_q = torch.min(target_q1, target_q2) - self.alpha * next_log_prob
            target = rewards + (1.0 - dones) * self.config.GAMMA * target_q

        # Critic update
        q1, q2 = self.critics(state, actions)
        critic_loss = nn.functional.mse_loss(q1, target) + nn.functional.mse_loss(q2, target)

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        if self.grad_clip is not None:
            nn.utils.clip_grad_norm_(self.critics.parameters(), self.grad_clip)
        self.critic_optimizer.step()

        # Actor update (fresh graph so GNN can be optimized with actor)
        state_actor = self.gnn(obs_player, obs_asteroid, obs_edge_index, obs_edge_attr)
        new_action, log_prob = self.actor(state_actor, deterministic=False)
        q1_pi = self.critics.q1_forward(state_actor, new_action)
        actor_loss = (self.alpha * log_prob - q1_pi).mean()

        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        if self.grad_clip is not None:
            nn.utils.clip_grad_norm_(
                list(self.gnn.parameters()) + list(self.actor.parameters()),
                self.grad_clip
            )
        self.actor_optimizer.step()

        # Alpha / entropy update
        alpha_loss = torch.tensor(0.0, device=self.device)
        if self.auto_entropy:
            alpha_loss = -(self.log_alpha * (log_prob + self.target_entropy).detach()).mean()
            self.alpha_optimizer.zero_grad()
            alpha_loss.backward()
            self.alpha_optimizer.step()

        # Target network soft update
        with torch.no_grad():
            for tgt, src in zip(self.target_critics.parameters(), self.critics.parameters()):
                tgt.copy_(tgt * (1.0 - self.config.TAU) + src * self.config.TAU)

        metrics = {
            "critic_loss": float(critic_loss.item()),
            "actor_loss": float(actor_loss.item()),
            "alpha_loss": float(alpha_loss.item()),
            "alpha_value": float(self.alpha.item()),
            "q1_mean": float(q1.mean().item()),
            "q2_mean": float(q2.mean().item()),
        }
        return metrics

    def state_dict(self) -> Dict[str, object]:
        return {
            "gnn": self.gnn.state_dict(),
            "actor": self.actor.state_dict(),
            "critics": self.critics.state_dict(),
            "target_critics": self.target_critics.state_dict(),
            "log_alpha": self.log_alpha.detach().cpu().item(),
            "actor_optimizer": self.actor_optimizer.state_dict(),
            "critic_optimizer": self.critic_optimizer.state_dict(),
            "alpha_optimizer": self.alpha_optimizer.state_dict() if self.alpha_optimizer else None,
        }

    def load_state_dict(self, state: Dict[str, object]) -> None:
        self.gnn.load_state_dict(state["gnn"])
        self.actor.load_state_dict(state["actor"])
        self.critics.load_state_dict(state["critics"])
        if "target_critics" in state:
            self.target_critics.load_state_dict(state["target_critics"])
        if "log_alpha" in state:
            self.log_alpha.data = torch.tensor(float(state["log_alpha"]), device=self.device)
        if "actor_optimizer" in state:
            self.actor_optimizer.load_state_dict(state["actor_optimizer"])
        if "critic_optimizer" in state:
            self.critic_optimizer.load_state_dict(state["critic_optimizer"])
        if self.alpha_optimizer and state.get("alpha_optimizer"):
            self.alpha_optimizer.load_state_dict(state["alpha_optimizer"])
