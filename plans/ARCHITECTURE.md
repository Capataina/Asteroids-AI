# System Architecture

## Scope / Purpose

This document is the top-down structural truth for AsteroidsAI. It describes what is currently in the repository, how subsystems depend on each other, and the execution/data-flow of the implemented training loop so new AI methods can be added without breaking separation of concerns.

## Current Implemented System

### Repository Structure (Implemented)

```text
Asteroids AI\
├─ Asteroids.py                          # Windowed arcade game (visual playback + manual play)
├─ README.md                             # Project mission/direction (immutable)
├─ AGENTS.md                             # Repo workflow rules
├─ ai_agents\
│  ├─ base_agent.py                      # BaseAgent interface (state -> action)
│  ├─ neuroevolution\
│  │  └─ nn_agent.py                     # NNAgent wrapper used by GA (FeedforwardPolicy)
│  └─ policies\
│     ├─ feedforward.py                  # MLP (tanh hidden, sigmoid output) parameter unpacking
│     └─ linear.py                       # LinearPolicy (present, currently unused)
├─ game\
│  ├─ globals.py                         # Physics/constants shared by windowed + headless
│  ├─ headless_game.py                   # HeadlessAsteroidsGame used for parallel rollouts
│  ├─ classes\
│  │  ├─ player.py                       # Player physics + shooting cooldown
│  │  ├─ bullet.py                       # Bullet kinematics + lifetime
│  │  └─ asteroid.py                     # Asteroid spawn/randomization + fragmentation + HP
│  ├─ debug\
│  │  └─ visuals.py                      # Collision/velocity/facing overlays (windowed)
│  └─ sprites\                           # PNG assets
├─ interfaces\
│  ├─ ActionInterface.py                 # Action validation/normalization + to_game_input mapping
│  ├─ EnvironmentTracker.py              # Spatial queries + wrapped distance utilities
│  ├─ MetricsTracker.py                  # Episode counters (shots, hits, kills, time_alive)
│  ├─ RewardCalculator.py                # ComposableRewardCalculator + per-component tracking
│  ├─ StateEncoder.py                    # StateEncoder abstract base
│  ├─ encoders\
│  │  └─ VectorEncoder.py                # Fixed-size egocentric state encoding (player + asteroids)
│  └─ rewards\                           # RewardComponent implementations (preset selects subset)
├─ training\
│  ├─ analytics\                         # TrainingAnalytics facade + collection/analysis/reporting
│  ├─ config\
│  │  ├─ genetic_algorithm.py            # GAConfig hyperparameters
│  │  └─ rewards.py                      # Reward preset selection for training rollouts
│  ├─ core\
│  │  ├─ population_evaluator.py         # Parallel evaluation (ThreadPoolExecutor) + aggregation
│  │  ├─ episode_runner.py               # Single-episode runner (used for windowed stepping)
│  │  ├─ episode_result.py               # EpisodeResult container
│  │  └─ display_manager.py              # Fresh-game playback + generalization capture
│  ├─ methods\
│  │  └─ genetic_algorithm\
│  │     ├─ driver.py                    # GADriver (evolve population + adaptive mutation)
│  │     ├─ selection.py                 # Tournament selection
│  │     └─ operators.py                 # BLX-alpha crossover + gaussian/uniform mutation
│  └─ scripts\
│     └─ train_ga.py                     # Main entry point: run GA training in arcade window
├─ tests\
│  ├─ test_ga_dimensions.py              # Encoder/action sizes + NN parameter count checks
│  └─ test_kill_asteroid_reward.py       # Reward component behavior/unit tests
├─ plans\                                # Living docs (this folder)
│  ├─ ARCHITECTURE.md
│  ├─ GAME_ENGINE.md
│  ├─ GENETIC_ALGORITHM.md
│  ├─ ANALYTICS.md
│  ├─ EVOLUTION_STRATEGIES.md
│  └─ NEAT.md
├─ training_data.json                    # Training metrics export (generated)
└─ training_summary.md                   # Training report (generated)
```

### Subsystem Responsibilities (Implemented)

| Subsystem                             | Responsibility                                                                                                              |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Game** (`game/`, `Asteroids.py`)    | Simulates entities, collisions, spawning, wrapping, and episode termination (player removed on collision in training mode). |
| **Interfaces** (`interfaces/`)        | Provides state encoding, action translation, metric tracking, and composable reward calculation.                            |
| **Agents** (`ai_agents/`)             | Defines the `BaseAgent` contract and provides a GA-used neural policy wrapper (`NNAgent`).                                  |
| **Training** (`training/`)            | Orchestrates GA evolution, parallel rollouts, best-agent playback, and analytics recording.                                 |
| **Analytics** (`training/analytics/`) | Stores metrics, computes summaries, and outputs reports/exports.                                                            |

### Dependency Direction & Data Flow (Implemented)

- **Game** is the lowest layer; training/agents should not be required to import game internals beyond public state.
- **Interfaces** depend on game state to produce: encoded state vectors, reward, metrics, and wrapped distance queries.
- **Agents** depend on interface contracts: take encoded state and output an action vector `[left, right, thrust, shoot]` in `[0, 1]`.
- **Training** wires game + interfaces + agents and executes evaluation/evolution loops.
- **Analytics** consumes aggregated metrics produced by the training loop.

Per-step control/data loop: `Game state -> VectorEncoder.encode(...) -> Agent.get_action(...) -> ActionInterface.to_game_input(...) -> Game.on_update(...)`.

### Core Execution Flow (Implemented GA)

- `training/scripts/train_ga.py` builds the GA training stack:
  - State: `VectorEncoder(...)` (player + nearest asteroids).
  - Action: `ActionInterface(action_space_type="boolean")` (threshold at `0.5`).
  - Reward: preset from `training/config/rewards.py`.
  - Method: `GADriver(param_size=...)`.
  - Analytics: `TrainingAnalytics()` configured with run metadata.
  - Display: `DisplayManager(...)` for best-agent playback and generalization capture.
- Evaluation phase:
  - `evaluate_population_parallel(...)` evaluates each genome on `GAConfig.SEEDS_PER_AGENT` seeds using `HeadlessAsteroidsGame(random_seed=...)`.
  - Fitness is averaged across seeds; per-agent metrics are returned for distributions.
  - Aggregated metrics include action counts, durations, wrapped-distance engagement, reward breakdowns, and heatmap inputs.
- Evolution phase:
  - `GADriver.evolve(...)` performs tournament selection, BLX-alpha crossover, gaussian mutation, elitism, and adaptive mutation under stagnation.
- Fresh-game (generalization) phase:
  - `DisplayManager.start_display(...)` runs a windowed episode with fixed `GAConfig.FRAME_DELAY` stepping.
  - Fresh-game results and generalization ratios are recorded via `TrainingAnalytics.record_fresh_game(...)`.

## Implemented Outputs / Artifacts

- `training_summary.md`: Markdown report produced by `TrainingAnalytics.generate_markdown_report(...)`.
- `training_data.json`: JSON export produced by `TrainingAnalytics.save_json(...)` (schema version, config, generations, distributions, fresh-game data).

## In Progress / Partially Implemented

- [ ] `interfaces/EnvironmentTracker.get_tick()`: References `game.time`, but the game objects do not define `time`; this method is unused/broken.
- [ ] `interfaces/ActionInterface(action_space_type="continuous")`: Exists, but currently thresholds exactly like `"boolean"` (no true continuous controls yet).
- [ ] `interfaces/encoders/VectorEncoder(include_bullets/include_global)`: Constructor supports these flags, but `encode(...)` currently emits only player + nearest asteroids.
- [ ] `ai_agents/policies/linear.py`: Present but unused by current training scripts/agents.

## Planned / Missing / To Be Changed

- [ ] Evolution Strategies method: Implement ES under `training/methods/` consistent with root `README.md`.
- [ ] NEAT method: Implement variable-topology genomes/speciation/innovation tracking consistent with root `README.md`.
- [ ] Additional state encoders: Add alternative encoders (e.g., sensor/noise, variable-cardinality, graph) without coupling to a specific method.
- [ ] Training dashboard: Add multi-method parallel training/display consistent with root `README.md`.
- [ ] Checkpointing/resume: Persist method state (e.g., GA population + best genome) so long runs can resume.

## Notes / Design Considerations

- Windowed gameplay uses `AsteroidsGame` (arcade), while training rollouts use `HeadlessAsteroidsGame`; parity is maintained by sharing constants (`game/globals.py`) and explicit collision radii.
- Analytics report sparklines use extended glyphs; on some terminals this can render as mojibake depending on encoding/font.

## Discarded / Obsolete / No Longer Relevant

- No architecture-level subsystems have been formally removed; items that exist-but-unused are tracked under "In Progress / Partially Implemented" until adopted or explicitly deleted.
