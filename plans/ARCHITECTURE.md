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
│   │   ├── nn_agent_tf.py               # NNAgentTF: TensorFlow agent wrapper (present, currently unused by training scripts)
│   │   └── neat/
│   │       ├── genes.py                 # NEAT node/connection gene primitives
│   │       ├── genome.py                # NEAT genome: mutations, crossover, compatibility distance
│   │       ├── network.py               # Feedforward NEAT network compilation + forward pass
│   │       └── agent.py                 # NEATAgent wrapper for NEAT genomes
│   ├── policies/
│       ├── feedforward.py               # FeedforwardPolicy NumPy MLP unpacking + forward pass
│       ├── feedforward_tf.py            # FeedforwardPolicyTF TensorFlow Keras MLP for ES
│       └── linear.py                    # LinearPolicy (present, currently unused)
│   └── reinforcement_learning/
│       └── sac_agent.py                 # SACAgent: inference wrapper for GNN-SAC
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
│   │   ├── GraphEncoder.py              # Graph payload encoder for GNN-SAC
│   │   ├── HybridEncoder.py             # Hybrid “fovea + raycasts” fixed-size encoder (used by GA training)
│   │   ├── TemporalStackEncoder.py       # Temporal stack wrapper (N frames + deltas)
│   │   └── VectorEncoder.py             # Legacy/baseline fixed-size encoder (not used by current training script)
│   └── rewards/                         # RewardComponent implementations
│
├── training/
│   ├── scripts/
│   │   ├── train_ga.py                  # Main GA entry point: evaluate -> playback -> evolve (+ analytics)
│   │   ├── train_es.py                  # Main ES entry point: sample -> evaluate -> playback -> update (+ analytics)
│   │   ├── train_neat.py                # Main NEAT entry point: evaluate -> playback -> evolve (+ analytics)
│   │   ├── train_gnn_sac.py             # Main GNN-SAC entry point: collect -> learn -> log (+ analytics)
│   │   ├── view_gnn_sac.py              # Windowed viewer for best-so-far SAC playback
│   │   └── simulate_gnn_sac.py          # Single-process training + best-so-far playback
│   ├── config/
│   │   ├── genetic_algorithm.py         # GAConfig hyperparameters (population, seeds, mutation/crossover)
│   │   ├── evolution_strategies.py      # ESConfig hyperparameters (CMA-ES + legacy classic ES)
│   │   ├── neat.py                      # NEATConfig hyperparameters (speciation, mutation, population)
│   │   ├── sac.py                       # SACConfig hyperparameters (GNN-SAC)
│   │   ├── rewards.py                   # Training reward preset (ComposableRewardCalculator assembly)
│   │   ├── analytics.py                 # AnalyticsConfig: report section toggles + windows
│   │   ├── pareto.py                    # ParetoConfig for multi-objective ranking (shared)
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
│   │   ├── evolution_strategies/
│   │   │   ├── driver.py                # ESDriver (classic ES, present but unused by train_es.py)
│   │   │   ├── cmaes_driver.py          # CMAESDriver: diagonal CMA-ES update used by train_es.py
│   │   │   └── fitness_shaping.py       # Rank transformation + utility computation
│   │   └── neat/
│   │       ├── driver.py                # NEATDriver: speciation, crossover, mutation, population evolution
│   │       ├── innovation.py            # InnovationTracker for connection ids and split tracking
│   │       └── species.py               # Species state and stagnation tracking
│   │   ├── sac/
  - Networks: `training/methods/sac/networks.py` provides GNN backbone + actor/critics.
│   │   │   ├── replay_buffer.py        # Graph-native replay buffer
│   │   │   └── learner.py              # SAC learner/update logic
│   ├── components/
│   │   ├── novelty.py                   # Behavior vector + kNN novelty scoring
│   │   ├── diversity.py                 # Reward diversity (entropy) scoring + warnings
│   │   ├── archive.py                   # BehaviorArchive for novelty history
│   │   └── selection.py                 # Combined selection score (fitness + novelty + diversity)
│   │   ├── pareto/                      # Multi-objective ranking utilities
│   │       ├── objectives.py            # Objective extraction (kills/time_alive/accuracy)
│   │       ├── ranking.py               # Pareto fronts + crowding distance
│   │       ├── utility.py               # Ordering helper for selection/update
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
│   ├── NEAT.md
│   └── GNN_SAC.md
│
├── training_data.json                   # Generated GA training metrics export
├── training_summary.md                  # Generated GA training report
├── training_data_es.json                # Generated ES training metrics export
├── training_summary_es.md               # Generated ES training report
├── training_data_neat.json              # Generated NEAT training metrics export
└── training_summary_neat.md             # Generated NEAT training report
```

### Subsystem Responsibilities (Implemented)

| Subsystem                                      | Primary Responsibility                                                                             |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Game (Windowed)** (`Asteroids.py`, `game/`)  | Real-time simulation + rendering + debug overlays, with flags to support training playback parity. |
| **Game (Headless)** (`game/headless_game.py`)  | Fast seeded simulation for parallel rollouts without rendering.                                    |
| **Interfaces** (`interfaces/`)                 | Stable contracts around state encoding, action mapping, reward composition, and episode metrics (ActionInterface enforces mutually exclusive turning). |
| **Encoders** (`interfaces/encoders/`)          | Transform game state into fixed-size vectors or graph payloads (currently `HybridEncoder`, `TemporalStackEncoder`, `VectorEncoder`, `GraphEncoder`). |
| **Agents** (`ai_agents/`)                      | Implement the `BaseAgent` state->action contract; GA/ES use `NNAgent` (NumPy) while SAC playback uses `SACAgent`. |
| **Training Core** (`training/core/`)           | Executes evaluation/playback orchestration and wires game + interfaces + agents.                   |
| **Training Methods** (`training/methods/`)     | Algorithm-specific optimization logic; GA, ES, NEAT, and SAC are implemented.                      |
| **Shared Components** (`training/components/`) | Method-agnostic novelty/diversity scoring plus Pareto ranking utilities.                           |
| **Analytics** (`training/analytics/`)          | Records generation data, exports JSON, and generates the markdown training report.                 |

### Dependency Direction & Data Flow (Implemented)

- **Game** is the lowest layer; training/agents should not reach into entity internals except through trackers/encoders.
- **Interfaces** depend on game state to provide: state encoding inputs, action mapping, reward components, and metrics tracking.
- **Encoders** depend on `EnvironmentTracker` (and constants in `game/globals.py`) to produce model inputs.
- **Agents** depend on encoder outputs: GA/ES/NEAT output `[turn, thrust, shoot]` in `[0, 1]` (turn remapped to signed), while SAC outputs signed turn in `[-1, 1]` with thrust in `[0, 1]`.
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

  - Encoder: `TemporalStackEncoder(HybridEncoder(num_rays=16, num_fovea_asteroids=3))` when `ESConfig.USE_TEMPORAL_STACK=True` (base encoder is shared with GA).
  - Action mapping: `ActionInterface(action_space_type="boolean")` (same as GA).
  - Reward preset: `training/config/rewards.py:create_reward_calculator()` (same as GA for fair comparison).
  - Driver: `training/methods/evolution_strategies/cmaes_driver.py:CMAESDriver(...)` (diagonal CMA-ES mean/sigma/cov updates with Pareto-ranked selection).
  - Analytics: `training/analytics/analytics.py:TrainingAnalytics` (same pipeline as GA).
  - Display: `training/core/display_manager.py:DisplayManager` (same playback infrastructure).

- **Sampling phase**

  - `CMAESDriver.sample_population()` samples candidates from a diagonal Gaussian around the mean.
  - If `USE_ANTITHETIC=True`, generates paired `+epsilon`/`-epsilon` samples for variance reduction.
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
  - `CMAESDriver.update(...)` performs:
    - Pareto ranking over (`kills`, `time_alive`, `accuracy`) to select top-mu parents.
    - Mean update using weighted recombination of selected steps.
    - Step-size and diagonal covariance updates via CMA-ES evolution paths.

### Core Execution Flow (Implemented: NEAT)

`training/scripts/train_neat.py` orchestrates NEAT training inside the arcade window:

- **Infrastructure setup**

  - Encoder: `HybridEncoder(num_rays=16, num_fovea_asteroids=3)` (same baseline as GA).
  - Action mapping: `ActionInterface(action_space_type="boolean")` (same as GA/ES).
  - Reward preset: `training/config/rewards.py:create_reward_calculator()` (same for comparability).
  - Driver: `training/methods/neat/driver.py:NEATDriver(...)` (speciation + topology growth).
  - Analytics: `training/analytics/analytics.py:TrainingAnalytics` (shared pipeline).
  - Display: `training/core/display_manager.py:DisplayManager` (best-genome playback).

- **Evaluation phase**

  - `training/core/population_evaluator.py:evaluate_population_parallel(...)` evaluates genomes using an `agent_factory` hook that builds `NEATAgent` instances.
  - Multi-seed averaging uses `NEATConfig.SEEDS_PER_AGENT` and optional CRN via `NEATConfig.USE_COMMON_SEEDS`.
  - Returns fitnesses and behavior metrics for analytics and selection shaping.

- **Playback (fresh game) phase**

  - Best genome (Pareto-ranked for display) is played in the windowed game.
  - Fresh-game metrics and generalization ratios are recorded via `TrainingAnalytics.record_fresh_game(...)`.

- **Evolution phase**
  - `NEATDriver.evolve(...)` performs:
    - Compatibility-distance speciation with fitness sharing.
    - Species stagnation tracking and pruning.
    - Crossover alignment by innovation id.
    - Structural mutations (add-node, add-connection) and weight perturbation.

### Core Execution Flow (Implemented: GNN-SAC)

`training/scripts/train_gnn_sac.py` orchestrates GNN-SAC training in a headless loop:

- **Infrastructure setup**

  - Encoder: `interfaces/encoders/GraphEncoder.py:GraphEncoder(...)` (graph payload).
  - Reward preset: `training/config/rewards.py:create_reward_calculator()` (shared preset).
  - Networks: `training/methods/sac/networks.py` provides GNN backbone + actor/critics.
  - Replay: `training/methods/sac/replay_buffer.py:ReplayBuffer(...)`.
  - Analytics: `training/analytics/analytics.py:TrainingAnalytics`.

- **Collection phase**

  - `HeadlessAsteroidsGame` runs step-based rollouts with `continuous_control_mode=True`.
  - Transitions are stored as graph payloads with actions `[turn, thrust, shoot]`.

- **Update phase**

  - `SACLearner.update(...)` runs critic, actor, and entropy-temperature updates.
  - Target critics are updated via Polyak averaging (`SACConfig.TAU`).

- **Logging phase**

  - `TrainingAnalytics.record_generation(...)` logs interval snapshots using episode-return windows.

### Core Execution Flow (Implemented: GNN-SAC Simulated)

`training/scripts/simulate_gnn_sac.py` runs headless training and windowed playback in one process:

- **Training loop**

  - Headless training steps run in the background using `SACConfig.TRAIN_STEPS_PER_FRAME` per render frame.
  - Fixed-seed evaluation runs every `SACConfig.EVAL_EVERY_EPISODES` to update the best snapshot.

- **Playback loop**

  - Windowed `AsteroidsGame` playback uses `DisplayManager` + `SACAgent` with the best snapshot.
  - Viewer seeds rotate per episode using `SACConfig.VIEWER_SEED_MODE`.

## Implemented Outputs / Artifacts (if applicable)

- `training_summary.md`: Markdown report generated by `TrainingAnalytics.generate_markdown_report(...)`.
- `training_data.json`: JSON export generated by `TrainingAnalytics.save_json(...)` (schema + config + per-generation data + fresh-game data).
- `training_summary_es.md`: Markdown report generated by ES training via `TrainingAnalytics.generate_markdown_report(...)`.
- `training_data_es.json`: JSON export generated by ES training via `TrainingAnalytics.save_json(...)`.
- `training_summary_neat.md`: Markdown report generated by NEAT training via `TrainingAnalytics.generate_markdown_report(...)`.
- `training_data_neat.json`: JSON export generated by NEAT training via `TrainingAnalytics.save_json(...)`.
- `training_summary_sac.md`: Markdown report generated by GNN-SAC training via `TrainingAnalytics.generate_markdown_report(...)`.
- `training_data_sac.json`: JSON export generated by GNN-SAC training via `TrainingAnalytics.save_json(...)`.
- `training/sac_checkpoints/best_sac.pt`: Best-so-far GNN-SAC checkpoint (GNN + actor weights + eval metadata).
- `training/neat_artifacts/*`: Best-genome JSON and DOT exports produced by NEAT training.

## In Progress / Partially Implemented

- [ ] `interfaces/EnvironmentTracker.get_tick()`: References `game.time`, but the game objects do not define `time`; this method is unused/broken.
- [ ] `interfaces/encoders/VectorEncoder.py`: Provides `encode/get_state_size/reset/clone` but does not inherit `StateEncoder` (duck-typed compatibility only).
- [ ] `training/core/population_evaluator.py`: Type hints `VectorEncoder` for `state_encoder`, but evaluation works with any encoder that supports `clone/reset/encode`.
- [ ] Novelty/diversity analytics visibility: GA computes novelty/diversity for selection, but the markdown report does not yet visualize these signals.
- [ ] `tests/test_ga_dimensions.py`: References removed legacy modules under `ai_agents/neuroevolution/genetic_algorithm/*` and does not reflect the current training stack.

## Planned / Missing / To Be Changed

- [ ] Multi-method training dashboard: Parallel training/display infrastructure consistent with `README.md` ("single environment, multiple minds").
- [ ] Checkpointing/resume: Persist method state (e.g., GA population + ES mean + best genome) so long runs can resume and be replayed.
- [ ] Unified evaluator interface: Consider consolidating `population_evaluator.py` and `population_evaluator_tf.py` with a policy factory pattern.
- [ ] Curriculum hooks (future): Add environment-level difficulty knobs and training hooks for progressive difficulty, while keeping the progression metric as an open design decision.

## Notes / Design Considerations (optional)

- Windowed gameplay uses per-instance RNG (`AsteroidsGame.rng`) so playback can be seeded; headless rollouts use an isolated `random.Random(seed)` per rollout for reproducibility.
- Windowed playback uses `manual_spawning` + fixed stepping to reduce drift between headless training and fresh-game evaluation.

## Discarded / Obsolete / No Longer Relevant

- No architecture-level subsystems have been formally removed; legacy/unreferenced code paths should be tracked under “In Progress / Partially Implemented” until adopted or explicitly deleted.
