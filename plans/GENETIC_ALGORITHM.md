# Genetic Algorithm (GA) Implementation

## Scope / Purpose

The Genetic Algorithm is the currently implemented optimization method in AsteroidsAI. Its purpose is to evolve a neural network policy that can survive and score reward under the same simulation rules used by future methods, providing a concrete baseline for training infrastructure, analytics, and environment parity.

## Current Implemented System

### Policy Representation (Implemented)

- **Genome**: A flat `List[float]` parameter vector (weights + biases).
- **Policy**: `ai_agents/policies/feedforward.py:FeedforwardPolicy` (MLP).
  - **Hidden activation**: `tanh`.
  - **Output activation**: `sigmoid` clamped to avoid overflow.
  - **Unpacking**: `W1` (input×hidden), `b1` (hidden), `W2` (hidden×output), `b2` (output).
- **Agent wrapper**: `ai_agents/neuroevolution/nn_agent.py:NNAgent` implements `BaseAgent` and delegates to `FeedforwardPolicy`.
- **Parameter count**:
  - Computed via `NNAgent.get_parameter_count(...)`.
  - Formula: `input*hidden + hidden + hidden*output + output`.

### State Encoding (Implemented)

- **Encoder**: `interfaces/encoders/VectorEncoder.py:VectorEncoder`.
- **Player features (3)**:
  - Forward velocity (egocentric, normalized).
  - Lateral velocity (egocentric, normalized).
  - Shooting cooldown (normalized 0..1).
- **Asteroid features (4 per asteroid)**:
  - Distance (normalized 0..1).
  - Angle-to-target (normalized -1..1).
  - Closing speed (normalized -1..1).
  - Size/scale (normalized 0..1).
- **Cardinality**:
  - Configured by `GAConfig.NUM_NEAREST_ASTEROIDS` (currently 8).
  - State size formula: `3 + 4 * NUM_NEAREST_ASTEROIDS` (currently `3 + 4*8 = 35`).
- **Wrapping-aware geometry**:
  - Toroidal shortest-path adjustment is applied when computing relative asteroid position before distance/angle calculations.

### Action Space (Implemented)

- **Action vector shape**: 4 floats in `[0, 1]`.
- **Action meaning/order** (as consumed by the game):
  - `action[0] -> left_pressed`
  - `action[1] -> right_pressed`
  - `action[2] -> up_pressed` (thrust)
  - `action[3] -> space_pressed` (shoot)
- **Thresholding**: `ActionInterface.to_game_input(...)` uses `> 0.5` to convert to booleans.
- **Validation**: `ActionInterface.validate(...)` enforces length and rejects NaN/inf.

### GA Hyperparameters (Implemented)

From `training/config/genetic_algorithm.py:GAConfig`:

| Setting | Value | Meaning |
|---|---:|---|
| `POPULATION_SIZE` | 25 | Individuals per generation. |
| `NUM_GENERATIONS` | 500 | Total generations in a training run. |
| `SEEDS_PER_AGENT` | 20 | Rollouts per individual (fitness averaged). |
| `MAX_STEPS` | 1500 | Episode cap (step limit). |
| `HIDDEN_LAYER_SIZE` | 24 | Hidden units in the MLP. |
| `MUTATION_PROBABILITY` | 0.05 | Per-gene mutation chance. |
| `MUTATION_GAUSSIAN_SIGMA` | 0.1 | Stddev for gaussian mutation noise. |
| `CROSSOVER_PROBABILITY` | 0.7 | Probability to apply crossover on a parent pair. |
| `CROSSOVER_ALPHA` | 0.5 | BLX-alpha blend/extrapolation factor. |
| `FRAME_DELAY` | 1/60 | Fixed step used for training + playback. |

### Evolution Operators (Implemented)

- **Parent selection** (`training/methods/genetic_algorithm/selection.py`):
  - Tournament selection with `tournament_size=3`.
  - Produces a parent list the same size as the population.
- **Crossover** (`training/methods/genetic_algorithm/operators.py`):
  - BLX-alpha blend crossover implemented as `crossover_blend(...)`.
  - Produces two children by sampling from an extended per-gene interval.
- **Mutation** (`training/methods/genetic_algorithm/operators.py`):
  - Gaussian mutation implemented as `mutate_gaussian(...)` (per-gene probabilistic noise).
  - Uniform mutation implemented as `mutate_uniform(...)` (present; not used by current driver).
- **Adaptive mutation** (`training/methods/genetic_algorithm/driver.py`):
  - If stagnation exceeds 10 generations, mutation probability and sigma are boosted up to caps.
- **Elitism** (`training/methods/genetic_algorithm/driver.py`):
  - Keeps ~10% top individuals (minimum 2) each generation.
  - Preserves all-time best genome into the elite when stagnation is not too long (`< 30`).

### Evaluation Loop (Implemented)

- **Parallel evaluation** (`training/core/population_evaluator.py`):
  - Uses `ThreadPoolExecutor` to evaluate many individuals concurrently.
  - Each individual is evaluated on `SEEDS_PER_AGENT` deterministic seeds using `HeadlessAsteroidsGame(random_seed=...)`.
  - Fitness is averaged across seeds.
- **Per-agent metrics returned by the evaluator**:
  - `fitness`, `steps_survived`, `kills`, `shots_fired`, `hits`, `accuracy`, `time_alive`.
  - Action counts: `thrust_frames`, `turn_frames`, `shoot_frames`.
  - Action durations: `avg_thrust_duration`, `avg_turn_duration`, `avg_shoot_duration`.
  - Engagement: `idle_rate`, `avg_asteroid_dist`, `screen_wraps`.
  - Reward anatomy: `reward_breakdown`, `quarterly_scores`.
  - Heatmap inputs: `position_history`, `kill_data`.
- **Population-level aggregation**:
  - Averages of the above, plus “best agent” and “population sample” heatmap streams.

### Training Orchestration & Display (Implemented)

- **Entry point**: `training/scripts/train_ga.py`.
- **Phases**:
  - Evaluate population → show best agent in windowed “fresh game” → evolve population.
- **Generalization capture** (`training/core/display_manager.py`):
  - Windowed episode is stepped with fixed `GAConfig.FRAME_DELAY` even if arcade provides variable `delta_time`.
  - Fresh-game performance is recorded into analytics with ratio metrics and a letter grade.

## Implemented Outputs / Artifacts

- **`training_summary.md`**: Generated at save points via `TrainingAnalytics.generate_markdown_report(...)`.
- **`training_data.json`**: Generated at save points via `TrainingAnalytics.save_json(...)`.
- **Windowed best-agent playback**: The best genome is executed in the arcade window between generations.

## In Progress / Partially Implemented

- [ ] Alternate operators: `mutate_uniform(...)` and `crossover_arithmetic(...)` exist but are not used by the current GA driver.
- [ ] Checkpointing/resume: The run exports metrics, but does not persist the GA population/genomes for resuming training.

## Planned / Missing / To Be Changed

- [ ] Genome persistence: Save best-of-generation and all-time-best genomes to reloadable files for playback/re-evaluation.
- [ ] Novelty/diversity shaping: Add novelty tracking or other diversity-preservation mechanisms (beyond basic fitness stddev).
- [ ] Multi-episode fresh-game validation: Replace single fresh-game playback with multiple rollouts and averaged generalization stats.
- [ ] Method abstraction: If ES/NEAT are added, consider refactoring evaluator interfaces so non-GA policies can reuse rollouts cleanly.

## Notes / Design Considerations

- The action space is currently boolean-thresholded; "continuous" mode exists in `ActionInterface` but behaves identically to boolean thresholding.
- The windowed game's internal reward calculator differs from the training reward preset; training fitness should be interpreted using `training/config/rewards.py`.
- **Training data before the headless bullet-lifetime fix is invalid**: A bug caused bullets to never expire in headless mode, inflating training accuracy (70-80%) vs real gameplay (10-20%). Agents learned to exploit "zombie bullets" that wrap infinitely. Previous training runs should be discarded and rerun with the fixed headless game.

## Discarded / Obsolete / No Longer Relevant

- No GA features have been formally removed; unused-but-present components should remain listed under "In Progress / Partially Implemented" until adopted or deleted.

