# Evolution Strategies (ES)

## Scope / Purpose

Evolution Strategies (ES) is the second optimization method implemented in AsteroidsAI. Its purpose is to benchmark a distribution-based, gradient-estimation approach against the GA while reusing the same environment, state/action interfaces, reward components, and analytics outputs for fair comparison.

ES maintains a probability distribution over parameter space (Gaussian with mean `theta` and stddev `sigma`) and iteratively updates the distribution mean by estimating the gradient of expected fitness through sampling. This contrasts with GA's selection/crossover/mutation approach.

## Current Implemented System

### ES Method Implementation Status (Implemented)

| Component                      | File                                                       | Status                                                          |
| ------------------------------ | ---------------------------------------------------------- | --------------------------------------------------------------- |
| Configuration                  | `training/config/evolution_strategies.py`                  | Implemented                                                     |
| Driver (used)                  | `training/methods/evolution_strategies/cmaes_driver.py`    | Implemented (diagonal CMA-ES).                                  |
| Classic ES Driver (present)    | `training/methods/evolution_strategies/driver.py`          | Present but unused by `training/scripts/train_es.py`.           |
| Fitness Shaping (present)      | `training/methods/evolution_strategies/fitness_shaping.py` | Present but unused by CMA-ES.                                   |
| Training Script                | `training/scripts/train_es.py`                             | Implemented                                                     |
| NumPy Policy (used)            | `ai_agents/policies/feedforward.py`                        | Used by ES training via `NNAgent` (same as GA).                 |
| NumPy Agent (used)             | `ai_agents/neuroevolution/nn_agent.py`                     | Used by ES training for candidate evaluation and playback.      |
| Shared Evaluator (used)        | `training/core/population_evaluator.py`                    | Used by ES training for headless rollouts and metrics.          |
| TensorFlow Policy (present)    | `ai_agents/policies/feedforward_tf.py`                     | Present but currently unused by `training/scripts/train_es.py`. |
| TensorFlow Agent (present)     | `ai_agents/neuroevolution/nn_agent_tf.py`                  | Present but currently unused by `training/scripts/train_es.py`. |
| TensorFlow Evaluator (present) | `training/core/population_evaluator_tf.py`                 | Present but currently unused by `training/scripts/train_es.py`. |

### Entry Point & Orchestration (Implemented)

| Component                 | File                                                    | Granular Responsibility                                                                                                 |
| ------------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Training script           | `training/scripts/train_es.py`                          | Creates encoder/action/reward/driver/analytics/display stack and runs the sample -> evaluate -> display -> update loop. |
| Shared evaluator (used)   | `training/core/population_evaluator.py`                 | Runs seeded headless rollouts in parallel using `NNAgent` (NumPy).                                                      |
| Driver (ES logic)         | `training/methods/evolution_strategies/cmaes_driver.py` | Maintains mean, sigma, and diagonal covariance; samples candidates and updates the distribution using CMA-ES rules.     |
| Playback + generalization | `training/core/display_manager.py`                      | Runs best candidate in windowed "fresh game" (shared with GA).                                                          |

### Policy Representation (Implemented)

| Concept                          | Implementation                                             | Details                                                                                    |
| -------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Mean vector                      | `np.ndarray`                                               | Flat parameter vector representing all weights and biases (center of search distribution). |
| Policy (used by training)        | `ai_agents/policies/feedforward.py:FeedforwardPolicy`      | Pure-Python forward pass (`tanh` hidden activation, `sigmoid` outputs).                    |
| Agent wrapper (used by training) | `ai_agents/neuroevolution/nn_agent.py:NNAgent`             | Wraps `FeedforwardPolicy` and implements `BaseAgent` contract.                             |
| TensorFlow policy (unused)       | `ai_agents/policies/feedforward_tf.py:FeedforwardPolicyTF` | Keras MLP implementation present but not wired into `training/scripts/train_es.py`.        |

**Temporal input wrapper (implemented)**

- `interfaces/encoders/TemporalStackEncoder.py` wraps the base `HybridEncoder` output with 4-frame stacking plus deltas when `ESConfig.USE_TEMPORAL_STACK=True`.

**Parameter count (fixed topology, temporal ES input)**

- Formula: `input*hidden + hidden + hidden*output + output`.
- Current default sizes (temporal enabled):
  - Base input: `HybridEncoder.get_state_size() = 47`
  - Temporal stack: `N=4`, include deltas -> input size `47 * (2N - 1) = 329`
  - Hidden: `ESConfig.HIDDEN_LAYER_SIZE = 24`
  - Output: `3` (signed turn, thrust, shoot)
  - Parameter count: `329*24 + 24 + 24*3 + 3 = 7995`
- If temporal stacking is disabled, input size returns to `47` (param count `1227`).

### ES Hyperparameters (Implemented)

From `training/config/evolution_strategies.py:ESConfig`:

**Core Parameters (CMA-ES):**

| Setting           |     Value | Meaning                                            |
| ----------------- | --------: | -------------------------------------------------- |
| `OPTIMIZER`       | `"cmaes"` | ES optimizer mode used by `train_es.py`.           |
| `POPULATION_SIZE` |     `100` | Number of candidates sampled per generation.       |
| `NUM_GENERATIONS` |     `500` | Total generations in a run.                        |
| `CMAES_SIGMA`     |    `0.15` | Initial CMA-ES step size (global sigma).           |
| `CMAES_MU`        |    `None` | Parent count (defaults to `POPULATION_SIZE // 2`). |
| `CMAES_COV_MIN`   |    `1e-6` | Minimum diagonal covariance value (stability).     |
| `CMAES_COV_TARGET_RATE` | `1e-3` | Target aggregate covariance learning rate (`c1+cmu`) for diagonal CMA-ES. |
| `CMAES_COV_MAX_SCALE`   | `1e4`  | Maximum scaling factor applied to `c1/cmu` to hit the target rate.       |
| `SIGMA_MIN`       |    `0.02` | Minimum sigma floor.                               |

**Evaluation & Sampling:**

**Temporal Encoding (ES Config):**

| Setting                            |  Value | Meaning                                                 |
| ---------------------------------- | -----: | ------------------------------------------------------- |
| `ESConfig.USE_TEMPORAL_STACK`      | `True` | Enable temporal stack wrapper around the base encoder.  |
| `ESConfig.TEMPORAL_STACK_SIZE`     |    `4` | Number of consecutive frames stacked.                   |
| `ESConfig.TEMPORAL_INCLUDE_DELTAS` | `True` | Append per-feature deltas (`N-1`) after stacked frames. |

| Setting            |  Value | Meaning                                             |
| ------------------ | -----: | --------------------------------------------------- |
| `SEEDS_PER_AGENT`  |    `3` | Headless rollouts per candidate (fitness averaged). |
| `MAX_STEPS`        | `1500` | Step limit per rollout/playback.                    |
| `USE_COMMON_SEEDS` | `True` | CRN mode: all candidates see same seeds.            |
| `USE_ANTITHETIC`   | `True` | Use mirrored sampling when population size is even. |

**Noise Handling & Restarts (ES Config):**

| Setting                         | Value | Meaning                                                                 |
| ------------------------------- | ----: | ----------------------------------------------------------------------- |
| `NOISE_HANDLING_ENABLED`        | `True` | Re-evaluate top candidates with extra seeds to reduce seed luck.        |
| `NOISE_HANDLING_TOP_K`          |    `5` | Number of top candidates to confirm per generation.                     |
| `NOISE_HANDLING_EXTRA_SEEDS`    |    `1` | Extra seeds per confirmed candidate.                                    |
| `NOISE_HANDLING_SEED_OFFSET`    | `100000` | Offset to avoid overlapping training seeds.                           |
| `RESTART_ENABLED`               | `True` | Allow CMA-ES restarts when stagnating.                                  |
| `RESTART_PATIENCE`              |   `12` | Generations without best-fitness improvement before restart triggers.   |
| `RESTART_MIN_GENERATIONS`       |    `5` | Minimum generations before restarts are allowed.                        |
| `RESTART_COOLDOWN`              |    `5` | Cooldown generations between restart triggers.                          |
| `RESTART_SIGMA_MULTIPLIER`      |   `1.0` | Sigma multiplier applied on restart.                                    |
| `RESTART_USE_BEST_CANDIDATE`    | `True` | Restart mean from best candidate instead of random initialization.      |

**Pareto Objectives (Shared):**

| Setting                                      |                        Value | Meaning                                                             |
| -------------------------------------------- | ---------------------------: | ------------------------------------------------------------------- |
| `ParetoConfig.OBJECTIVES`                    | `hits, time_alive, softmin_ttc` | Objective vector optimized by CMA-ES selection.                  |
| `ParetoConfig.ACCURACY_MIN_SHOTS`            |                          `5` | Minimum shots required before accuracy counts.                      |
| `ParetoConfig.ACCURACY_ZERO_BELOW_MIN_SHOTS` |                       `True` | Accuracy becomes 0 below the shot minimum.                          |
| `ParetoConfig.FRAME_DELAY`                   |                       `1/60` | Used to derive `time_alive` if missing.                             |
| `ParetoConfig.FITNESS_TIEBREAKER`            |                       `True` | Use fitness as a tie-breaker when Pareto rank + crowding are equal. |

### ES Algorithm Components (Implemented)

| Component      | File                                              | Granular Behavior                                                                                                                |
| -------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Sampling       | `cmaes_driver.py:CMAESDriver.sample_population()` | Samples candidates from a diagonal Gaussian using the current mean, sigma, and covariance vector (optionally mirrored sampling). |
| CMA-ES update  | `cmaes_driver.py:CMAESDriver.update()`            | Updates mean, sigma, and diagonal covariance using CMA-ES evolution paths and Pareto-ranked candidate selection.                 |
| Pareto ranking | `training/components/pareto/*`                    | Computes objective vectors (`hits`, `time_alive`, `softmin_ttc`, `accuracy`), assigns Pareto fronts, and orders candidates for selection. |

### Evaluation Loop (Implemented)

**Parallel rollouts (shared evaluator)**

- `training/core/population_evaluator.py:evaluate_population_parallel(...)` evaluates each candidate on `SEEDS_PER_AGENT` seeds derived from a per-generation `generation_seed` using `HeadlessAsteroidsGame(random_seed=...)` (with optional CRN via `use_common_seeds`).
- Uses `ai_agents/neuroevolution/nn_agent.py:NNAgent` for forward passes (same policy stack as GA).
- Rollouts are executed concurrently via `ThreadPoolExecutor(max_workers=os.cpu_count())`.
- Returns same metrics structure as GA evaluator for analytics compatibility.

**Common Random Numbers (CRN) for ES (Implemented)**

- `evaluate_population_parallel(...)` accepts a `use_common_seeds` parameter (default `False`).
- When `use_common_seeds=True` (used by ES training):
  - All candidates within a generation are evaluated on the **same** seed set.
  - Seed derivation: `seed = generation_seed + seed_offset` (independent of agent index).
  - This ensures fitness differences reflect parameter differences, not environmental luck.
  - The seed set changes across generations to maintain generalization pressure.
  - Antithetic pairs (`+epsilon` and `-epsilon`) now see identical rollout randomness, enabling proper variance reduction.
- When `use_common_seeds=False` (used by GA training):
  - Each agent gets unique seeds: `seed = generation_seed + agent_idx * seeds_per_agent + seed_offset`.
  - GA is more noise-tolerant due to tournament selection + elitism.

**Noise Handling (Implemented)**

- When `NOISE_HANDLING_ENABLED=True`, the top-K Pareto candidates are re-evaluated with extra seeds.
- Confirmed results replace the initial averages for those candidates before selection and CMA-ES updates.
- This reduces seed-luck artifacts without re-evaluating the full population.

**Restarts (Implemented)**

- When best fitness stagnates for `RESTART_PATIENCE` generations, CMA-ES can reset mean/sigma/cov.
- Restart mean defaults to the best candidate when `RESTART_USE_BEST_CANDIDATE=True`.

### Reward Preset (Implemented)

- Default reward preset is rebalanced so no single component dominates total fitness:
  - `VelocitySurvivalBonus(reward_multiplier=1.5, max_velocity_cap=15.0)`
  - `DistanceBasedKillReward(max_reward_per_kill=18.0, min_reward_fraction=0.15)`
  - `ConservingAmmoBonus(hit_bonus=4.0, shot_penalty=-2.0)`
  - `ExplorationBonus(grid_rows=3, grid_cols=4, bonus_per_cell=5.0)`
  - `DeathPenalty(penalty=-150.0, early_death_scale=1.0)` with max time derived from `max_steps * frame_delay`
- `create_reward_calculator(max_steps, frame_delay)` now passes `max_time_alive` into `DeathPenalty` for early-death scaling.

### Action Mapping (Implemented)

- Signed turn control: `ActionInterface` converts `action[0]` into a signed turn value (`turn_value = action[0] * 2 - 1`) with no deadzone; left if `< 0`, right if `> 0`.
- Thrust and shoot remain thresholded at `> 0.5` for `action[1]` and `action[2]`.

### Pareto Objectives (Implemented)

- ES uses shared Pareto objective vectors (`hits`, `time_alive`, `softmin_ttc`) for candidate ranking and CMA-ES updates.
- Accuracy remains computed and available for Pareto selection by swapping `ParetoConfig.OBJECTIVES`.
- When accuracy is used as a Pareto objective, it enforces a minimum shots threshold (`ACCURACY_MIN_SHOTS=5`) to avoid single-shot perfect accuracy.
- Fitness is used as a tie-breaker when Pareto rank and crowding are identical (`ParetoConfig.FITNESS_TIEBREAKER=True`).
- Reward-based fitness is still computed for analytics and display, but it does not drive CMA-ES selection.

**Best Candidate Tracking (Implemented)**

- `training/scripts/train_es.py` stores the actual best candidate parameter vector (`best_candidate`) rather than the distribution mean.
- The best candidate is selected using Pareto ordering over `hits`, `time_alive`, and `softmin_ttc`.
- A normalized Pareto score is tracked across generations to pick a best-of-run candidate for playback.
- All-time best fitness is tracked separately as the maximum fitness observed across the population for display/analytics.
- Fitness is still recorded for display and analytics, but it does not drive selection or updates.

**Per-candidate averaged metrics**

Same as GA:

- Fitness, steps_survived, time_alive, kills, shots_fired, accuracy, softmin_ttc
- thrust_frames, turn_frames, shoot_frames, idle_rate
- **Detailed turn metrics: left_only_frames, right_only_frames, both_turn_frames** (for diagnosing spin behavior)
- avg_asteroid_dist, min_asteroid_dist, screen_wraps
- behavior_vector, reward_diversity
- output_saturation, action_entropy

### Analytics Integration (Implemented)

ES records the same generation-level keys as GA, plus ES-specific metrics:

**Standard metrics (shared with GA):**

- `generation`, `best_fitness`, `avg_fitness`, `min_fitness`, `median_fitness`, `std_dev`
- `population_size`, percentiles, improvements, stagnation counter
- Behavioral metrics: kills, accuracy, survival, action patterns
- Spatial data: positions, kill events (for heatmaps)

**ES-specific metrics:**

- `sigma`: Current CMA-ES global step size.
- `mean_param_norm`: L2 norm of the current CMA-ES mean vector.
- `cov_diag_mean`: Mean of the diagonal covariance vector.
- `cov_diag_min`: Minimum diagonal covariance value.
- `cov_diag_max`: Maximum diagonal covariance value.
- `cov_diag_std`: Standard deviation of diagonal covariance values.
- `cov_diag_mean_abs_dev`: Mean absolute deviation of diagonal covariance from 1.0.
- `cov_diag_max_abs_dev`: Largest absolute deviation of diagonal covariance from 1.0.
- `cov_lr_scale`: Scaling factor applied to `c1/cmu` for diagonal covariance adaptation.
- `cov_lr_effective_rate`: Effective `c1 + cmu` rate after scaling/clamping.
- `pareto_enabled`: Whether Pareto ranking was active for the update.
- `pareto_tiebreaker`: Tie-breaker strategy applied after Pareto ranking (e.g., fitness).
- `pareto_front0_size`: Population size of the first Pareto front.
- `pareto_best_crowding`: Largest crowding distance observed in the front.

### Fresh-Game Generalization (Implemented)

- Same infrastructure as GA via `DisplayManager.start_display(...)`.
- Best candidate of each generation is displayed in the windowed game.
- Fresh-game metrics and generalization ratios are recorded via `TrainingAnalytics.record_fresh_game(...)`.

## Implemented Outputs / Artifacts (if applicable)

- `training_summary_es.md`: Markdown report generated by ES training, containing run summary metrics, config snapshot, and ES optimizer diagnostics in the Technical Appendix.
- `training_data_es.json`: JSON export with schema, config, and per-generation data.

## In Progress / Partially Implemented
- [ ] TensorFlow ES pipeline usage decision: TF policy/evaluator exist but are not invoked by `training/scripts/train_es.py`, leaving two ES stacks (NumPy-wired vs TF-unused).
- [ ] ES evaluation robustness: CRN + antithetic sampling exist, but there is no confirmation re-evaluation step for top candidates (best-of-generation can still be seed-noise-driven).
- [ ] Classic ES config drift: AdamW, rank transformation, and elitism settings remain in `ESConfig` but are no longer used by the CMA-ES driver.
- [ ] CMA-ES elite retention gap: Best candidates are tracked for display, but there is no explicit elite injection into sampling/evaluation for stability.
- [ ] CMA-ES progress signal mismatch: Stagnation/restarts are driven by scalar best fitness, while updates are driven by Pareto ordering, so “improvement” signals can disagree.
- [ ] Seed-noise robustness gap: Evaluator produces per-candidate `fitness_std` across seeds, but selection/update logic does not use it to damp noisy updates or prefer stable candidates.
- [ ] Pareto diagnostics visibility gap: Only a small subset of Pareto structure is exported/reported, limiting objective-set evaluation and tuning.

## Planned / Missing / To Be Changed

### Implementation Roadmap (Easy / Medium / Hard)

### Adaptive Hyperparameter Roadmap (Planned)

These items describe ways ES can move from fixed knobs to **adaptive schedules** (noise-aware, stagnation-aware, or diversity-aware), while keeping runs interpretable via explicit logging.

- [ ] Adaptive classic-ES learning rate schedule: when `ESConfig.OPTIMIZER="classic"`, schedule `LEARNING_RATE` using plateau/stagnation heuristics.
- [ ] Adaptive population size schedule: adjust `POPULATION_SIZE` based on gradient estimate noise (and log cost/benefit).
- [ ] Adaptive seeds-per-agent schedule: adjust `SEEDS_PER_AGENT` when rankings are unstable (seed variance spikes).
- [ ] Adaptive noise-handling schedule: adjust `NOISE_HANDLING_TOP_K` and `NOISE_HANDLING_EXTRA_SEEDS` based on observed seed noise and confirmation flips.
- [ ] Adaptive restart policy: adjust `RESTART_PATIENCE` and `RESTART_SIGMA_MULTIPLIER` based on stagnation severity and sigma collapse.
- [ ] Adaptive elite injection schedule: adjust `ELITE_INJECTION_FREQUENCY` based on drift away from known-good elites.
- [ ] Adaptive elite pull schedule: adjust `ELITE_PULL_STRENGTH` and `ELITE_PULL_PATIENCE` based on stagnation length and update stability.
- [ ] Adaptive novelty pressure schedule: adjust `NOVELTY_WEIGHT` based on behavior collapse (low diversity / low novelty).
- [ ] Adaptive diversity pressure schedule: adjust `DIVERSITY_WEIGHT` based on reward concentration (high dominance / low entropy).
- [ ] Adaptive objective set schedule (shared): rotate or reweight `ParetoConfig.OBJECTIVES` across phases while logging the active objective set.

#### Easy (low-risk, high-leverage ES improvements)

**Controllability (make behavior changes continuous rather than cliff-based):**

- [ ] Continuous turning control path: Replace signed-turn thresholding with a true continuous turn value (small output changes produce small turn changes).
- [ ] Turn stability shaping (ES-only optional): Add an ES evaluation metric/penalty for one-direction dominance (extreme `turn_balance`) and zero switching (`turn_switch_rate`) to prevent spin-lock collapse.

**Learnability (make ES updates reflect real improvement, not seed luck):**

- [ ] Candidate confirmation evaluation: Re-evaluate top-K candidates with additional rollouts and use the confirmed ranking for elite tracking and/or updates.
- [ ] Persistent validation seeds: Add a held-out seed set for periodic evaluation so “best-of-run” is not defined only by training seeds.
- [ ] Update gating: Reduce learning rate and/or skip mean updates when the ranking is unstable (e.g., poor agreement between cheap-vs-confirmed evaluation).
- [ ] CMA-ES elite injection (replacement): Replace one sampled candidate per generation with the best-so-far candidate so elite evaluation is compute-neutral.
- [ ] CMA-ES elite evaluation telemetry: Record the injected elite’s fitness/objectives/seed variance so drift away from “known good” is observable.
- [ ] CMA-ES mean pull toward elite: Apply a controlled `mean <- mean + pull_strength * (elite - mean)` when stagnating to recover without restarting.
- [ ] CMA-ES pull cooldown: Add a cooldown so elite pulls cannot trigger repeatedly across consecutive generations.
- [ ] CMA-ES post-pull sigma bump: Optionally multiply sigma briefly after a pull to re-expand local exploration around the recovered region.
- [ ] Pareto-consistent stagnation metric: Trigger stagnation based on a Pareto-aligned progress scalar instead of scalar best fitness.
- [ ] Variance-aware progress scalar: Track a stability-aware score (e.g., `fitness - k*fitness_std`) to reduce seed-luck dominance without additional seeds.
- [ ] `fitness_std` tie-break: When Pareto rank/crowding are similar, prefer lower `fitness_std` candidates to reduce brittle “lucky” selection.
- [ ] `fitness_std` update damping: Scale down mean step size when the selected parents have unusually high seed variance to prevent noisy over-updates.
- [ ] `fitness_std` parent down-weighting: Down-weight high-variance parents during recombination so they influence the update less than stable parents.
- [ ] Seed-stability Pareto objective (optional): Add `fitness_std` as a minimization objective so Pareto ordering directly favors robust candidates without extra rollouts.
- [ ] Elite parent eligibility rule: Allow the injected elite to participate in recombination only when it is within a configurable trust radius of the current mean.
- [ ] Elite exclusion default: Exclude the injected elite from recombination by default so elite evaluation does not destabilize the CMA-ES update.
- [ ] `CMAES_MU` tuning (compute-neutral): Reduce `mu` to increase selection pressure without changing `POPULATION_SIZE`.
- [ ] Crowding-informed recombination weights: Modulate recombination weights using crowding distance so the update preserves front diversity.
- [ ] Crowding normalization rule: Define a deterministic mapping for finite vs infinite crowding so weighting is stable and reproducible.

**Alignment (make “better fitness” mean “plays better”):**

- [ ] Skill proxy objective surfacing: Ensure the ES scalar score includes measurable skill proxies (aim-at-shot, danger reaction, efficient shooting, movement/coverage), not only survival/death timing.
- [ ] Degenerate behavior suppression (ES-only optional): Penalize “always shoot” or “never thrust” regimes using existing behavioral metrics so the optimizer cannot win by trivial input saturation.

- [ ] Pareto objective usage audit (reporting): Report per-objective variance/spread so objectives that have no selection effect can be detected explicitly.
- [ ] Pareto objective dominance audit (reporting): Report objective correlations and rank sensitivity so redundant objectives are identified explicitly.

**Observability (ensure the policy can perceive what it needs to control):**

- [ ] Threat-imminence minimal features: Add “nearest threat closing speed” and “nearest threat bearing” to the ES state (if not already sufficiently represented by current encoder features).

- [ ] Pareto front histogram export (reporting): Export per-generation front rank counts (front0/front1/...) so front growth/collapse is measurable.
- [ ] Pareto crowding distribution export (reporting): Export crowding distance percentiles and infinite-count per generation so diversity pressure is visible.
- [ ] Objective spread export (reporting): Export objective summaries (mean/median/p10/p90) for full population and for front0 only.
- [ ] Pareto-vs-fitness consistency export (reporting): Export whether the Pareto-selected candidate is also top-k by scalar fitness so selection alignment is explicit.
- [ ] Pareto tie-break telemetry (reporting): Export counts of tie-break usage so Pareto stability is measurable.

#### Medium (multi-step changes across ES, encoder, and evaluation stack)

**Observability (temporal information without changing the optimizer):**

- [ ] Predictive perception features: Add time-to-collision (TTC) features to represent imminent collision risk explicitly (per-ray closing-speed is already emitted by `HybridEncoder.encode_rays(...)`).

**Controllability (structured action heads and smoothing):**

- [ ] Action head scaling: Use different sensitivity/scale per action channel (turn vs thrust vs shoot) so turn can be fine-grained without making shoot noisy.
- [ ] Action smoothing filter (policy-side): Apply inertia/smoothing to turn output to reduce oscillation and improve aim tracking stability.

**Learnability (noise control and trustworthiness):**

- [ ] Two-stage evaluation pipeline: Use cheap evaluation for ranking all candidates, then expensive evaluation for confirming top candidates (and for computing the ES update signal if needed).
- [ ] Seed curriculum (stability + generalization): Maintain a persistent “core” seed set for stable gradients, plus a rotating seed set for generalization pressure.

**Alignment (explicit skill targets):**

- [ ] Ray-danger avoidance shaping (shared): Add a reward component that penalizes time spent with dangerous ray hits (e.g., min ray distance below a threshold) and rewards increasing clearance while under threat.
- [ ] Aim-alignment shaping (shared): Add a reward component that pays per-second based on “front-aligned” nearest threat (highest when a threat is forward, decaying toward rear) to encourage deliberate aiming before firing.
- [ ] Output saturation penalty (shared): Penalize sustained saturated outputs (especially constant shoot output) using existing saturation diagnostics to discourage trivial always-on control.

#### Hard (architectural and algorithmic upgrades; large implementation + validation effort)

**Learnability (ES algorithm upgrades beyond isotropic noise):**

- [ ] Update-quality control variates: Add stronger variance-reduction techniques (e.g., control variates/baselines) and step-size schedules that respond to ranking stability over time.

**Observability + controllability (temporal policies, not just temporal inputs):**

- [ ] Recurrent policy (GRU/LSTM): Replace the memoryless MLP with a recurrent policy so the agent can maintain internal state (tracking, mode switching, stabilization).
- [ ] Temporal convolution policy: Alternative to RNNs; use short temporal conv over stacked frames for smoother, learnable control dynamics.

**Alignment (optimize "plays well" as a multi-dimensional target):**

- [ ] Pareto expansion beyond core objectives: Add additional objectives (e.g., multi-threat danger risk, turn sanity, optional fitness) only after the 3-objective baseline is stable and interpretable.

**Exploration (escape discretization dead-zones and brittle determinism):**

- [ ] Stochastic policy outputs with annealing: Treat action outputs as distributions (probabilistic shoot/thrust, continuous turn with noise) and anneal exploration over time while keeping evaluation RNG controlled.

**Operational robustness (long-run practicality):**

- [ ] Checkpointing: Save/load ES state (mean vector, sigma, best_candidate, optimizer state, archive state) to resume long runs and reproduce best policies.
- [ ] Comparative analysis tools: Side-by-side GA vs ES metric visualizations with compute-normalized comparisons (episode budget, wall time, seed sets).
- [ ] ES-specific markdown report sections: Dedicated visualization for sigma decay, elite tracking, update stability, and multi-objective front summaries when enabled.

### Key Differences vs Current ES (Why These Changes Are Non-Trivial)

- Current ES uses diagonal CMA-ES; moving to full covariance (LM-CMA) adds state, compute, and stability constraints.
- Current policy uses temporal stacking; moving to recurrent or temporal-CNN policies adds state, compute, and stricter evaluation-noise control.
- Current action mapping is thresholded; true continuous control changes behavior emergence and requires tight parity across headless evaluation and windowed playback.
- Current Pareto set is limited to 3 objectives; expanding the objective vector increases front size and demands stronger normalization and selection pressure.

## Implementation Details

### ES Algorithm Overview

```
Initialize:
  mean = zeros(param_size)          # Distribution mean
  sigma = initial_sigma             # Global step size
  cov_diag = ones(param_size)       # Diagonal covariance
  p_sigma = zeros(param_size)       # Step-size path
  p_c = zeros(param_size)           # Covariance path

For each generation:
    1. Sample: z_i ~ N(0, I)
       y_i = sqrt(cov_diag) * z_i
       x_i = mean + sigma * y_i
       (optional antithetic pairs)

    2. Evaluate: collect per-candidate metrics
      objectives = [hits, time_alive, softmin_ttc]

    3. Rank: assign Pareto fronts + crowding distance

    4. Select: choose top mu candidates by Pareto order
       compute weighted mean direction y_w

    5. Update mean:
       mean <- mean + sigma * y_w

    6. Update paths:
       p_sigma <- (1 - c_sigma) * p_sigma + sqrt(c_sigma * (2 - c_sigma) * mu_eff) * z_w
       p_c <- (1 - c_c) * p_c + h_sigma * sqrt(c_c * (2 - c_c) * mu_eff) * y_w

    7. Update covariance (diagonal):
       cov_diag <- (1 - c1 - cmu) * cov_diag + c1 * p_c^2 + cmu * sum(w_i * y_i^2)

    8. Update sigma:
       sigma <- sigma * exp((c_sigma / d_sigma) * (||p_sigma|| / E||N(0,I)|| - 1))
```

### Key Differences from GA

| Aspect                     | GA                           | ES                                                            |
| -------------------------- | ---------------------------- | ------------------------------------------------------------- |
| Representation             | Population of individuals    | Distribution mean + diagonal covariance                       |
| Selection                  | Tournament on combined score | Pareto-ranked recombination (front + crowding)                |
| Crossover                  | BLX-alpha blending           | None (distribution update)                                    |
| Mutation                   | Per-gene Gaussian noise      | Distribution sampling with covariance adaptation              |
| Elitism                    | Preserve top 10%             | Best-of-run tracked for display (no explicit elite injection) |
| Optimizer                  | N/A (direct replacement)     | CMA-ES update rules (paths, sigma, covariance)                |
| Update rule                | Replace population           | Recombine selected candidates into new distribution           |
| Sigma schedule             | N/A                          | CMA-ES step-size adaptation (path-based)                      |
| Framework (current wiring) | NumPy                        | NumPy                                                         |

### File Structure (Implemented)

```
ai_agents/
├── neuroevolution/
│   ├── nn_agent.py                 # NumPy agent wrapper (used by GA + ES training scripts)
│   └── nn_agent_tf.py              # TensorFlow agent wrapper (present, currently unused by ES script)
└── policies/
    ├── feedforward.py              # Pure-Python policy forward pass (used by GA + ES training scripts)
    └── feedforward_tf.py           # TensorFlow Keras policy (present, currently unused by ES script)

training/
├── config/
│   └── evolution_strategies.py     # ESConfig class
├── core/
│   ├── population_evaluator.py     # Shared evaluator (used by GA + ES training scripts)
│   └── population_evaluator_tf.py  # TensorFlow parallel evaluator (present, currently unused by ES script)
├── methods/
│   └── evolution_strategies/
│       ├── __init__.py
│       ├── driver.py               # ESDriver class
│       └── fitness_shaping.py      # Rank transformation utilities
└── scripts/
    └── train_es.py                 # ES training entry point
```

- `training/methods/evolution_strategies/cmaes_driver.py`: CMA-ES driver used by `train_es.py`.
- `training/config/pareto.py`: Shared Pareto objective configuration.
- `training/components/pareto/*`: Pareto objective extraction, ranking, and ordering utilities.

## Notes / Design Considerations (optional)

- **CRN implementation rationale**: ES gradient estimation is highly sensitive to evaluation noise. With CRN (`use_common_seeds=True`), all candidates see identical environments, so fitness differences purely reflect parameter quality. The seed set changes across generations to maintain generalization pressure. This is critical for ES but less important for GA (which uses tournament selection + elitism for noise tolerance).
- **Antithetic sampling with CRN**: The `+epsilon`/`-epsilon` variance reduction technique now works correctly because paired perturbations see identical rollout randomness.
- **Best candidate vs mean**: ES now stores the actual best-performing candidate weights for playback, not the distribution mean. The mean is a smoothed estimate that was never directly evaluated, so using it for "best policy" was misleading.
- **CMA-ES diagonal covariance**: ES adapts per-parameter variance; full covariance is deferred for complexity/compute reasons.
- **Pareto-first selection**: Candidate ordering uses Pareto front + crowding over hits/time_alive/softmin_ttc; reward fitness is still logged for display.
- **Turn direction metrics**: The evaluator now tracks `left_only_frames`, `right_only_frames`, and `both_turn_frames` separately. This allows diagnosing whether agents are spinning in one direction, alternating intelligently, or pressing both turn keys (which cancel out to ~0 rotation).
- Action discontinuity: `interfaces/ActionInterface.py` thresholds outputs at `0.5`, creating a piecewise-constant policy mapping that makes the fitness landscape jagged for ES-style updates.
- Sample budget comparability: ES "one generation" can cost far more rollouts than GA (population \* seeds per candidate), so wall-clock comparisons should be normalized by total episodes evaluated.
- TensorFlow stack status: A TF policy/evaluator exists but is not currently used by the ES training entry point; the canonical ES execution path today is NumPy-based.
- Compute budget constraint (ES): Prefer compute-neutral robustness (elite replacement, `fitness_std` tie-break/damping, crowding-weighted recombination) over increasing `POPULATION_SIZE` or `SEEDS_PER_AGENT`.

## Discarded / Obsolete / No Longer Relevant

- TensorFlow-only ES documentation: Earlier documentation treated ES as TensorFlow-first; the current wired training path uses the shared NumPy policy/evaluator, and TF components are present but unused.
- Natural Evolution Strategies (NES): Considered as a covariance-adaptive ES direction, but explicitly deprioritized in favor of implementing CMA-ES/LM-CMA as the single covariance-adaptive ES track to avoid conflicting optimizer semantics in the planned roadmap.
