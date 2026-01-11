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
│   ├── neuroevolution/
│   │   └── genetic_algorithm/
│   │       ├── nn_ga_agent.py    # CURRENT: Agent with a neural network policy
│   │       ├── operators.py      # Mutation and crossover operators
│   │       └── ...               # Legacy agent files
│   └── reinforcement_learning/   # PLANNED: Future home for GNN+SAC agent
├── interfaces/
│   ├── EnvironmentTracker.py     # Provides a clean API to the current game state
│   ├── MetricsTracker.py         # Aggregates episode statistics (kills, accuracy, etc.)
│   ├── RewardCalculator.py       # Composable, component-based reward system
│   ├── StateEncoder.py           # Abstract base class for state encoders
│   ├── ActionInterface.py        # Validates and normalizes agent actions
│   ├── encoders/                 # State encoder implementations (VectorEncoder)
│   └── rewards/                  # Individual reward components (VelocitySurvivalBonus, etc.)
├── training/
│   ├── base/                     # Base classes for all training pipelines
│   │   ├── BaseAgent.py          # Abstract agent interface for all AIs
│   │   ├── EpisodeRunner.py      # Runs a single agent episode (used for visual display)
│   │   └── EpisodeResult.py      # Dataclass for storing episode results
│   ├── analytics/                # Analytics and reporting subsystem
│   │   ├── analytics.py          # Facade for the analytics system
│   │   ├── collection/           # Data collection models and functions
│   │   ├── analysis/             # Analysis logic (population, behavioral, etc.)
│   │   └── reporting/            # Report generation (Markdown, JSON)
│   ├── train_ga_parallel.py      # PRIMARY training script for the GA
│   └── parallel_evaluator.py     # Logic for parallel fitness evaluation
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
- **`RewardCalculator`**: Modular system for calculating fitness. Current composition:
  - `VelocitySurvivalBonus`: Rewards moving fast while staying alive.
  - `DistanceBasedKillReward`: Higher points for close-range kills.
  - `ConservingAmmoBonus`: Rewards accuracy.
  - `DeathPenalty`: Significant penalty for crashing.

### 3. GA Implementation (`ai_agents/neuroevolution/`)

- **`NeuralNetworkGAAgent`**: Feedforward neural network policy.
  - **Inputs (11):** Player velocity (2), Shoot cooldown (1), Nearest 2 Asteroids (4 features each: dist, angle, closing speed, size).
  - **Outputs (4):** Thrust, Turn Left, Turn Right, Shoot.
- **`operators.py`**: Genetic operators. Current configuration uses a low mutation rate (0.05) to preserve learned behaviors.

### 4. Parallel Training Pipeline (`training/`)

- **`train_ga_parallel.py`**: Orchestrates the evolutionary loop (Selection -> Crossover -> Mutation -> Evaluation).
- **`parallel_evaluator.py`**: Uses `ThreadPoolExecutor` to evaluate 25-50 agents in parallel. Each agent is tested on **12 different random seeds** to force generalization and prevent overfitting.

### 5. Analytics Subsystem (`training/analytics/`)

A comprehensive suite for monitoring training health.

- **Collection**: Tracks fitness, kills, accuracy, action frequencies, and timing metadata.
- **Analysis**:
  - **Behavioral Classification**: Tags agents as "Sniper", "Dogfighter", "Turret", etc.
  - **Population Health**: Detects stagnation and diversity collapse.
  - **Generalization**: Compares training performance vs. performance on a fresh, unseen seed.
- **Reporting**: Generates a detailed `training_summary.md` with ASCII charts, trend tables, and efficiency metrics.

## Data Flow: Parallel Training Loop

1.  **Initialization**: Population of neural networks created with random weights.
2.  **Parallel Evaluation**: Each agent plays 12 games on 12 unique seeds in `headless_game.py`. Fitness is averaged.
3.  **Data Collection**: Metrics (accuracy, kills, inputs) are aggregated and sent to Analytics.
4.  **Display Phase**: The single best agent plays ONE game in the visual `Asteroids.py` window on a **fresh seed** to demonstrate true capability (generalization test).
5.  **Evolution**: The top agents are selected to breed. Offspring are mutated.
6.  **Loop**: Repeats for 500+ generations.
7.  **Termination**: Final report and JSON data saved.

## Implementation Status

- ✅ **Sim-to-Real Parity**: Visual and Headless games use identical physics/hitboxes via `globals.py`.
- ✅ **Toroidal Vision**: AI correctly sees across screen boundaries.
- ✅ **Generalization Focus**: Training on 12 seeds/agent forces robust policy learning.
- ✅ **Deep Analytics**: Full behavioral profiling and health monitoring active.
- 🚧 **Configuration**: Hyperparameters are still hardcoded in `train_ga_parallel.py` (planned move to YAML/JSON).
