# Evolution Strategies (ES)

## Scope / Purpose

Evolution Strategies (ES) is the second optimization method implemented in AsteroidsAI. Its purpose is to benchmark a distribution-based, gradient-estimation approach against the GA while reusing the same environment, state/action interfaces, reward components, and analytics outputs for fair comparison.

ES maintains a probability distribution over parameter space (Gaussian with mean θ and stddev σ) and iteratively updates the distribution mean by estimating the gradient of expected fitness through sampling. This contrasts with GA's selection/crossover/mutation approach.

## Current Implemented System

### ES Method Implementation Status (Implemented)

| Component | File | Status |
|-----------|------|--------|
| Configuration | `training/config/evolution_strategies.py` | Implemented |
| Driver | `training/methods/evolution_strategies/driver.py` | Implemented |
| Fitness Shaping | `training/methods/evolution_strategies/fitness_shaping.py` | Implemented |
| Training Script | `training/scripts/train_es.py` | Implemented |
| TensorFlow Policy | `ai_agents/policies/feedforward_tf.py` | Implemented |
| TensorFlow Agent | `ai_agents/neuroevolution/nn_agent_tf.py` | Implemented |
| TensorFlow Evaluator | `training/core/population_evaluator_tf.py` | Implemented |

### Entry Point & Orchestration (Implemented)

| Component | File | Granular Responsibility |
|-----------|------|-------------------------|
| Training script | `training/scripts/train_es.py` | Creates encoder/action/reward/driver/analytics/display stack and runs the sample → evaluate → display → update loop. |
| TensorFlow evaluator | `training/core/population_evaluator_tf.py` | Runs seeded headless rollouts in parallel using `NNAgentTF` (TensorFlow). |
| Driver (ES logic) | `training/methods/evolution_strategies/driver.py` | Maintains mean vector, samples perturbations, computes gradient updates. |
| Playback + generalization | `training/core/display_manager.py` | Runs best candidate in windowed "fresh game" (shared with GA). |

### Policy Representation (Implemented)

| Concept | Implementation | Details |
|---------|----------------|---------|
| Mean vector | `np.ndarray` | Flat parameter vector representing all weights and biases (center of search distribution). |
| Policy | `ai_agents/policies/feedforward_tf.py:FeedforwardPolicyTF` | TensorFlow Keras MLP with `tanh` hidden activation and `sigmoid` outputs. |
| Agent wrapper | `ai_agents/neuroevolution/nn_agent_tf.py:NNAgentTF` | Implements `BaseAgent`, builds `FeedforwardPolicyTF` using `state_encoder.get_state_size()` as input size. |

**Parameter count (fixed topology, same as GA)**

- Formula: `input*hidden + hidden + hidden*output + output`.
- Current default sizes:
  - Input: `HybridEncoder.get_state_size() = 31`
  - Hidden: `ESConfig.HIDDEN_LAYER_SIZE = 24`
  - Output: `4`
  - Parameter count: `31*24 + 24 + 24*4 + 4 = 868`

### ES Hyperparameters (Implemented)

From `training/config/evolution_strategies.py:ESConfig`:

| Setting | Value | Meaning |
|---------|------:|---------|
| `POPULATION_SIZE` | `50` | Number of perturbations per generation. |
| `NUM_GENERATIONS` | `500` | Total generations in a run. |
| `SIGMA` | `0.1` | Initial noise standard deviation. |
| `LEARNING_RATE` | `0.01` | Step size for mean updates. |
| `SEEDS_PER_AGENT` | `5` | Headless rollouts per candidate (fitness averaged). |
| `MAX_STEPS` | `1500` | Step limit per rollout/playback. |
| `FRAME_DELAY` | `1/60` | Fixed time step for evaluation and playback. |
| `HIDDEN_LAYER_SIZE` | `24` | Hidden units in the MLP (matches GA). |
| `USE_ANTITHETIC` | `True` | Use mirrored sampling (ε and -ε pairs). |
| `USE_RANK_TRANSFORMATION` | `True` | Apply rank-based fitness shaping. |
| `WEIGHT_DECAY` | `0.005` | L2 regularization coefficient. |
| `SIGMA_DECAY` | `0.999` | Per-generation sigma decay factor. |
| `SIGMA_MIN` | `0.01` | Minimum sigma floor. |

### ES Algorithm Components (Implemented)

| Component | File | Granular Behavior |
|-----------|------|-------------------|
| Sampling | `driver.py:ESDriver.sample_population()` | Generates Gaussian perturbations; if antithetic, uses ε and -ε pairs. |
| Gradient update | `driver.py:ESDriver.update()` | Applies rank transformation, computes `grad = (1/Nσ) * Σ utility * ε`, updates `θ ← θ + α * grad`. |
| Fitness shaping | `fitness_shaping.py:rank_transformation()` | OpenAI ES-style rank transformation: `u = max(0, log(N/2+1) - log(rank))`, normalized. |
| Sigma decay | `driver.py:ESDriver._decay_sigma()` | `σ ← max(σ * decay, σ_min)` after each generation. |
| Weight decay | `driver.py:ESDriver.update()` | `θ ← θ * (1 - weight_decay)` for L2 regularization. |

### Evaluation Loop (Implemented)

**Parallel rollouts (TensorFlow)**

- `evaluate_population_parallel_tf(...)` evaluates each candidate on `SEEDS_PER_AGENT` deterministic seeds using `HeadlessAsteroidsGame(random_seed=...)`.
- Uses `NNAgentTF` with TensorFlow `FeedforwardPolicyTF` for forward passes.
- Rollouts are executed concurrently via `ThreadPoolExecutor(max_workers=os.cpu_count())`.
- Returns same metrics structure as GA evaluator for analytics compatibility.

**Per-candidate averaged metrics**

Same as GA:
- Fitness, steps_survived, kills, shots_fired, accuracy
- thrust_frames, turn_frames, shoot_frames, idle_rate
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

### Fresh-Game Generalization (Implemented)

- Same infrastructure as GA via `DisplayManager.start_display(...)`.
- Best candidate of each generation is displayed in the windowed game.
- Fresh-game metrics and generalization ratios are recorded via `TrainingAnalytics.record_fresh_game(...)`.

## Implemented Outputs / Artifacts (if applicable)

- `training_summary_es.md`: Markdown report generated by ES training.
- `training_data_es.json`: JSON export with schema, config, and per-generation data.

## In Progress / Partially Implemented

- [ ] Novelty/diversity integration: ES supports `ENABLE_NOVELTY` and `ENABLE_DIVERSITY` config flags, but they are disabled by default and not fully tested.
- [ ] ES-specific report sections: Analytics records ES metrics (`sigma`, `gradient_norm`, etc.) but the markdown report doesn't have dedicated sections for them.

## Planned / Missing / To Be Changed

- [ ] Adaptive learning rate: Implement learning rate scheduling or adaptive step sizes based on fitness improvement.
- [ ] Natural Evolution Strategies (NES): Implement fitness-weighted covariance adaptation for more sophisticated exploration.
- [ ] Adam-style momentum: Add momentum terms to the gradient update for smoother optimization.
- [ ] Checkpointing: Save/load ES state (mean vector, sigma) for resuming training.
- [ ] Comparative analysis tools: Side-by-side GA vs ES metric visualizations.

## Implementation Details

### ES Algorithm Overview

```
Initialize: θ = zeros(param_size), σ = initial_sigma

For each generation:
    1. Sample: Generate N noise vectors ε_i ~ N(0, I)
       If antithetic: use ε and -ε pairs

    2. Perturb: Create candidates θ_i = θ + σ * ε_i

    3. Evaluate: F_i = evaluate(θ_i) averaged over multiple seeds

    4. Shape: Transform F_i to utilities u_i via rank transformation

    5. Update: θ ← θ + α * (1/Nσ) * Σ u_i * ε_i

    6. Decay: σ ← max(σ * decay, σ_min)
```

### Key Differences from GA

| Aspect | GA | ES |
|--------|----|----|
| Representation | Population of individuals | Single mean + noise samples |
| Selection | Tournament on combined score | Implicit via weighted update |
| Crossover | BLX-alpha blending | None (gradient-based) |
| Mutation | Per-gene Gaussian noise | Global perturbation sampling |
| Elitism | Preserve top 10% | Mean naturally preserved |
| Update rule | Replace population | Gradient step on mean |
| Framework | NumPy | TensorFlow |

### File Structure (Implemented)

```
ai_agents/
├── neuroevolution/
│   └── nn_agent_tf.py              # TensorFlow agent wrapper
└── policies/
    └── feedforward_tf.py           # TensorFlow Keras policy

training/
├── config/
│   └── evolution_strategies.py     # ESConfig class
├── core/
│   └── population_evaluator_tf.py  # TensorFlow parallel evaluator
├── methods/
│   └── evolution_strategies/
│       ├── __init__.py
│       ├── driver.py               # ESDriver class
│       └── fitness_shaping.py      # Rank transformation utilities
└── scripts/
    └── train_es.py                 # ES training entry point
```

## Notes / Design Considerations (optional)

- ES uses TensorFlow while GA uses NumPy. This was a deliberate choice for learning purposes and CV value, though both could theoretically use either framework.
- The TensorFlow overhead is negligible for this network size (868 params) - the game simulation is the bottleneck.
- Antithetic sampling (mirrored noise) is enabled by default as it significantly reduces gradient variance with minimal overhead.
- Rank-based fitness shaping is critical for ES stability - raw fitness values can cause erratic updates.
- Unlike GA, ES has no explicit elitism, but the mean is naturally preserved and refined across generations.
- Sigma decay prevents over-exploration in later generations but has a floor (`SIGMA_MIN`) to maintain adaptability.
- Weight decay provides mild regularization and prevents parameter blow-up in long runs.

## Discarded / Obsolete / No Longer Relevant

- Pure NumPy ES implementation: Originally considered using NumPy for fair comparison with GA, but TensorFlow was chosen for learning value and future extensibility.
- Shared evaluator: A unified evaluator was considered but separate evaluators (`population_evaluator.py` for GA, `population_evaluator_tf.py` for ES) were implemented for clarity and to allow framework-specific optimizations.
