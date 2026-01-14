# Evolution Strategies (ES)

## Scope / Purpose

Evolution Strategies (ES) is the second optimization method implemented in AsteroidsAI. Its purpose is to benchmark a distribution-based, gradient-estimation approach against the GA while reusing the same environment, state/action interfaces, reward components, and analytics outputs for fair comparison.

ES maintains a probability distribution over parameter space (Gaussian with mean `theta` and stddev `sigma`) and iteratively updates the distribution mean by estimating the gradient of expected fitness through sampling. This contrasts with GA's selection/crossover/mutation approach.

## Current Implemented System

### ES Method Implementation Status (Implemented)

| Component | File | Status |
|-----------|------|--------|
| Configuration | `training/config/evolution_strategies.py` | Implemented |
| Driver | `training/methods/evolution_strategies/driver.py` | Implemented |
| Fitness Shaping | `training/methods/evolution_strategies/fitness_shaping.py` | Implemented |
| Training Script | `training/scripts/train_es.py` | Implemented |
| NumPy Policy (used) | `ai_agents/policies/feedforward.py` | Used by ES training via `NNAgent` (same as GA). |
| NumPy Agent (used) | `ai_agents/neuroevolution/nn_agent.py` | Used by ES training for candidate evaluation and playback. |
| Shared Evaluator (used) | `training/core/population_evaluator.py` | Used by ES training for headless rollouts and metrics. |
| TensorFlow Policy (present) | `ai_agents/policies/feedforward_tf.py` | Present but currently unused by `training/scripts/train_es.py`. |
| TensorFlow Agent (present) | `ai_agents/neuroevolution/nn_agent_tf.py` | Present but currently unused by `training/scripts/train_es.py`. |
| TensorFlow Evaluator (present) | `training/core/population_evaluator_tf.py` | Present but currently unused by `training/scripts/train_es.py`. |

### Entry Point & Orchestration (Implemented)

| Component | File | Granular Responsibility |
|-----------|------|-------------------------|
| Training script | `training/scripts/train_es.py` | Creates encoder/action/reward/driver/analytics/display stack and runs the sample -> evaluate -> display -> update loop. |
| Shared evaluator (used) | `training/core/population_evaluator.py` | Runs seeded headless rollouts in parallel using `NNAgent` (NumPy). |
| Driver (ES logic) | `training/methods/evolution_strategies/driver.py` | Maintains mean vector, samples perturbations, computes gradient updates. |
| Playback + generalization | `training/core/display_manager.py` | Runs best candidate in windowed "fresh game" (shared with GA). |

### Policy Representation (Implemented)

| Concept | Implementation | Details |
|---------|----------------|---------|
| Mean vector | `np.ndarray` | Flat parameter vector representing all weights and biases (center of search distribution). |
| Policy (used by training) | `ai_agents/policies/feedforward.py:FeedforwardPolicy` | Pure-Python forward pass (`tanh` hidden activation, `sigmoid` outputs). |
| Agent wrapper (used by training) | `ai_agents/neuroevolution/nn_agent.py:NNAgent` | Wraps `FeedforwardPolicy` and implements `BaseAgent` contract. |
| TensorFlow policy (unused) | `ai_agents/policies/feedforward_tf.py:FeedforwardPolicyTF` | Keras MLP implementation present but not wired into `training/scripts/train_es.py`. |

**Parameter count (fixed topology, same as GA)**

- Formula: `input*hidden + hidden + hidden*output + output`.
- Current default sizes:
  - Input: `HybridEncoder.get_state_size() = 31`
  - Hidden: `ESConfig.HIDDEN_LAYER_SIZE = 24`
  - Output: `3` (signed turn, thrust, shoot)
  - Parameter count: `31*24 + 24 + 24*3 + 3 = 843`

### ES Hyperparameters (Implemented)

From `training/config/evolution_strategies.py:ESConfig`:

**Core Parameters:**

| Setting | Value | Meaning |
|---------|------:|---------|
| `POPULATION_SIZE` | `100` | Number of perturbations per generation. |
| `NUM_GENERATIONS` | `500` | Total generations in a run. |
| `SIGMA` | `0.15` | Initial noise standard deviation for perturbations. |
| `LEARNING_RATE` | `0.03` | Step size for mean updates (reduced for stability with AdamW). |
| `WEIGHT_DECAY` | `0.0025` | L2 regularization coefficient. |

**Sigma Schedule:**

| Setting | Value | Meaning |
|---------|------:|---------|
| `SIGMA_DECAY` | `0.99` | Per-generation sigma decay (faster than before). |
| `SIGMA_MIN` | `0.02` | Minimum sigma floor. |
| `ADAPTIVE_SIGMA_ENABLED` | `True` | Accelerate decay when stagnating. |
| `ADAPTIVE_SIGMA_PATIENCE` | `10` | Generations without improvement before adaptive decay. |
| `ADAPTIVE_SIGMA_FACTOR` | `0.95` | Additional decay factor when stagnating. |

**AdamW Optimizer:**

| Setting | Value | Meaning |
|---------|------:|---------|
| `USE_ADAMW` | `True` | Use AdamW instead of vanilla SGD. |
| `ADAMW_BETA1` | `0.9` | First moment decay (momentum). |
| `ADAMW_BETA2` | `0.999` | Second moment decay (adaptive LR). |
| `ADAMW_EPSILON` | `1e-8` | Numerical stability constant. |

**Elitism:**

| Setting | Value | Meaning |
|---------|------:|---------|
| `ENABLE_ELITISM` | `True` | Track and preserve best-ever candidate. |
| `ELITE_INJECTION_FREQUENCY` | `1` | Inject elite into candidate pool every N generations. |
| `ELITE_PULL_ENABLED` | `True` | Pull mean toward elite when stagnating. |
| `ELITE_PULL_STRENGTH` | `0.1` | How much to pull mean toward elite (0-1). |
| `ELITE_PULL_PATIENCE` | `15` | Generations of stagnation before pulling. |

**Evaluation & Sampling:**

| Setting | Value | Meaning |
|---------|------:|---------|
| `SEEDS_PER_AGENT` | `3` | Headless rollouts per candidate (fitness averaged). |
| `MAX_STEPS` | `1500` | Step limit per rollout/playback. |
| `USE_COMMON_SEEDS` | `True` | CRN mode: all candidates see same seeds. |
| `USE_ANTITHETIC` | `True` | Use mirrored sampling (`epsilon` and `-epsilon` pairs). |
| `USE_RANK_TRANSFORMATION` | `True` | Apply rank-based fitness shaping. |

**Novelty/Diversity:**

| Setting | Value | Meaning |
|---------|------:|---------|
| `ENABLE_NOVELTY` | `True` | Add novelty bonus to fitness before shaping. |
| `ENABLE_DIVERSITY` | `True` | Add reward-diversity bonus to fitness before shaping. |
| `NOVELTY_WEIGHT` | `0.1` | Novelty bonus coefficient (scaled by fitness_std). |
| `DIVERSITY_WEIGHT` | `0.1` | Diversity bonus coefficient (scaled by fitness_std). |

### ES Algorithm Components (Implemented)

| Component | File | Granular Behavior |
|-----------|------|-------------------|
| Sampling | `driver.py:ESDriver.sample_population()` | Generates Gaussian perturbations; if antithetic, uses `epsilon` and `-epsilon` pairs. Injects elite if enabled. |
| Gradient update | `driver.py:ESDriver.update()` | Applies rank transformation, computes `grad = (1/(N*sigma)) * sum(utility * epsilon)`, updates via AdamW or SGD. |
| AdamW optimizer | `driver.py:ESDriver._adamw_update()` | Momentum + adaptive per-parameter LR + decoupled weight decay. |
| Elitism | `driver.py:ESDriver` | Tracks best-ever candidate, injects into population, pulls mean when stagnating. |
| Fitness shaping | `fitness_shaping.py:rank_transformation()` | OpenAI ES-style rank transformation: `u = max(0, log(N/2+1) - log(rank))`, normalized. |
| Sigma decay | `driver.py:ESDriver._decay_sigma()` | `sigma <- max(sigma * decay, sigma_min)` with adaptive acceleration when stagnating. |
| Elite pull | `driver.py:ESDriver._apply_elite_pull()` | Pulls mean toward best-ever candidate when stagnation exceeds patience. |

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

### Reward Preset (Implemented)

- Default reward preset is rebalanced so no single component dominates total fitness:
  - `VelocitySurvivalBonus(reward_multiplier=1.5, max_velocity_cap=15.0)`
  - `DistanceBasedKillReward(max_reward_per_kill=18.0, min_reward_fraction=0.15)`
  - `ConservingAmmoBonus(hit_bonus=4.0, shot_penalty=-2.0)`
  - `ExplorationBonus(grid_rows=3, grid_cols=4, bonus_per_cell=5.0)`
  - `DeathPenalty(penalty=-150.0, early_death_scale=1.0)` with max time derived from `max_steps * frame_delay`
- `create_reward_calculator(max_steps, frame_delay)` now passes `max_time_alive` into `DeathPenalty` for early-death scaling.

### Action Mapping (Implemented)

- Signed turn control: `ActionInterface` converts `action[0]` into a signed turn value (`turn_value = action[0] * 2 - 1`) with a deadzone; left if `< -0.4`, right if `> 0.4`.
- Thrust and shoot remain thresholded at `> 0.5` for `action[1]` and `action[2]`.

**Best Candidate Tracking (Implemented)**

- `training/scripts/train_es.py` now stores the actual best candidate parameter vector (`best_candidate`) rather than the distribution mean.
- The best candidate is the parameter vector that achieved the highest fitness during evaluation.
- This ensures playback shows the true best-performing policy, not the distribution center.
- Also tracks `best_generation` for reference.

**Per-candidate averaged metrics**

Same as GA:
- Fitness, steps_survived, kills, shots_fired, accuracy
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
- `sigma`: Current noise scale (decays over time).
- `learning_rate`: Current learning rate.
- `gradient_norm`: L2 norm of the gradient estimate.
- `mean_param_norm`: L2 norm of the mean parameter vector.
- `avg_novelty`: Average raw novelty score across population.
- `avg_novelty_bonus`: Average scaled novelty bonus added to fitness.
- `avg_diversity`: Average raw diversity score across population.
- `avg_diversity_bonus`: Average scaled diversity bonus added to fitness.
- `fitness_scale_used`: The fitness standard deviation used for scaling bonuses.
- `archive_size`: Current size of the behavior archive.
- `best_ever_fitness`: Best fitness achieved across all generations.
- `best_ever_generation`: Generation that achieved the best-ever fitness.
- `generations_since_improvement`: Stagnation counter.
- `elite_injected`: Whether elite was injected this generation.
- `elite_pull_applied`: Whether elite pull was triggered this generation.
- `elite_pull_distance`: Distance from mean to elite when pull was applied.
- `adaptive_sigma_triggered`: Whether adaptive sigma decay was triggered.
- `adam_t`: AdamW optimizer timestep (for bias correction).

### Fresh-Game Generalization (Implemented)

- Same infrastructure as GA via `DisplayManager.start_display(...)`.
- Best candidate of each generation is displayed in the windowed game.
- Fresh-game metrics and generalization ratios are recorded via `TrainingAnalytics.record_fresh_game(...)`.

## Implemented Outputs / Artifacts (if applicable)

- `training_summary_es.md`: Markdown report generated by ES training, containing run summary metrics and a config section populated from `TrainingAnalytics.set_config(...)` at runtime.
- `training_data_es.json`: JSON export with schema, config, and per-generation data.

## In Progress / Partially Implemented

- [ ] ES-specific report sections: Analytics records ES metrics (`sigma`, `gradient_norm`, etc.) but the markdown report doesn't have dedicated sections for them.
- [ ] TensorFlow ES pipeline usage decision: TF policy/evaluator exist but are not invoked by `training/scripts/train_es.py`, leaving two ES stacks (NumPy-wired vs TF-unused).

## Planned / Missing / To Be Changed

- [ ] Add validation seed set: Re-evaluate candidate policies on a held-out seed set before labeling them as best-of-run.
- [ ] Ray-danger avoidance shaping (shared): Add a reward component that penalizes time spent with dangerous ray hits (e.g., min ray distance below a threshold) and rewards increasing clearance while under threat.
- [ ] Aim-alignment reward (shared): Add a reward component that pays per-second based on how "front-aligned" the nearest asteroid is (e.g., highest reward when a threat is on the front ray, decaying to ~0 toward rear rays) to incentivize deliberate aiming.
- [ ] Output saturation penalty (shared): Penalize sustained saturated NN outputs (especially near-constant shoot output) using existing `output_saturation` metrics to discourage degenerate always-on control signals.
- [ ] Natural Evolution Strategies (NES): Implement fitness-weighted covariance adaptation for more sophisticated exploration.
- [ ] Perception upgrade (shared): Increase `HybridEncoder.num_rays` (e.g., 16 -> 32) and include rear/side coverage rays to reduce blind-spot exploitation.
- [ ] Predictive ray features (shared): Add per-ray time-to-collision (TTC) or closing-speed features for imminent-threat detection without changing the ES algorithm itself.
- [ ] Checkpointing: Save/load ES state (mean vector, sigma, best_candidate, adam_m, adam_v) for resuming training.
- [ ] Comparative analysis tools: Side-by-side GA vs ES metric visualizations.
- [ ] ES-specific markdown report sections: Dedicated visualization for sigma decay curve, elite tracking, and AdamW statistics.

## Implementation Details

### ES Algorithm Overview

```
Initialize:
  theta = zeros(param_size) # Mean parameter vector
  sigma = initial_sigma     # Exploration noise
  m = zeros(param_size)     # AdamW first moment
  v = zeros(param_size)     # AdamW second moment
  elite = None              # Best-ever candidate

For each generation:
    1. Sample: Generate N-1 noise vectors epsilon_i ~ N(0, I)
       If antithetic: use epsilon and -epsilon pairs
       If elitism enabled: inject elite as Nth candidate

    2. Perturb: Create candidates theta_i = theta + sigma * epsilon_i

    3. Evaluate: F_i = evaluate(theta_i) averaged over common seeds (CRN)

    4. Update elite: If best F_i > elite_fitness, store that candidate

    5. Shape: Transform F_i to utilities u_i via rank transformation

    6. Gradient: grad = (1/(N*sigma)) * sum(u_i * epsilon_i)

    7. AdamW Update:
       m = beta1*m + (1-beta1)*grad
       v = beta2*v + (1-beta2)*grad^2
       theta = theta*(1-lr*weight_decay) + lr * m_hat/(sqrt(v_hat) + adam_eps)

    8. Elite Pull: If stagnating, pull theta toward elite

    9. Sigma Decay: sigma <- max(sigma * decay * adaptive_factor, sigma_min)
```

### Key Differences from GA

| Aspect | GA | ES |
|--------|----|----|
| Representation | Population of individuals | Single mean + noise samples |
| Selection | Tournament on combined score | Implicit via weighted update |
| Crossover | BLX-alpha blending | None (gradient-based) |
| Mutation | Per-gene Gaussian noise | Global perturbation sampling |
| Elitism | Preserve top 10% | Best-ever injection + mean pull |
| Optimizer | N/A (direct replacement) | AdamW (momentum + adaptive LR) |
| Update rule | Replace population | Gradient step on mean |
| Sigma schedule | N/A | Adaptive decay based on stagnation |
| Framework (current wiring) | NumPy | NumPy |

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

## Notes / Design Considerations (optional)

- **CRN implementation rationale**: ES gradient estimation is highly sensitive to evaluation noise. With CRN (`use_common_seeds=True`), all candidates see identical environments, so fitness differences purely reflect parameter quality. The seed set changes across generations to maintain generalization pressure. This is critical for ES but less important for GA (which uses tournament selection + elitism for noise tolerance).
- **Antithetic sampling with CRN**: The `+epsilon`/`-epsilon` variance reduction technique now works correctly because paired perturbations see identical rollout randomness.
- **Best candidate vs mean**: ES now stores the actual best-performing candidate weights for playback, not the distribution mean. The mean is a smoothed estimate that was never directly evaluated, so using it for "best policy" was misleading.
- **Turn direction metrics**: The evaluator now tracks `left_only_frames`, `right_only_frames`, and `both_turn_frames` separately. This allows diagnosing whether agents are spinning in one direction, alternating intelligently, or pressing both turn keys (which cancel out to ~0 rotation).
- **Novelty/diversity scaling for rank transformation**: ES applies novelty/diversity bonuses pre-rank-shaping. Since rank transformation discards magnitude information, the bonuses are now scaled by `fitness_std` (with a floor of 10.0) to ensure they meaningfully affect rankings. With typical fitness std of ~150-200, a novelty score of 0.3 with weight 0.1 adds ~5-6 to fitness (enough to shift a few rankings).
- Action discontinuity: `interfaces/ActionInterface.py` thresholds outputs at `0.5`, creating a piecewise-constant policy mapping that makes the fitness landscape jagged for ES-style updates.
- Sample budget comparability: ES "one generation" can cost far more rollouts than GA (population * seeds per candidate), so wall-clock comparisons should be normalized by total episodes evaluated.
- Fitness shaping role: Rank transformation reduces sensitivity to outliers and keeps update scales stable across generations.
- Regularization role: Weight decay limits parameter blow-up; sigma decay (with a floor) prevents perpetual over-exploration while retaining adaptability.
- TensorFlow stack status: A TF policy/evaluator exists but is not currently used by the ES training entry point; the canonical ES execution path today is NumPy-based.

## Discarded / Obsolete / No Longer Relevant

- TensorFlow-only ES documentation: Earlier documentation treated ES as TensorFlow-first; the current wired training path uses the shared NumPy policy/evaluator, and TF components are present but unused.
