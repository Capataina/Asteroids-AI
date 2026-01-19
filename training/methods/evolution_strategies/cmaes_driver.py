"""
Lightweight CMA-ES driver (diagonal covariance).

Implements CMA-ES-style updates using a diagonal covariance vector to keep
compute overhead low while still learning correlated step sizes.
"""

from typing import Dict, List, Optional, Tuple
import math
import time
import numpy as np

from training.config.evolution_strategies import ESConfig
from training.config.pareto import ParetoConfig
from training.components.pareto.objectives import compute_objective_matrix
from training.components.pareto.utility import pareto_order


class CMAESDriver:
    """
    Diagonal CMA-ES driver.

    Maintains:
      - mean vector
      - global step size (sigma)
      - diagonal covariance (per-parameter variance)
      - evolution paths for step-size and covariance adaptation
    """

    def __init__(
        self,
        param_size: int,
        config: Optional[ESConfig] = None,
        pareto_config: Optional[ParetoConfig] = None
    ):
        self.param_size = param_size
        self.config = config or ESConfig()
        self.pareto_config = pareto_config or ParetoConfig()

        self.mean = self._initialize_mean()
        sigma = ESConfig.CMAES_SIGMA if ESConfig.CMAES_SIGMA is not None else ESConfig.SIGMA
        self.sigma = float(sigma)

        # Diagonal covariance (variance per parameter)
        self.cov_diag = np.ones(self.param_size, dtype=np.float32)

        # Evolution paths
        self.p_sigma = np.zeros(self.param_size, dtype=np.float32)
        self.p_c = np.zeros(self.param_size, dtype=np.float32)

        # Strategy parameters
        self.pop_size = int(ESConfig.POPULATION_SIZE)
        self.mu = int(ESConfig.CMAES_MU) if ESConfig.CMAES_MU else self.pop_size // 2
        self.weights = self._init_weights(self.mu)
        self.mu_eff = float(1.0 / np.sum(self.weights ** 2))

        self.c_sigma = (self.mu_eff + 2.0) / (self.param_size + self.mu_eff + 5.0)
        self.d_sigma = 1.0 + self.c_sigma + 2.0 * max(
            0.0,
            math.sqrt((self.mu_eff - 1.0) / (self.param_size + 1.0)) - 1.0
        )
        self.c_c = (4.0 + self.mu_eff / self.param_size) / (
            self.param_size + 4.0 + 2.0 * self.mu_eff / self.param_size
        )
        self.c1_base = 2.0 / ((self.param_size + 1.3) ** 2 + self.mu_eff)
        self.cmu_base = min(
            1.0 - self.c1_base,
            2.0 * (self.mu_eff - 2.0 + 1.0 / self.mu_eff) / ((self.param_size + 2.0) ** 2 + self.mu_eff)
        )
        self.cov_lr_scale = 1.0
        target_rate = ESConfig.CMAES_COV_TARGET_RATE
        if target_rate is not None:
            base_total = self.c1_base + self.cmu_base
            if base_total > 0:
                scale = target_rate / base_total
                scale = max(1.0, min(scale, ESConfig.CMAES_COV_MAX_SCALE))
                self.cov_lr_scale = float(scale)
        self.c1 = self.c1_base * self.cov_lr_scale
        self.cmu = self.cmu_base * self.cov_lr_scale
        cov_total = self.c1 + self.cmu
        if cov_total > 0.9:
            factor = 0.9 / cov_total
            self.c1 *= factor
            self.cmu *= factor
            self.cov_lr_scale *= factor

        self.chi_n = math.sqrt(self.param_size) * (
            1.0 - 1.0 / (4.0 * self.param_size) + 1.0 / (21.0 * self.param_size ** 2)
        )

        # Sampling buffers
        self.last_z: Optional[np.ndarray] = None
        self.last_y: Optional[np.ndarray] = None

        self.current_generation = 0
        self.last_update_stats: Dict = {}
        self.last_update_duration: float = 0.0

    def _initialize_mean(self) -> np.ndarray:
        if ESConfig.INIT_MEAN_ZERO:
            return np.zeros(self.param_size, dtype=np.float32)
        return np.random.uniform(
            ESConfig.INIT_UNIFORM_LOW,
            ESConfig.INIT_UNIFORM_HIGH,
            self.param_size
        ).astype(np.float32)

    @staticmethod
    def _init_weights(mu: int) -> np.ndarray:
        weights = np.array([math.log(mu + 0.5) - math.log(i + 1) for i in range(mu)], dtype=np.float32)
        weights = weights / np.sum(weights)
        return weights

    def sample_population(self) -> Tuple[List[List[float]], np.ndarray]:
        """
        Sample candidate parameter vectors.
        """
        n = self.pop_size
        if ESConfig.USE_ANTITHETIC and n % 2 == 0:
            half = n // 2
            z_half = np.random.randn(half, self.param_size).astype(np.float32)
            z = np.vstack([z_half, -z_half])
        else:
            z = np.random.randn(n, self.param_size).astype(np.float32)

        y = z * np.sqrt(self.cov_diag)
        x = self.mean + self.sigma * y

        self.last_z = z
        self.last_y = y

        return [row.tolist() for row in x], z

    def update(
        self,
        fitnesses: List[float],
        per_agent_metrics: Optional[List[Dict]] = None,
        objective_vectors: Optional[List[List[float]]] = None,
        objective_directions: Optional[List[str]] = None
    ) -> None:
        """
        Update CMA-ES parameters based on ranked candidates.
        """
        start_time = time.time()
        if self.last_z is None or self.last_y is None:
            raise RuntimeError("Must call sample_population() before update().")

        self.current_generation += 1

        n = len(fitnesses)
        if n != self.pop_size:
            raise ValueError(f"Population size mismatch: got {n}, expected {self.pop_size}")

        if self.pareto_config.ENABLED:
            if objective_vectors is None or objective_directions is None:
                if per_agent_metrics is None:
                    raise ValueError("Pareto enabled but no objective vectors or metrics provided.")
                objective_vectors, objective_directions, _ = compute_objective_matrix(
                    per_agent_metrics,
                    self.pareto_config
                )
            order, front_rank, crowding = pareto_order(objective_vectors, objective_directions)
            if self.pareto_config.FITNESS_TIEBREAKER:
                order = sorted(range(n), key=lambda i: (front_rank[i], -crowding[i], -fitnesses[i]))
                pareto_tiebreaker = "fitness"
            else:
                pareto_tiebreaker = "none"
        else:
            order = sorted(range(n), key=lambda i: fitnesses[i], reverse=True)
            front_rank = [0 for _ in range(n)]
            crowding = [0.0 for _ in range(n)]
            pareto_tiebreaker = "none"

        finite_crowding = [c for c in crowding if math.isfinite(c)]
        best_crowding = float(max(finite_crowding)) if finite_crowding else 0.0
        inf_crowding_count = int(sum(1 for c in crowding if not math.isfinite(c)))
        cov_dev = np.abs(self.cov_diag - 1.0)
        cov_std = float(np.std(self.cov_diag))
        cov_mean_abs_dev = float(np.mean(cov_dev))
        cov_max_abs_dev = float(np.max(cov_dev))

        # Select top mu by Pareto order (or fitness order).
        selected = order[:self.mu]
        weights = self.weights.reshape((self.mu, 1))

        z_sel = self.last_z[selected]
        y_sel = self.last_y[selected]

        z_w = np.sum(weights * z_sel, axis=0)
        y_w = np.sum(weights * y_sel, axis=0)

        # Update mean
        self.mean = self.mean + self.sigma * y_w

        # Step-size adaptation
        self.p_sigma = (1.0 - self.c_sigma) * self.p_sigma + math.sqrt(
            self.c_sigma * (2.0 - self.c_sigma) * self.mu_eff
        ) * z_w

        norm_p_sigma = float(np.linalg.norm(self.p_sigma))
        h_sigma_cond = norm_p_sigma / math.sqrt(
            1.0 - (1.0 - self.c_sigma) ** (2.0 * self.current_generation)
        )
        h_sigma = 1.0 if h_sigma_cond < (1.4 + 2.0 / (self.param_size + 1.0)) * self.chi_n else 0.0

        # Covariance path update
        self.p_c = (1.0 - self.c_c) * self.p_c + h_sigma * math.sqrt(
            self.c_c * (2.0 - self.c_c) * self.mu_eff
        ) * y_w

        # Covariance (diagonal) update
        y_sq = np.sum(weights * (y_sel ** 2), axis=0)
        self.cov_diag = (
            (1.0 - self.c1 - self.cmu) * self.cov_diag
            + self.c1 * (self.p_c ** 2)
            + self.cmu * y_sq
        )

        self.cov_diag = np.maximum(self.cov_diag, ESConfig.CMAES_COV_MIN)

        # Sigma update
        self.sigma = self.sigma * math.exp((self.c_sigma / self.d_sigma) * (norm_p_sigma / self.chi_n - 1.0))
        self.sigma = max(self.sigma, ESConfig.SIGMA_MIN)

        # Stats
        self.last_update_stats = {
            "sigma": float(self.sigma),
            "mean_param_norm": float(np.linalg.norm(self.mean)),
            "cov_diag_mean": float(np.mean(self.cov_diag)),
            "cov_diag_min": float(np.min(self.cov_diag)),
            "cov_diag_max": float(np.max(self.cov_diag)),
            "cov_diag_std": cov_std,
            "cov_diag_mean_abs_dev": cov_mean_abs_dev,
            "cov_diag_max_abs_dev": cov_max_abs_dev,
            "cov_lr_scale": float(self.cov_lr_scale),
            "cov_lr_effective_rate": float(self.c1 + self.cmu),
            "pareto_enabled": bool(self.pareto_config.ENABLED),
            "pareto_tiebreaker": pareto_tiebreaker,
            "pareto_front0_size": int(sum(1 for r in front_rank if r == 0)),
            "pareto_best_crowding": best_crowding,
            "pareto_infinite_crowding_count": inf_crowding_count,
        }
        self.last_update_duration = time.time() - start_time

    def restart(self, mean: Optional[np.ndarray] = None, sigma: Optional[float] = None, reason: str = "stagnation") -> None:
        """Restart CMA-ES state to escape stagnation."""
        self.mean = mean.copy() if mean is not None else self._initialize_mean()
        base_sigma = ESConfig.CMAES_SIGMA if ESConfig.CMAES_SIGMA is not None else ESConfig.SIGMA
        self.sigma = float(sigma if sigma is not None else base_sigma)
        self.cov_diag = np.ones(self.param_size, dtype=np.float32)
        self.p_sigma = np.zeros(self.param_size, dtype=np.float32)
        self.p_c = np.zeros(self.param_size, dtype=np.float32)
        self.current_generation = 0
        self.last_update_stats = {
            "sigma": float(self.sigma),
            "mean_param_norm": float(np.linalg.norm(self.mean)),
            "cov_diag_mean": float(np.mean(self.cov_diag)),
            "cov_diag_min": float(np.min(self.cov_diag)),
            "cov_diag_max": float(np.max(self.cov_diag)),
            "cov_diag_std": float(np.std(self.cov_diag)),
            "cov_diag_mean_abs_dev": 0.0,
            "cov_diag_max_abs_dev": 0.0,
            "cov_lr_scale": float(self.cov_lr_scale),
            "cov_lr_effective_rate": float(self.c1 + self.cmu),
            "restart_triggered": True,
            "restart_reason": reason,
        }

    def get_mean_as_list(self) -> List[float]:
        return self.mean.tolist()
