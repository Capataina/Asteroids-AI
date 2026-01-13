# Game Engine & Simulation

## Scope / Purpose

The game engine is the simulated “world” used by both humans (windowed play) and training rollouts (headless). Its purpose is to provide consistent physics/rules across windowed and headless execution so that behaviors learned in fast evaluation remain valid in real-time playback.

## Current Implemented System

### Two Execution Modes (Implemented)

- **Windowed game (`Asteroids.py:AsteroidsGame`)**: An `arcade.Window` implementation for rendering and interactive playback.
- **Headless game (`game/headless_game.py:HeadlessAsteroidsGame`)**: A non-rendering simulation used for parallel evaluation.
- **Shared constants (`game/globals.py`)**: Screen dimensions, physics constants, and collision radii used by both modes.

### Core Entities (Implemented)

- **Player (`game/classes/player.py`)**:
  - **Kinematics**: Position integrates `change_x/change_y`; friction multiplies velocity each update.
  - **Rotation**: Left/right rotate by a fixed degree step per update.
  - **Thrust**: Adds acceleration in the facing direction (angle-based).
  - **Shooting**: Uses a cooldown timer (`shoot_timer`) and spawns `Bullet` when ready.
- **Bullet (`game/classes/bullet.py`)**:
  - **Velocity**: Constant speed in the ship’s facing direction.
  - **Lifetime**: Decrements per update and removes itself when expired.
- **Asteroid (`game/classes/asteroid.py`)**:
  - **Spawn randomness**: Edge-spawned with random velocity/rotation.
  - **Size tiers**: Large/medium/small controlled by scale constants.
  - **HP by size**: Large=3, medium=2, small=1.
  - **Fragmentation**: Large breaks into 2 medium; medium breaks into 3 small; small breaks into none.

### Collision & Episode Termination (Implemented)

- **Bullet–asteroid collisions**:
  - **Circle collision**: Explicit radii (`BULLET_RADIUS`, `ASTEROID_BASE_RADIUS * scale`) are used for parity (headless sprites may not have valid texture geometry).
  - **Asteroid damage**: HP decremented on hit; fragmentation occurs when HP reaches 0.
  - **Metrics updates**: Hits and kills are tracked via `MetricsTracker`.
- **Player–asteroid collisions**:
  - **Circle collision**: Explicit radii (`PLAYER_RADIUS`, `ASTEROID_BASE_RADIUS * scale`).
  - **Training mode**: Player is removed from `player_list` when collision occurs (episode ends).
  - **Manual play mode**: `AsteroidsGame` can auto-reset on collision when enabled.

### Wrapping & Spatial Queries (Implemented)

- **World wrapping**: Entities are teleported to the opposite edge when exceeding screen bounds (toroidal world).
- **Wrapped distance queries** (`interfaces/EnvironmentTracker.get_distance(...)`): Computes shortest path distances accounting for wrap and is used by state encoding and analytics sampling.

### Debug Visuals (Implemented)

- **Overlays (`game/debug/visuals.py`)**:
  - Player collision circle + facing vector + velocity vector.
  - Asteroid collision circles + velocity vectors.
  - Bullet collision circles.

### Configuration Surface (Implemented)

Key constants live in `game/globals.py` (selected examples):

| Constant | Meaning |
|---|---|
| `SCREEN_WIDTH`, `SCREEN_HEIGHT` | World dimensions (currently `800x600`). |
| `PLAYER_ACCELERATION`, `PLAYER_FRICTION`, `PLAYER_ROTATION_SPEED` | Player movement model. |
| `BULLET_SPEED`, `BULLET_LIFETIME`, `BULLET_COOLDOWN` | Weapon behavior. |
| `ASTEROID_SPAWN_INTERVAL` | Spawn cadence in seconds. |
| `ASTEROID_SPEED_*`, `ASTEROID_HP_*`, `ASTEROID_SCALE_*` | Asteroid tier physics/health/size. |
| `PLAYER_RADIUS`, `BULLET_RADIUS`, `ASTEROID_BASE_RADIUS` | Explicit collision radii. |

## Implemented Outputs / Artifacts

- **Simulation state**: `player_list`, `asteroid_list`, `bullet_list` are exposed to trackers/encoders in both windowed and headless modes.
- **Per-episode metrics**: `interfaces/MetricsTracker.py` accumulates shots/hits/kills/time_alive.
- **Reward accumulation**: `interfaces/RewardCalculator.py` tracks total score and per-component contributions.

## In Progress / Partially Implemented

- [ ] Deterministic parity (windowed vs. headless RNG): Headless rollouts can be seeded via an isolated RNG; the windowed game uses global `random` without explicit seeding.
- [ ] True frame-rate independence: Entity motion is currently "per update step" rather than scaled by `delta_time`; training and playback rely on fixed stepping for consistency.

## Recently Fixed

- [x] **Bullet/asteroid lifetime expiration in headless mode**: `Bullet.update()` and `Asteroid.update()` call `remove_from_sprite_lists()` when lifetime expires, but this arcade method does nothing for plain Python lists used in headless mode. Bullets and asteroids would never expire, wrapping around the screen indefinitely. This caused agents to exploit "zombie bullets" that don't exist in windowed mode, inflating training accuracy (70-80%) vs fresh game accuracy (10-20%). Fixed by adding explicit lifetime filtering in `HeadlessAsteroidsGame.on_update()`.

## Planned / Missing / To Be Changed

- [ ] Difficulty scaling: Increase asteroid density/speed over time or by curriculum schedule.
- [ ] Multi-agent variants: Add player-to-player or competitive interactions for future experiments.
- [ ] Expanded observability hooks: Expose per-tick events (shots fired this tick, asteroids destroyed this tick) for cleaner analytics/reward components.

## Notes / Design Considerations

- Collision detection does not currently account for wrap-around overlap at the moment of collision; entities are wrapped first and then checked in their wrapped positions.
- Headless mode uses explicit radii to avoid dependency on sprite textures (which may not load without an arcade window context).

## Discarded / Obsolete / No Longer Relevant

- No engine features have been formally removed; planned replacements should be captured under "Planned / Missing / To Be Changed".

