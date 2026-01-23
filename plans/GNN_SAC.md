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
| GNN-SAC training method | Implemented (MVP) | `training/scripts/train_gnn_sac.py` drives collection + updates using `training/methods/sac/*`. |
| Graph state encoder | Implemented | `interfaces/encoders/GraphEncoder.py` emits `GraphPayload` with wrapped deltas. |
| RL agent wrapper for playback | Implemented | `ai_agents/reinforcement_learning/sac_agent.py` provides inference wrapper. |
| Continuous (analog) game control | Implemented | `continuous_control_mode` + `Player.apply_continuous_controls(...)` in windowed + headless. |
| PyTorch / PyG dependencies | Not implemented | Repo has no pinned dependency file for RL. |

### Implemented Components (MVP)

- Graph encoder: `interfaces/encoders/GraphEncoder.py` produces a framework-agnostic `GraphPayload`.
- Continuous control path: `continuous_control_mode`, `turn_magnitude`, `thrust_magnitude`, and `shoot_requested` are respected in both game modes.
- GNN backbone + policy/value networks: `training/methods/sac/networks.py` provides `GNNBackbone`, `Actor`, and `TwinCritics`.
- PyTorch + PyG backbone: `GNNBackbone` uses `torch_geometric.nn.GATv2Conv` for message passing.
- Replay buffer: `training/methods/sac/replay_buffer.py` stores graph transitions and collates batches.
- SAC learner: `training/methods/sac/learner.py` performs critic, actor, and entropy updates with target critics.
- Training loop: `training/scripts/train_gnn_sac.py` runs step-based collection + updates and logs analytics.
- Best-so-far evaluation: fixed-seed headless evaluation drives `best_sac.pt` checkpoint updates.
- Playback agent: `ai_agents/reinforcement_learning/sac_agent.py` enables deterministic inference.
- Viewer: `training/scripts/view_gnn_sac.py` replays the best checkpoint continuously in the windowed game.
- Viewer seeds: `SACConfig.VIEWER_SEED_MODE` drives per-episode seed changes for non-repetitive playback.
- Single-process simulator: `training/scripts/simulate_gnn_sac.py` trains headless and replays the best snapshot in one windowed run.
- Observation normalization: `training/methods/sac/normalization.py` tracks running stats for graph features and normalizes in the learner.
- Reward scaling: `SACConfig.REWARD_SCALE` scales step and terminal rewards before replay storage and logging.
- Action smoothing: `SACConfig.ACTION_SMOOTHING_*` optionally applies EMA smoothing to actions in training/eval/playback.
- Adaptive gradient clipping: `SACLearner` optionally scales per-parameter gradients using AGC before global clipping.
- Huber critic loss: `SACConfig.CRITIC_LOSS="huber"` reduces sensitivity to TD-error outliers vs pure MSE.
- Parallel collectors: `SACConfig.NUM_COLLECTORS` runs multiple headless games in the training loop for broader data coverage.
- Held-out evaluation: `SACConfig.HOLDOUT_EVAL_SEEDS` enables periodic evaluation on a separate seed set.

### Existing Infrastructure We Will Reuse (Implemented)

| Component | File | Granular Responsibility |
|---|---|---|
| Headless simulation | `game/headless_game.py` | Fast deterministic rollouts via per-instance RNG (seeded `random.Random`). |
| Windowed simulation | `Asteroids.py` | Rendered gameplay and training playback. |
| State encoder contract | `interfaces/StateEncoder.py` | Allows encoders to return `Any` (not limited to fixed-size vectors). |
| Environment queries | `interfaces/EnvironmentTracker.py` | Provides access to player/asteroids and wrapped distance utilities (note: `get_tick()` is currently broken/unused). |
| Reward composition | `interfaces/RewardCalculator.py` + `training/config/rewards.py` | Training uses an external reward calculator preset for comparability across methods. |
| Metrics | `interfaces/MetricsTracker.py` | Tracks shots/hits/kills/time_alive for evaluation and analytics. |
| Action boundary (current) | `interfaces/ActionInterface.py` | Validates/normalizes actions and now supports **continuous** mapping via `to_game_input_continuous(...)`. |
| Episode stepping helper | `training/core/episode_runner.py` | Runs step-based episodes with `state_encoder -> agent -> action_interface -> game` loop. |
| Parallel evaluator pattern | `training/core/population_evaluator.py` | Demonstrates step loop, per-step reward, and rich behavioral metric extraction. |
| Playback + generalization capture | `training/core/display_manager.py` | Plays best policy in a “fresh game” and records generalization metrics. |
| Analytics pipeline | `training/analytics/*` | Writes `training_data_*.json` and `training_summary_*.md` with extensive metrics. |

### Diagnostics & Analytics (Implemented)

- SAC reporting interval: Uses `TrainingAnalytics.record_generation(...)` to log RL metrics on a fixed step interval.
- SAC timebase keys: Records `sac_env_steps_total` and `sac_updates_total` each interval for a true RL timebase.
- Held-out eval metrics: `sac_eval_holdout_*` keys record validation returns on `HOLDOUT_EVAL_SEEDS` when configured.
- Action health diagnostics: Logs turn/thrust/shoot mean/std and saturation/zero rates to detect control collapse.
- Learner stability diagnostics: Logs critic/actor loss, TD-error tails, Q/target-Q stats, and gradient/clip rates.
- Replay/data health diagnostics: Logs replay size, episode length distribution, and step/terminal reward stats.
- Representation health diagnostics: Logs embedding norm/std/cosine similarity to detect collapse.
- Drift diagnostics: Logs probe-set policy drift and critic/target gap to detect local minima or instability.
- Weight snapshots: Logs mean/std/norm/zero-fraction for GNN/actor/critic weights per interval.

## Implemented Outputs / Artifacts (if applicable)

- `training_summary_sac.md`: Markdown report generated by GNN-SAC training via `TrainingAnalytics.generate_markdown_report(...)`.
- `training_data_sac.json`: JSON export generated by GNN-SAC training via `TrainingAnalytics.save_json(...)`.
- `training/sac_checkpoints/best_sac.pt`: Best-so-far checkpoint containing GNN + actor weights and eval metadata.


## In Progress / Partially Implemented

- [ ] Dependency manifest missing: No `requirements-rl.txt`/`pyproject` extras to pin PyTorch/PyG.
- [ ] Checkpointing/resume: GNN-SAC training does not yet save/load optimizer or replay state.
- [ ] `interfaces/EnvironmentTracker.get_tick()` references `game.time`, but game objects do not define `time`; this is unused/broken and blocks any RL code that relies on 'tick'.

## Planned / Missing / To Be Changed


### C. Model Architecture (GNN + SAC)

#### C1. GNN Backbone (Remaining)

- [ ] Keep backbone swappable via config:
  - `GNN_BACKBONE = transformerconv | gatv2 | ...`
  - `NUM_LAYERS`, `HIDDEN_DIM`, `DROPOUT`

### D. Training System (Collector + Replay + Learner)

#### D4. Evaluation, Playback, and Analytics Parity (Remaining)

- [ ] Use `training/core/display_manager.py` infrastructure for 'fresh-game' playback and generalization capture.

### E. File & Module Layout (Implemented)

Current directories (aligned with existing repo layout):

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
      normalization.py           # Running graph feature normalization
      replay_buffer.py           # Graph-native replay
      learner.py                 # SAC losses + optimizers + target updates
  scripts/
    train_gnn_sac.py             # Collector + trainer loop entrypoint
    view_gnn_sac.py              # Windowed playback for best-so-far SAC agent
    simulate_gnn_sac.py          # Single-process training + playback
```

### F. Performance / “Pro-Level” Improvement Roadmap (Planned)

These are concrete upgrades we expect to matter for “rival strong human players” performance.

#### F1. Environment Fidelity & Control (High Leverage)

- [ ] Optional “shoot gating” heuristics for evaluation-only playback (kept off during training unless explicitly enabled).

#### F3. Sample Efficiency & Scaling (Medium/High)

- [ ] Prioritized replay (PER) as an optional module.
- [ ] n-step returns as an optional module.
- [ ] REDQ-style ensembles (optional, later).

#### F4. Representation Upgrades (Medium)

- [ ] Add bullets as nodes (optional) once asteroid-only baseline is stable.
- [ ] Add kNN asteroid↔asteroid edges (optional) if multi-asteroid interaction prediction improves dodging.
- [ ] Add explicit TTC edge attribute (optional) if learned avoidance is unstable.

#### F5. Adaptive Training Controls (Planned)

These items turn fixed SAC knobs into **data-driven / schedule-driven** knobs. Each is intended to be:

- Logged every interval (so runs remain interpretable).
- Deterministic given a seed + config (no hidden randomness).
- Disable-able (true ablation).

**Learning & optimization adaptivity**

- [ ] Adaptive actor LR scheduler: adjust `ACTOR_LR` using a schedule (e.g., plateau on eval return or actor-loss stability).
- [ ] Adaptive critic LR scheduler: adjust `CRITIC_LR` using a schedule (e.g., plateau on TD-error tails or critic-loss stability).
- [ ] Adaptive alpha LR scheduler: adjust `ALPHA_LR` when entropy tuning oscillates (alpha volatility thresholds).
- [ ] Adaptive update ratio: adjust `UPDATES_PER_STEP` to target a stable update/data ratio as replay grows.
- [ ] Adaptive gradient clipping: adjust `GRAD_CLIP_NORM` when clip rate or grad norms are persistently unhealthy.

**Exploration / policy output adaptivity**

- [ ] Adaptive target entropy schedule: schedule `TARGET_ENTROPY` from exploratory early training to more deterministic late training.
- [ ] Adaptive action smoothing alpha: adjust `ACTION_SMOOTHING_ALPHA` based on oscillation proxies (turn switches / saturation).

**Reward / value-scale adaptivity**

- [ ] Adaptive reward scaling: adapt `REWARD_SCALE` via a stable heuristic (e.g., target Q magnitude band) while keeping replay semantics consistent.

**Data collection / evaluation adaptivity**

- [ ] Adaptive collector scheduling: adjust `NUM_COLLECTORS` upward as training stabilizes to widen the state distribution.
- [ ] Adaptive evaluation cadence: adjust `EVAL_EVERY_EPISODES` (more frequent early, less frequent later) without breaking best tracking.
- [ ] Adaptive holdout evaluation policy: schedule/expand/rotate `HOLDOUT_EVAL_SEEDS` while logging the exact seed set used per eval.

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
| Critic LR | `CRITIC_LR` | `1e-4` | Critic optimizer step size. |
| Alpha LR | `ALPHA_LR` | `3e-4` | Entropy temperature LR (auto-tuning). |
| Entropy | `TARGET_ENTROPY` | `-(action_dim)` | Target entropy heuristic baseline. |
| Grad clip | `GRAD_CLIP_NORM` | `10.0` | Gradient norm cap (stability). |
| Reward | `REWARD_SCALE` | `0.2` | Scalar multiplier applied to all rewards. |
| Critic loss | `CRITIC_LOSS` | `huber` | TD loss type for critic updates (mse vs huber). |
| Adaptive grad clip | `AGC_ENABLED` | `True` | Per-parameter AGC before global clipping. |
| Graph cap | `MAX_ASTEROIDS` | `None` | All asteroids by default. |
| Device | `DEVICE` | `cuda` if available | Training device selection. |

### Debugging & Sanity Checklist (First-Time GNN + SAC)

These are concrete checks to run before “tuning for performance”.

#### Environment + control parity

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
