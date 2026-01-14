"""
Evolution Strategies Driver.

This module implements the core ES algorithm logic, including:
- Mean parameter vector maintenance
- Gaussian noise sampling (with optional antithetic/mirrored sampling)
- Fitness-weighted gradient estimation
- AdamW optimizer for stable updates
- Elitism to prevent forgetting good solutions
- Adaptive sigma decay based on stagnation
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

    Features:
    - AdamW optimizer for momentum and adaptive learning rates
    - Elitism to track and preserve best-ever solution
    - Adaptive sigma decay when stagnating
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

        # AdamW optimizer state
        self.adam_m = np.zeros(self.param_size, dtype=np.float32)  # First moment
        self.adam_v = np.zeros(self.param_size, dtype=np.float32)  # Second moment
        self.adam_t = 0  # Timestep for bias correction

        # Elitism state
        self.best_ever_candidate: Optional[np.ndarray] = None
        self.best_ever_fitness: float = float('-inf')
        self.best_ever_generation: int = 0

        # Stagnation tracking
        self.generations_since_improvement: int = 0
        self.current_generation: int = 0

        # Noise vectors from last sampling (needed for gradient computation)
        self.last_noise_vectors: Optional[np.ndarray] = None
        self.elite_index: Optional[int] = None  # Index of elite in candidates if injected

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

        If elitism is enabled, the best-ever candidate is included in the pool.

        Returns:
            Tuple of:
                - List of candidate parameter vectors (as List[float])
                - NumPy array of noise vectors used (for gradient computation)
        """
        n = ESConfig.POPULATION_SIZE
        self.elite_index = None

        # Determine if we should inject elite this generation
        inject_elite = (
            ESConfig.ENABLE_ELITISM and
            self.best_ever_candidate is not None and
            self.current_generation % ESConfig.ELITE_INJECTION_FREQUENCY == 0
        )

        # Adjust n to make room for elite if needed
        n_samples = n - 1 if inject_elite else n

        if ESConfig.USE_ANTITHETIC:
            # Generate half the noise vectors, use both + and -
            half_n = n_samples // 2
            noise_half = np.random.randn(half_n, self.param_size).astype(np.float32)

            # Stack positive and negative perturbations
            noise = np.vstack([noise_half, -noise_half])

            # If n_samples is odd, add one more random noise vector
            if n_samples % 2 == 1:
                extra_noise = np.random.randn(1, self.param_size).astype(np.float32)
                noise = np.vstack([noise, extra_noise])
        else:
            # Standard sampling
            noise = np.random.randn(n_samples, self.param_size).astype(np.float32)

        # Create candidates: mean + sigma * noise
        candidates = []
        for i in range(n_samples):
            candidate = self.mean + self.sigma * noise[i]
            candidates.append(candidate.tolist())

        # Inject elite if enabled
        if inject_elite:
            self.elite_index = len(candidates)
            candidates.append(self.best_ever_candidate.tolist())
            # Add a zero noise vector for the elite (it's not a perturbation of the mean)
            elite_noise = np.zeros((1, self.param_size), dtype=np.float32)
            noise = np.vstack([noise, elite_noise])

        # Store for later gradient computation
        self.last_noise_vectors = noise

        return candidates, noise

    def get_mean_as_list(self) -> List[float]:
        """Get the current mean parameter vector as a list."""
        return self.mean.tolist()

    def get_best_ever_as_list(self) -> Optional[List[float]]:
        """Get the best-ever candidate parameter vector as a list."""
        if self.best_ever_candidate is not None:
            return self.best_ever_candidate.tolist()
        return None

    def update(
        self,
        fitnesses: List[float],
        per_agent_metrics: Optional[List[Dict]] = None
    ) -> None:
        """
        Update the mean parameter vector based on fitness-weighted gradient.

        Uses AdamW optimizer if enabled, otherwise vanilla SGD.

        Args:
            fitnesses: Fitness scores for each candidate.
            per_agent_metrics: Optional per-agent metrics for novelty/diversity.
        """
        start_time = time.time()
        self.current_generation += 1

        if self.last_noise_vectors is None:
            raise RuntimeError("Must call sample_population() before update()")

        fitnesses_array = np.array(fitnesses, dtype=np.float32)
        n = len(fitnesses)

        # Update elitism tracking
        best_idx = int(np.argmax(fitnesses_array))
        best_fitness = fitnesses_array[best_idx]

        if best_fitness > self.best_ever_fitness:
            self.best_ever_fitness = best_fitness
            # Reconstruct the candidate from mean + sigma * noise
            if self.elite_index is not None and best_idx == self.elite_index:
                # Best is the elite itself, keep it
                pass
            else:
                # Store the actual candidate that achieved this fitness
                self.best_ever_candidate = (
                    self.mean + self.sigma * self.last_noise_vectors[best_idx]
                ).copy()
            self.best_ever_generation = self.current_generation
            self.generations_since_improvement = 0
        else:
            self.generations_since_improvement += 1

        # Apply novelty/diversity bonuses if enabled
        if per_agent_metrics is not None:
            fitnesses_array = self._apply_novelty_diversity(fitnesses_array, per_agent_metrics)

        # Exclude elite from gradient computation if it was injected
        # (elite is not a perturbation of the mean, so it shouldn't contribute to gradient)
        if self.elite_index is not None:
            mask = np.ones(n, dtype=bool)
            mask[self.elite_index] = False
            grad_fitnesses = fitnesses_array[mask]
            grad_noise = self.last_noise_vectors[mask]
            n_grad = n - 1
        else:
            grad_fitnesses = fitnesses_array
            grad_noise = self.last_noise_vectors
            n_grad = n

        # Apply fitness shaping (rank transformation)
        if ESConfig.USE_RANK_TRANSFORMATION:
            utilities = rank_transformation(grad_fitnesses.tolist())
        else:
            # Simple normalization
            mean_fit = grad_fitnesses.mean()
            std_fit = grad_fitnesses.std()
            if std_fit > 1e-8:
                utilities = (grad_fitnesses - mean_fit) / std_fit
            else:
                utilities = np.zeros(n_grad)

        # Compute gradient estimate
        # grad = (1 / (n * sigma)) * sum(utility_i * noise_i)
        gradient = np.dot(utilities, grad_noise) / (n_grad * self.sigma)

        # Update mean using AdamW or vanilla SGD
        if ESConfig.USE_ADAMW:
            self._adamw_update(gradient)
        else:
            self._sgd_update(gradient)

        # Apply elite pull if stagnating
        self._apply_elite_pull()

        # Decay sigma (with adaptive acceleration if stagnating)
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
            'best_ever_fitness': self.best_ever_fitness,
            'best_ever_generation': self.best_ever_generation,
            'generations_since_improvement': self.generations_since_improvement,
            'elite_injected': self.elite_index is not None,
            'adam_t': self.adam_t if ESConfig.USE_ADAMW else 0,
        }

        # Clear noise vectors
        self.last_noise_vectors = None
        self.elite_index = None

    def _sgd_update(self, gradient: np.ndarray) -> None:
        """Apply vanilla SGD update to the mean."""
        self.mean = self.mean + ESConfig.LEARNING_RATE * gradient

        # Apply weight decay (L2 regularization)
        if ESConfig.WEIGHT_DECAY > 0:
            self.mean = self.mean * (1.0 - ESConfig.WEIGHT_DECAY)

    def _adamw_update(self, gradient: np.ndarray) -> None:
        """
        Apply AdamW update to the mean.

        AdamW provides:
        - Momentum (smooths noisy gradient estimates)
        - Adaptive per-parameter learning rates
        - Decoupled weight decay (better regularization)
        """
        self.adam_t += 1

        beta1 = ESConfig.ADAMW_BETA1
        beta2 = ESConfig.ADAMW_BETA2
        eps = ESConfig.ADAMW_EPSILON
        lr = ESConfig.LEARNING_RATE

        # Update biased first moment estimate (momentum)
        self.adam_m = beta1 * self.adam_m + (1 - beta1) * gradient

        # Update biased second moment estimate (adaptive LR)
        self.adam_v = beta2 * self.adam_v + (1 - beta2) * (gradient ** 2)

        # Compute bias-corrected moment estimates
        m_hat = self.adam_m / (1 - beta1 ** self.adam_t)
        v_hat = self.adam_v / (1 - beta2 ** self.adam_t)

        # AdamW update: decoupled weight decay
        # θ = θ - lr * (m_hat / (sqrt(v_hat) + eps) + weight_decay * θ)
        adam_update = m_hat / (np.sqrt(v_hat) + eps)

        if ESConfig.WEIGHT_DECAY > 0:
            # Decoupled weight decay (AdamW style)
            self.mean = self.mean * (1.0 - lr * ESConfig.WEIGHT_DECAY) + lr * adam_update
        else:
            self.mean = self.mean + lr * adam_update

    def _apply_elite_pull(self) -> None:
        """
        Pull the mean toward the best-ever candidate when stagnating.

        This helps ES recover when the mean has drifted away from a good region.
        """
        if not ESConfig.ELITE_PULL_ENABLED:
            return

        if self.best_ever_candidate is None:
            return

        if self.generations_since_improvement < ESConfig.ELITE_PULL_PATIENCE:
            return

        # Pull mean toward elite
        pull_strength = ESConfig.ELITE_PULL_STRENGTH
        direction = self.best_ever_candidate - self.mean
        self.mean = self.mean + pull_strength * direction

        self.last_update_stats['elite_pull_applied'] = True
        self.last_update_stats['elite_pull_distance'] = float(np.linalg.norm(direction))

    def _apply_novelty_diversity(
        self,
        fitnesses: np.ndarray,
        per_agent_metrics: List[Dict]
    ) -> np.ndarray:
        """
        Apply novelty and diversity bonuses to fitness values.

        For ES with rank transformation, the bonuses need to be scaled appropriately
        to actually affect rankings. We use fitness standard deviation as a reference
        scale, similar to how GA uses novelty_fitness_scale and fitness_magnitude.

        Args:
            fitnesses: Raw fitness values.
            per_agent_metrics: Per-agent metrics containing behavior_vector and reward_diversity.

        Returns:
            Adjusted fitness values with novelty/diversity bonuses.
        """
        adjusted = fitnesses.copy()

        # Calculate fitness statistics for scaling bonuses
        # Using std ensures bonuses are meaningful relative to fitness spread
        fitness_std = float(fitnesses.std())
        fitness_scale = max(fitness_std, 10.0)  # Floor of 10 to avoid division issues

        # Novelty bonus
        if ESConfig.ENABLE_NOVELTY and self.behavior_archive is not None:
            behavior_vectors = [m.get('behavior_vector', [0.0] * 7) for m in per_agent_metrics]
            novelty_scores = compute_population_novelty(
                behavior_vectors,
                self.behavior_archive.get_behaviors(),
                self.novelty_config.k_nearest
            )
            self.behavior_archive.add_batch(behavior_vectors, novelty_scores)

            # Add novelty bonus scaled to be meaningful relative to fitness variance
            novelty_array = np.array(novelty_scores, dtype=np.float32)
            novelty_bonus = ESConfig.NOVELTY_WEIGHT * novelty_array * fitness_scale
            adjusted = adjusted + novelty_bonus

            self.last_update_stats['avg_novelty'] = float(novelty_array.mean())
            self.last_update_stats['avg_novelty_bonus'] = float(novelty_bonus.mean())
            self.last_update_stats['archive_size'] = self.behavior_archive.size()
        else:
            self.last_update_stats['avg_novelty'] = 0.0
            self.last_update_stats['avg_novelty_bonus'] = 0.0
            self.last_update_stats['archive_size'] = 0

        # Diversity bonus
        if ESConfig.ENABLE_DIVERSITY:
            diversity_scores = [m.get('reward_diversity', 0.0) for m in per_agent_metrics]
            diversity_array = np.array(diversity_scores, dtype=np.float32)

            # Scale diversity bonus by fitness scale, similar to novelty
            diversity_bonus = ESConfig.DIVERSITY_WEIGHT * diversity_array * fitness_scale
            adjusted = adjusted + diversity_bonus

            self.last_update_stats['avg_diversity'] = float(diversity_array.mean())
            self.last_update_stats['avg_diversity_bonus'] = float(diversity_bonus.mean())
        else:
            self.last_update_stats['avg_diversity'] = 0.0
            self.last_update_stats['avg_diversity_bonus'] = 0.0

        # Log combined bonus impact for debugging
        self.last_update_stats['fitness_scale_used'] = fitness_scale

        return adjusted

    def _decay_sigma(self) -> None:
        """
        Apply sigma decay with minimum floor.

        If adaptive sigma is enabled and we're stagnating, apply additional decay
        to force faster exploitation.
        """
        # Base decay
        decay_factor = ESConfig.SIGMA_DECAY

        # Adaptive decay when stagnating
        if ESConfig.ADAPTIVE_SIGMA_ENABLED:
            if self.generations_since_improvement >= ESConfig.ADAPTIVE_SIGMA_PATIENCE:
                # Apply additional decay on top of base decay
                decay_factor *= ESConfig.ADAPTIVE_SIGMA_FACTOR
                self.last_update_stats['adaptive_sigma_triggered'] = True
            else:
                self.last_update_stats['adaptive_sigma_triggered'] = False

        self.sigma = max(
            ESConfig.SIGMA_MIN,
            self.sigma * decay_factor
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
