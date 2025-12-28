# Component-Based Reward System

## Goal and Scope

**Deliverables:**

- `interfaces/RewardCalculator.py` - Base `RewardComponent` abstract class and `ComposableRewardCalculator` class
- `interfaces/rewards/` directory with individual reward component implementations
- Modular, composable reward system where components can be enabled/disabled independently
- Removal of score calculation from game core (`Asteroids.py`)
- Integration with EnvironmentTracker and MetricsTracker
- Foundation for configuration-driven reward shaping (future: config files)

**Out of Scope:**

- Configuration file system integration (covered in plan 006)
- Historical reward tracking/visualization (future enhancement)
- Reward normalization/scaling utilities (can be added later if needed)
- Reward component discovery/automatic tuning (future enhancement)

## Context and Justification

**Why Now:**

- Score calculation currently embedded in game logic (`Asteroids.py`)
- AI wrappers duplicate reward logic (`env_wrapper.py` uses `game.score` directly)
- Need flexible, experimental reward shaping without code changes
- All 5 AI methods need consistent reward interface
- Reward shaping is a first-class experimental variable (per README)
- EnvironmentTracker and MetricsTracker are now complete (plans 001-002)

**What It Enables:**

- Game core focuses only on physics/simulation (no reward logic)
- Easy experimentation: enable/disable reward components without code changes
- No duplication of reward logic across AI wrappers
- Clean separation: game → tracker → reward → AI
- Modular design: add new reward components without modifying existing ones
- Future: configuration-driven reward shaping via config files
- Debugging: can see individual component contributions

**Rejected Alternatives:**

- **Monolithic reward functions** (SurvivalReward, AccuracyReward, etc.): Less flexible, harder to compose, requires new classes for combinations
- **Single reward function with flags**: Still monolithic, hard to extend
- **Strategy pattern with separate reward classes**: More verbose, less composable than components
- **Component-based chosen**: Maximum flexibility, easy toggling, clean separation of concerns

**Key Requirements:**

- Must use EnvironmentTracker and MetricsTracker as inputs (no direct game access)
- Must support both step-level and episode-level rewards
- Components must be independently testable
- Must handle edge cases gracefully (empty lists, zero metrics, None values)
- Components can have configurable parameters (bonus amounts, thresholds, etc.)

## Interfaces and Contracts

### RewardComponent Base Interface

**Abstract Base Class:** `RewardComponent` (in `interfaces/RewardCalculator.py`)

**Core Methods:**

```python
@abstractmethod
def calculate_step_reward(
    env_tracker: EnvironmentTracker,
    metrics_tracker: MetricsTracker,
    prev_metrics: Dict[str, Any],  # snapshot from previous step
    current_metrics: Dict[str, Any]  # snapshot from current step
) -> float:
    """
    Calculate reward contribution for this step.
    Returns 0.0 if component doesn't apply this step.
    Should be pure (no side effects).
    """
    pass

@abstractmethod
def calculate_episode_reward(
    metrics_tracker: MetricsTracker
) -> float:
    """
    Calculate episode-level reward contribution.
    Returns 0.0 if component doesn't apply.
    Called once at episode end.
    """
    pass

def reset(self) -> None:
    """
    Reset any internal state for new episode.
    Called at episode start by ComposableRewardCalculator.
    Default implementation does nothing (override if needed).
    """
    pass
```

**Invariants:**

- Components are pure: no side effects on trackers or game state
- Use only EnvironmentTracker and MetricsTracker as inputs
- Handle edge cases gracefully (return 0.0 if not applicable)
- Step rewards are additive: total = sum of all enabled component rewards
- Episode rewards are additive: total = sum of all enabled component rewards

### ComposableRewardCalculator Class

**Main Interface:** `ComposableRewardCalculator` (in `interfaces/RewardCalculator.py`)

**Core Methods:**

```python
def __init__(self, components: Dict[str, RewardComponent] = None):
    """Initialize with optional dict of components. All enabled by default."""

def add_component(self, name: str, component: RewardComponent) -> None:
    """Add a component (enabled by default)"""

def enable_component(self, name: str) -> None:
    """Enable a component"""

def disable_component(self, name: str) -> None:
    """Disable a component"""

def is_enabled(self, name: str) -> bool:
    """Check if component is enabled"""

def calculate_step_reward(
    env_tracker: EnvironmentTracker,
    metrics_tracker: MetricsTracker
) -> float:
    """
    Calculate total step reward from all enabled components.
    Takes snapshots of metrics for delta calculations.
    """

def calculate_episode_reward(metrics_tracker: MetricsTracker) -> float:
    """Calculate total episode-level reward from all enabled components"""

def reset(self) -> None:
    """Reset all components for new episode"""
```

**Design:**

- Maintains dict of components with string names (keys)
- Maintains set of enabled component names
- Tracks previous metrics snapshot for delta calculations
- Sums contributions from all enabled components
- Components can be toggled at runtime (future: via config)

### Reward Component Types

**Initial Components** (in `interfaces/rewards/`):

1. **`SurvivalBonus`** (`survival.py`)

   - Rewards time alive (survival)
   - Step-level: constant reward per frame/step
   - Parameters: `reward_per_second: float`

2. **`KillAsteroidBonus`** (`kill_asteroid.py`)

   - Rewards each asteroid kill
   - Step-level: bonus when `total_kills` increases
   - Parameters: `bonus_amount: float`

3. **`AccuracyBonus`** (`accuracy.py`)

   - Rewards high accuracy (hits/shots ratio)
   - Step-level: bonus per step if accuracy above threshold
   - Parameters: `bonus_per_second: float`, `min_accuracy: float`

4. **`NearMissBonus`** (`near_miss.py`)

   - Rewards getting close to asteroids without colliding
   - Step-level: reward based on distance to nearest asteroid
   - Parameters: `safe_distance: float`, `bonus_multiplier: float`

5. **`ChunkExplorationBonus`** (`chunk_exploration.py`)
   - Rewards movement across chunk boundaries (current score system)
   - Step-level: bonus when player moves threshold distance
   - Parameters: `chunk_size: float`, `bonus_per_chunk: float`
   - Internal state: tracks last player position

**Future Components** (not in scope, examples):

- Efficiency bonus (kills per shot)
- Risk-taking bonus (proximity-based)
- Combo bonuses (consecutive kills)
- Survival streak bonuses
- Distance traveled bonus (alternative to chunk exploration)

**Component Design Principles:**

- Each component calculates one specific reward aspect
- Components are independent (can be combined in any way)
- Components have sensible defaults but accept parameters
- Components handle edge cases (return 0.0 if not applicable)
- Step-level vs episode-level: choose based on when reward should apply

## Impacted Areas

**Files to Create:**

- `interfaces/RewardCalculator.py` - Base classes (`RewardComponent`, `ComposableRewardCalculator`)
- `interfaces/rewards/__init__.py` - Package init
- `interfaces/rewards/survival.py` - `SurvivalBonus` component
- `interfaces/rewards/kill_asteroid.py` - `KillAsteroidBonus` component
- `interfaces/rewards/accuracy.py` - `AccuracyBonus` component
- `interfaces/rewards/near_miss.py` - `NearMissBonus` component
- `interfaces/rewards/chunk_exploration.py` - `ChunkExplorationBonus` component

**Files to Modify:**

- `Asteroids.py` - Remove score calculation logic from `on_update()`:
  - Remove `self.score += math.ceil(delta_time) / 10` (line 125)
  - Remove movement chunk score logic (lines 134-155)
  - Remove `self.score += 10` for asteroid kills (line 180)
  - Optionally keep `self.score` for display purposes (calculated by RewardCalculator)
- `ai_agents/reinforcement_learning/gnn_and_sac/env_wrapper.py` - Replace `reward = self.game.score - prev_score` with RewardCalculator
- `train_agent.py` - Integrate RewardCalculator into training loop (create instance, call `calculate_step_reward`)

**Dependencies:**

- Requires EnvironmentTracker (plan 001 - complete)
- Requires MetricsTracker (plan 002 - complete)
- Will be used by all AI methods (future)
- Foundation for configuration system (plan 006)

## Incremental Implementation

### Step 1: Create base classes and structure

**Intent**: Establish the foundation for component-based reward system

**Implementation**:

- [x] Create `interfaces/RewardCalculator.py` with `RewardComponent` abstract base class
  - Define abstract methods: `calculate_step_reward()`, `calculate_episode_reward()`, `reset()`
  - Add docstrings and type hints
- [x] Create `ComposableRewardCalculator` class in same file
  - Implement component storage (dict), enabled components (set)
  - Implement `add_component()`, `enable_component()`, `disable_component()`, `is_enabled()`
  - Implement `reset()` (calls reset on all components)
- [ ] Create `interfaces/rewards/__init__.py` (empty package init for now)

**Verification**: Can import classes, instantiate `ComposableRewardCalculator`, add components, enable/disable them

### Step 2: Implement SurvivalBonus component

**Intent**: Simple time-based survival reward (replaces `self.score += math.ceil(delta_time) / 10`)

**Implementation**:

- [x] Create `interfaces/rewards/survival.py`
- [x] Implement `SurvivalBonus(RewardComponent)` class
  - `__init__(reward_per_second: float = 1.0)` - configurable reward rate
  - `calculate_step_reward()` - returns `reward_per_second / 60.0` (assuming 60 FPS)
  - `calculate_episode_reward()` - returns 0.0 (step-level only)
  - `reset()` - no-op (no state)
- [x] Test component independently

**Verification**: Component returns correct reward per step, handles zero/negative values gracefully

### Step 3: Implement KillAsteroidBonus component

**Intent**: Reward asteroid kills (replaces `self.score += 10` per kill)

**Implementation**:

- [x] Create `interfaces/rewards/kill_asteroid.py`
- [x] Implement `KillAsteroidBonus(RewardComponent)` class
  - `__init__(bonus_amount: float = 10.0)` - configurable kill bonus
  - `calculate_step_reward()` - calculates delta: `current_metrics['total_kills'] - prev_metrics['total_kills']`, returns `delta * bonus_amount`
  - `calculate_episode_reward()` - returns 0.0 (step-level only)
  - `reset()` - no-op (no state)
- [x] Test component independently (mock metrics snapshots)

**Verification**: Component returns bonus only when kills increase, handles no kills gracefully

### Step 4: Implement ChunkExplorationBonus component

**Intent**: Reward movement across chunk boundaries (replaces movement chunk score logic)

**Implementation**:

- [ ] Create `interfaces/rewards/chunk_exploration.py`
- [ ] Implement `ChunkExplorationBonus(RewardComponent)` class
  - `__init__(chunk_size: float = 50.0, bonus_per_chunk: float = 1.0)` - configurable chunk size and bonus
  - Store `last_player_x`, `last_player_y` (internal state)
  - `calculate_step_reward()` - gets player position from `env_tracker.get_player()`, calculates distance moved, awards bonus per chunk if exceeds threshold
  - `calculate_episode_reward()` - returns 0.0 (step-level only)
  - `reset()` - resets `last_player_x`, `last_player_y` to None
- [ ] Test component independently (mock player position changes)

**Verification**: Component tracks position correctly, awards bonus only when threshold exceeded, resets properly

### Step 5: Implement AccuracyBonus component

**Intent**: Reward high accuracy with time-based bonus

**Implementation**:

- [ ] Create `interfaces/rewards/accuracy.py`
- [ ] Implement `AccuracyBonus(RewardComponent)` class
  - `__init__(bonus_per_second: float = 1.0, min_accuracy: float = 0.5)` - configurable bonus rate and threshold
  - `calculate_step_reward()` - gets accuracy from `metrics_tracker.get_accuracy()`, returns `bonus_per_second / 60.0` if above threshold, else 0.0
  - `calculate_episode_reward()` - returns 0.0 (step-level only)
  - `reset()` - no-op (no state)
- [ ] Test component independently (mock accuracy values)

**Verification**: Component returns bonus only when accuracy above threshold, handles zero shots gracefully

### Step 6: Implement NearMissBonus component

**Intent**: Reward getting close to asteroids without colliding

**Implementation**:

- [ ] Create `interfaces/rewards/near_miss.py`
- [ ] Implement `NearMissBonus(RewardComponent)` class
  - `__init__(safe_distance: float = 50.0, bonus_multiplier: float = 0.1)` - configurable distance threshold and multiplier
  - `calculate_step_reward()` - gets distance from `env_tracker.get_distance_to_nearest_asteroid()`, returns reward if distance < safe_distance (closer = more reward, but should be small)
  - `calculate_episode_reward()` - returns 0.0 (step-level only)
  - `reset()` - no-op (no state)
- [ ] Test component independently (mock distances)

**Verification**: Component returns reward when asteroids are close, handles None/empty asteroid list gracefully

### Step 7: Complete ComposableRewardCalculator implementation

**Intent**: Wire up step and episode reward calculation with metrics snapshots

**Implementation**:

- [x] Implement `calculate_step_reward()` in `ComposableRewardCalculator`
  - Create current metrics snapshot: `{'total_kills': metrics_tracker.total_kills, 'total_hits': metrics_tracker.total_hits, 'total_shots_fired': metrics_tracker.total_shots_fired, 'time_alive': metrics_tracker.time_alive}`
  - Iterate enabled components, call `calculate_step_reward()` with prev/current snapshots
  - Sum all contributions
  - Update `prev_metrics_snapshot` for next step
- [x] Implement `calculate_episode_reward()` in `ComposableRewardCalculator`
  - Iterate enabled components, call `calculate_episode_reward()`
  - Sum all contributions
- [x] Update `reset()` to reset `prev_metrics_snapshot` dict

**Verification**: Calculator sums component rewards correctly, handles empty component list, snapshots work for delta calculations

### Step 8: Remove score calculation from game core

**Intent**: Game no longer calculates score, only physics/simulation

**Implementation**:

- [ ] Remove `self.score += math.ceil(delta_time) / 10` from `Asteroids.py.on_update()` (line 125)
- [ ] Remove movement chunk score logic (lines 134-155) from `Asteroids.py.on_update()`
  - Keep movement tracking if needed, but remove score calculation
- [ ] Remove `self.score += 10` for asteroid kills (line 180) from `Asteroids.py.on_update()`
- [ ] Decide: keep `self.score` attribute for display, or remove entirely?
  - If keeping: can set to 0 or calculate from RewardCalculator for display
  - If removing: update score display code (lines 55, 119, 211)

**Verification**: Game runs without score calculation, no errors, score display either removed or shows 0/calculated value

### Step 9: Integrate RewardCalculator into training loop

**Intent**: AI wrappers use RewardCalculator instead of `game.score`

**Implementation**:

- [ ] In `train_agent.py` or wrapper initialization, create `ComposableRewardCalculator` instance
  - Add default components: `SurvivalBonus()`, `KillAsteroidBonus()`, `ChunkExplorationBonus()`
  - Enable all by default
- [ ] In `ai_agents/reinforcement_learning/gnn_and_sac/env_wrapper.py.step()`:
  - Remove `reward = self.game.score - prev_score` (line 127)
  - Call `reward_calculator.calculate_step_reward(env_tracker, metrics_tracker)`
  - Store calculator instance in `__init__` or pass as parameter
- [ ] Update episode end logic if needed (call `calculate_episode_reward()`)
- [ ] Call `reward_calculator.reset()` at episode start

**Verification**: Training loop receives rewards from calculator, rewards are non-zero, episodes work correctly

### Step 10: Integration testing

**Intent**: Verify entire system works end-to-end

**Implementation**:

- [ ] Test with all components enabled
- [ ] Test with some components disabled
- [ ] Test component toggling at runtime
- [ ] Verify rewards match expected behavior (survival, kills, movement, etc.)
- [ ] Test edge cases: no asteroids, no shots, player dies immediately

**Verification**: All tests pass, rewards are reasonable, system is stable

## Testing and Validation

**Unit Tests** (per component):

- [ ] Each component independently testable
- [ ] Edge cases: empty lists, zero metrics, None values
- [ ] Parameter validation (negative values, zero, etc.)
- [ ] State management (components with internal state reset correctly)

**Integration Tests**:

- [ ] `ComposableRewardCalculator` sums components correctly
- [ ] Metrics snapshots work for delta calculations
- [ ] Works with EnvironmentTracker and MetricsTracker
- [ ] Game no longer calculates score
- [ ] Training loops receive correct rewards
- [ ] Component enable/disable works at runtime

**Manual Testing**:

- [ ] Run game, verify no score calculation errors
- [ ] Run training loop, verify rewards are computed
- [ ] Toggle components, verify reward changes
- [ ] Verify rewards are reasonable (not NaN, not infinite, in expected range)

**Test Structure**:

- Create `tests/test_rewards/` directory
- `test_reward_component_base.py` - test base class
- `test_survival_bonus.py` - test SurvivalBonus
- `test_kill_asteroid_bonus.py` - test KillAsteroidBonus
- `test_chunk_exploration_bonus.py` - test ChunkExplorationBonus
- `test_accuracy_bonus.py` - test AccuracyBonus
- `test_near_miss_bonus.py` - test NearMissBonus
- `test_composable_calculator.py` - test ComposableRewardCalculator

## Risks and Failure Modes

**Reward Scale Issues:**

- **Risk**: Different components produce rewards at very different scales, leading to imbalance
- **Mitigation**: Use sensible defaults, document expected ranges, can add normalization later
- **Detection**: Monitor reward distributions, check if one component dominates

**Delta Calculation Errors:**

- **Risk**: Metrics snapshot timing issues, missing deltas, double-counting
- **Mitigation**: Snapshot metrics at consistent point in step, ensure calculator calls update() on trackers first
- **Detection**: Compare reward totals to expected values, log component contributions

**State Management:**

- **Risk**: Components with internal state (e.g., ChunkExplorationBonus) not reset properly
- **Mitigation**: Always call `reset()` on calculator at episode start, test reset thoroughly
- **Detection**: Run multiple episodes, verify state doesn't leak between episodes

**Performance:**

- **Risk**: Calculating rewards from many components every step is expensive
- **Mitigation**: Components should be efficient (no unnecessary calculations), profile if needed
- **Detection**: Profile reward calculation time, should be negligible compared to game update

**Integration Complexity:**

- **Risk**: Changing reward system breaks existing training loops
- **Mitigation**: Test thoroughly with existing wrappers, maintain backward compatibility where possible
- **Detection**: Integration tests, verify training still works

**Edge Cases:**

- **Risk**: Components crash on edge cases (no asteroids, no shots, etc.)
- **Mitigation**: All components handle None/empty gracefully, return 0.0 if not applicable
- **Detection**: Unit tests for edge cases, integration tests with minimal game state

## Exit Criteria

**Correctness:**

- [ ] All score logic removed from game core (`Asteroids.py`)
- [ ] Reward components compute correctly (unit tests pass)
- [ ] ComposableRewardCalculator sums components correctly
- [ ] No duplication of reward logic
- [ ] Edge cases handled gracefully (no crashes, returns 0.0 when appropriate)

**Integration:**

- [ ] Works with EnvironmentTracker and MetricsTracker
- [ ] Training loops use RewardCalculator (no direct `game.score` access)
- [ ] Component enable/disable works at runtime
- [ ] Reset works correctly (state doesn't leak between episodes)

**Code Quality:**

- [ ] All components follow RewardComponent interface
- [ ] Type hints and docstrings present
- [ ] Code is testable (components can be instantiated independently)
- [ ] No direct game access in reward components (only trackers)

**Functionality:**

- [ ] At least 5 reward components implemented (Survival, KillAsteroid, ChunkExploration, Accuracy, NearMiss)
- [ ] Components can be composed in any combination
- [ ] Rewards are reasonable (not NaN, not infinite, in expected ranges)
- [ ] System is ready for configuration integration (plan 006)

## Future Considerations

**Configuration Integration** (plan 006):

- Components defined and toggled via config files
- Component parameters (bonus amounts, thresholds) configurable via config
- Different reward configurations for different experiments

**Additional Components:**

- Efficiency bonus (kills per shot ratio)
- Combo bonuses (consecutive kills)
- Survival streak bonuses
- Distance traveled bonus (alternative to chunk exploration)
- Risk-taking bonus (more aggressive near miss calculation)

**Reward Analysis:**

- Historical reward tracking (per component, over time)
- Reward visualization/debugging tools
- Automatic reward function discovery
- Curriculum learning with reward shaping

**Optimization:**

- Reward normalization/scaling utilities
- Reward shaping utilities (e.g., reward clipping, discounting)
- Performance profiling and optimization if needed

**Testing:**

- Property-based testing for reward components
- Fuzzing reward calculations with random inputs
- Reward distribution analysis tools

---

**Status**: planned (waiting for plans 001-002 completion)

**Last Updated**: 2025-01-XX (refactored to component-based architecture)
