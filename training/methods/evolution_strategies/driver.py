"""
Evolution Strategies Driver.

This module implements the core ES algorithm logic, including:
- Mean parameter vector maintenance
- Gaussian noise sampling (with optional antithetic/mirrored sampling)
- Fitness-weighted gradient estimation
- Mean update with optional weight decay
"""

import time
import random
import math
from typing import List, Dict, Tuple, Optional
import numpy as np

from training.config.evolution_strategies import ESConfig
from training.methods.evolution_strategies.fitness_shaping import rank_transformation, compute_centered_ranks
from training.components.archive import BehaviorArchive
from training.components.novelty import compute_population_novelty
from training.config.novelty import NoveltyConfig


class ESDriver:
    """
    Manages the Evolution Strategies optimization process.

    ES maintains a distribution over parameter space (Gaussian with mean θ)
    and updates the mean by estimating the gradient of expected fitness
    through sampling.
    """

    def __init__(
        self,
        param_size: int,
        config: Optional[ESConfig] = None,
        novelty_config: Optional[NoveltyConfig] = None
    ):
        """
        Initialize the ES driver.

        Args:
            param_size: Number of parameters in the policy.
            config: ES configuration (uses defaults if None).
            novelty_config: Novelty/diversity configuration (optional).
        """
        self.param_size = param_size
        self.config = config or ESConfig()
        self.novelty_config = novelty_config or NoveltyConfig()

        # Core ES state
        self.mean = self._initialize_mean()
        self.sigma = ESConfig.SIGMA

        # Noise vectors from last sampling (needed for gradient computation)
        self.last_noise_vectors: Optional[np.ndarray] = None

        # Statistics tracking
        self.last_update_stats: Dict = {}
        self.last_update_duration: float = 0.0

        # Behavior archive for novelty (if enabled)
        if ESConfig.ENABLE_NOVELTY:
            self.behavior_archive = BehaviorArchive(
                max_size=self.novelty_config.archive_max_size,
                novelty_threshold=self.novelty_config.archive_novelty_threshold,
                k_nearest=self.novelty_config.k_nearest
            )
        else:
            self.behavior_archive = None

    def _initialize_mean(self) -> np.ndarray:
        """Initialize the mean parameter vector."""
        if ESConfig.INIT_MEAN_ZERO:
            return np.zeros(self.param_size, dtype=np.float32)
        else:
            return np.random.uniform(
                ESConfig.INIT_UNIFORM_LOW,
                ESConfig.INIT_UNIFORM_HIGH,
                self.param_size
            ).astype(np.float32)

    def sample_population(self) -> Tuple[List[List[float]], np.ndarray]:
        """
        Generate perturbations around the mean to create candidate policies.

        If antithetic sampling is enabled, generates N/2 noise vectors and
        uses both +ε and -ε perturbations, resulting in N candidates.

        Returns:
            Tuple of:
                - List of candidate parameter vectors (as List[float])
                - NumPy array of noise vectors used (for gradient computation)
        """
        n = ESConfig.POPULATION_SIZE

        if ESConfig.USE_ANTITHETIC:
            # Generate half the noise vectors, use both + and -
            half_n = n // 2
            noise_half = np.random.randn(half_n, self.param_size).astype(np.float32)

            # Stack positive and negative perturbations
            noise = np.vstack([noise_half, -noise_half])

            # If n is odd, add one more random noise vector
            if n % 2 == 1:
                extra_noise = np.random.randn(1, self.param_size).astype(np.float32)
                noise = np.vstack([noise, extra_noise])
        else:
            # Standard sampling
            noise = np.random.randn(n, self.param_size).astype(np.float32)

        # Store for later gradient computation
        self.last_noise_vectors = noise

        # Create candidates: mean + sigma * noise
        candidates = []
        for i in range(n):
            candidate = self.mean + self.sigma * noise[i]
            candidates.append(candidate.tolist())

        return candidates, noise

    def get_mean_as_list(self) -> List[float]:
        """Get the current mean parameter vector as a list."""
        return self.mean.tolist()

    def update(
        self,
        fitnesses: List[float],
        per_agent_metrics: Optional[List[Dict]] = None
    ) -> None:
        """
        Update the mean parameter vector based on fitness-weighted gradient.

        Args:
            fitnesses: Fitness scores for each candidate.
            per_agent_metrics: Optional per-agent metrics for novelty/diversity.
        """
        start_time = time.time()

        if self.last_noise_vectors is None:
            raise RuntimeError("Must call sample_population() before update()")

        fitnesses_array = np.array(fitnesses, dtype=np.float32)
        n = len(fitnesses)

        # Apply novelty/diversity bonuses if enabled
        if per_agent_metrics is not None:
            fitnesses_array = self._apply_novelty_diversity(fitnesses_array, per_agent_metrics)

        # Apply fitness shaping (rank transformation)
        if ESConfig.USE_RANK_TRANSFORMATION:
            utilities = rank_transformation(fitnesses_array.tolist())
        else:
            # Simple normalization
            mean_fit = fitnesses_array.mean()
            std_fit = fitnesses_array.std()
            if std_fit > 1e-8:
                utilities = (fitnesses_array - mean_fit) / std_fit
            else:
                utilities = np.zeros(n)

        # Compute gradient estimate
        # grad = (1 / (n * sigma)) * sum(utility_i * noise_i)
        # Using matrix multiplication for efficiency
        gradient = np.dot(utilities, self.last_noise_vectors) / (n * self.sigma)

        # Update mean
        self.mean = self.mean + ESConfig.LEARNING_RATE * gradient

        # Apply weight decay (L2 regularization)
        if ESConfig.WEIGHT_DECAY > 0:
            self.mean = self.mean * (1.0 - ESConfig.WEIGHT_DECAY)

        # Decay sigma
        self._decay_sigma()

        # Record statistics
        self.last_update_duration = time.time() - start_time
        self.last_update_stats = {
            'sigma': self.sigma,
            'learning_rate': ESConfig.LEARNING_RATE,
            'gradient_norm': float(np.linalg.norm(gradient)),
            'mean_param_norm': float(np.linalg.norm(self.mean)),
            'fitness_mean': float(fitnesses_array.mean()),
            'fitness_std': float(fitnesses_array.std()),
        }

        # Clear noise vectors
        self.last_noise_vectors = None

    def _apply_novelty_diversity(
        self,
        fitnesses: np.ndarray,
        per_agent_metrics: List[Dict]
    ) -> np.ndarray:
        """
        Apply novelty and diversity bonuses to fitness values.

        Args:
            fitnesses: Raw fitness values.
            per_agent_metrics: Per-agent metrics containing behavior_vector and reward_diversity.

        Returns:
            Adjusted fitness values with novelty/diversity bonuses.
        """
        adjusted = fitnesses.copy()

        # Novelty bonus
        if ESConfig.ENABLE_NOVELTY and self.behavior_archive is not None:
            behavior_vectors = [m.get('behavior_vector', [0.0] * 7) for m in per_agent_metrics]
            novelty_scores = compute_population_novelty(
                behavior_vectors,
                self.behavior_archive.get_behaviors(),
                self.novelty_config.k_nearest
            )
            self.behavior_archive.add_batch(behavior_vectors, novelty_scores)

            # Add novelty bonus
            novelty_array = np.array(novelty_scores, dtype=np.float32)
            adjusted = adjusted + ESConfig.NOVELTY_WEIGHT * novelty_array

            self.last_update_stats['avg_novelty'] = float(novelty_array.mean())
            self.last_update_stats['archive_size'] = self.behavior_archive.size()
        else:
            self.last_update_stats['avg_novelty'] = 0.0
            self.last_update_stats['archive_size'] = 0

        # Diversity bonus
        if ESConfig.ENABLE_DIVERSITY:
            diversity_scores = [m.get('reward_diversity', 0.0) for m in per_agent_metrics]
            diversity_array = np.array(diversity_scores, dtype=np.float32)
            adjusted = adjusted + ESConfig.DIVERSITY_WEIGHT * diversity_array

            self.last_update_stats['avg_diversity'] = float(diversity_array.mean())
        else:
            self.last_update_stats['avg_diversity'] = 0.0

        return adjusted

    def _decay_sigma(self) -> None:
        """Apply sigma decay with minimum floor."""
        self.sigma = max(
            ESConfig.SIGMA_MIN,
            self.sigma * ESConfig.SIGMA_DECAY
        )

    def get_population_for_display(self) -> List[List[float]]:
        """
        Get a "population" for compatibility with GA-style infrastructure.

        ES doesn't maintain a population, but we can return the mean
        and recent candidates for visualization purposes.

        Returns:
            List containing just the mean (as a single-element population).
        """
        return [self.mean.tolist()]
