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
├── ai/
│   ├── env_wrapper.py        # Graph-based RL wrapper (AsteroidsGraphEnv)
│   ├── gnn.py                # Graph neural network models
│   ├── policies.py           # Policy implementations
│   └── sac.py                # Soft Actor-Critic RL algorithm
├── interfaces/
│   └── Environment.py        # EnvironmentTracker (incomplete stub)
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
- **Current**: Stub `EnvironmentTracker` (incomplete)
- **Planned**: `EnvironmentTracker` (current state snapshot) + `MetricsTracker` (aggregated stats)
- **Purpose**: Stable API for all AI methods to access game state and metrics

### AI Wrappers (`ai/`)
- **AsteroidsGraphEnv**: Converts game state to PyTorch Geometric graph format
- **Direct Access**: Currently accesses `self.game.*` directly (61 references)
- **Future**: Will use `EnvironmentTracker`/`MetricsTracker` interface

### Training (`train_agent.py`)
- **AIDriver**: Orchestrates training loop, episode management
- **Integration**: Creates game instance, wraps with `AsteroidsGraphEnv`

## Data Flow

1. **Game Update**: `AsteroidsGame.on_update()` → updates sprites, collisions, score
2. **AI Observation**: `AsteroidsGraphEnv._get_graph_state()` → reads `self.game.*` directly
3. **AI Action**: `AsteroidsGraphEnv.step()` → sets `self.game.left_pressed`, etc.
4. **Training Loop**: `AIDriver.update()` → calls `env.step()`, collects rewards

## Planned Changes

- **EnvironmentTracker**: Centralised state access, event tracking, derived metrics
- **MetricsTracker**: Episode-level statistics (accuracy, kills, time alive)
- **Refactor**: Replace direct `self.game.*` access in `AsteroidsGraphEnv` with tracker calls

