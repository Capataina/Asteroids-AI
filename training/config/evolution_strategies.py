"""
Evolution Strategies Configuration.

Contains hyperparameters for the ES training algorithm.
"""


class ESConfig:
    """Configuration for Evolution Strategies training."""

    # Population and generations
    POPULATION_SIZE = 100         # Number of perturbations per generation (increased for better gradients)
    NUM_GENERATIONS = 500         # Total generations to run

    # ES core parameters
    SIGMA = 0.15                  # Noise standard deviation for perturbations (slightly higher for exploration)
    LEARNING_RATE = 0.05          # Step size for mean updates (5x increase for faster learning)
    WEIGHT_DECAY = 0.0025          # L2 regularization coefficient

    # Sigma schedule
    SIGMA_DECAY = 0.999             # Per-generation sigma decay factor (no decay - maintain exploration)
    SIGMA_MIN = 0.01              # Minimum sigma floor

    # Sampling strategy
    USE_ANTITHETIC = True         # Use mirrored sampling (reduces variance by ~50%)
    USE_RANK_TRANSFORMATION = True  # Use rank-based fitness shaping

    # Evaluation settings
    SEEDS_PER_AGENT = 3           # Rollouts per perturbation for fitness averaging (reduced for speed)
    MAX_STEPS = 1500              # Maximum steps per rollout
    FRAME_DELAY = 1.0 / 60.0      # Fixed time step for evaluation and playback

    # Neural network architecture (must match GA for fair comparison)
    HIDDEN_LAYER_SIZE = 24        # Hidden units in the MLP

    # Initialization
    INIT_MEAN_ZERO = True         # Initialize mean to zeros (False = random uniform)
    INIT_UNIFORM_LOW = -1.0       # Lower bound for random initialization
    INIT_UNIFORM_HIGH = 1.0       # Upper bound for random initialization

    # Novelty/diversity integration (optional)
    ENABLE_NOVELTY = True        # Add novelty bonus to fitness before shaping
    ENABLE_DIVERSITY = True      # Add diversity bonus to fitness before shaping
    NOVELTY_WEIGHT = 0.1          # Weight for novelty bonus
    DIVERSITY_WEIGHT = 0.1        # Weight for diversity bonus
