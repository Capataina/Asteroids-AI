# Plan 008: Fresh Game Display for Best Agent

## Problem Statement

The current implementation attempts to replay the best agent's evaluation by syncing random seeds between the headless evaluation and visual display. However, this approach has critical flaws:

1. **RNG Mismatch**: HeadlessAsteroidsGame uses an isolated `random.Random()` instance, while AsteroidsGame uses the global `random` module. Even with the same seed, the asteroid configurations diverge.

2. **Collision Detection Differences**: Headless uses explicit radius-based collision (hardcoded values), while visual uses `arcade.check_for_collision_with_list()` (sprite bounds).

3. **Misleading Results**: An agent evaluated at 6500 fitness with 65 kills might only achieve 500 points and 5 kills during "replay" - confusing users about actual agent capability.

## Proposed Solution

Instead of attempting to replay the exact evaluation scenario, **run the best agent in a completely fresh game** between generations. This approach:

1. **Tests generalization**: Does the agent actually understand the game, or did it get lucky?
2. **Eliminates sync bugs**: No need to match RNG between different game implementations
3. **Simpler code**: Remove all seed-syncing logic
4. **Honest evaluation**: Shows true agent capability on unseen scenarios

## Why This Works

The GA agents use a **reactive linear policy**, not memorization:

```
action[i] = sum(weights[j] * current_state[j])
```

The agent responds to:
- Current player position/velocity/angle
- Current nearest asteroid positions/velocities

It does NOT store:
- "Press left at frame 100"
- "Shoot at frame 250"

Therefore, agents can generalize to any asteroid configuration - they're learning relationships between state and actions, not sequences.

## Implementation Changes

### File: `training/train_ga_parallel.py`

#### 1. Remove seed storage from evaluation phase

**Before:**
```python
self.fitnesses, self.display_seed, gen_metrics = evaluate_population_parallel(...)
```

**After:**
```python
self.fitnesses, _, gen_metrics = evaluate_population_parallel(...)
# display_seed no longer needed
```

#### 2. Remove `self.display_seed` attribute

Remove from `__init__` and all references.

#### 3. Simplify `_start_best_agent_display()`

**Before:**
```python
def _start_best_agent_display(self):
    # Use the SAME random seed as evaluation for reproducible asteroid spawning
    if self.display_seed is not None:
        random.seed(self.display_seed)

    # Enable manual spawning mode to match headless game timing exactly
    self.game.manual_spawning = True
    ...
```

**After:**
```python
def _start_best_agent_display(self):
    # Run best agent in a FRESH game to test generalization
    # No seed syncing - let the game use natural randomness

    # Use normal arcade.schedule spawning (not manual)
    self.game.manual_spawning = False
    ...
```

#### 4. Update display logging

**Before:**
```python
print(f"Displaying generation's best agent (fitness={self.display_fitness:.2f}, all-time best={self.best_fitness:.2f}, seed={self.display_seed})...")
```

**After:**
```python
print(f"Testing best agent in fresh game (training fitness={self.display_fitness:.2f}, all-time best={self.best_fitness:.2f})...")
```

#### 5. Update info text

Change text from "replaying" language to "testing" language to reflect the new approach.

### Files NOT Changed

- `parallel_evaluator.py`: Still uses isolated RNG for fair evaluation (all agents same seed per generation)
- `headless_game.py`: No changes needed
- `Asteroids.py`: No changes needed (will use normal random spawning)

## Expected Behavior After Change

### Before (Broken Replay)
```
Generation 10: Best=6531.34, BestKills=65
Displaying generation's best agent (seed=138472117)...
  Step 100: Score=-5.1, Kills=0   <- Completely different game!
  Step 300: Score=491.0, Kills=5
Best agent died after 386 steps   <- Nothing like the 65 kills in training
```

### After (Fresh Game Test)
```
Generation 10: Best=6531.34, BestKills=65
Testing best agent in fresh game (training fitness=6531.34)...
  Step 100: Score=298.2, Kills=3  <- Reasonable performance
  Step 300: Score=892.1, Kills=9
  Step 500: Score=1503.4, Kills=15
  ...                             <- May vary, but tests real capability
```

## Benefits

1. **No more confusing discrepancies** - Users won't see "6500 fitness" agents getting 500 points
2. **True generalization test** - See if agents actually learned useful behaviors
3. **Simpler codebase** - Remove complex seed-syncing that never worked correctly
4. **Better debugging** - If an agent performs poorly in fresh games, it indicates overfitting to specific scenarios (though unlikely with linear policy)

## Risks and Mitigations

### Risk: Display performance varies wildly
**Mitigation**: This is actually valuable information! High variance suggests the agent relies on lucky spawns rather than skill.

### Risk: Users expect exact replay
**Mitigation**: Update UI text to clearly indicate this is a "generalization test" not a "replay". The training fitness shown is the authoritative measure.

## Success Criteria

1. Best agent display no longer requires seed synchronization
2. Display performance is in the same ballpark as training performance (within 50% typically)
3. Code is simpler with seed-syncing logic removed
4. User can observe agent actually responding to asteroids intelligently

## Future Considerations

- Could add option to run multiple fresh games and average display performance
- Could track "generalization score" as metric (display performance / training performance)
- Could use fresh game testing as part of fitness evaluation (train on seed A, bonus points for performance on seed B)
