# Architecture Overview

Top-down view of the AsteroidsAI codebase structure and responsibilities.

## Repository Structure

```
Asteroids AI/
├── Asteroids.py              # Main game loop (arcade.Window)
├── game/
│   ├── classes/              # Game entity classes
│   │   ├── player.py         # Player ship (movement, shooting)
│   │   ├── bullet.py         # Bullet projectiles
│   │   └── asteroid.py       # Asteroids (HP, fragmentation)
│   └── sprites/              # Image assets
├── ai_agents/
│   └── reinforcement_learning/
│       └── gnn_and_sac/
│           ├── env_wrapper.py # Graph-based RL wrapper (AsteroidsGraphEnv)
│           ├── gnn.py         # Graph neural network models
│           ├── policies.py   # Policy implementations
│           └── sac.py         # Soft Actor-Critic RL algorithm
├── interfaces/
│   ├── EnvironmentTracker.py # Current state snapshot, events, derived metrics
│   ├── MetricsTracker.py     # Aggregated episode statistics
│   ├── RewardCalculator.py   # Component-based reward system
│   ├── rewards/              # Individual reward component implementations
│   │   ├── SurvivalBonus.py
│   │   ├── KillAsteroid.py
│   │   ├── ChunkBonus.py
│   │   ├── AccuracyBonus.py
│   │   ├── NearMiss.py
│   │   └── KPMBonus.py
│   ├── StateEncoder.py        # Abstract base class for state encoders (plan 004)
│   ├── encoders/             # State encoder implementations (plan 004)
│   │   ├── VectorEncoder.py  # Fixed-size vector for GA/ES/NEAT
│   │   └── GraphEncoder.py   # Graph encoding for GNN
│   └── ActionInterface.py    # Action validation and normalization (plan 004)
└── train_agent.py            # Training loop driver
```

## Core Subsystems

### Game Core (`Asteroids.py`)
- **Responsibility**: Physics simulation, collision detection, rendering, input handling
- **Key Classes**: `AsteroidsGame` (arcade.Window subclass)
- **State**: Player, asteroids, bullets (arcade.SpriteList), score, key states
- **Update Loop**: `on_update(delta_time)` handles all game logic

### Game Entities (`game/classes/`)
- **Player**: Movement (thrust, rotation), shooting with cooldown
- **Bullet**: Projectile with lifetime, velocity
- **Asteroid**: HP-based destruction, fragmentation into smaller asteroids

### AI Interface Layer (`interfaces/`)
- **EnvironmentTracker**: Current state snapshot, derived metrics, event detection
  - ✅ Complete: Basic state access, derived metrics (nearest asteroid, distances)
  - Provides stable API for game state access
- **MetricsTracker**: Aggregated statistics over episode (accuracy, kills, time alive)
  - ✅ Complete: Episode-level statistics, accuracy, rates
  - Tracks cumulative metrics over episode
- **RewardCalculator**: Component-based reward system
  - ✅ Complete: `ComposableRewardCalculator` + 6 reward components
  - Modular, composable reward components
- **StateEncoder** (plan 004): Abstract base class for state encoders
  - **VectorEncoder**: Fixed-size vector encoding for GA/ES/NEAT
  - **GraphEncoder**: Graph encoding for GNN (refactored from env_wrapper)
  - All encoders use EnvironmentTracker (no direct game access)
- **ActionInterface** (plan 004): Action validation and normalization
  - Standardizes action format: `[left, right, thrust, shoot]`
  - Supports boolean and continuous action spaces
- **Purpose**: Stable API for all AI methods to access game state, metrics, rewards, and encode states

### AI Wrappers (`ai_agents/reinforcement_learning/gnn_and_sac/`)
- **AsteroidsGraphEnv**: Graph-based RL wrapper for GNN+SAC
- **Current State**: Accesses `self.game.*` directly, uses `_get_graph_state()` method
- **Future**: Will use `GraphEncoder` from interfaces (after plan 004 complete)
- **Note**: Wrapper refactoring deferred until after infrastructure plans (001-006) complete

### Training (`train_agent.py`)
- **Current State**: Legacy training loop, creates game and wraps with `AsteroidsGraphEnv`
- **Future**: Will be refactored in plan 005 to use BaseAgent and EpisodeRunner
- **Integration**: Will use all infrastructure (trackers, rewards, encoders, actions) via EpisodeRunner

## Data Flow

### Current Flow (Legacy)

1. **Game Update**: `AsteroidsGame.on_update()` → updates sprites, collisions, calls `tracker.update()`
2. **Tracker Update**: `EnvironmentTracker.update()` → detects events, `MetricsTracker.update()` → aggregates stats
3. **AI Observation**: `AsteroidsGraphEnv._get_graph_state()` → reads `self.game.*` directly
4. **AI Action**: `AsteroidsGraphEnv.step()` → sets `self.game.left_pressed`, etc.
5. **Reward Calculation**: `ComposableRewardCalculator.calculate_step_reward()` → sums enabled component rewards
6. **Training Loop**: `AIDriver.update()` → calls `env.step()`, receives rewards from RewardCalculator

### Future Flow (After Plans 004-005)

1. **Game Update**: `AsteroidsGame.on_update()` → updates sprites, collisions, calls `tracker.update()`
2. **Tracker Update**: `EnvironmentTracker.update()` → detects events, `MetricsTracker.update()` → aggregates stats
3. **State Encoding**: `StateEncoder.encode(env_tracker)` → converts tracker state to AI representation (vector/graph)
4. **AI Observation**: `BaseAgent.get_action(state)` → receives encoded state
5. **Action Conversion**: `ActionInterface.to_game_input(action)` → converts action to game inputs
6. **Game Step**: Game processes action, updates state
7. **Reward Calculation**: `ComposableRewardCalculator.calculate_step_reward()` → sums enabled component rewards
8. **Episode Loop**: `EpisodeRunner.run_episode()` → orchestrates full episode lifecycle

## Implementation Status

### Completed Infrastructure

- **EnvironmentTracker**: ✅ Complete (centralised state access, event tracking, derived metrics)
- **MetricsTracker**: ✅ Complete (episode-level statistics: accuracy, kills, time alive)
- **RewardCalculator**: ✅ Complete (component-based reward system, 6 components implemented)
- **Score Removal**: ✅ Complete (score calculation removed from `Asteroids.py`, uses RewardCalculator)

### Planned Infrastructure

- **StateEncoder & Encoders** (plan 004): State encoding interfaces and implementations
  - VectorEncoder for GA/ES/NEAT
  - GraphEncoder refactored from env_wrapper
- **ActionInterface** (plan 004): Action validation and normalization
- **BaseAgent & EpisodeRunner** (plan 005): Agent interface and episode execution infrastructure
- **Configuration System** (plan 006): Configuration and agent save/load utilities

### Future Refactoring

- **AI Wrapper Refactoring**: Replace direct `self.game.*` access in `AsteroidsGraphEnv` with trackers and encoders (deferred until infrastructure complete)
- **Training Loop Refactoring**: Refactor `train_agent.py` to use BaseAgent and EpisodeRunner (plan 005)

