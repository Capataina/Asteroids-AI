from dataclasses import dataclass
from typing import List, Optional, Tuple
import random

import torch

from interfaces.encoders.GraphEncoder import GraphPayload


@dataclass
class Transition:
    """Single SAC transition with graph observations."""
    obs: GraphPayload
    action: List[float]
    reward: float
    next_obs: GraphPayload
    done: bool


class ReplayBuffer:
    """Simple cyclic replay buffer for SAC."""
    def __init__(self, capacity: int, seed: Optional[int] = None):
        self.capacity = capacity
        self.buffer: List[Transition] = []
        self.position = 0
        self.rng = random.Random(seed)

    def push(self, transition: Transition) -> None:
        if len(self.buffer) < self.capacity:
            self.buffer.append(transition)
        else:
            self.buffer[self.position] = transition
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size: int) -> List[Transition]:
        if batch_size > len(self.buffer):
            raise ValueError(f"Cannot sample {batch_size} from buffer of size {len(self.buffer)}")
        return self.rng.sample(self.buffer, batch_size)

    def __len__(self) -> int:
        return len(self.buffer)

    @staticmethod
    def collate_graphs(
        payloads: List[GraphPayload],
        device: torch.device,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Convert a list of GraphPayloads into batched tensors.

        Returns:
            player_feat: [batch, player_dim]
            asteroid_feat: [total_asteroids, asteroid_dim]
            edge_index: [2, total_edges] (asteroid_idx -> player_idx)
            edge_attr: [total_edges, edge_dim]
        """
        batch_size = len(payloads)
        player_dim = GraphPayload.PLAYER_DIM
        asteroid_dim = GraphPayload.ASTEROID_DIM
        edge_dim = GraphPayload.EDGE_DIM

        player_feat = torch.zeros((batch_size, player_dim), dtype=torch.float32, device=device)
        asteroid_feat_list: List[List[float]] = []
        edge_attr_list: List[List[float]] = []
        edge_src: List[int] = []
        edge_dst: List[int] = []

        asteroid_offset = 0
        for i, payload in enumerate(payloads):
            player_feat[i] = torch.tensor(payload.player_features, dtype=torch.float32, device=device)

            for j, ast_feat in enumerate(payload.asteroid_features):
                asteroid_feat_list.append(ast_feat)
                edge_src.append(asteroid_offset + j)
                edge_dst.append(i)

            edge_attr_list.extend(payload.edge_attr)
            asteroid_offset += payload.num_asteroids

        if asteroid_feat_list:
            asteroid_feat = torch.tensor(asteroid_feat_list, dtype=torch.float32, device=device)
            edge_attr = torch.tensor(edge_attr_list, dtype=torch.float32, device=device)
            edge_index = torch.tensor([edge_src, edge_dst], dtype=torch.long, device=device)
        else:
            asteroid_feat = torch.zeros((0, asteroid_dim), dtype=torch.float32, device=device)
            edge_attr = torch.zeros((0, edge_dim), dtype=torch.float32, device=device)
            edge_index = torch.zeros((2, 0), dtype=torch.long, device=device)

        return player_feat, asteroid_feat, edge_index, edge_attr

    def sample_batch(
        self,
        batch_size: int,
        device: torch.device,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor,
               torch.Tensor, torch.Tensor,
               torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor,
               torch.Tensor]:
        """
        Sample a batch and collate into tensors.

        Returns:
            obs_player, obs_asteroid, obs_edge_index, obs_edge_attr,
            actions, rewards,
            next_player, next_asteroid, next_edge_index, next_edge_attr,
            dones
        """
        transitions = self.sample(batch_size)

        obs_payloads = [t.obs for t in transitions]
        next_payloads = [t.next_obs for t in transitions]
        actions = torch.tensor([t.action for t in transitions], dtype=torch.float32, device=device)
        rewards = torch.tensor([t.reward for t in transitions], dtype=torch.float32, device=device).unsqueeze(-1)
        dones = torch.tensor([t.done for t in transitions], dtype=torch.float32, device=device).unsqueeze(-1)

        obs_player, obs_asteroid, obs_edge_index, obs_edge_attr = ReplayBuffer.collate_graphs(obs_payloads, device)
        next_player, next_asteroid, next_edge_index, next_edge_attr = ReplayBuffer.collate_graphs(next_payloads, device)

        return (
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
        )
