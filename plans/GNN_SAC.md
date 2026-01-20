# Graph Neural Network + Soft Actor-Critic (GNN-SAC)

## Scope / Purpose

This plan defines the **Graph Neural Network (GNN) + Soft Actor-Critic (SAC)** Reinforcement Learning method for AsteroidsAI.

Its purpose is to provide a **gold-standard, real continuous-control RL agent** that:

- Uses **variable-cardinality perception** (a graph that grows/shrinks with the number of entities).
- Uses **true continuous actuation** (analog turning and thrust) so SAC optimizes a smooth control problem (not thresholded key presses).
- Handles **toroidal wrapping** correctly so “near across an edge” is represented as near.
- Reuses the existing environment/reward/analytics infrastructure so performance is **comparable** to GA/ES/NEAT.

---

## Current Implemented System

### RL Subsystem Status (Implemented)

| Area | Status | Notes |
|---|---|---|
| GNN-SAC training method | Not implemented | No `training/methods/sac/` exists. |
| Graph state encoder | Not implemented | No graph encoder exists under `interfaces/encoders/`. |
| RL agent wrapper for playback | Not implemented | `ai_agents/reinforcement_learning/` exists but is empty. |
| Continuous (analog) game control | Not implemented | Game currently applies **boolean** inputs only (fixed-step rotation/thrust). |
| PyTorch / PyG dependencies | Not implemented | Repo has no pinned dependency file for RL. |

### Existing Infrastructure We Will Reuse (Implemented)

| Component | File | Granular Responsibility |
|---|---|---|
| Headless simulation | `game/headless_game.py` | Fast deterministic rollouts via per-instance RNG (seeded `random.Random`). |
| Windowed simulation | `Asteroids.py` | Rendered gameplay and training playback. |
| State encoder contract | `interfaces/StateEncoder.py` | Allows encoders to return `Any` (not limited to fixed-size vectors). |
| Environment queries | `interfaces/EnvironmentTracker.py` | Provides access to player/asteroids and wrapped distance utilities (note: `get_tick()` is currently broken/unused). |
| Reward composition | `interfaces/RewardCalculator.py` + `training/config/rewards.py` | Training uses an external reward calculator preset for comparability across methods. |
| Metrics | `interfaces/MetricsTracker.py` | Tracks shots/hits/kills/time_alive for evaluation and analytics. |
| Action boundary (current) | `interfaces/ActionInterface.py` | Validates/normalizes action vectors but currently converts to **boolean** inputs via thresholding. |
| Episode stepping helper | `training/core/episode_runner.py` | Runs step-based episodes with `state_encoder -> agent -> action_interface -> game` loop. |
| Parallel evaluator pattern | `training/core/population_evaluator.py` | Demonstrates step loop, per-step reward, and rich behavioral metric extraction. |
| Playback + generalization capture | `training/core/display_manager.py` | Plays best policy in a “fresh game” and records generalization metrics. |
| Analytics pipeline | `training/analytics/*` | Writes `training_data_*.json` and `training_summary_*.md` with extensive metrics. |

## Implemented Outputs / Artifacts (if applicable)

- No GNN-SAC artifacts are produced yet (no RL run outputs exist).

## In Progress / Partially Implemented

- [ ] `ai_agents/reinforcement_learning/` folder exists but contains no RL agents; it is currently an empty placeholder.
- [ ] `interfaces/ActionInterface(action_space_type="continuous")` exists but still thresholds to booleans; it is not a true continuous-control path.
- [ ] `interfaces/EnvironmentTracker.get_tick()` references `game.time`, but game objects do not define `time`; this is unused/broken and blocks any RL code that relies on “tick”.

## Planned / Missing / To Be Changed

### A. Architectural Commitments (Decisions We Lock In)

#### A1. Framework & Libraries (Pinned)

- [ ] **PyTorch** is the RL framework of record for this subsystem.
- [ ] **PyTorch Geometric (PyG)** is the graph batching/message passing library of record for this subsystem.
- [ ] Keep RL deep-learning dependencies **isolated** to the RL stack (do not require PyTorch for GA/ES/NEAT runs).

#### A2. “Real SAC” Action Semantics (True Continuous Control)

We will implement **analog actuation** in the game loop so SAC optimizes the control problem it is designed for.

- [ ] Add analog turning:
  - The policy outputs `turn_value ∈ [-1, 1]` each step.
  - The environment applies `angle += rotation_speed * turn_value` (scaled by `delta_time` if enabled).
- [ ] Add analog thrust:
  - The policy outputs `thrust_value ∈ [0, 1]` each step.
  - The environment applies `velocity += acceleration * thrust_value * facing_dir` (scaled by `delta_time` if enabled).
- [ ] Keep shooting discrete in the simulation:
  - The policy outputs `shoot_prob ∈ [0, 1]` each step.
  - The environment fires a bullet if `shoot` is sampled True (training) or if `shoot_prob > threshold` (evaluation/playback).

Backward compatibility (non-breaking requirement):

- [ ] Boolean inputs continue to behave exactly as today:
  - `left_pressed/right_pressed` map to `turn_value = -1/+1/0`.
  - `up_pressed` maps to `thrust_value = 1/0`.
  - `space_pressed` remains a boolean fire request.

#### A3. Graph Cardinality Policy (Default: All Asteroids)

- [ ] Default: include **all asteroids** as nodes each step.
- [ ] Configurable cap: allow `MAX_ASTEROIDS = K` for experiments (e.g., K nearest by wrapped distance).
- [ ] Deterministic selection rule when capped (stable tie-breaks) so training is reproducible.

### B. Graph State Representation (Encoder Spec)

#### B1. Core Toroidal Geometry (Non-Negotiable)

All relative geometry must be computed in **wrapped coordinates** so “near across the boundary” is encoded correctly.

Wrapped delta (canonical implementation target):

```text
dx = ((ax - px + W/2) % W) - W/2
dy = ((ay - py + H/2) % H) - H/2
```

- [ ] Use wrapped `(dx, dy)` for:
  - distance
  - bearing
  - relative velocity projections
  - any future bullet/asteroid interactions

#### B2. Graph Schema (Planned)

We will encode the environment as a graph with typed nodes and edge attributes.

**Nodes**

- [ ] Player node (exactly 1):
  - Features (initial baseline):
    - `vel_x`, `vel_y` (normalized)
    - `heading_sin`, `heading_cos`
    - `shoot_cooldown_frac` (0..1)
  - Optional planned additions:
    - `angular_velocity` (requires new tracking or state in `Player`)
    - `speed`, `speed_std` (if we add running filters)

- [ ] Asteroid nodes (N, variable):
  - Features (initial baseline):
    - `radius` / `scale` (normalized)
    - `vel_x`, `vel_y` (normalized)
    - `is_fragment` / `tier_onehot` (planned)

**Edges**

- [ ] Directed bipartite edges `asteroid -> player`:
  - Edge attributes (initial baseline):
    - wrapped `dx`, wrapped `dy` (normalized by screen dims)
    - `dist` (normalized)
    - `bearing_sin`, `bearing_cos`
    - relative velocity `rel_vx`, `rel_vy` (normalized)
  - Optional planned additions:
    - time-to-collision proxy `ttc` (capped)
    - “closing speed” scalar along the bearing

Diagram (default topology):

```text
Asteroid_1  ─┐
Asteroid_2  ─┼─>  Player
...         ─┤
Asteroid_N  ─┘
```

#### B3. Encoder Output Type (Planned)

To avoid leaking PyTorch/PyG into the generic `interfaces/` layer:

- [ ] `interfaces/encoders/GraphEncoder.py` returns a lightweight, framework-agnostic payload, e.g.:
  - `node_features` (numpy/torch CPU tensors)
  - `edge_index` (COO indices)
  - `edge_attr`
  - optional masks/metadata (node counts, entity ids if introduced later)
- [ ] The RL stack converts this payload into `torch_geometric.data.Data` and `Batch` at sampling time.

### C. Model Architecture (GNN + SAC)

#### C1. GNN Backbone (Planned: Attention + Edge Attributes)

- [ ] Use an attention-based message passing layer that consumes edge attributes (PyG backbone).
- [ ] Player node acts as the readout token:
  - The player embedding after message passing becomes the global “state embedding”.
- [ ] Keep backbone swappable via config:
  - `GNN_BACKBONE = transformerconv | gatv2 | ...`
  - `NUM_LAYERS`, `HIDDEN_DIM`, `DROPOUT`

#### C2. Actor (Planned: Squashed Gaussian + Bernoulli Shoot)

- [ ] Actor head outputs:
  - `turn_mean`, `turn_log_std`  → sample `turn` via reparameterization and squash to `[-1, 1]`
  - `thrust_mean`, `thrust_log_std` → sample `thrust` and squash to `[0, 1]` (tanh then remap)
  - `shoot_logit` → sample shoot via relaxed Bernoulli during training; deterministic threshold during evaluation
- [ ] Entropy temperature `alpha` uses automatic tuning (target entropy configured).

#### C3. Critics (Planned: Twin Q Networks)

- [ ] Two Q networks (Double Q):
  - Input: `[state_embedding, turn, thrust, shoot]`
  - Output: scalar Q value
- [ ] Target critics:
  - Polyak averaging with `tau` (configurable)

### D. Training System (Collector + Replay + Learner)

#### D1. Step-Based Collection (Planned)

- [ ] Use `HeadlessAsteroidsGame` instances as data collectors (no rendering).
- [ ] Per step:
  - encode graph observation
  - sample action from actor
  - step env
  - compute reward using shared reward calculator preset
  - store transition in replay

#### D2. Replay Buffer (Planned: Graph-Native, Memory-Safe)

- [ ] Store transitions in a replay buffer that does not require pickling live PyG objects.
- [ ] Transition fields:
  - `obs_graph_payload`
  - `action` (turn, thrust, shoot)
  - `reward`
  - `next_obs_graph_payload`
  - `done`
- [ ] Sampling:
  - convert sampled payloads → PyG `Batch`
  - move to device (GPU) only at training time

#### D3. SAC Learner (Planned)

- [ ] Standard SAC update steps:
  - critic loss against Bellman target using target critics
  - actor loss maximizing `Q - alpha * log_prob`
  - alpha temperature update (optional auto-tuning)
  - target network Polyak update

#### D4. Evaluation, Playback, and Analytics Parity (Planned)

- [ ] Implement an inference-only `SACAgent` under `ai_agents/reinforcement_learning/` that:
  - loads trained weights
  - runs deterministic actions for playback (mean actions + deterministic shoot rule)
- [ ] Use `training/core/display_manager.py` infrastructure for “fresh-game” playback and generalization capture.
- [ ] Emit RL analytics outputs consistent with existing methods:
  - `training_data_sac.json`
  - `training_summary_sac.md`
- [ ] Emit RL observability metrics: Record action/embedding/learner/replay health so “stuckness” can be diagnosed from exports (no manual guessing).
- [ ] RL logging interval mapping: Reuse the existing `generations_data` schema by treating “generation” as an RL **reporting interval** (e.g., every N environment steps) and include `env_steps_total`/`updates_total` keys for a true timebase.

#### D5. RL Observability Metrics (Planned: What We Record and Why)

These metrics are recorded so we can detect common GNN+SAC failure modes (exploration collapse, embedding collapse, critic instability) directly in analytics.

**Action health (continuous-control)**

- [ ] Record mean absolute turn magnitude to detect “never turns”.
- [ ] Record turn near-zero rate to detect turn collapse.
- [ ] Record turn saturation rate to detect “always max turn”.
- [ ] Record thrust mean to detect always-on/off thrust.
- [ ] Record thrust zero rate to detect “never thrust”.
- [ ] Record thrust saturation rate to detect always-max thrust.
- [ ] Record shoot probability mean to detect shoot collapse.
- [ ] Record realized shoot rate to detect “always shoot” vs “never shoot”.
- [ ] Record policy entropy mean to detect exploration collapse.

**Embedding health (GNN representation)**

- [ ] Record embedding mean norm to detect representation scale drift.
- [ ] Record embedding per-dimension std mean to detect representation collapse (low variance).
- [ ] Record embedding cosine similarity statistics to detect “all states look the same”.

**Learner stability (SAC optimization)**

- [ ] Record critic TD loss mean to track value learning stability.
- [ ] Record actor loss mean to track policy improvement stability.
- [ ] Record alpha (temperature) value to track exploration pressure.
- [ ] Record Q-value means to detect value scale blow-ups.
- [ ] Record TD-error mean/std to detect instability vs progress.
- [ ] Record actor/critic gradient norms to detect exploding/vanishing gradients.
- [ ] Record gradient-clip hit rate to detect overly aggressive learning rates.

**Replay/data health (off-policy data quality)**

- [ ] Record replay size to make warmup/coverage visible.
- [ ] Record learn-start progress to make “not learning yet” explicit.
- [ ] Record episode length mean/p90 to track survivability distribution over time.
- [ ] Record reward mean/std to track reward scale and noise over time.

### E. Proposed File & Module Layout (Planned)

Planned directories (chosen to align with existing repo layout):

```text
ai_agents/
  reinforcement_learning/
    sac_agent.py                 # Playback/inference wrapper (BaseAgent-compatible)

interfaces/
  encoders/
    GraphEncoder.py              # EnvironmentTracker -> graph payload (framework-agnostic)

training/
  config/
    sac.py                       # SACConfig (hyperparameters, graph caps, devices)
  methods/
    sac/
      networks.py                # GNN backbone + actor + critics
      replay_buffer.py           # Graph-native replay
      learner.py                 # SAC losses + optimizers + target updates
      checkpoints.py             # Save/load for long runs (optional but recommended)
  scripts/
    train_gnn_sac.py             # Collector + trainer loop entrypoint
```

### F. Performance / “Pro-Level” Improvement Roadmap (Planned)

These are concrete upgrades we expect to matter for “rival strong human players” performance.

#### F1. Environment Fidelity & Control (High Leverage)

- [ ] Analog turn/thrust in both headless and windowed modes (parity required).
- [ ] Optional action smoothing (policy-side) to reduce oscillation without removing control authority.
- [ ] Optional “shoot gating” heuristics for evaluation-only playback (kept off during training unless explicitly enabled).

#### F2. Learning Stability (High Leverage)

- [ ] Observation normalization for node/edge features.
- [ ] Reward scaling/normalization options (logged and made explicit in run config).
- [ ] Separate held-out evaluation seed set (periodic validation).

#### F3. Sample Efficiency & Scaling (Medium/High)

- [ ] Multiple parallel collectors (vectorized envs).
- [ ] Prioritized replay (PER) as an optional module.
- [ ] n-step returns as an optional module.
- [ ] REDQ-style ensembles (optional, later).

#### F4. Representation Upgrades (Medium)

- [ ] Add bullets as nodes (optional) once asteroid-only baseline is stable.
- [ ] Add kNN asteroid↔asteroid edges (optional) if multi-asteroid interaction prediction improves dodging.
- [ ] Add explicit TTC edge attribute (optional) if learned avoidance is unstable.

### G. Dependency & Reproducibility (Planned)

- [ ] Add a pinned dependency manifest for RL (e.g., `requirements-rl.txt` or `pyproject.toml` extras):
  - `torch`
  - `torch_geometric`
  - PyG backend deps (`torch_scatter`, `torch_sparse`, etc.) as required by the chosen install method
- [ ] Record device + versions in RL analytics config output for reproducibility.

## Notes / Design Considerations (optional)

### Non-Breaking Principle (Hard Constraint)

- Existing GA/ES/NEAT training scripts must continue to run without modification.
- Continuous-control changes must be additive (boolean path preserved).

### Why Bipartite Edges First

- `asteroid -> player` edges encode “what threatens me” directly and keep message passing O(N).
- Asteroid↔asteroid edges are deferred until we can prove benefit (they add O(N²) worst-case cost unless capped).

### Why “All Asteroids” Default Still Needs a Config

- Graph cardinality affects batch size and training throughput.
- A cap provides a controlled ablation knob and a fallback when performance becomes a bottleneck.

### SAC Mental Model (What Is “The Network” vs “The Algorithm”)

SAC is the **training algorithm**; the neural networks are the **actor** and **critics** (plus target critics).

| Concept | What It Is | What Learns It | What It Does |
|---|---|---|---|
| Actor (“policy”) | Neural network | Backprop (gradient descent) | Maps observation → action distribution. |
| Critic Q1 | Neural network | Backprop | Predicts “long-term reward if we take action A in state S”. |
| Critic Q2 | Neural network | Backprop | Second independent Q to reduce overestimation bias. |
| Target critics | Neural network copies | Polyak averaging | Stabilize learning by providing slowly-changing targets. |
| SAC | Algorithm | N/A | Defines losses and update rules for actor/critics/alpha. |
| Optimizer | `Adam`/`AdamW` (planned) | N/A | Performs the parameter updates once SAC defines the gradients. |
| Replay buffer | Data store | N/A | Stores experience so training uses diverse past transitions. |

Granular implementation implications:

- [ ] Actor is a PyTorch `nn.Module` that consumes the GNN “state embedding” and outputs action distribution parameters.
- [ ] Critic is a PyTorch `nn.Module` that consumes `[state embedding + action]` and outputs a scalar.
- [ ] SAC updates are gradient-based, so the actor/critics must be differentiable modules (unlike GA/ES/NEAT update rules).

### “Stuckness” in SAC (Failure Modes + Fix Knobs)

SAC can get “stuck” for RL-specific reasons (not just classic supervised-learning local minima).

#### Exploration Collapse (policy becomes too deterministic too early)

- Symptom (granular): `shoot_prob` saturates near 0 or 1 and stays there for long windows.
- Symptom (granular): `turn_value` magnitude stays near 0 (or near max) almost always.
- Fix knob (granular): tune target entropy and alpha auto-tuning (`target_entropy`, `alpha_lr`, `alpha_init`).
- Fix knob (granular): increase warmup random steps so replay contains diverse early behaviors.
- Fix knob (granular): add optional action-noise floor for early training only (config-guarded).

#### Critic Miscalibration (actor follows a “wrong judge”)

- Symptom (granular): critic losses explode or oscillate while episode returns do not improve.
- Symptom (granular): Q-values drift to extreme magnitudes inconsistent with reward scale.
- Fix knob (granular): adjust `tau` (slower target updates) to stabilize bootstrapping.
- Fix knob (granular): reduce critic learning rate and/or add gradient clipping for critic updates.
- Fix knob (granular): increase batch size and/or decrease update-to-data ratio to reduce overfitting to recent noise.

#### Reward Scale / Composition Instability

- Symptom (granular): small code/config reward changes cause drastic policy collapse across runs.
- Symptom (granular): entropy tuning behaves erratically (alpha spikes) because reward magnitudes are too large/small.
- Fix knob (granular): explicit `REWARD_SCALE` multiplier (logged) applied to all step rewards.
- Fix knob (granular): keep reward preset shared with GA/ES/NEAT initially for comparability; introduce SAC-only shaping behind a flag.

#### Replay Quality Issues (data is too correlated or too narrow)

- Symptom (granular): training improves on training seeds but fails badly on held-out seeds.
- Symptom (granular): policy “forgets” previously learned skills as buffer composition changes.
- Fix knob (granular): increase replay capacity and delay learning start (`LEARN_START_STEPS`) until buffer is sufficiently diverse.
- Fix knob (granular): run multiple collectors with different seeds to widen the state distribution.
- Fix knob (granular): add PER as an optional module once baseline is stable.

#### GNN-Specific Optimization Issues (oversmoothing / edge-feature misuse)

- Symptom (granular): state embedding collapses (very low variance across steps) even with changing asteroid configurations.
- Symptom (granular): policy behaves as if it “ignores” distance/bearing (no improvement in dodging/aiming).
- Fix knob (granular): keep GNN shallow initially (few layers) with residual connections and normalization.
- Fix knob (granular): verify the chosen PyG layer actually consumes `edge_attr` (unit test forward pass with perturbed edge attributes).
- Fix knob (granular): add dropout and/or layer norm to prevent embedding collapse.

### Default Training Baseline (v1 “Strong Starting Point”)

This baseline is the first configuration to implement and log; tuning happens after correctness and parity are verified.

| Category | Setting | Planned Default | Meaning |
|---|---:|---:|---|
| Discounting | `GAMMA` | `0.99` | Future reward discount. |
| Target update | `TAU` | `0.005` | Polyak averaging factor. |
| Batch | `BATCH_SIZE` | `256` | Replay sample size per update. |
| Replay | `REPLAY_SIZE` | `1_000_000` | Max transitions stored. |
| Warmup | `LEARN_START_STEPS` | `10_000` | Steps before learning begins. |
| Update ratio | `UPDATES_PER_STEP` | `1` | Gradient steps per env step. |
| Actor LR | `ACTOR_LR` | `3e-4` | Actor optimizer step size. |
| Critic LR | `CRITIC_LR` | `3e-4` | Critic optimizer step size. |
| Alpha LR | `ALPHA_LR` | `3e-4` | Entropy temperature LR (auto-tuning). |
| Entropy | `TARGET_ENTROPY` | `-(action_dim)` | Target entropy heuristic baseline. |
| Grad clip | `GRAD_CLIP_NORM` | `10.0` | Gradient norm cap (stability). |
| Reward | `REWARD_SCALE` | `1.0` | Scalar multiplier applied to all rewards. |
| Graph cap | `MAX_ASTEROIDS` | `None` | All asteroids by default. |
| Device | `DEVICE` | `cuda` if available | Training device selection. |

### Debugging & Sanity Checklist (First-Time GNN + SAC)

These are concrete checks to run before “tuning for performance”.

#### Environment + control parity

- [ ] Check (granular): analog turn/thrust produces identical behavior in windowed vs headless for the same action stream.
- [ ] Check (granular): boolean action path remains identical for GA/ES/NEAT (no regression).

#### Graph encoding correctness

- [ ] Check (granular): wrapped delta `(dx, dy)` is small when player and asteroid are near across screen edges.
- [ ] Check (granular): edge attributes change continuously as asteroids move (no discontinuities at wrap boundary).
- [ ] Check (granular): `MAX_ASTEROIDS=K` selection is deterministic and stable under ties.

#### SAC learning health

- [ ] Check (granular): critic losses decrease from initial values under a fixed seed run.
- [ ] Check (granular): Q-value magnitudes stay within a plausible band given observed reward scale.
- [ ] Check (granular): action entropy does not collapse immediately (alpha auto-tuning behaves smoothly).
- [ ] Check (granular): evaluation on held-out seeds improves over time, not only on training seeds.

## Discarded / Obsolete / No Longer Relevant

- PPO as the initial method: discarded for now because it is on-policy and less sample-efficient for long-horizon tuning in this environment.
- Fixed-size vector (MLP-only) as the primary RL perception: not the target here because it reintroduces padding/masking or lossy selection of entities.
