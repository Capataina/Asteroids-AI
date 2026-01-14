"""
Genetic Algorithm Configuration.

Contains hyperparameters for the GA training algorithm.

GA maintains a population of individuals (parameter vectors) and evolves them
through selection, crossover, and mutation operators over generations.
"""


class GAConfig:
    """Configuration for Genetic Algorithm training."""

    # ==========================================================================
    # Population and Generations
    # ==========================================================================

    # Number of individuals in the population.
    # Smaller populations evolve faster but may lack diversity.
    # Larger populations explore more but cost more compute.
    POPULATION_SIZE = 10

    # Total number of generations to train for.
    # Each generation: evaluate → select → crossover → mutate.
    NUM_GENERATIONS = 500

    # ==========================================================================
    # Genetic Operators
    # ==========================================================================

    # Probability of mutating each gene (parameter) in an individual.
    # Higher = more exploration but may disrupt good solutions.
    # Lower = more exploitation but may get stuck.
    MUTATION_PROBABILITY = 0.05

    # Probability of applying crossover between two parents.
    # When crossover doesn't occur, parents pass directly to next generation.
    CROSSOVER_PROBABILITY = 0.7

    # Standard deviation for Gaussian mutation noise.
    # Controls the magnitude of parameter changes during mutation.
    MUTATION_GAUSSIAN_SIGMA = 0.1

    # Bounds for uniform random mutation (used for initialization).
    MUTATION_UNIFORM_LOW = -1.0
    MUTATION_UNIFORM_HIGH = 1.0

    # BLX-alpha crossover blending factor.
    # Controls how much offspring can extend beyond parent values.
    # alpha=0 = simple averaging, alpha=0.5 = can explore 50% beyond parents.
    CROSSOVER_ALPHA = 0.5

    # ==========================================================================
    # Evaluation Settings
    # ==========================================================================

    # Number of rollouts per individual for fitness averaging.
    # Higher = more robust fitness estimates but slower evaluation.
    SEEDS_PER_AGENT = 5

    # Maximum steps per rollout episode.
    # Episodes end early if the agent dies.
    MAX_STEPS = 1500

    # Fixed time step for evaluation and playback (1/60 = 60 FPS).
    FRAME_DELAY = 1.0 / 60.0

    # Use Common Random Numbers (CRN) for evaluation.
    # When True: All individuals in a generation see the same seed set.
    # GA is more noise-tolerant than ES due to tournament selection + elitism,
    # so this is optional (default False for GA).
    USE_COMMON_SEEDS = False

    # ==========================================================================
    # Neural Network Architecture
    # ==========================================================================

    # Number of nearest asteroids to encode in the state vector.
    # Only used if VectorEncoder is selected (HybridEncoder has its own config).
    NUM_NEAREST_ASTEROIDS = 8

    # Number of hidden units in the single-layer MLP.
    # Must match ES for fair comparison.
    # Total params = input*hidden + hidden + hidden*output + output.
    HIDDEN_LAYER_SIZE = 24
