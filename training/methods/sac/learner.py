import math
from typing import Dict, Tuple

import torch
import torch.nn as nn
import torch.optim as optim

from training.config.sac import SACConfig
from training.methods.sac.networks import GNNBackbone, Actor, TwinCritics
from training.methods.sac.normalization import GraphNormalizer


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

        self.normalizer = GraphNormalizer(
            player_dim=5,
            asteroid_dim=3,
            edge_dim=7,
            device=device,
            enabled=getattr(config, "OBS_NORM_ENABLED", True),
            eps=getattr(config, "OBS_NORM_EPS", 1e-8),
            clip=getattr(config, "OBS_NORM_CLIP", None),
        )

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

        # Optimizer split:
        # - Critic trains both critics and the shared GNN encoder (representation learning is primarily critic-driven).
        # - Actor trains only the actor (encoder gradients from actor are disabled in update()).
        self.critic_optimizer = optim.Adam(
            list(self.gnn.parameters()) + list(self.critics.parameters()),
            lr=config.CRITIC_LR,
        )
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=config.ACTOR_LR)

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
        self.agc_enabled = getattr(config, "AGC_ENABLED", False)
        self.agc_clip_factor = getattr(config, "AGC_CLIP_FACTOR", 0.01)
        self.agc_eps = getattr(config, "AGC_EPS", 1e-3)
        self.critic_loss_type = getattr(config, "CRITIC_LOSS", "mse").lower()
        self.huber_delta = getattr(config, "HUBER_DELTA", 1.0)

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
            player_feat, asteroid_feat, edge_attr = self.normalizer.normalize(
                player_feat, asteroid_feat, edge_attr
            )
            state = self.gnn(player_feat, asteroid_feat, edge_index, edge_attr)
            action, log_prob = self.actor(state, deterministic=deterministic)

        self.gnn.train()
        self.actor.train()
        return action, log_prob

    def _compute_grad_norm(self, parameters) -> float:
        """Compute the total gradient norm across parameters."""
        total_norm = 0.0
        for p in parameters:
            if p.grad is not None:
                total_norm += p.grad.data.norm(2).item() ** 2
        return total_norm ** 0.5

    def _apply_agc(self, parameters) -> int:
        """Apply adaptive gradient clipping (AGC) per-parameter tensor."""
        if not self.agc_enabled:
            return 0
        clip_hits = 0
        for p in parameters:
            if p.grad is None:
                continue
            param_norm = p.detach().norm(2)
            grad_norm = p.grad.detach().norm(2)
            max_norm = self.agc_clip_factor * (param_norm + self.agc_eps)
            if grad_norm > max_norm:
                p.grad.mul_(max_norm / (grad_norm + 1e-6))
                clip_hits += 1
        return clip_hits

    @staticmethod
    def _huber_loss(input_tensor: torch.Tensor, target_tensor: torch.Tensor, delta: float) -> torch.Tensor:
        """Compute mean Huber loss with a configurable delta."""
        diff = input_tensor - target_tensor
        abs_diff = diff.abs()
        quadratic = torch.clamp(abs_diff, max=delta)
        linear = abs_diff - quadratic
        loss = 0.5 * quadratic.pow(2) + delta * linear
        return loss.mean()

    def _compute_embedding_stats(self, embedding: torch.Tensor) -> Dict[str, float]:
        """Compute health statistics for embeddings."""
        with torch.no_grad():
            # Mean norm of embeddings
            norms = embedding.norm(dim=-1)
            mean_norm = norms.mean().item()

            # Per-dimension std (low = collapse)
            per_dim_std = embedding.std(dim=0)
            mean_dim_std = per_dim_std.mean().item()

            # Cosine similarity between random pairs (high = collapse)
            if embedding.size(0) >= 2:
                # Normalize embeddings
                normalized = embedding / (embedding.norm(dim=-1, keepdim=True) + 1e-8)
                # Compute pairwise cosine similarity for first few samples
                n_samples = min(embedding.size(0), 16)
                cos_sim = torch.mm(normalized[:n_samples], normalized[:n_samples].t())
                # Get off-diagonal elements
                mask = ~torch.eye(n_samples, dtype=torch.bool, device=embedding.device)
                mean_cos_sim = cos_sim[mask].mean().item()
            else:
                mean_cos_sim = 0.0

        return {
            "embedding_norm": mean_norm,
            "embedding_dim_std": mean_dim_std,
            "embedding_cos_sim": mean_cos_sim,
        }

    @staticmethod
    def _percentile(values: torch.Tensor, q: float) -> float:
        """Compute percentile for a 1D tensor."""
        if values.numel() == 0:
            return 0.0
        flat = values.flatten()
        try:
            return torch.quantile(flat, q).item()
        except Exception:
            # Fallback for older torch versions
            k = max(0, int(math.ceil(q * flat.numel())) - 1)
            k = min(k, flat.numel() - 1)
            return flat.kthvalue(k + 1).values.item()

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

        if self.normalizer.enabled:
            self.normalizer.update(obs_player, obs_asteroid, obs_edge_attr)
            self.normalizer.update(next_player, next_asteroid, next_edge_attr)
            obs_player, obs_asteroid, obs_edge_attr = self.normalizer.normalize(
                obs_player, obs_asteroid, obs_edge_attr
            )
            next_player, next_asteroid, next_edge_attr = self.normalizer.normalize(
                next_player, next_asteroid, next_edge_attr
            )

        # === Critic update (also trains the GNN encoder) ===
        state = self.gnn(obs_player, obs_asteroid, obs_edge_index, obs_edge_attr)

        with torch.no_grad():
            next_state = self.gnn(next_player, next_asteroid, next_edge_index, next_edge_attr)
            next_action, next_log_prob = self.actor(next_state, deterministic=False)
            target_q1, target_q2 = self.target_critics(next_state, next_action)
            target_q = torch.min(target_q1, target_q2) - self.alpha * next_log_prob
        target = rewards + (1.0 - dones) * self.config.GAMMA * target_q

        # Critic loss
        q1, q2 = self.critics(state, actions)
        if self.critic_loss_type == "huber":
            critic_loss = self._huber_loss(q1, target, self.huber_delta) + self._huber_loss(q2, target, self.huber_delta)
        else:
            critic_loss = nn.functional.mse_loss(q1, target) + nn.functional.mse_loss(q2, target)

        # TD error diagnostics (absolute)
        td_abs_q1 = (target - q1).detach().abs()
        td_abs_q2 = (target - q2).detach().abs()
        td_abs_all = torch.cat([td_abs_q1, td_abs_q2], dim=0)

        self.critic_optimizer.zero_grad()
        critic_loss.backward()

        # Capture critic+encoder gradient norm before clipping
        critic_params = list(self.gnn.parameters()) + list(self.critics.parameters())
        critic_grad_norm_raw = self._compute_grad_norm(critic_params)
        critic_agc_hits = self._apply_agc(critic_params)
        critic_grad_norm = self._compute_grad_norm(critic_params)
        critic_clip_hit = 1.0 if self.grad_clip is not None and critic_grad_norm > self.grad_clip else 0.0

        if self.grad_clip is not None:
            nn.utils.clip_grad_norm_(critic_params, self.grad_clip)
        self.critic_optimizer.step()

        # === Actor update (encoder frozen; gradients flow through critics to actions only) ===
        with torch.no_grad():
            state_actor = self.gnn(obs_player, obs_asteroid, obs_edge_index, obs_edge_attr)
        new_action, log_prob = self.actor(state_actor, deterministic=False)

        # Freeze critic parameters for the actor update (avoid accumulating unused grads).
        for p in self.critics.parameters():
            p.requires_grad = False
        q1_pi = self.critics.q1_forward(state_actor, new_action)
        for p in self.critics.parameters():
            p.requires_grad = True

        actor_loss = (self.alpha * log_prob - q1_pi).mean()

        self.actor_optimizer.zero_grad()
        actor_loss.backward()

        # Capture actor gradient norm before clipping
        actor_params = list(self.actor.parameters())
        actor_grad_norm_raw = self._compute_grad_norm(actor_params)
        actor_agc_hits = self._apply_agc(actor_params)
        actor_grad_norm = self._compute_grad_norm(actor_params)
        actor_clip_hit = 1.0 if self.grad_clip is not None and actor_grad_norm > self.grad_clip else 0.0

        if self.grad_clip is not None:
            nn.utils.clip_grad_norm_(actor_params, self.grad_clip)
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

        # Compute embedding health stats
        embedding_stats = self._compute_embedding_stats(state_actor)

        # Compute policy entropy (from log_prob)
        policy_entropy = -log_prob.mean().item()

        metrics = {
            "critic_loss": float(critic_loss.item()),
            "actor_loss": float(actor_loss.item()),
            "alpha_loss": float(alpha_loss.item()),
            "alpha_value": float(self.alpha.item()),
            "q1_mean": float(q1.mean().item()),
            "q2_mean": float(q2.mean().item()),
            "q1_std": float(q1.std().item()),
            "q2_std": float(q2.std().item()),
            "target_q_mean": float(target_q.mean().item()),
            "target_q_std": float(target_q.std().item()),
            "td_abs_mean": float(td_abs_all.mean().item()),
            "td_abs_p90": float(self._percentile(td_abs_all, 0.90)),
            "td_abs_p99": float(self._percentile(td_abs_all, 0.99)),
            "critic_grad_norm": critic_grad_norm,
            "actor_grad_norm": actor_grad_norm,
            "critic_grad_norm_raw": critic_grad_norm_raw,
            "actor_grad_norm_raw": actor_grad_norm_raw,
            "critic_clip_hit": critic_clip_hit,
            "actor_clip_hit": actor_clip_hit,
            "critic_agc_hit_frac": float(critic_agc_hits) / max(1, len(critic_params)),
            "actor_agc_hit_frac": float(actor_agc_hits) / max(1, len(actor_params)),
            "policy_entropy": policy_entropy,
            **embedding_stats,
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
            "normalizer": self.normalizer.state_dict(),
        }

    def load_state_dict(self, state: Dict[str, object]) -> None:
        self.gnn.load_state_dict(state["gnn"])
        self.actor.load_state_dict(state["actor"])
        self.critics.load_state_dict(state["critics"])
        if "target_critics" in state:
            self.target_critics.load_state_dict(state["target_critics"])
        if "log_alpha" in state:
            self.log_alpha.data = torch.tensor(float(state["log_alpha"]), device=self.device)
        if "actor_optimizer" in state and state["actor_optimizer"] is not None:
            try:
                self.actor_optimizer.load_state_dict(state["actor_optimizer"])
            except Exception:
                pass
        if "critic_optimizer" in state and state["critic_optimizer"] is not None:
            try:
                self.critic_optimizer.load_state_dict(state["critic_optimizer"])
            except Exception:
                pass
        if self.alpha_optimizer and state.get("alpha_optimizer"):
            self.alpha_optimizer.load_state_dict(state["alpha_optimizer"])
        if "normalizer" in state:
            self.normalizer.load_state_dict(state["normalizer"])
