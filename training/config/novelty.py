"""
Novelty and Diversity Configuration

Shared configuration for behavior novelty and reward diversity systems
that apply to all optimization methods (GA, ES, NEAT, etc.).
"""


class NoveltyConfig:
    """Configuration for novelty and diversity systems."""

    # === Behavior Novelty Settings ===

    # Enable/disable behavior novelty in selection
    enable_behavior_novelty: bool = True

    # Weight of behavior novelty in selection score
    # Higher = more emphasis on being different
    behavior_novelty_weight: float = 0.15

    # Scale factor to bring novelty scores into fitness range
    # Novelty scores are typically 0-2, fitness can be -150 to +500
    novelty_fitness_scale: float = 50.0

    # Number of nearest neighbors for novelty calculation
    k_nearest: int = 15

    # === Behavior Archive Settings ===

    # Maximum behaviors stored in the archive
    archive_max_size: int = 500

    # Minimum novelty score to be added to archive
    archive_novelty_threshold: float = 0.25

    # === Reward Diversity Settings ===

    # Enable/disable reward diversity in selection
    enable_reward_diversity: bool = True

    # Weight of reward diversity in selection score
    # Higher = more emphasis on balanced reward usage
    diversity_weight: float = 0.2

    # Minimum number of positive reward components for diversity bonus
    min_positive_components: int = 2

    # === Combined Selection ===

    # If True, normalize all scores before combining
    # If False, use raw weighted sum
    normalize_scores: bool = False

    def __init__(self, **kwargs):
        """
        Initialize config, optionally overriding defaults.

        Example:
            config = NoveltyConfig(behavior_novelty_weight=0.3, enable_reward_diversity=False)
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Unknown config parameter: {key}")

    def to_dict(self) -> dict:
        """Export config as dictionary for logging/saving."""
        return {
            'enable_behavior_novelty': self.enable_behavior_novelty,
            'behavior_novelty_weight': self.behavior_novelty_weight,
            'novelty_fitness_scale': self.novelty_fitness_scale,
            'k_nearest': self.k_nearest,
            'archive_max_size': self.archive_max_size,
            'archive_novelty_threshold': self.archive_novelty_threshold,
            'enable_reward_diversity': self.enable_reward_diversity,
            'diversity_weight': self.diversity_weight,
            'min_positive_components': self.min_positive_components,
            'normalize_scores': self.normalize_scores,
        }

    @classmethod
    def disabled(cls) -> 'NoveltyConfig':
        """Create config with all novelty/diversity features disabled."""
        return cls(
            enable_behavior_novelty=False,
            enable_reward_diversity=False
        )

    @classmethod
    def novelty_only(cls) -> 'NoveltyConfig':
        """Create config with only behavior novelty enabled."""
        return cls(
            enable_behavior_novelty=True,
            enable_reward_diversity=False
        )

    @classmethod
    def diversity_only(cls) -> 'NoveltyConfig':
        """Create config with only reward diversity enabled."""
        return cls(
            enable_behavior_novelty=False,
            enable_reward_diversity=True
        )

    @classmethod
    def aggressive(cls) -> 'NoveltyConfig':
        """Create config with higher novelty/diversity pressure."""
        return cls(
            behavior_novelty_weight=0.25,
            diversity_weight=0.35,
            archive_novelty_threshold=0.2
        )
