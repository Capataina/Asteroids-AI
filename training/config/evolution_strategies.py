"""
Evolution Strategies Configuration.

Contains hyperparameters for the ES training algorithm.

ES maintains a Gaussian distribution over parameter space (mean θ, stddev σ) and
iteratively updates the mean by estimating the gradient of expected fitness through
sampling perturbations.
"""


class ESConfig:
    """Configuration for Evolution Strategies training."""

    # ==========================================================================
    # Population and Generations
    # ==========================================================================

    # Number of perturbations sampled per generation.
    # Higher values give better gradient estimates but cost more compute.
    # With antithetic sampling, this is split into N/2 pairs of +ε/-ε.
    POPULATION_SIZE = 100

    # Total number of generations to train for.
    # Each generation: sample → evaluate → update mean.
    NUM_GENERATIONS = 500

    # ==========================================================================
    # ES Core Parameters
    # ==========================================================================

    # Noise standard deviation for perturbations.
    # Controls exploration radius around the current mean.
    # Higher = more exploration but noisier gradients.
    # Lower = more exploitation but risk of local optima.
    SIGMA = 0.15

    # Learning rate (step size) for mean updates.
    # Controls how far the mean moves in the estimated gradient direction.
    # Too high = unstable, too low = slow convergence.
    # With AdamW, this can be lower since momentum helps.
    LEARNING_RATE = 0.03

    # L2 regularization coefficient.
    # Penalizes large parameter values to prevent overfitting.
    # Applied as: θ ← θ * (1 - weight_decay) after gradient update.
    WEIGHT_DECAY = 0.0025

    # ==========================================================================
    # CMA-ES (Diagonal) Parameters
    # ==========================================================================

    # Optimizer type for ES training.
    # Options: "cmaes" (default), "classic"
    OPTIMIZER = "cmaes"

    # Initial CMA-ES sigma (step size). Defaults to SIGMA if left as None.
    CMAES_SIGMA = 0.15

    # Number of parents (mu). If None, uses POPULATION_SIZE // 2.
    CMAES_MU = None

    # Minimum diagonal covariance value (numerical stability).
    CMAES_COV_MIN = 1e-6
    # Target aggregate covariance learning rate (c1 + cmu) for diagonal CMA-ES.
    # If set, the base c1/cmu values are scaled up to reach this target in high dimensions.
    CMAES_COV_TARGET_RATE = 1e-3
    # Maximum scaling factor applied to c1/cmu when targeting CMAES_COV_TARGET_RATE.
    CMAES_COV_MAX_SCALE = 1e4

    # ==========================================================================
    # Sigma Schedule
    # ==========================================================================

    # Per-generation multiplicative decay factor for sigma.
    # Reduces exploration over time as the mean converges.
    # Set to 1.0 for no decay (constant exploration).
    # 0.99 reaches σ=0.05 by ~gen 50, 0.999 reaches σ=0.05 by ~gen 500.
    SIGMA_DECAY = 0.99

    # Minimum sigma floor.
    # Prevents sigma from decaying to zero, maintaining some exploration.
    SIGMA_MIN = 0.02

    # Adaptive sigma decay: accelerate decay when stagnating.
    # If enabled, sigma decays faster when no improvement for ADAPTIVE_SIGMA_PATIENCE generations.
    ADAPTIVE_SIGMA_ENABLED = True
    ADAPTIVE_SIGMA_PATIENCE = 10      # Generations without improvement before accelerating decay
    ADAPTIVE_SIGMA_FACTOR = 0.95      # Aggressive decay factor when stagnating (applied on top of normal decay)

    # ==========================================================================
    # Sampling Strategy
    # ==========================================================================

    # Use antithetic (mirrored) sampling.
    # Generates +ε and -ε perturbation pairs instead of independent samples.
    # Reduces gradient variance by ~50% when paired candidates see same seeds.
    USE_ANTITHETIC = True

    # Use rank-based fitness shaping (OpenAI ES style).
    # Transforms fitnesses to utilities based on rank, not magnitude.
    # Reduces sensitivity to outliers and keeps gradient scale stable.
    USE_RANK_TRANSFORMATION = True

    # ==========================================================================
    # Evaluation Settings
    # ==========================================================================

    # Number of rollouts per candidate for fitness averaging.
    # Higher = more robust fitness estimates but slower evaluation.
    SEEDS_PER_AGENT = 3

    # Maximum steps per rollout episode.
    # Episodes end early if the agent dies.
    MAX_STEPS = 1500

    # Fixed time step for evaluation and playback (1/60 = 60 FPS).
    FRAME_DELAY = 1.0 / 60.0

    # Use Common Random Numbers (CRN) for evaluation.
    # When True: All candidates in a generation see the same seed set.
    # This ensures fitness differences reflect parameter differences, not luck.
    # Critical for ES gradient estimation; enables proper antithetic variance reduction.
    # Seeds change across generations to maintain generalization pressure.
    USE_COMMON_SEEDS = True

    # ======================================================================
    # Noise Handling (ES)
    # ======================================================================

    # Re-evaluate top-K candidates with extra seeds to reduce seed luck.
    NOISE_HANDLING_ENABLED = True
    NOISE_HANDLING_TOP_K = 5
    NOISE_HANDLING_EXTRA_SEEDS = 1
    NOISE_HANDLING_SEED_OFFSET = 100000

    # ======================================================================
    # Restarts (ES)
    # ======================================================================

    # Restart search when best fitness stagnates for too long.
    RESTART_ENABLED = True
    RESTART_PATIENCE = 12
    RESTART_MIN_GENERATIONS = 5
    RESTART_COOLDOWN = 5
    RESTART_SIGMA_MULTIPLIER = 1.0
    RESTART_USE_BEST_CANDIDATE = True

    # ==========================================================================
    # Neural Network Architecture
    # ==========================================================================

    # Number of hidden units in the single-layer MLP.
    # Must match GA for fair comparison.
    # Total params = input*hidden + hidden + hidden*output + output.
    HIDDEN_LAYER_SIZE = 24

    # ==========================================================================
    # Temporal Encoding
    # ==========================================================================

    # Wrap the base encoder with temporal stacking (N frames) and deltas.
    USE_TEMPORAL_STACK = True

    # Number of frames to stack (N).
    TEMPORAL_STACK_SIZE = 4

    # Include frame-to-frame deltas (N-1) after the stacked frames.
    TEMPORAL_INCLUDE_DELTAS = True

    # ==========================================================================
    # Initialization
    # ==========================================================================

    # Initialize mean parameter vector to zeros.
    # If False, uses random uniform initialization.
    # Zero init is common for ES; outputs start near 0.5 (sigmoid midpoint).
    INIT_MEAN_ZERO = True

    # Bounds for random uniform initialization (only used if INIT_MEAN_ZERO=False).
    INIT_UNIFORM_LOW = -1.0
    INIT_UNIFORM_HIGH = 1.0

    # ==========================================================================
    # Novelty/Diversity Integration
    # ==========================================================================

    # Add behavior novelty bonus to fitness before rank shaping.
    # Rewards agents that behave differently from the population/archive.
    # Helps prevent premature convergence to local optima.
    ENABLE_NOVELTY = True

    # Add reward diversity bonus to fitness before rank shaping.
    # Rewards agents that earn rewards from multiple sources (not just one).
    # Helps prevent degenerate strategies like "camp and shoot".
    ENABLE_DIVERSITY = True

    # Weight for novelty bonus.
    # Actual bonus = NOVELTY_WEIGHT * novelty_score * fitness_std.
    # Scaled by fitness_std to ensure bonuses affect rankings meaningfully.
    NOVELTY_WEIGHT = 0.1

    # Weight for diversity bonus.
    # Actual bonus = DIVERSITY_WEIGHT * diversity_score * fitness_std.
    # Scaled by fitness_std to ensure bonuses affect rankings meaningfully.
    DIVERSITY_WEIGHT = 0.1

    # ==========================================================================
    # AdamW Optimizer
    # ==========================================================================

    # Use AdamW optimizer instead of vanilla SGD for mean updates.
    # AdamW provides momentum (smooths noisy gradients) and adaptive per-parameter
    # learning rates, which helps with ES's noisy gradient estimates.
    USE_ADAMW = True

    # Beta1: Exponential decay rate for first moment (momentum).
    # Higher = more momentum, smoother updates but slower to adapt.
    # Typical value: 0.9
    ADAMW_BETA1 = 0.9

    # Beta2: Exponential decay rate for second moment (adaptive LR).
    # Higher = more stable per-parameter LR estimates.
    # Typical value: 0.999
    ADAMW_BETA2 = 0.999

    # Epsilon: Small constant for numerical stability in AdamW.
    ADAMW_EPSILON = 1e-8

    # ==========================================================================
    # Elitism
    # ==========================================================================

    # Enable elitism: track best-ever candidate and include it in evaluation.
    # This prevents "forgetting" good solutions when the mean drifts away.
    ENABLE_ELITISM = True

    # How often to inject the elite into the candidate pool (every N generations).
    # Set to 1 to always include elite, higher values for occasional injection.
    ELITE_INJECTION_FREQUENCY = 1

    # Whether to bias the mean toward the elite when stagnating.
    # If enabled, pulls the mean slightly toward the best-ever candidate.
    ELITE_PULL_ENABLED = True
    ELITE_PULL_STRENGTH = 0.1         # How much to pull mean toward elite (0-1)
    ELITE_PULL_PATIENCE = 15          # Generations of stagnation before pulling
