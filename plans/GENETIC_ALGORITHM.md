# Genetic Algorithm (GA) Implementation

## Scope / Purpose

The Genetic Algorithm is the currently implemented optimization method in AsteroidsAI. Its purpose is to evolve a fixed-topology neural network policy under the shared simulation + reward interfaces, providing a concrete baseline for training infrastructure, analytics, and future method comparisons (ES/NEAT/RL).

## Current Implemented System

### Entry Point & Orchestration (Implemented)

| Component                 | File                                           | Granular Responsibility                                                                                     |
| ------------------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Training script           | `training/scripts/train_ga.py`                 | Creates encoder/action/reward/driver/analytics/display stack and runs the evaluate → display → evolve loop. |
| Population evaluator      | `training/core/population_evaluator.py`        | Runs seeded headless rollouts in parallel and aggregates per-agent + per-generation metrics.                |
| Driver (GA logic)         | `training/methods/genetic_algorithm/driver.py` | Maintains population and applies selection/crossover/mutation/elitism (+ novelty/diversity selection).      |
| Playback + generalization | `training/core/display_manager.py`             | Runs best agent in windowed “fresh game” and records generalization metrics into analytics.                 |

### Policy Representation (Implemented)

| Concept       | Implementation                                        | Details                                                                                                  |
| ------------- | ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Genome        | `List[float]`                                         | Flat parameter vector representing all weights and biases.                                               |
| Policy        | `ai_agents/policies/feedforward.py:FeedforwardPolicy` | MLP with `tanh` hidden activation and `sigmoid` outputs (clamped for numerical stability).               |
| Agent wrapper | `ai_agents/neuroevolution/nn_agent.py:NNAgent`        | Implements `BaseAgent`, builds `FeedforwardPolicy` using `state_encoder.get_state_size()` as input size. |

**Parameter count (fixed topology)**

- Formula (as implemented): `input*hidden + hidden + hidden*output + output`.
- Current default sizes:
  - Input: `HybridEncoder.get_state_size() = 31` (see `plans/STATE_REPRESENTATION.md`)
  - Hidden: `GAConfig.HIDDEN_LAYER_SIZE = 24`
  - Output: `4`
  - Parameter count: `31*24 + 24 + 24*4 + 4 = 868`

### State Encoding (Implemented)

The current GA training script uses `interfaces/encoders/HybridEncoder.py` (not `VectorEncoder`).

| Encoder         | File                                   | Default Size | Used In                        |
| --------------- | -------------------------------------- | -----------: | ------------------------------ |
| `HybridEncoder` | `interfaces/encoders/HybridEncoder.py` |         `31` | `training/scripts/train_ga.py` |

**HybridEncoder feature layout (granular)**

- Proprioception (3):
  - Forward velocity (egocentric, normalized).
  - Lateral velocity (egocentric, normalized).
  - Shoot cooldown fraction (normalized).
- Fovea list (3 asteroids × 4):
  - Wrapped distance to asteroid (normalized).
  - Signed angle-to-target relative to ship heading (normalized).
  - Closing speed (normalized/clamped).
  - Asteroid size/scale (normalized).
- Peripheral rays (16):
  - Normalized ray hit distances (`1.0` indicates max range/no hit).

### Action Space (Implemented)

| Output Index | Meaning    | Mapping         |
| -----------: | ---------- | --------------- |
|          `0` | Turn left  | `left_pressed`  |
|          `1` | Turn right | `right_pressed` |
|          `2` | Thrust     | `up_pressed`    |
|          `3` | Shoot      | `space_pressed` |

- Output range: 4 floats in `[0, 1]`.
- Discretization: `ActionInterface.to_game_input(...)` thresholds `> 0.5` (even when `action_space_type="continuous"`).

### GA Hyperparameters (Implemented)

From `training/config/genetic_algorithm.py:GAConfig`:

| Setting                     |        Value | Meaning                                                    |
| --------------------------- | -----------: | ---------------------------------------------------------- |
| `POPULATION_SIZE`           |         `10` | Individuals per generation.                                |
| `NUM_GENERATIONS`           |        `500` | Total generations in a run.                                |
| `SEEDS_PER_AGENT`           |          `5` | Headless rollouts per individual (fitness averaged).       |
| `MAX_STEPS`                 |       `1500` | Step limit per rollout/playback.                           |
| `FRAME_DELAY`               |       `1/60` | Fixed time step used for training evaluation and playback. |
| `USE_COMMON_SEEDS`          |      `False` | If `True`, all individuals share the same seed set per generation (CRN mode); if `False`, each individual uses unique seeds. |
| `HIDDEN_LAYER_SIZE`         |         `24` | Hidden units in the MLP.                                   |
| `MUTATION_PROBABILITY`      |       `0.05` | Per-gene mutation chance.                                  |
| `MUTATION_GAUSSIAN_SIGMA`   |        `0.1` | Stddev for gaussian noise.                                 |
| `MUTATION_UNIFORM_LOW/HIGH` | `-1.0 / 1.0` | Bounds for uniform mutation / initialization.              |
| `CROSSOVER_PROBABILITY`     |        `0.7` | Probability to apply crossover to a parent pair.           |
| `CROSSOVER_ALPHA`           |        `0.5` | BLX-alpha expansion factor.                                |

### Evolution Operators (Implemented)

| Operator             | File                                                              | Granular Behavior                                                                      |
| -------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Tournament selection | `training/methods/genetic_algorithm/selection.py`                 | Picks `tournament_size=3` competitors and selects the best by selection score.         |
| Crossover            | `training/methods/genetic_algorithm/operators.py:crossover_blend` | BLX-alpha blend crossover producing two children sampled from expanded gene intervals. |
| Mutation             | `training/methods/genetic_algorithm/operators.py:mutate_gaussian` | Per-gene gaussian noise with probability `mutation_probability`.                       |
| Elitism              | `training/methods/genetic_algorithm/driver.py`                    | Preserves top ~10% (min 2) by raw fitness; injects all-time best if stagnation is low. |
| Adaptive mutation    | `training/methods/genetic_algorithm/driver.py:_adapt_mutation`    | Boosts mutation probability and sigma after stagnation threshold (10 gens).            |

### Novelty & Reward Diversity Selection (Implemented)

GA selection is not based purely on raw fitness:

- Per-agent behavior vectors are computed from action/engagement metrics (`training/components/novelty.py`).
- Per-agent reward diversity is computed from the reward breakdown entropy (`training/components/diversity.py`).
- Selection score is computed as `fitness + novelty_bonus + diversity_bonus` (`training/components/selection.py`).
- A `BehaviorArchive` stores historically novel behaviors and influences novelty distances (`training/components/archive.py`).

See `plans/SHARED_COMPONENTS.md` for the full novelty/diversity system details.

### Evaluation Loop (Implemented)

**Parallel rollouts**

- `evaluate_population_parallel(...)` evaluates each individual on `SEEDS_PER_AGENT` seeded rollouts using `HeadlessAsteroidsGame(random_seed=...)`.
- Rollouts are executed concurrently via `ThreadPoolExecutor(max_workers=os.cpu_count())`.
- Seed assignment is deterministic per generation and depends on `GAConfig.USE_COMMON_SEEDS`:
  - Default (`USE_COMMON_SEEDS=False`): `generation_seed + agent_idx * seeds_per_agent + seed_offset` (unique seeds per individual).
  - CRN mode (`USE_COMMON_SEEDS=True`): `generation_seed + seed_offset` (shared seed set across individuals).

**Per-agent averaged metrics (returned from evaluator)**

Each agent's metrics are averaged across its seeds and returned in `per_agent_metrics`:

- Fitness:
  - `fitness`: averaged total reward score.
- Core gameplay:
  - `steps_survived`: averaged survival steps.
  - `kills`: averaged kills.
  - `shots_fired`: averaged shots.
  - `accuracy`: averaged kills/shots.
- Action usage:
  - `thrust_frames`, `turn_frames`, `shoot_frames`: averaged counts.
  - `left_only_frames`, `right_only_frames`, `both_turn_frames`: averaged detailed turn breakdown (spin diagnosis).
  - `idle_rate`: averaged fraction of "no input" frames.
- Engagement / risk:
  - `avg_asteroid_dist`: averaged nearest-asteroid distance.
  - `min_asteroid_dist`: averaged closest approach distance (risk proxy).
  - `screen_wraps`: averaged wrap count (coverage proxy).
- Reward anatomy:
  - `reward_breakdown`: averaged per-component totals.
- Novelty/diversity inputs:
  - `behavior_vector`: 7D behavior characterization vector.
  - `reward_diversity`: entropy-based diversity score.
- Neural/behavior health:
  - `output_saturation`: % of outputs near 0/1 (saturated).
  - `action_entropy`: Shannon entropy of action-combination distribution.

**Per-generation aggregated metrics (returned from evaluator)**

- Population averages for the above (e.g. `avg_kills`, `avg_accuracy`, `avg_action_entropy`).
- Population action-style averages:
  - `avg_thrust_duration`, `avg_turn_duration`, `avg_shoot_duration`
- Population detailed turn averages:
  - `avg_left_only_frames`, `avg_right_only_frames`, `avg_both_turn_frames`
- Best-agent aggregates:
  - `best_agent_positions`, `best_agent_kill_events` (heatmap inputs).
- Population sample aggregates:
  - `population_positions`, `population_kill_events` (heatmap inputs).
- Reward aggregates:
  - `avg_reward_breakdown`
  - `avg_quarterly_scores`

### Windowed Playback & Fresh-Game Generalization (Implemented)

- `DisplayManager.start_display(...)` runs the best agent in the windowed `AsteroidsGame`.
- Playback uses:
  - `manual_spawning=True` (spawn timing parity with headless).
  - Forced fixed time step `GAConfig.FRAME_DELAY` even if arcade provides variable `delta_time`.
  - Optional debug overlays, including `draw_hybrid_encoder_debug(...)` when enabled.
- Fresh-game metrics and generalization ratios/grade are recorded into analytics via `TrainingAnalytics.record_fresh_game(...)`.

## Implemented Outputs / Artifacts (if applicable)

- `training_summary.md`: Training report generated by `TrainingAnalytics.generate_markdown_report(...)`.
- `training_data.json`: Training export generated by `TrainingAnalytics.save_json(...)`.

## In Progress / Partially Implemented

- [ ] Checkpointing/resume: Training exports analytics but does not persist the GA population/genomes for resuming runs.
- [ ] Novelty/diversity reporting: Novelty/diversity influences selection, but the markdown report does not explicitly visualize these signals.
- [ ] `ActionInterface(action_space_type="continuous")`: Exists but behaves identically to boolean thresholding.
- [ ] Encoder/test drift: `VectorEncoder` still exists and some legacy code assumes it, while current training uses `HybridEncoder`.
- [ ] `GAConfig.NUM_NEAREST_ASTEROIDS`: Remains in config but is not used by the current `HybridEncoder` training setup.

## Planned / Missing / To Be Changed

### CRUCIAL: Migration to DEAP Framework

The current GA implementation uses entirely custom-written operators and selection logic. **Long-term, we want to migrate to DEAP (Distributed Evolutionary Algorithms in Python)** for the following reasons:

**What DEAP would provide:**

| Feature                              | Current Custom Implementation                     | DEAP Equivalent                                        |
| ------------------------------------ | ------------------------------------------------- | ------------------------------------------------------ |
| Individual/Population representation | `List[List[float]]` in `GADriver`                 | `deap.creator.Individual`, `deap.tools.initRepeat`     |
| Tournament selection                 | `training/methods/genetic_algorithm/selection.py` | `deap.tools.selTournament`                             |
| Crossover operators                  | `operators.py:crossover_blend`                    | `deap.tools.cxBlend`, `cxTwoPoint`, `cxUniform`, etc.  |
| Mutation operators                   | `operators.py:mutate_gaussian`                    | `deap.tools.mutGaussian`, `mutPolynomialBounded`, etc. |
| Elitism                              | Manual in `driver.py`                             | `deap.tools.selBest` combined with selection           |
| Statistics tracking                  | Manual aggregation                                | `deap.tools.Statistics`, `deap.tools.Logbook`          |
| Hall of Fame                         | `best_individual` tracking                        | `deap.tools.HallOfFame`                                |
| Parallelization                      | `ThreadPoolExecutor`                              | `deap.tools.map` with `multiprocessing`                |
| Checkpointing                        | Not implemented                                   | `deap.tools.History` + pickle                          |

**Why migrate:**

- [ ] **Industry standard**: DEAP is widely recognized in evolutionary computation research and industry.
- [ ] **Battle-tested operators**: DEAP's operators are well-tested and optimized.
- [ ] **Built-in statistics**: Automatic tracking of min/max/avg/std without manual aggregation.
- [ ] **Extensibility**: Easy to add new operators, selection schemes, or multi-objective optimization (NSGA-II, SPEA2).
- [ ] **CV value**: DEAP experience is valuable for demonstrating evolutionary algorithm expertise.
- [ ] **Reduced maintenance**: Less custom code to maintain and debug.

**Migration approach (when undertaken):**

- [ ] Replace `GADriver._initialize_population()` with DEAP creator/toolbox.
- [ ] Replace custom selection with `deap.tools.selTournament`.
- [ ] Replace custom crossover/mutation with DEAP equivalents.
- [ ] Integrate `deap.tools.Statistics` with existing `TrainingAnalytics`.
- [ ] Use `deap.tools.HallOfFame` for best individual tracking.
- [ ] Maintain compatibility with existing evaluation infrastructure.

**Current status:** Custom implementation is functional and stable. Migration to DEAP is planned but not urgent. The custom implementation serves as a learning exercise and provides full control over the algorithm details.

---

### Other Planned Work

- [ ] Genome persistence: Save best-of-generation and all-time-best genomes to reloadable files for playback/re-evaluation.
- [ ] Multi-episode fresh-game validation: Replace single fresh-game playback with multiple rollouts and averaged generalization stats.
- [ ] Evaluation abstraction: Generalize evaluator interfaces so ES/NEAT policies can reuse rollouts without hard-coded GA assumptions.
- [ ] Continuous action support: Implement true continuous control (or explicitly remove the misleading "continuous" mode).

## Notes / Design Considerations (optional)

- Training fitness is defined by `training/config/rewards.py` and is intentionally decoupled from the game’s internal reward components.
- Hybrid state encoding changes the input dimensionality and should be treated as a “schema change” for any persisted genomes.
- Evaluation-noise tolerance: Tournament selection + elitism tends to be more tolerant of per-individual seed differences than ES-style gradient estimation, so GA can look stronger under noisy evaluation.
- Seeds-per-agent trade-off: Increasing `GAConfig.SEEDS_PER_AGENT` reduces luck and selects for generalization, but increases episode cost per generation.

## Discarded / Obsolete / No Longer Relevant

- The GA training system no longer relies on `VectorEncoder` as its default encoder; the current baseline encoder for training is `HybridEncoder`.
