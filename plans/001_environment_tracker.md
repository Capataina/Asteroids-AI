# EnvironmentTracker and MetricsTracker Implementation

## Goal and Scope

**Deliverables:**

- `interfaces/EnvironmentTracker`: Class providing current game state snapshot and derived metrics
- `interfaces/MetricsTracker`: Class tracking aggregated statistics over episode/lifetime
- Integration with `AsteroidsGame.on_update()` to keep tracker in sync
- Complete event detection (shots fired, asteroids destroyed)
- All derived state methods (nearest asteroid, distances, near misses)

**Out of Scope:**

- Changes to game entity classes (Player, Bullet, Asteroid)
- Modifications to core game physics or collision logic
- Implementation of specific reward functions (tracker provides data, reward shaping is separate)
- **AI wrapper refactoring** - Refactoring `AsteroidsGraphEnv` and other AI wrappers to use trackers is deferred until after all preliminary infrastructure plans (002-006) are complete
- Changes to `train_agent.py` for AI integration (deferred until after infrastructure is complete)

## Context and Justification

**Why Now:**

- Current AI wrappers directly access `self.game.*` (61 references in `env_wrapper.py`)
- No centralised place to track metrics (accuracy, shots fired, hits, near misses)
- Game state access is scattered, making it hard to add new derived metrics
- Future AI methods (neuroevolution, ES, GA, GP) will need consistent state interface

**What It Enables:**

- Stable API for all AI methods (game internals can change without breaking AI code)
- Metrics tracking (accuracy, near misses, time alive) without modifying game code
- Derived state computation (nearest asteroid, distances, relative positions)
- Extensibility: new metrics/features added in one place

**Rejected Alternatives:**

- Keep direct `self.game.*` access: Too fragile, no metrics, scattered logic
- Single monolithic tracker: Separation of concerns (current state vs aggregated stats) is cleaner
- Event-driven system: Overkill for current needs, adds complexity

**Assumptions/Constraints:**

- Tracker observes game state but doesn't control it (game updates tracker, not vice versa)
- Tracker must be lightweight (updated every frame, no heavy computation)
- Must maintain backward compatibility during migration (incremental refactor)

## Interfaces and Contracts

### EnvironmentTracker Interface

```python
class EnvironmentTracker:
    def __init__(self, game: AsteroidsGame)
    def update(self, game: AsteroidsGame) -> None  # Called each frame after game update

    # Current state access
    def get_all_bullets(self) -> List[Bullet]
    def get_all_asteroids(self) -> List[Asteroid]
    def get_player(self) -> Optional[Player]
    def get_tick(self) -> int

    # Per-tick events (reset each frame)
    def get_shots_fired_this_tick(self) -> int
    def get_asteroids_destroyed_this_tick(self) -> int

    # Derived state
    def get_nearest_asteroid(self) -> Optional[Asteroid]
    def get_distance_to_nearest_asteroid(self) -> Optional[float]
    def get_asteroids_in_range(self, distance: float) -> List[Asteroid]
    def get_near_miss_score(self, safe_distance: float = 50.0) -> float
```

**Invariants:**

- `update()` must be called exactly once per game frame
- Per-tick counters reset to 0 at start of each `update()`
- All getters return data from last `update()` call (no stale state)

### MetricsTracker Interface

```python
class MetricsTracker:
    def __init__(self, env_tracker: EnvironmentTracker)
    def reset(self) -> None  # Called at episode start
    def update(self, env_tracker: EnvironmentTracker) -> None  # Called each frame

    # Aggregated statistics
    def get_total_shots_fired(self) -> int
    def get_total_hits(self) -> int
    def get_total_kills(self) -> int
    def get_accuracy(self) -> float  # hits / shots_fired, or 0.0 if no shots
    def get_time_alive(self) -> float  # seconds
    def get_episode_duration(self) -> int  # ticks

    # Rates
    def get_shots_per_second(self) -> float
    def get_kills_per_minute(self) -> float

    # Episode summary
    def get_episode_stats(self) -> Dict[str, Any]
```

**Invariants:**

- `reset()` clears all counters (called on episode start)
- `update()` aggregates from `env_tracker` events
- Rates computed from totals / time_alive

**Must-Not-Break:**

- Existing `AsteroidsGraphEnv` functionality (graph state generation)
- Game update loop performance (tracker update must be fast)
- No changes to game entity interfaces

## Impacted Areas

**Files to Create:**

- [ ] `interfaces/EnvironmentTracker.py` (new file)
- [ ] `interfaces/MetricsTracker.py` (new file)

**Files to Modify:**

- [ ] `interfaces/Environment.py` (remove incomplete stub, or keep as legacy if needed)
- [ ] `Asteroids.py` (add tracker initialisation and `update()` call in `on_update()`)

**Modules Affected:**

- Game update loop (integration point)
- Tracker infrastructure (core implementation)

**Deferred (After Plans 002-006 Complete):**

- AI wrapper refactoring (`ai_agents/reinforcement_learning/gnn_and_sac/env_wrapper.py`)
- Training loop integration (`train_agent.py`)
- All AI method implementations

**No Schema/State Machine Changes:**

- Game entities unchanged
- No CLI/config changes

## Incremental Implementation

### Step 1: Create EnvironmentTracker skeleton

**Intent**: Establish class structure and basic state access methods
**Implementation**:

- [x] Create `interfaces/EnvironmentTracker.py`
- [x] Implement `__init__()`, `update()`, `get_all_bullets()`, `get_all_asteroids()`, `get_player()`, `get_tick()`
- [x] Store reference to game, initialise tick counter
      **Verification**: Can instantiate tracker, call getters, tick increments on update

### Step 2: Add event detection

**Intent**: Track shots fired and asteroids destroyed per tick
**Implementation**:

- [x] In `update()`, compare bullet count to previous frame (increase = shot fired)
- [x] Track asteroid removals (compare lists, detect HP->0 transitions)
- [ ] Store per-tick counters, reset each frame
      **Verification**: Counters increment correctly when events occur, reset to 0 each frame

### Step 3: Add derived state methods

**Intent**: Compute nearest asteroid, distances, near miss scores
**Implementation**:

- [x] `get_nearest_asteroid()`: iterate asteroids, compute distance to player, return minimum
- [x] `get_distance_to_nearest_asteroid()`: wrapper around nearest asteroid distance
- [x] `get_asteroids_in_range()`: filter asteroids within specified distance
- [ ] `get_near_miss_score()`: compute min distance, return reward if below threshold
      **Verification**: Methods return correct values, handle empty asteroid list gracefully

### Step 4: Create MetricsTracker

**Intent**: Track aggregated statistics over episode
**Implementation**:

- [x] Create `interfaces/MetricsTracker.py`
- [ ] Implement counters: total_shots, total_hits, total_kills, time_alive
- [x] `update()` aggregates from `env_tracker` events
- [x] `reset()` clears all counters
- [x] Compute accuracy, rates from totals
      **Verification**: Counters accumulate correctly, accuracy computed properly, reset works

### Step 5: Integrate with game update loop

**Intent**: Keep tracker in sync with game state
**Implementation**:

- [x] In `AsteroidsGame.__init__()`, create `self.tracker = EnvironmentTracker(self)`
- [x] At end of `AsteroidsGame.on_update()`, call `self.tracker.update(self)`
- [x] Ensure tracker updates after all game state changes
      **Verification**: Tracker state matches game state after each frame

### Step 6: Clean up and documentation

**Intent**: Remove old stub, add docstrings, verify integration
**Implementation**:

- [x] Remove `interfaces/Environment.py` stub
- [ ] Add comprehensive docstrings to both tracker classes
- [ ] Add type hints
- [ ] Verify tracker functionality independently (without AI wrappers)
      **Verification**: Code is clean, documented, trackers work correctly

## Testing and Validation

**Unit Tests:**

- `EnvironmentTracker`: event detection, derived state computation, edge cases (empty lists)
- `MetricsTracker`: counter accumulation, accuracy calculation, reset behaviour

**Integration Tests:**

- Tracker updates match game state after each frame
- Trackers work correctly with game update loop
- MetricsTracker aggregates correctly from EnvironmentTracker

**Manual Verification:**

```bash
# Run training and verify tracker updates
python train_agent.py

# Check that metrics are being tracked (add debug prints if needed)
# Verify no performance regression (tracker update should be <1ms)
```

**Expected Signals:**

- Game runs successfully with trackers integrated
- Trackers update correctly each frame
- Metrics accumulate correctly (shots fired, hits, accuracy)
- No exceptions or errors in tracker update
- Trackers are ready for use by future infrastructure (RewardCalculator, StateEncoders, etc.)

## Risks and Failure Modes

**Event Detection Failures:**

- **Risk**: Shot detection misses bullets fired in same frame as removal
- **Detection**: `get_shots_fired_this_tick()` returns 0 when bullet fired
- **Mitigation**: Compare bullet count before/after game update, or track `player.shoot()` calls

**Performance Regression:**

- **Risk**: Tracker update adds latency to game loop
- **Detection**: Frame rate drops, update takes >5ms
- **Mitigation**: Cache computed values, only recalculate when needed, profile with cProfile

**State Synchronisation Issues:**

- **Risk**: Tracker reads stale state if update called at wrong time
- **Detection**: Tracker state doesn't match game state
- **Mitigation**: Always call `tracker.update()` at end of `on_update()`, after all game logic

**AI Wrapper Compatibility:**

- **Note**: AI wrapper refactoring is deferred until after plans 002-006 are complete
- **Current State**: AI wrappers may still access `self.game.*` directly
- **Future**: Once infrastructure is complete, AI wrappers will be refactored to use trackers

**Edge Cases:**

- Empty asteroid/bullet lists: methods must return empty lists, not None
- Player death: `get_player()` returns None, derived methods handle gracefully
- Concurrent access: Not an issue (single-threaded game loop)

**Concurrency/Latency:**

- Single-threaded game loop, no concurrency issues
- Tracker update is synchronous, no async concerns

## Exit Criteria

**Correctness:**

- [ ] All tracker getters return correct values matching game state
- [ ] Event detection works (shots fired, asteroids destroyed)
- [ ] Metrics accumulate correctly over episode
- [ ] Trackers integrate correctly with game update loop
- [ ] Trackers are ready for use by RewardCalculator and StateEncoders

**Performance:**

- [ ] Tracker update adds <2ms to game loop (60 FPS = 16.67ms budget)
- [ ] No frame rate drops during training

**Operability:**

- [ ] Tracker initialises automatically with game
- [ ] Metrics reset on episode start
- [ ] No manual intervention required

**Documentation:**

- [ ] Both tracker classes have comprehensive docstrings
- [ ] Type hints added to all public methods
- [ ] `plans/README.md` updated with plan status
- [ ] Architecture doc updated if structure changes

## Future Considerations

**Follow-ons (After Plans 002-006 Complete):**

- Refactor AI wrappers to use trackers instead of direct game access
- Integrate trackers with RewardCalculator (plan 003)
- Integrate trackers with StateEncoders (plan 004)
- Use trackers in BaseAgent and EpisodeRunner (plan 005)
- Add more derived metrics (bullet trajectories, asteroid velocities relative to player)
- Create AI method implementations using tracker interface (GA, GP, ES, NEAT, GNN+SAC)

**Known Limits:**

- Tracker doesn't track historical state (only current snapshot)
- No prediction/forecasting (where will asteroid be in N frames)
- Event detection is frame-based (may miss very fast events)

**Explicit Tech Debt:**

- AI wrappers still access `self.game.*` directly (will be refactored after plans 002-006)
- Score access still via `self.game.score` (will be handled by RewardCalculator in plan 003)
- Action outputs (`left_pressed` etc.) still set directly on game (intentional, not observations)
- No persistence of metrics across training sessions (episode-only)

**Extension Points:**

- Tracker can be extended with new derived metrics without changing game
- MetricsTracker can add new statistics without changing EnvironmentTracker
- Both trackers can be mocked for testing AI methods independently
