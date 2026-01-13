# Architecture Overview

This document provides a top-down view of the AsteroidsAI codebase structure and key subsystem responsibilities.

## Repository Structure

```
Asteroids AI/
├── Asteroids.py                  # Main visual game (arcade.Window)
├── game/
│   ├── globals.py                # SINGLE SOURCE OF TRUTH for physics & game constants
│   ├── classes/                  # Game entity classes (Player, Asteroid, Bullet)
│   ├── headless_game.py          # Fast, non-visual game for parallel evaluation
│   ├── debug/                    # Debug visualizers
│   │   └── visuals.py            # Overlays for hitboxes and vectors
│   └── sprites/                  # Image assets
├── ai_agents/
│   ├── base_agent.py             # Abstract base class for all agents
│   ├── policies/                 # Neural network architectures (stateless)
│   │   ├── feedforward.py        # MLP implementation
│   │   └── linear.py             # Linear policy implementation
│   └── neuroevolution/           # Evolutionary agents
│       └── nn_agent.py           # Agent wrapper for feedforward policy
├── interfaces/
│   ├── EnvironmentTracker.py     # Provides a clean API to the current game state
│   ├── MetricsTracker.py         # Aggregates episode statistics (kills, accuracy, etc.)
│   ├── RewardCalculator.py       # Composable, component-based reward system
│   ├── StateEncoder.py           # Abstract base class for state encoders
│   ├── ActionInterface.py        # Validates and normalizes agent actions
│   ├── encoders/                 # State encoder implementations (VectorEncoder)
│   └── rewards/                  # Individual reward components (VelocitySurvivalBonus, etc.)
├── training/
│   ├── config/                   # Centralized configuration
│   │   ├── rewards.py            # Reward presets and composition
│   │   └── genetic_algorithm.py  # GA hyperparameters (Pop size, mutation rates, etc.)
│   ├── core/                     # Shared training infrastructure
│   │   ├── episode_runner.py     # Runs a single episode (visual or headless)
│   │   ├── episode_result.py     # Data class for episode outcomes
│   │   ├── population_evaluator.py # Parallel evaluation logic
│   │   └── display_manager.py    # Visual display orchestration
│   ├── methods/                  # Training algorithms
│   │   └── genetic_algorithm/    # GA implementation details
│   │       ├── driver.py         # Main evolution loop logic
│   │       ├── operators.py      # Mutation and crossover functions
│   │       └── selection.py      # Tournament selection
│   ├── analytics/                # Analytics and reporting subsystem
│   │   ├── analytics.py          # Facade for the analytics system
│   │   ├── collection/           # Data collection models and functions
│   │   ├── analysis/             # Analysis logic (population, behavioral, etc.)
│   │   └── reporting/            # Report generation (Markdown, JSON)
│   └── scripts/                  # Entry points
│       └── train_ga.py           # Primary GA training script
└── plans/                        # Project documentation
```

## Core Subsystems

### 1. Game Core & Parity

- **`globals.py`**: The **Single Source of Truth** for all game constants (screen size, physics, hitboxes). Both the visual game and headless simulation import from here to ensure 100% parity.
- **`Asteroids.py`**: The visual game. Uses a custom collision loop that mirrors the headless math exactly, rather than Arcade's default sprite collision. Includes a Debug Mode ('D' key) to visualize the actual hitboxes used by the AI.
- **`headless_game.py`**: High-speed simulation logic. Identical to `Asteroids.py` but strips all rendering and inputs.

### 2. AI Interface Layer (`interfaces/`)

Decouples the AI from the game logic.

- **`EnvironmentTracker`**: Provides a safe API for the AI to query game state (e.g., `get_nearest_asteroid`).
- **`VectorEncoder`**: Converts the game state into a neural network-friendly vector. Uses **Toroidal Distance** math to correctly perceive objects wrapping around the screen.
- **`RewardCalculator`**: Modular system for calculating fitness. Components are configured in `training/config/rewards.py`.

### 3. Agent & Policy Layer (`ai_agents/`)

Separates the "Brain" (Policy) from the "Body" (Agent).

- **`policies/`**: Contains pure mathematical models (e.g., `FeedforwardPolicy`). These classes compute `f(state) -> action` and know nothing about the game or training method.
- **`neuroevolution/nn_agent.py`**: Wraps a policy to implement the `BaseAgent` interface. This is what interacts with the environment.

### 4. Training Infrastructure (`training/`)

- **`config/`**: Centralized settings. `genetic_algorithm.py` controls population size, mutation rates, and network architecture sizes.
- **`core/`**: Reusable components. `EpisodeRunner` executes games. `PopulationEvaluator` handles multithreaded evaluation on headless games. `DisplayManager` handles the visualization of the best agent.
- **`methods/`**: Implementation of specific training algorithms. The GA logic (Selection -> Crossover -> Mutation) resides here, separated from the agent code.
- **`scripts/`**: The executable entry points (e.g., `train_ga.py`) that wire everything together.

### 5. Analytics Subsystem (`training/analytics/`)

A comprehensive suite for monitoring training health.

- **Collection**: Tracks fitness, kills, accuracy, action frequencies, and timing metadata.
- **Analysis**:
  - **Behavioral Classification**: Tags agents as "Sniper", "Dogfighter", "Turret", etc.
  - **Population Health**: Detects stagnation and diversity collapse.
  - **Generalization**: Compares training performance vs. performance on a fresh, unseen seed.
  - **Heatmaps**: Generates spatial heatmaps for best agents and population averages.
- **Reporting**: Generates a detailed `training_summary.md` with ASCII charts, trend tables, and efficiency metrics.

## Data Flow: Parallel Training Loop

1.  **Initialization**: `train_ga.py` initializes the `GADriver`, which creates a population of random parameter vectors.
2.  **Parallel Evaluation**: `PopulationEvaluator` runs 12 games per agent (on different seeds) in parallel `headless_game.py` instances.
3.  **Data Collection**: Metrics are aggregated and sent to `TrainingAnalytics`.
4.  **Display Phase**: `DisplayManager` visually renders the best agent of the generation on a **fresh seed** to test generalization.
5.  **Evolution**: `GADriver` selects parents and applies operators (`training/methods/genetic_algorithm/operators.py`) to create the next generation.
6.  **Loop**: Repeats for `NUM_GENERATIONS` (defined in config).
7.  **Termination**: Final report and JSON data saved.

## Implementation Status

- ✅ **Modular Architecture**: Clean separation of Policy, Agent, Training, and Config.
- ✅ **Sim-to-Real Parity**: Visual and Headless games use identical physics/hitboxes via `globals.py`.
- ✅ **Toroidal Vision**: AI correctly sees across screen boundaries.
- ✅ **Generalization Focus**: Training on 20 seeds/agent forces robust policy learning.
- ✅ **Deep Analytics**: Full behavioral profiling, heatmaps, and health monitoring.
- ✅ **Centralized Config**: Hyperparameters and rewards managed in `training/config/`.