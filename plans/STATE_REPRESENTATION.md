# State Representation & Encoders

## Scope / Purpose

State representation defines the information boundary between the game simulation and any AI method. Its purpose is to provide **stable, comparable, and swappable** encodings of the current Asteroids world so different training paradigms (GA, future ES, future NEAT, etc.) can be evaluated fairly under the same physics and reward rules.

## Current Implemented System

### Encoder Contract (`interfaces/StateEncoder.py`)

| Method                        | Return                          | Responsibility                                                           |
| ----------------------------- | ------------------------------- | ------------------------------------------------------------------------ |
| `encode(environment_tracker)` | `Any` (currently `List[float]`) | Produce a method-ready state representation from tracked game state.     |
| `get_state_size()`            | `int`                           | Report the fixed input size required by the current encoding.            |
| `reset()`                     | `None`                          | Reset any encoder internal state (buffers, history, RNG, etc.).          |
| `clone()`                     | `StateEncoder`                  | Provide a fresh copy for parallel rollouts (avoid shared mutable state). |

### Implemented Encoders (`interfaces/encoders/`)

| Encoder                | File                                           |                       Output Size (Default) | Used By (Current)                                            | Purpose                                                                                                                     |
| ---------------------- | ---------------------------------------------- | ------------------------------------------: | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| `HybridEncoder`        | `interfaces/encoders/HybridEncoder.py`         |                                        `31` | `training/scripts/train_ga.py` (base), `train_es.py` (base)  | Hybrid ??oFovea + Raycasts??? representation to reduce degenerate spinning/turret behaviors while preserving precise targeting. |
| `TemporalStackEncoder` | `interfaces/encoders/TemporalStackEncoder.py`  | `base_size * (2N-1)` (default `217` at N=4) | `training/scripts/train_es.py`                               | Wraps a base encoder with N-frame stacking plus per-frame deltas for temporal awareness.                                   |
| `VectorEncoder`        | `interfaces/encoders/VectorEncoder.py`         |          `3 + 4*N` (default `35` for `N=8`) | Not used by current training script                          | Baseline egocentric object-list encoding (player + nearest asteroids).                                                      |

### `HybridEncoder` (Implemented)

**Configuration surface**

| Parameter             |                 Default | Meaning                                                             |
| --------------------- | ----------------------: | ------------------------------------------------------------------- |
| `num_rays`            |                    `16` | Number of egocentric rays cast for “peripheral vision”.             |
| `num_fovea_asteroids` |                     `3` | Number of nearest asteroids encoded with “high precision” features. |
| `ray_max_distance`    | `diag(screen)` when `0` | Maximum raycast range before normalization.                         |

**Output layout (fixed ordering)**

1. **Proprioception (3 floats)**
   - Forward velocity (normalized, egocentric).
   - Lateral velocity (normalized, egocentric).
   - Shooting cooldown fraction (normalized `0..1`).
2. **Fovea asteroid list (`num_fovea_asteroids * 4` floats)**
   - Wrapped distance to asteroid (normalized `0..1`).
   - Signed angle-to-target relative to ship heading (normalized `-1..1`).
   - Closing speed (normalized/clamped `-1..1`).
   - Asteroid size/scale (normalized `0..1`).
3. **Peripheral rays (`num_rays` floats)**
   - For each ray: normalized hit distance (`0..1`), where `1.0` indicates max range/no hit.

**Geometry & normalization**

- **Toroidal geometry**: Relative asteroid positions are computed with screen-wrap shortest-path adjustment before distance/angle calculations.
- **Ray intersection**: Rays intersect asteroid circles using explicit radii (`ASTEROID_BASE_RADIUS * scale`) to avoid reliance on sprite textures.
- **Normalization bounds**:
  - Player terminal velocity is approximated by `PLAYER_ACCELERATION / (1 - PLAYER_FRICTION)`.
  - Relative closing speed is normalized by `max_player_velocity + max_asteroid_velocity`.


### `TemporalStackEncoder` (Implemented)

**Configuration surface**

| Parameter | Default | Meaning |
| --- | ---: | --- |
| `stack_size` | `4` | Number of consecutive frames to concatenate. |
| `include_deltas` | `True` | Append per-feature frame deltas (`N-1`) after the stacked frames. |

**Output layout (fixed ordering)**

- Stacked frames: `s(t), s(t-1), ..., s(t-N+1)` (base encoder output repeated for N frames).
- Deltas: `delta(t), delta(t-1), ..., delta(t-N+2)` where `delta(k) = s(k) - s(k-1)`.

**Default output size**

- `base_size * (2N - 1)` (e.g., `31 * 7 = 217` for `HybridEncoder` with `N=4`).
- Used by `training/scripts/train_es.py` when `ESConfig.USE_TEMPORAL_STACK=True`.

### `VectorEncoder` (Implemented; currently unused by training)

**Encoded features**

- **Player (3 floats)**:
  - Forward velocity (normalized, egocentric).
  - Lateral velocity (normalized, egocentric).
  - Shooting cooldown fraction (normalized `0..1`).
- **Nearest asteroids (`num_nearest_asteroids * 4` floats)**:
  - Wrapped distance (normalized `0..1`).
  - Signed angle-to-target (normalized `-1..1`).
  - Closing speed (normalized/clamped `-1..1`).
  - Size/scale (normalized `0..1`).
- **Padding for missing asteroids**:
  - `[1.0, 0.0, 0.0, 0.0]` (safe “far away, non-threatening” defaults).

### Debug Visualizations (Implemented)

- `game/debug/visuals.py:draw_hybrid_encoder_debug(...)`: Draws the `HybridEncoder` raycast fan and highlights hit distances in the windowed game.
- `game/debug/visuals.py:draw_debug_overlays(...)`: Draws collision circles and velocity vectors for player/asteroids/bullets.

### Data Flow (Implemented)

```text
AsteroidsGame / HeadlessAsteroidsGame
  -> EnvironmentTracker (interfaces/EnvironmentTracker.py)
    -> StateEncoder.encode(...)
      -> BaseAgent.get_action(encoded_state)
        -> ActionInterface.to_game_input(...)
          -> Game.on_update(...)
```

## Implemented Outputs / Artifacts (if applicable)

- No persistent artifacts are produced by encoders; they output in-memory `List[float]` state vectors consumed directly by agents.

## In Progress / Partially Implemented

- [ ] `VectorEncoder` does not inherit `StateEncoder`: It is compatible by duck typing (`encode/get_state_size/reset/clone`) but not formally part of the abstract interface.
- [ ] Ray ordering is not formally versioned: `HybridEncoder.encode_rays(...)` defines a sweep direction/order that is stable in code but not yet captured as a schema/version for long-term compatibility.
- [ ] Encoder reset semantics are minimal: `HybridEncoder.reset()` is currently a no-op; `TemporalStackEncoder` resets history, but future temporal encoders may need richer reset behavior.

## Planned / Missing / To Be Changed

- [ ] Sensor noise / partial observability toggles: Add configurable noise or dropout to test robustness and generalization.
- [ ] Increase ray resolution (shared): Increase `HybridEncoder.num_rays` (e.g., 16 -> 32) to improve angular coverage and reduce blind-spot exploitation.
- [ ] Add rear/side ray coverage (shared): Distribute rays to include rear and lateral directions (not only forward-biased sweeps) so "spinning turret" policies cannot rely on unseen approaches.
- [ ] Add ray time-to-collision (TTC) features (shared): Add per-ray predictive TTC estimates to represent imminent collisions explicitly (industry-standard avoidance signal).
- [ ] Add per-ray closing-speed features (shared): Add per-ray relative approach speed so the agent can distinguish “near but receding” from “far but rapidly closing”.
- [ ] Add aim-alignment features (shared): Provide a compact "frontness" / best-ray index signal (e.g., weighted by which ray has the nearest hit) to support aiming reward shaping without new object detectors.
- [ ] Encoder schema versioning (shared): Version encoder output layouts so ray-count/layout changes are tracked and old genomes/checkpoints can be invalidated intentionally.
- [ ] Variable-cardinality representations: Add graph-based or set-based encoders for methods that can consume variable entity counts.
- [ ] Encoder benchmarking harness: Standardize offline tests that validate normalization ranges and output stability across game modes (windowed vs headless).

### ES-Oriented Observability Roadmap (Easy / Medium / Hard)

#### Easy

- [ ] Add “closest-ray index” feature: Emit the ray index of the nearest ray hit (or a soft one-hot) to give the policy a direct directional cue.
- [ ] Add “min ray distance” feature: Emit the minimum ray distance across all rays to provide a single scalar “imminent threat” signal.
- [ ] Add “nearest threat bearing” feature: Emit a compact bearing-to-nearest-asteroid feature (if current fovea angle is insufficient for stable aiming).

#### Medium

- [ ] TTC + closing-speed per-ray bundle: Provide per-ray TTC/approach features so avoidance can be learned from predictive signals rather than reactive proximity only.

#### Hard

- [ ] Temporal encoder with internal state: Maintain a compact internal belief (e.g., smoothed velocity/threat trackers) and emit stable latent features.
- [ ] Encoder parity validation suite: Compare headless vs windowed encoder outputs for identical seeds/trajectories (required when temporal features are added).

## Notes / Design Considerations (optional)

- Stable input ordering matters: Any change to feature ordering or normalization implicitly invalidates old genomes/checkpoints and makes cross-run comparisons noisy.
- Hybrid fovea + rays is intentionally redundant: The fovea carries precise dynamics for aiming; rays provide coarse global situational awareness to reduce "spin-lock" strategies.
- Frame stacking and TTC features materially change what the policy can represent; they should be treated as major experimental changes and captured in run metadata and analytics exports.

## Discarded / Obsolete / No Longer Relevant

- The “Hybrid Raycast Encoder (Fovea design)” is no longer speculative; it is implemented as `interfaces/encoders/HybridEncoder.py` and used by the GA training script.
