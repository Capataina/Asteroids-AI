"""
Running normalization utilities for GNN-SAC observations.

Maintains running mean/variance for player, asteroid, and edge features,
and applies normalization with optional clipping.
"""

from typing import Dict, Any, Optional, Tuple

import torch


class RunningStats:
    """Tracks running mean/variance via sum/sumsq."""

    def __init__(self, dim: int, device: torch.device, eps: float = 1e-8, clip: Optional[float] = None):
        self.dim = dim
        self.device = device
        self.eps = eps
        self.clip = clip
        self.count = torch.zeros(1, device=device)
        self.sum = torch.zeros(dim, device=device)
        self.sumsq = torch.zeros(dim, device=device)

    def update(self, x: torch.Tensor) -> None:
        if x.numel() == 0:
            return
        x = x.detach()
        if x.dim() == 1:
            x = x.unsqueeze(0)
        n = x.shape[0]
        self.count += float(n)
        self.sum += x.sum(dim=0)
        self.sumsq += (x ** 2).sum(dim=0)

    def mean(self) -> torch.Tensor:
        if self.count.item() <= 0:
            return torch.zeros(self.dim, device=self.device)
        return self.sum / self.count

    def var(self) -> torch.Tensor:
        if self.count.item() <= 0:
            return torch.ones(self.dim, device=self.device)
        mean = self.mean()
        return torch.clamp(self.sumsq / self.count - mean ** 2, min=0.0)

    def normalize(self, x: torch.Tensor) -> torch.Tensor:
        if self.count.item() <= 0 or x.numel() == 0:
            return x
        mean = self.mean()
        std = torch.sqrt(self.var() + self.eps)
        if x.dim() == 1:
            out = (x - mean) / std
        else:
            out = (x - mean.unsqueeze(0)) / std.unsqueeze(0)
        if self.clip is not None:
            out = torch.clamp(out, -self.clip, self.clip)
        return out

    def state_dict(self) -> Dict[str, Any]:
        return {
            "count": self.count.detach().cpu(),
            "sum": self.sum.detach().cpu(),
            "sumsq": self.sumsq.detach().cpu(),
            "eps": self.eps,
            "clip": self.clip,
        }

    def load_state_dict(self, state: Dict[str, Any]) -> None:
        self.count = state.get("count", torch.zeros(1)).to(self.device)
        self.sum = state.get("sum", torch.zeros(self.dim)).to(self.device)
        self.sumsq = state.get("sumsq", torch.zeros(self.dim)).to(self.device)
        self.eps = state.get("eps", self.eps)
        self.clip = state.get("clip", self.clip)


class GraphNormalizer:
    """Running normalizer for GraphEncoder features."""

    def __init__(
        self,
        player_dim: int,
        asteroid_dim: int,
        edge_dim: int,
        device: torch.device,
        enabled: bool = True,
        eps: float = 1e-8,
        clip: Optional[float] = None,
    ):
        self.enabled = enabled
        self.player_stats = RunningStats(player_dim, device, eps=eps, clip=clip)
        self.asteroid_stats = RunningStats(asteroid_dim, device, eps=eps, clip=clip)
        self.edge_stats = RunningStats(edge_dim, device, eps=eps, clip=clip)

    def update(
        self,
        player_feat: torch.Tensor,
        asteroid_feat: torch.Tensor,
        edge_attr: torch.Tensor,
    ) -> None:
        if not self.enabled:
            return
        self.player_stats.update(player_feat)
        self.asteroid_stats.update(asteroid_feat)
        self.edge_stats.update(edge_attr)

    def normalize(
        self,
        player_feat: torch.Tensor,
        asteroid_feat: torch.Tensor,
        edge_attr: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        if not self.enabled:
            return player_feat, asteroid_feat, edge_attr
        return (
            self.player_stats.normalize(player_feat),
            self.asteroid_stats.normalize(asteroid_feat),
            self.edge_stats.normalize(edge_attr),
        )

    def state_dict(self) -> Dict[str, Any]:
        return {
            "enabled": self.enabled,
            "player": self.player_stats.state_dict(),
            "asteroid": self.asteroid_stats.state_dict(),
            "edge": self.edge_stats.state_dict(),
        }

    def load_state_dict(self, state: Dict[str, Any]) -> None:
        self.enabled = state.get("enabled", self.enabled)
        if "player" in state:
            self.player_stats.load_state_dict(state["player"])
        if "asteroid" in state:
            self.asteroid_stats.load_state_dict(state["asteroid"])
        if "edge" in state:
            self.edge_stats.load_state_dict(state["edge"])
