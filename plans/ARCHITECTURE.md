# Architecture Overview

This document provides a top-down view of the AsteroidsAI codebase structure and key subsystem responsibilities.

## Repository Structure

```
Asteroids AI/
├── Asteroids.py                  # Main visual game (arcade.Window)
├── game/
│   ├── classes/                  # Game entity classes (Player, Asteroid, Bullet)
│   ├── headless_game.py          # Fast, non-visual game for parallel evaluation
│   └── sprites/                  # Image assets
├── ai_agents/
│   ├── neuroevolution/
│   │   └── genetic_algorithm/
│   │       ├── nn_ga_agent.py    # CURRENT: Agent with a neural network policy
│   │       ├── operators.py      # Mutation and crossover operators
│   │       ├── ga_agent.py       # LEGACY: Agent with a simple linear policy
│   │       ├── ga_trainer.py     # LEGACY: Unused GA component container
│   │       └── ga_fitness.py     # LEGACY: Broken and unused
│   └── reinforcement_learning/
│       └── gnn_and_sac/          # PLANNED: Future home for GNN+SAC agent
├── interfaces/
│   ├── EnvironmentTracker.py     # Provides a clean API to the current game state
│   ├── MetricsTracker.py         # Aggregates episode statistics (kills, accuracy, etc.)
│   ├── RewardCalculator.py       # Composable, component-based reward system
│   ├── StateEncoder.py           # Abstract base class for state encoders
│   ├── ActionInterface.py        # Validates and normalizes agent actions
│   ├── encoders/                 # State encoder implementations
│   └── rewards/                  # Individual reward components
├── training/
│   ├── base/                     # Base classes for all training pipelines
│   │   ├── BaseAgent.py          # Abstract agent interface for all AIs
│   │   ├── EpisodeRunner.py      # Runs a single agent episode (used for visual display)
│   │   └── EpisodeResult.py      # Dataclass for storing episode results
│   ├── analytics/                # Analytics and reporting subsystem
│   │   ├── analytics.py          # Facade for the analytics system
│   │   ├── collection/           # Data collection models and functions
│   │   └── reporting/            # Report generation (Markdown, JSON)
│   ├── train_ga_parallel.py      # PRIMARY training script for the GA
│   ├── parallel_evaluator.py     # Logic for parallel fitness evaluation
│   ├── train_ga.py               # LEGACY: Original, sequential GA training script
│   └── train_agent.py            # LEGACY: Original, pre-GA training script
└── plans/                        # Project documentation
```

## Core Subsystems

### 1. Game Core
- **`Asteroids.py`**: The main visual game window, powered by Arcade. During training, this is used **only** to display the best-performing agent of a generation in a fresh, unseeded game.
- **`headless_game.py`**: A high-speed, non-visual version of the game simulation. Its sole purpose is to run in parallel threads for the fast evaluation of the agent population.

### 2. AI Interface Layer (`interfaces/`)
This layer decouples the AI from the game. It provides a stable set of contracts that all agents and training pipelines use.
- **`EnvironmentTracker` & `MetricsTracker`**: Provide read-only access to game state and performance statistics.
- **`RewardCalculator`**: A flexible system that computes agent fitness from a collection of individual reward components.
- **`StateEncoder` & `ActionInterface`**: Standardize the "input" (what the agent sees) and "output" (what the agent does) for all AI models.

### 3. GA Implementation (`ai_agents/neuroevolution/genetic_algorithm/`)
- **`NeuralNetworkGAAgent`**: The current agent policy. It is a feedforward neural network whose weights and biases are evolved by the GA. The default architecture is `Input(16) -> Hidden(24, tanh) -> Output(4, sigmoid)`.
- **`operators.py`**: Contains the genetic operators (e.g., `mutate_gaussian`, `crossover_blend`) used in the evolutionary process.

### 4. Parallel Training Pipeline (`training/`)
This is the heart of the current GA implementation.
- **`train_ga_parallel.py`**: The main entry point. The `ParallelGATrainingDriver` class within this file manages the primary training loop (population, evolution, visualization).
- **`parallel_evaluator.py`**: Contains the `evaluate_population_parallel` function. This powerful component uses a `ThreadPoolExecutor` to run the entire population's fitness evaluations simultaneously in headless game instances.
- **`EpisodeRunner`**: A simpler, single-episode runner. In the parallel pipeline, its role is limited to running the single best agent in the visual game window for generalization testing.

### 5. Analytics Subsystem (`training/analytics/`)
- **`analytics.py`**: Acts as a facade for the analytics system, providing a simple API for recording data and generating reports.
- **`collection/`**: Contains the data models (`AnalyticsData`) that define the schema for `training_data.json` and the functions that collect metrics.
- **`reporting/`**: Contains the logic for generating the final `training_summary.md` report and `training_data.json` file.

## Data Flow: Parallel Training Loop

1.  **Initialization**: `ParallelGATrainingDriver` creates an initial population of random parameter vectors, each representing a `NeuralNetworkGAAgent`.
2.  **Parallel Evaluation**: `evaluate_population_parallel` is called. It spawns a thread for each agent, each with its own `HeadlessAsteroidsGame` instance, and calculates its fitness.
3.  **Data Collection**: The results are passed to the `TrainingAnalytics` instance, which records all statistics for the generation.
4.  **Display Phase**: The best agent from the generation is instantiated and run in the visual `Asteroids.py` game with **new, random asteroid positions** to test its generalization capability. The results of this "fresh game" test are also recorded by the analytics system.
5.  **Evolution**: `ParallelGATrainingDriver` creates the next generation's population using tournament selection, crossover, mutation, and elitism.
6.  **Loop**: The process repeats from Step 2 for the specified number of generations.
7.  **Termination**: On exit, the `TrainingAnalytics` instance saves all collected data to `training_data.json` and generates the final `training_summary.md` report.

## Implementation Status & Known Issues

- **Primary Implementation Complete**: The parallel GA training pipeline with a neural network agent is fully functional. All core interfaces are integrated.
- **Known Issue: Hardcoded Configuration**: Many key hyperparameters (hidden layer size, population size, mutation rates) are hardcoded in `train_ga_parallel.py`. A dedicated configuration system is the next major planned feature.
- **Legacy Code**: Several files, such as `ga_agent.py` and `ga_trainer.py`, are now considered legacy and are not used by the primary training pipeline. They are kept for historical reference.