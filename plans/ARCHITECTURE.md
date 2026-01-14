# System Architecture

## Scope / Purpose

This document is the top-down structural truth for AsteroidsAI. It describes the implemented repository structure, subsystem responsibilities, and the execution/data-flow of the current GA training loop so new AI methods can be added without breaking separation of concerns or cross-method comparability.

## Current Implemented System

### Repository Structure (Implemented)

```text
Asteroids AI/
├── Asteroids.py                         # Windowed arcade game (rendering + manual play + training playback hooks)
├── README.md                            # Project mission/direction (immutable)
├── AGENTS.md                            # Repo workflow rules (docs/code alignment)
│
├── ai_agents/
│   ├── base_agent.py                    # BaseAgent contract: encoded_state -> action_vector
│   ├── neuroevolution/
│   │   ├── nn_agent.py                  # NNAgent: wraps FeedforwardPolicy for GA (NumPy, fixed-topology MLP)
│   │   └── nn_agent_tf.py               # NNAgentTF: TensorFlow agent wrapper (present, currently unused by training scripts)
│   └── policies/
│       ├── feedforward.py               # FeedforwardPolicy NumPy MLP unpacking + forward pass
│       ├── feedforward_tf.py            # FeedforwardPolicyTF TensorFlow Keras MLP for ES
│       └── linear.py                    # LinearPolicy (present, currently unused)
│
├── game/
│   ├── globals.py                       # Physics/constants shared by windowed + headless
│   ├── headless_game.py                 # HeadlessAsteroidsGame for seeded parallel rollouts
│   ├── classes/
│   │   ├── player.py                    # Player physics + shooting cooldown
│   │   ├── bullet.py                    # Bullet kinematics + lifetime
│   │   └── asteroid.py                  # Asteroid spawn/randomization + fragmentation + HP
│   ├── debug/
│   │   └── visuals.py                   # Collision/velocity overlays + HybridEncoder ray visualization
│   └── sprites/                         # PNG assets
│
├── interfaces/
│   ├── ActionInterface.py               # Action validation/normalization + to_game_input mapping
│   ├── EnvironmentTracker.py            # Spatial queries + wrapped distance utilities
│   ├── MetricsTracker.py                # Episode counters (shots, hits, kills, time_alive)
│   ├── RewardCalculator.py              # ComposableRewardCalculator + per-component tracking
│   ├── StateEncoder.py                  # Abstract encoder contract (encode/get_state_size/reset/clone)
│   ├── encoders/
│   │   ├── HybridEncoder.py             # Hybrid “fovea + raycasts” fixed-size encoder (used by GA training)
│   │   └── VectorEncoder.py             # Legacy/baseline fixed-size encoder (not used by current training script)
│   └── rewards/                         # RewardComponent implementations
│
├── training/
│   ├── scripts/
│   │   ├── train_ga.py                  # Main GA entry point: evaluate -> playback -> evolve (+ analytics)
│   │   └── train_es.py                  # Main ES entry point: sample -> evaluate -> playback -> update (+ analytics)
│   ├── config/
│   │   ├── genetic_algorithm.py         # GAConfig hyperparameters (population, seeds, mutation/crossover)
│   │   ├── evolution_strategies.py      # ESConfig hyperparameters (sigma schedule, CRN, antithetic sampling, AdamW, elitism)
│   │   ├── rewards.py                   # Training reward preset (ComposableRewardCalculator assembly)
│   │   ├── analytics.py                 # AnalyticsConfig: report section toggles + windows
│   │   └── novelty.py                   # NoveltyConfig: novelty/diversity selection weighting + archive params
│   ├── core/
│   │   ├── population_evaluator.py      # Parallel evaluation for GA (ThreadPoolExecutor + NNAgent)
│   │   ├── population_evaluator_tf.py   # TensorFlow parallel evaluator (present, currently unused by training scripts)
│   │   ├── episode_runner.py            # Windowed stepping helper for playback (EpisodeRunner)
│   │   ├── episode_result.py            # EpisodeResult container
│   │   └── display_manager.py           # Best-agent playback + fresh-game generalization capture
│   ├── methods/
│   │   ├── genetic_algorithm/
│   │   │   ├── driver.py                # GADriver: evolve population + adaptive mutation + novelty selection
│   │   │   ├── selection.py             # Tournament selection
│   │   │   └── operators.py             # BLX-alpha crossover + gaussian/uniform mutation
│   │   └── evolution_strategies/
│   │       ├── driver.py                # ESDriver: sample perturbations + gradient update (AdamW) + elitism + adaptive sigma
│   │       └── fitness_shaping.py       # Rank transformation + utility computation
│   ├── components/
│   │   ├── novelty.py                   # Behavior vector + kNN novelty scoring
│   │   ├── diversity.py                 # Reward diversity (entropy) scoring + warnings
│   │   ├── archive.py                   # BehaviorArchive for novelty history
│   │   └── selection.py                 # Combined selection score (fitness + novelty + diversity)
│   └── analytics/
│       ├── analytics.py                 # TrainingAnalytics facade
│       ├── collection/                  # Data collection + schema model
│       ├── analysis/                    # Statistics/correlation/convergence utilities
│       └── reporting/                   # Markdown + JSON exporters + report sections
│
├── tests/
│   ├── test_kill_asteroid_reward.py     # Reward component unit tests
│   └── test_ga_dimensions.py            # Legacy GA dimension script (currently out of date / broken)
│
├── plans/                               # Living docs (this folder)
│   ├── ARCHITECTURE.md
│   ├── GAME_ENGINE.md
│   ├── STATE_REPRESENTATION.md
│   ├── GENETIC_ALGORITHM.md
│   ├── SHARED_COMPONENTS.md
│   ├── ANALYTICS.md
│   ├── EVOLUTION_STRATEGIES.md
│   └── NEAT.md
│
├── training_data.json                   # Generated GA training metrics export
├── training_summary.md                  # Generated GA training report
├── training_data_es.json                # Generated ES training metrics export
└── training_summary_es.md               # Generated ES training report
```

### Subsystem Responsibilities (Implemented)

| Subsystem                                      | Primary Responsibility                                                                             |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Game (Windowed)** (`Asteroids.py`, `game/`)  | Real-time simulation + rendering + debug overlays, with flags to support training playback parity. |
| **Game (Headless)** (`game/headless_game.py`)  | Fast seeded simulation for parallel rollouts without rendering.                                    |
| **Interfaces** (`interfaces/`)                 | Stable contracts around state encoding, action mapping, reward composition, and episode metrics.   |
| **Encoders** (`interfaces/encoders/`)          | Transform game state into fixed-size vectors (currently `HybridEncoder`, `VectorEncoder`).         |
| **Agents** (`ai_agents/`)                      | Implement the `BaseAgent` state->action contract; GA and ES training scripts currently use `NNAgent` (NumPy). |
| **Training Core** (`training/core/`)           | Executes evaluation/playback orchestration and wires game + interfaces + agents.                   |
| **Training Methods** (`training/methods/`)     | Algorithm-specific optimization logic; GA and ES are implemented.                                  |
| **Shared Components** (`training/components/`) | Method-agnostic novelty/diversity scoring utilities used during selection.                         |
| **Analytics** (`training/analytics/`)          | Records generation data, exports JSON, and generates the markdown training report.                 |

### Dependency Direction & Data Flow (Implemented)

- **Game** is the lowest layer; training/agents should not reach into entity internals except through trackers/encoders.
- **Interfaces** depend on game state to provide: state encoding inputs, action mapping, reward components, and metrics tracking.
- **Encoders** depend on `EnvironmentTracker` (and constants in `game/globals.py`) to produce model inputs.
- **Agents** depend on encoder outputs: GA agents output an action vector `[left, right, thrust, shoot]` in `[0, 1]`.
- **Training** wires game + interfaces + agents + method logic and runs evaluation/evolution loops.
- **Analytics** consumes aggregated metrics produced by the training loop and emits human/machine-readable reports.

Per-step control/data loop:

```text
Game state
  -> EnvironmentTracker
    -> StateEncoder.encode(...)
      -> BaseAgent.get_action(...)
        -> ActionInterface.to_game_input(...)
          -> Game.on_update(...)
            -> MetricsTracker / RewardCalculator updates
```

### Core Execution Flow (Implemented: GA)

`training/scripts/train_ga.py` orchestrates GA training inside the arcade window:

- **Infrastructure setup**

  - Encoder: `HybridEncoder(num_rays=16, num_fovea_asteroids=3)` (see `plans/STATE_REPRESENTATION.md`).
  - Action mapping: `ActionInterface(action_space_type="boolean")` (threshold at `0.5`).
  - Reward preset: `training/config/rewards.py:create_reward_calculator()` (external to the game’s internal rewards).
  - Driver: `training/methods/genetic_algorithm/driver.py:GADriver(...)` (includes novelty/diversity selection).
  - Analytics: `training/analytics/analytics.py:TrainingAnalytics`.
  - Display: `training/core/display_manager.py:DisplayManager` (fresh-game playback + generalization capture).

- **Evaluation phase**

  - `training/core/population_evaluator.py:evaluate_population_parallel(...)` evaluates each genome on `GAConfig.SEEDS_PER_AGENT` seeded rollouts using `HeadlessAsteroidsGame(random_seed=...)`.
  - Seed assignment mode is controlled by `GAConfig.USE_COMMON_SEEDS` (default `False`): unique seeds per genome vs CRN (shared seed set across the population).
  - Fitness is averaged across seeds; aggregated generation metrics and per-agent averaged metrics are returned.

- **Playback (fresh game) phase**

  - `DisplayManager.start_display(...)` runs the best-of-generation genome in the windowed game.
  - Windowed playback enables `manual_spawning=True` and uses a forced fixed step (`GAConfig.FRAME_DELAY`) to match headless timing.
  - Fresh-game results + generalization ratios/grade are recorded via `TrainingAnalytics.record_fresh_game(...)`.

- **Evolution phase**
  - `GADriver.evolve(...)` performs:
    - Tournament selection over a combined score (fitness + novelty + reward diversity).
    - BLX-alpha crossover and gaussian mutation.
    - Elitism and adaptive mutation under stagnation.

### Core Execution Flow (Implemented: ES)

`training/scripts/train_es.py` orchestrates ES training inside the arcade window:

- **Infrastructure setup**

  - Encoder: `HybridEncoder(num_rays=16, num_fovea_asteroids=3)` (same as GA).
  - Action mapping: `ActionInterface(action_space_type="boolean")` (same as GA).
  - Reward preset: `training/config/rewards.py:create_reward_calculator()` (same as GA for fair comparison).
  - Driver: `training/methods/evolution_strategies/driver.py:ESDriver(...)` (manages mean + sigma + gradient updates).
  - Analytics: `training/analytics/analytics.py:TrainingAnalytics` (same pipeline as GA).
  - Display: `training/core/display_manager.py:DisplayManager` (same playback infrastructure).

- **Sampling phase**

  - `ESDriver.sample_population()` generates Gaussian perturbations around the mean.
  - If `USE_ANTITHETIC=True`, generates paired `+epsilon` and `-epsilon` perturbations for variance reduction.
  - Returns candidate parameter vectors for evaluation.

- **Evaluation phase**

  - `training/core/population_evaluator.py:evaluate_population_parallel(...)` evaluates candidates using `NNAgent` (NumPy).
  - Same multi-seed averaging as GA (`ESConfig.SEEDS_PER_AGENT` rollouts per candidate).
  - Seed assignment mode is controlled by `ESConfig.USE_COMMON_SEEDS` (default `True`) to enable CRN + antithetic variance reduction.
  - Returns fitnesses and behavioral metrics.

- **Playback (fresh game) phase**

  - `DisplayManager.start_display(...)` runs the best candidate in the windowed game.
  - Same infrastructure as GA for generalization capture.

- **Update phase**
  - `ESDriver.update(...)` performs:
    - Rank-based fitness transformation (if `USE_RANK_TRANSFORMATION=True`).
    - Gradient estimation: `grad = (1/(N*sigma)) * Σ (utility_i * epsilon_i)`.
    - Mean update: AdamW (when `USE_ADAMW=True`) or SGD (when `USE_ADAMW=False`) is applied to update `theta`.
    - Weight decay, adaptive sigma decay, and optional elite pull/injection are applied based on `ESConfig`.

## Implemented Outputs / Artifacts (if applicable)

- `training_summary.md`: Markdown report generated by `TrainingAnalytics.generate_markdown_report(...)`.
- `training_data.json`: JSON export generated by `TrainingAnalytics.save_json(...)` (schema + config + per-generation data + fresh-game data).
- `training_summary_es.md`: Markdown report generated by ES training via `TrainingAnalytics.generate_markdown_report(...)`.
- `training_data_es.json`: JSON export generated by ES training via `TrainingAnalytics.save_json(...)`.

## In Progress / Partially Implemented

- [ ] `interfaces/EnvironmentTracker.get_tick()`: References `game.time`, but the game objects do not define `time`; this method is unused/broken.
- [ ] `interfaces/ActionInterface(action_space_type="continuous")`: Exists, but currently thresholds exactly like `"boolean"` (no true continuous controls yet).
- [ ] `interfaces/encoders/VectorEncoder.py`: Provides `encode/get_state_size/reset/clone` but does not inherit `StateEncoder` (duck-typed compatibility only).
- [ ] `training/core/population_evaluator.py`: Type hints `VectorEncoder` for `state_encoder`, but evaluation works with any encoder that supports `clone/reset/encode`.
- [ ] Novelty/diversity analytics visibility: GA computes novelty/diversity for selection, but the markdown report does not yet visualize these signals.
- [ ] `tests/test_ga_dimensions.py`: References removed legacy modules under `ai_agents/neuroevolution/genetic_algorithm/*` and does not reflect the current training stack.

## Planned / Missing / To Be Changed

- [x] Evolution Strategies method: ES implemented under `training/methods/evolution_strategies/`; training script currently uses shared NumPy policy/evaluator (TF components are present but unused).
- [ ] NEAT method: Implement variable-topology genomes/speciation/innovation tracking consistent with `README.md` direction.
- [ ] Multi-method training dashboard: Parallel training/display infrastructure consistent with `README.md` ("single environment, multiple minds").
- [ ] Checkpointing/resume: Persist method state (e.g., GA population + ES mean + best genome) so long runs can resume and be replayed.
- [ ] Unified evaluator interface: Consider consolidating `population_evaluator.py` and `population_evaluator_tf.py` with a policy factory pattern.

## Notes / Design Considerations (optional)

- Windowed gameplay uses global `random` for spawns; headless rollouts use an isolated `random.Random(seed)` per rollout for reproducibility.
- Windowed playback uses `manual_spawning` + fixed stepping to reduce drift between headless training and fresh-game evaluation.

## Discarded / Obsolete / No Longer Relevant

- No architecture-level subsystems have been formally removed; legacy/unreferenced code paths should be tracked under “In Progress / Partially Implemented” until adopted or explicitly deleted.
