# Game Engine & Simulation

## Scope / Purpose

The game engine is the simulated world used by both humans (windowed play) and training rollouts (headless). Its purpose is to provide consistent physics, spawning, collision rules, and termination behavior so that policies learned in fast evaluation remain meaningful in real-time playback.

## Current Implemented System

### Execution Modes (Implemented)

| Mode | Implementation | Primary Use |
|---|---|---|
| Windowed | `Asteroids.py:AsteroidsGame` (`arcade.Window`) | Rendering, manual play, and best-agent playback during training. |
| Headless | `game/headless_game.py:HeadlessAsteroidsGame` | Fast seeded rollouts for parallel evaluation. |

### Training/Playback Control Flags (Implemented)

| Flag | Location | Meaning |
|---|---|---|
| `update_internal_rewards` | `AsteroidsGame`, `HeadlessAsteroidsGame` | When `False`, the game does not update its own internal `reward_calculator` (training uses an external reward calculator). |
| `auto_reset_on_collision` | `AsteroidsGame`, `HeadlessAsteroidsGame` | When `False`, a collision ends the episode by removing the player (training loop handles resets). |
| `manual_spawning` | `AsteroidsGame` | When `True`, asteroid spawns are driven by the same per-step timer logic used in headless mode (improves parity). |
| `external_control` | `AsteroidsGame` | When `True`, `AsteroidsGame.on_update(...)` returns early to avoid double-updating during training playback (training loop steps explicitly). |

### Core Entities (Implemented)

| Entity | File | Granular Responsibilities |
|---|---|---|
| Player | `game/classes/player.py` | Integrates velocity + friction each update; rotates left/right; thrusts in facing direction; shoots bullets using a cooldown timer. |
| Bullet | `game/classes/bullet.py` | Moves at a constant speed; decrements lifetime; expires when lifetime reaches 0. |
| Asteroid | `game/classes/asteroid.py` | Spawns at edges with randomized velocity/rotation; maintains HP based on size tier; fragments into smaller asteroids when destroyed. |

### Physics & Configuration Surface (Implemented)

Key constants live in `game/globals.py`:

| Constant | Meaning |
|---|---|
| `SCREEN_WIDTH`, `SCREEN_HEIGHT` | World dimensions (currently `800x600`). |
| `PLAYER_ACCELERATION`, `PLAYER_FRICTION`, `PLAYER_ROTATION_SPEED` | Player movement model (per-step). |
| `BULLET_SPEED`, `BULLET_LIFETIME`, `BULLET_COOLDOWN` | Weapon behavior and firing constraints. |
| `ASTEROID_SPAWN_INTERVAL` | Spawn cadence in seconds. |
| `ASTEROID_SPEED_*`, `ASTEROID_HP_*`, `ASTEROID_SCALE_*` | Asteroid tier physics/health/size. |
| `PLAYER_RADIUS`, `BULLET_RADIUS`, `ASTEROID_BASE_RADIUS` | Explicit collision radii for parity between modes. |

### Collision & Episode Termination (Implemented)

**Bullet → asteroid**

- Circle collision uses explicit radii (`BULLET_RADIUS`, `ASTEROID_BASE_RADIUS * scale`) for parity (sprite texture geometry may be unavailable in headless).
- Asteroid HP decrements on hit; fragmentation occurs when HP reaches `0`.
- Metrics are updated via `MetricsTracker` (hits and kills).

**Player → asteroid**

- Circle collision uses explicit radii (`PLAYER_RADIUS`, `ASTEROID_BASE_RADIUS * scale`).
- Training mode behavior: player is removed from `player_list` (episode ends).
- Manual play behavior: game can auto-reset on collision when `auto_reset_on_collision=True`.

### Wrapping & Spatial Queries (Implemented)

- World is toroidal: entities wrap to the opposite edge when leaving bounds.
- `interfaces/EnvironmentTracker.get_distance(...)` computes shortest wrapped distances and is used by encoders and analytics sampling.

### Randomness & Determinism (Implemented)

- Windowed spawn randomness uses module-level `random` (`AsteroidsGame.spawn_asteroid`).
- Headless spawn randomness uses a per-instance `random.Random(random_seed)` to avoid cross-thread interference and allow deterministic replay per seed.

### Headless Parity Fix: Lifetime Expiration (Implemented)

- Headless mode maintains `bullet_list` and `asteroid_list` as plain Python lists.
- `Bullet.update()` / `Asteroid.update()` call `remove_from_sprite_lists()`, which is an arcade sprite-list operation and does not remove items from plain lists.
- `HeadlessAsteroidsGame.on_update(...)` explicitly filters expired bullets/asteroids by `lifetime > 0` to keep headless behavior aligned with windowed behavior.

### Debug Visuals (Implemented)

| Debug Feature | File | Description |
|---|---|---|
| Collision/velocity overlays | `game/debug/visuals.py:draw_debug_overlays` | Draws collision circles and velocity/facing vectors. |
| Hybrid encoder ray fan | `game/debug/visuals.py:draw_hybrid_encoder_debug` | Visualizes `HybridEncoder` raycasts during windowed playback. |

## Implemented Outputs / Artifacts (if applicable)

- Simulation state lists (`player_list`, `asteroid_list`, `bullet_list`) are exposed to trackers/encoders in both modes.
- Per-episode metrics are accumulated by `interfaces/MetricsTracker.py` (shots, hits, kills, time alive).
- Reward totals and per-component contributions are tracked by `interfaces/RewardCalculator.py` when enabled by the caller.

## In Progress / Partially Implemented

- [ ] Deterministic parity (windowed vs headless RNG): Windowed mode does not provide a seedable RNG surface comparable to headless mode’s `random_seed`.
- [ ] True frame-rate independence: Motion is primarily “per update step”; training and playback rely on fixed stepping for consistency.

## Planned / Missing / To Be Changed

- [ ] Difficulty knobs (shared): Expose explicit difficulty parameters (e.g., max asteroid count, spawn interval, asteroid speed multipliers) that can be applied consistently in both windowed and headless modes.
- [ ] Curriculum hooks (shared): Allow training scripts to pass a per-episode/per-generation difficulty setting into the environment (headless + playback) without changing reward definitions.
- [ ] Progressive difficulty schedule (future): Define a curriculum schedule that increases difficulty as policies improve, while keeping metric selection and comparability as an open design decision (not yet a committed goal).
- [ ] Wrap-aware collisions: Detect collisions that occur across the screen edge (toroidal overlap) rather than only after wrapping positions.
- [ ] Per-tick event hooks: Expose "shots fired this tick", "asteroids destroyed this tick", etc., for cleaner reward components and analytics.

## Notes / Design Considerations (optional)

- Headless mode’s explicit radii avoid dependence on sprite textures, which may not load without an arcade window context.
- Debug overlays are intentionally decoupled from training logic; they are used for interpretability and diagnosing policy behaviors.

## Discarded / Obsolete / No Longer Relevant

- No engine features have been formally removed; replaced behavior should be captured as “Implemented” and prior issues should be tracked as “Fixed” within the implementation narrative.
