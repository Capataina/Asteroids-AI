# Architecture Overview

Top-down view of the AsteroidsAI codebase structure and responsibilities.

## Repository Structure

```
Asteroids AI/
├── Asteroids.py                  # Main visual game (arcade.Window)
├── game/
│   ├── classes/                  # Game entity classes
│   │   ├── player.py             # Player ship (movement, shooting)
│   │   ├── bullet.py             # Bullet projectiles
│   │   └── asteroid.py           # Asteroids (HP, fragmentation)
│   ├── headless_game.py          # Headless game for parallel evaluation
│   └── sprites/                  # Image assets
├── ai_agents/
│   ├── neuroevolution/
│   │   └── genetic_algorithm/
│   │       ├── ga_agent.py       # LEGACY: Agent with simple linear policy
│   │       ├── nn_ga_agent.py    # CURRENT: Agent with neural network policy
│   │       ├── ga_trainer.py     # GA configuration and component container
│   │       ├── ga_fitness.py     # Fitness evaluation (NOTE: broken, not used)
│   │       └── operators.py      # Mutation and crossover operators
│   └── reinforcement_learning/
│       └── gnn_and_sac/
│           ├── env_wrapper.py    # Graph-based RL wrapper (legacy)
│           ├── gnn.py            # Graph neural network models
│           ├── policies.py       # Policy implementations
│           └── sac.py            # Soft Actor-Critic RL algorithm
├── interfaces/
│   ├── EnvironmentTracker.py     # Current state snapshot, game access
│   ├── MetricsTracker.py         # Aggregated episode statistics
│   ├── RewardCalculator.py       # Component-based reward system
│   ├── StateEncoder.py           # Abstract base class for state encoders
│   ├── ActionInterface.py        # Action validation and normalization
│   ├── encoders/
│   │   └── VectorEncoder.py      # Fixed-size vector for GA
│   └── rewards/                  # Individual reward components
├── training/
│   ├── base/
│   │   ├── BaseAgent.py          # Abstract agent interface
│   │   ├── EpisodeRunner.py      # Episode execution (visual display)
│   │   └── EpisodeResult.py      # Episode result dataclass
│   ├── train_ga.py               # Original GA training (superseded)
│   ├── train_ga_parallel.py      # Parallel GA training driver (PRIMARY)
│   ├── parallel_evaluator.py     # Parallel fitness evaluation
│   └── analytics.py              # Training analytics and reporting
├── tests/
│   ├── test_ga_dimensions.py     # GA dimension tests
│   └── test_kill_asteroid_reward.py
└── train_agent.py                # Legacy training loop (not used for GA)
```

## Core Subsystems

### Game Core (`Asteroids.py` + `game/headless_game.py`)

- **Asteroids.py**: Visual game with arcade.Window for display. Used during training to display the best agent of a generation playing in a _fresh, unseeded_ game.
- **HeadlessAsteroidsGame**: Fast, non-visual game simulation used for the parallel evaluation of the agent population.

### AI Interface Layer (`interfaces/`)

- **EnvironmentTracker**: Provides a snapshot of the current game state (player, asteroids, bullets).
- **MetricsTracker**: Aggregates statistics over an episode (shots fired, kills, time alive, etc.).
- **RewardCalculator**: A composable system that combines multiple reward components into a single fitness score.
- **VectorEncoder**: Encodes the game state into a fixed-size vector for the agent. The default configuration produces a 16-dimensional vector (6 player features + 5 features for each of the 2 nearest asteroids).
- **ActionInterface**: Validates and normalizes the agent's output action vector.

### GA Implementation (`ai_agents/neuroevolution/genetic_algorithm/`)

- **NeuralNetworkGAAgent**: The current agent used for GA training. It implements `BaseAgent` with a feedforward neural network policy.

  - **Architecture**: Input(16) -> Hidden(24, tanh) -> Output(4, sigmoid).
  - The parameter vector evolved by the GA represents the flattened weights and biases of this network.
  - For the default architecture, this results in **508 parameters** per agent.

- **GATrainer**: A container class that holds hyperparameters (population size, mutation rates, etc.) and shared components (state encoder, action interface). Its `train()` method is **not** used by the current parallel training pipeline.

- **GAGeneticOperators**: A class in `operators.py` that implements the mutation (Gaussian) and crossover (blend) operators used in the evolutionary process.

### Parallel Training (`training/`)

- **train_ga_parallel.py**: The main entry point for GA training.
  - **ParallelGATrainingDriver**: This class contains the primary GA training loop. It manages the population, orchestrates evaluation, and runs the evolutionary steps (selection, crossover, mutation).
- **parallel_evaluator.py**: Provides the `evaluate_population_parallel()` function, which evaluates the entire population's fitness simultaneously using a `ThreadPoolExecutor` and headless game instances.
- **EpisodeRunner**: Used only during the visual display phase of the best agent, not for parallel evaluation.

## Data Flow: Current Parallel Training

1.  **Initialization**: `ParallelGATrainingDriver._initialize_population()` creates a population of random parameter vectors. Each vector corresponds to the flattened weights of a `NeuralNetworkGAAgent`.

2.  **Parallel Evaluation**: `evaluate_population_parallel()` is called. It creates a `HeadlessAsteroidsGame` for each agent in the population and runs them in parallel to get their fitness scores and behavioral metrics. All agents in a generation are evaluated using the same random seed for fairness.

3.  **Display Phase**: The best agent from the evaluated generation is instantiated as a `NeuralNetworkGAAgent`. It is then run in the main visual `AsteroidsGame` instance with **new, random asteroid positions** to test its ability to generalize.

4.  **Evolution**: `ParallelGATrainingDriver._evolve_generation()` creates the next generation's population using:

- Tournament selection
- Blend crossover
- Gaussian mutation
- Elitism (top 20% of the previous generation survive)

5.  **Loop**: The process repeats from Step 2 for the specified number of generations.

## Implementation Status

### Completed Infrastructure

- **Parallel GA Training**: A full, working implementation that uses a neural network agent, parallel evaluation, and visual display of the best agent.
- All core interfaces (`EnvironmentTracker`, `MetricsTracker`, `RewardCalculator`, `VectorEncoder`, `BaseAgent`) are integrated and functional.

### Known Issues (As of 2026-01-05 - _Updated_)

1.  **Hardcoded NN Architecture**: The neural network's hidden layer size (24) is hardcoded in `train_ga_parallel.py`. This should be moved to a configuration file or the `GATrainer` for better modularity.

2.  **Unused/Broken GA Files**: The original GA files are now outdated or broken and are not used by the main training pipeline.
    - `ga_trainer.py`: Its `train()` and `elitism()` methods are buggy and unused.
    - `ga_fitness.py`: This file is broken (references uninitialized attributes) and unused.
    - `ga_agent.py`: This is a legacy agent with a simpler linear policy and is not used.

### Previously Known Issues (Now Fixed)

- **~~VectorEncoder sorting~~**: This issue has been **FIXED**. The `VectorEncoder` now correctly sorts asteroids by distance.
- **~~operators.py crossover bug~~**: This issue has been **FIXED**. The `crossover_blend` operator now correctly uses the `crossover_alpha` parameter.

## Configuration

### Current GA Hyperparameters (`train_ga_parallel.py`)

```python
population_size = 100
num_generations = 500
hidden_size = 24                 # Neural network hidden layer size
mutation_probability = 0.20      # Per-gene probability
crossover_probability = 0.7
mutation_gaussian_sigma = 0.15
elitism = 20%                    # Top 20% survive
tournament_size = 3
max_steps = 1500                 # Per episode
```
