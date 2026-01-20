class NEATConfig:
    # Core training settings
    POPULATION_SIZE = 50
    NUM_GENERATIONS = 500
    SEEDS_PER_AGENT = 5  # Increased from 3 for more stable fitness estimates
    MAX_STEPS = 1500
    FRAME_DELAY = 1.0 / 60.0
    USE_COMMON_SEEDS = True  # CRN: all agents see same seeds, removes seed luck from rankings

    # NEAT structure
    OUTPUT_SIZE = 3
    INITIAL_WEIGHT_RANGE = (-1.0, 1.0)

    # Speciation
    COMPATIBILITY_THRESHOLD = 0.25
    C1 = 1.0  # excess coefficient
    C2 = 1.0  # disjoint coefficient
    C3 = 0.4  # weight diff coefficient
    SPECIES_STAGNATION = 7  # Reduced from 15 to fail fast on dead-end species
    ELITISM_PER_SPECIES = 1
    ADAPT_COMPATIBILITY_THRESHOLD = True
    TARGET_SPECIES = 8
    COMPATIBILITY_ADJUST_STEP = 0.02
    COMPATIBILITY_MIN = 0.05
    COMPATIBILITY_MAX = 3.0

    # Reliability & Stopping
    FITNESS_STD_PENALTY_RATIO = 1.0  # Penalize fitness by 1.0 * std_dev to filter out seed luck
    EARLY_STOPPING_GENERATIONS = 25  # Stop training if best fitness doesn't improve for 25 gens

    # Reproduction
    CROSSOVER_PROB = 0.75
    INHERIT_DISABLED_PROB = 0.75

    # Mutation
    WEIGHT_MUTATION_PROB = 0.1
    WEIGHT_MUTATION_SIGMA = 0.5
    ADD_CONNECTION_PROB = 0.05
    ADD_NODE_PROB = 0.03

    # Complexity guardrails
    MAX_NODES = None
    MAX_CONNECTIONS = None

    # Novelty/diversity selection shaping (behavior-based diversity pressure)
    ENABLE_NOVELTY = True  # Reward agents that behave differently from others
    ENABLE_DIVERSITY = True  # Reward agents that earn reward from multiple sources
