# Base Agent and Episode Infrastructure

## Implementation Strategy

**Incremental Approach - GA First:**

This plan establishes the shared infrastructure (BaseAgent interface and EpisodeRunner) that will be used by all AI methods. However, the initial implementation focuses on **Genetic Algorithms (GA) requirements only**. The infrastructure is designed to be extensible, allowing us to add support for other AI methods (ES, NEAT, GP, GNN) incrementally as each is implemented.

**Phase 1 (Current):** Implement infrastructure needed for GA:

- BaseAgent interface (designed to support all methods, but initially used by GA)
- EpisodeRunner (shared episode execution for GA)
- EpisodeResult data structure
- Integration with GA-specific components (VectorEncoder, etc.)

**Phase 2+ (Future):** As other AI methods are implemented:

- BaseAgent interface will be extended if needed (e.g., optional `update()` for RL methods)
- EpisodeRunner will work with all agent types without modification
- Additional agent types will implement BaseAgent interface

This approach allows us to:

- Get GA working quickly with proper shared infrastructure
- Validate the BaseAgent/EpisodeRunner design with real usage
- Evolve the infrastructure based on actual needs from GA implementation
- Ensure the shared infrastructure is solid before adding other methods

## Goal and Scope

**Deliverables:**

- `training/base/agent.py` - BaseAgent abstract base class
- `training/base/episode_runner.py` - EpisodeRunner for shared episode execution
- `training/base/episode_result.py` - EpisodeResult data structure
- `training/base/__init__.py` - Package initialization
- Refactored `train_agent.py` using new infrastructure
- Integration of all infrastructure components (EnvironmentTracker, MetricsTracker, RewardCalculator, StateEncoder, ActionInterface)

**Out of Scope:**

- Specific AI method implementations (separate plans, e.g., plan 007 for GA)
- Training dashboard (deferred until all AIs work)
- Advanced episode features (callbacks, hooks - future enhancement)
- Parallel episode execution (future enhancement)
- Episode replay/recording (future enhancement)

## Context and Justification

**Why Now:**

- GA implementation (plan 007) needs consistent agent interface
- Episode execution logic needs to be shared across all AI methods
- Need shared infrastructure for fair comparison (as other methods are added)
- Foundation for all AI implementations (starting with GA)
- All prerequisite infrastructure is complete (plans 001-004)

**What It Enables:**

- Consistent interface for all AI methods
- Shared episode execution (fair comparison across methods)
- Easy to add new AI methods (just implement BaseAgent)
- Clean separation: episode execution separate from learning
- Centralized integration point for all infrastructure components

**Rejected Alternatives:**

- **Per-method episode loops**: Inconsistent, harder to compare methods fairly
- **Direct game access in agents**: Too fragile, breaks when game changes
- **Keep legacy train_agent.py**: Doesn't use new infrastructure, inconsistent

**Key Requirements:**

- BaseAgent interface must support all AI methods (initially GA, extensible for others)
- EpisodeRunner must work with any BaseAgent (initially GA, extensible for others)
- Must use StateEncoder, ActionInterface, RewardCalculator (from plan 004)
- Must handle episode lifecycle (reset, step, done)
- Must integrate EnvironmentTracker and MetricsTracker (plans 001-002)
- Infrastructure must be extensible for future AI methods
- EpisodeRunner must manually step game (not rely on arcade scheduling)

## Interfaces and Contracts

### BaseAgent Interface

**Abstract Base Class:** `BaseAgent` (in `training/base/agent.py`)

```python
from abc import ABC, abstractmethod
from typing import List, Any

class BaseAgent(ABC):
    @abstractmethod
    def get_action(self, state: Any) -> List[float]:
        """
        Get action from encoded state.

        Args:
            state: Encoded state from StateEncoder (type depends on encoder:
                   List[float] for VectorEncoder, Data object for GraphEncoder, etc.)

        Returns:
            Action vector [left, right, thrust, shoot] in range [0.0, 1.0]
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """
        Reset agent state for new episode.

        For evolutionary agents (GA, ES, NEAT, GP), this is typically a no-op
        since they have no internal state. For RL agents, this may reset
        internal state (e.g., RNN hidden state).
        """
        pass

    # Optional method for RL agents (can be added in Phase 2+)
    # def update(self, state, action, reward, next_state, done) -> None:
    #     """Update agent based on experience (for RL methods)."""
    #     pass
```

**Invariants:**

- All agents implement `get_action(state)` (GA will be first)
- Actions are always in format `[left, right, thrust, shoot]` with values in [0.0, 1.0]
- Agents receive encoded state from StateEncoder (no direct game access)
- `reset()` is called at episode start (even if no-op for some agents)
- Interface is extensible for future agent types (optional methods can be added)

**Agent Types:**

- **Phase 1 (GA)**: GA agent implements `get_action()`, `reset()` (no-op)
- **Phase 2+ (Future)**: Other evolutionary agents (GP, ES, NEAT) will implement `get_action()`, `reset()` (no-op)
- **Phase 2+ (Future)**: RL agents (GNN+SAC) will implement `get_action()`, `reset()`, optional `update()`

### EpisodeRunner Interface

**Class:** `EpisodeRunner` (in `training/base/episode_runner.py`)

```python
from typing import TYPE_CHECKING, Optional
from Asteroids import AsteroidsGame
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker
from interfaces.RewardCalculator import ComposableRewardCalculator
from interfaces.StateEncoder import StateEncoder
from interfaces.ActionInterface import ActionInterface
from training.base.agent import BaseAgent
from training.base.episode_result import EpisodeResult

class EpisodeRunner:
    def __init__(
        self,
        game: AsteroidsGame,
        state_encoder: StateEncoder,
        action_interface: ActionInterface,
        reward_calculator: ComposableRewardCalculator,
        env_tracker: Optional[EnvironmentTracker] = None,
        metrics_tracker: Optional[MetricsTracker] = None
    ):
        """
        Initialize EpisodeRunner with game and infrastructure components.

        Args:
            game: AsteroidsGame instance
            state_encoder: StateEncoder instance (e.g., VectorEncoder for GA)
            action_interface: ActionInterface instance
            reward_calculator: ComposableRewardCalculator instance
            env_tracker: EnvironmentTracker instance (defaults to game.tracker)
            metrics_tracker: MetricsTracker instance (defaults to game.metrics_tracker)
        """
        self.game = game
        self.state_encoder = state_encoder
        self.action_interface = action_interface
        self.reward_calculator = reward_calculator
        self.env_tracker = env_tracker or game.tracker
        self.metrics_tracker = metrics_tracker or game.metrics_tracker

        # Frame rate for manual stepping (default 60 FPS)
        self.frame_delay = 1.0 / 60.0

    def run_episode(
        self,
        agent: BaseAgent,
        max_steps: int = 1000,
        render: bool = False
    ) -> EpisodeResult:
        """
        Run a single episode with the given agent.

        Episode lifecycle:
        1. Reset: game, trackers, agent, reward calculator
        2. Loop: observe → act → step → reward (until done)
        3. Collect: metrics, final reward, done reason

        Args:
            agent: BaseAgent instance to run episode with
            max_steps: Maximum number of steps before timeout
            render: Whether to render the episode (future: for visualization)

        Returns:
            EpisodeResult with episode statistics
        """
        # Reset everything
        self.game.reset_game()
        self.env_tracker.update(self.game)
        self.metrics_tracker.update(self.game)
        self.reward_calculator.reset()
        self.state_encoder.reset()
        agent.reset()

        total_reward = 0.0
        steps = 0
        done = False
        done_reason = "timeout"  # Default reason

        # Episode loop
        while not done and steps < max_steps:
            # Observe: encode current state
            state = self.state_encoder.encode(self.env_tracker)

            # Act: get action from agent
            action = agent.get_action(state)

            # Validate and normalize action
            self.action_interface.validate(action)
            action = self.action_interface.normalize(action)

            # Convert to game input format
            game_input = self.action_interface.to_game_input(action)

            # Apply action to game
            self.game.left_pressed = game_input["left_pressed"]
            self.game.right_pressed = game_input["right_pressed"]
            self.game.up_pressed = game_input["up_pressed"]
            self.game.space_pressed = game_input["space_pressed"]

            # Step game forward
            self.game.on_update(self.frame_delay)

            # Update trackers
            self.env_tracker.update(self.game)
            self.metrics_tracker.update(self.game)

            # Calculate reward
            step_reward = self.reward_calculator.calculate_step_reward(
                self.env_tracker,
                self.metrics_tracker
            )
            total_reward += step_reward

            steps += 1

            # Check done conditions
            if self.game.player not in self.game.player_list:
                # Player was removed (collision detected in on_update)
                done = True
                done_reason = "collision"

        # Calculate final episode reward (if any components have episode-level rewards)
        episode_reward = self.reward_calculator.calculate_episode_reward(
            self.metrics_tracker
        )
        total_reward += episode_reward

        # Collect metrics
        metrics = self.metrics_tracker.get_episode_stats()

        return EpisodeResult(
            total_reward=total_reward,
            steps=steps,
            metrics=metrics,
            done_reason=done_reason
        )
```

**Invariants:**

- Uses StateEncoder for observations (no direct game access)
- Uses ActionInterface for action validation and conversion
- Uses RewardCalculator for rewards (step and episode level)
- Uses EnvironmentTracker and MetricsTracker for state/metrics
- Manually steps game (calls `game.on_update()` directly)
- Handles all episode termination conditions (collision, timeout)
- Returns EpisodeResult with complete episode statistics

### EpisodeResult Data Structure

**Class:** `EpisodeResult` (in `training/base/episode_result.py`)

```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class EpisodeResult:
    """
    Data structure containing results from a single episode.
    """
    total_reward: float
    """Total reward accumulated during episode (step + episode rewards)."""

    steps: int
    """Number of steps taken in episode."""

    metrics: Dict[str, Any]
    """Episode metrics from MetricsTracker (accuracy, kills, time_alive, etc.)."""

    done_reason: str
    """Reason episode ended: 'collision', 'timeout', or 'manual'."""

    def __str__(self) -> str:
        """String representation for logging."""
        return (
            f"EpisodeResult(reward={self.total_reward:.2f}, "
            f"steps={self.steps}, "
            f"reason={self.done_reason}, "
            f"kills={self.metrics.get('total_kills', 0)}, "
            f"accuracy={self.metrics.get('accuracy', 0.0):.2%})"
        )
```

**Invariants:**

- All fields are populated after episode completes
- `total_reward` includes both step and episode-level rewards
- `metrics` contains all MetricsTracker statistics
- `done_reason` is one of: "collision", "timeout", "manual"

## Impacted Areas

**Files to Create:**

- `training/__init__.py` - Package initialization
- `training/base/__init__.py` - Base package initialization
- `training/base/agent.py` - BaseAgent abstract base class
- `training/base/episode_runner.py` - EpisodeRunner implementation
- `training/base/episode_result.py` - EpisodeResult data structure

**Files to Modify:**

- `train_agent.py` - Refactor to use EpisodeRunner (this is where all infrastructure from plans 001-004 gets integrated: MetricsTracker, RewardCalculator, StateEncoder, ActionInterface)
- All future AI trainers will use BaseAgent and EpisodeRunner

**Integration Responsibility:**

- Plan 005 is responsible for integrating all previous infrastructure into the training loop:
  - EnvironmentTracker and MetricsTracker (plans 001-002)
  - RewardCalculator (plan 003)
  - StateEncoder and ActionInterface (plan 004 - GA-focused: VectorEncoder)
- Plans 001-004 create the infrastructure but do NOT modify `train_agent.py` directly
- EpisodeRunner will orchestrate the full episode lifecycle using all these components
- Initially integrated for GA (plan 007), but designed to work with all future AI methods

**Dependencies:**

- Requires StateEncoder (plan 004) - ✅ Complete
- Requires ActionInterface (plan 004) - ✅ Complete
- Requires RewardCalculator (plan 003) - ✅ Complete
- Requires EnvironmentTracker and MetricsTracker (plans 001-002) - ✅ Complete

**No Schema/State Machine Changes:**

- Game entities unchanged
- No CLI/config changes (beyond refactoring train_agent.py)
- Action format unchanged (just standardized via ActionInterface)

## Incremental Implementation

### Step 1: Create training package structure

**Intent**: Establish package structure for training infrastructure

**Implementation:**

- [x] Create `training/` directory
- [x] Create `training/__init__.py` (empty or with package docstring)
- [x] Create `training/base/` directory
- [x] Create `training/base/__init__.py` (empty or with package docstring)

**Verification**: Can import `training.base` package

### Step 2: Implement EpisodeResult data structure

**Intent**: Create data structure for episode results

**Implementation:**

- [x] Create `training/base/episode_result.py`
- [x] Implement `EpisodeResult` dataclass with fields:
  - `total_reward: float`
  - `steps: int`
  - `metrics: Dict[str, Any]`
  - `done_reason: str`
- [x] Implement `__str__()` method for logging
- [x] Add docstrings and type hints

**Verification**: Can create EpisodeResult instances, all fields accessible, string representation works

### Step 3: Implement BaseAgent interface

**Intent**: Create abstract base class for all agents

**Implementation:**

- [x] Create `training/base/BaseAgent.py`
- [x] Implement `BaseAgent` abstract base class:
  - `@abstractmethod get_action(state: Any) -> List[float]`
  - `@abstractmethod reset() -> None`
- [x] Add comprehensive docstrings explaining:
  - State format (depends on encoder)
  - Action format (always [left, right, thrust, shoot])
  - When reset() is called
- [x] Add type hints

**Verification**: Can import BaseAgent, cannot instantiate (abstract), can create subclass

### Step 4: Implement EpisodeRunner

**Intent**: Create episode execution infrastructure

**Implementation:**

- [x] Create `training/base/episode_runner.py`
- [x] Implement `EpisodeRunner.__init__()`:
  - Store game, state_encoder, action_interface, reward_calculator
  - Store env_tracker and metrics_tracker (default to game.tracker, game.metrics_tracker)
  - Set frame_delay (default 1/60 for 60 FPS)
- [x] Implement `run_episode()`:
  - Reset: game.reset_game(), trackers.update(), reward_calculator.reset(), state_encoder.reset(), agent.reset()
  - Episode loop:
    - Encode state using state_encoder
    - Get action from agent
    - Validate and normalize action
    - Convert to game input
    - Apply to game (set left_pressed, etc.)
    - Step game (call game.on_update())
    - Update trackers
    - Calculate step reward
    - Check done conditions (collision, timeout)
  - Calculate episode reward
  - Collect metrics
  - Return EpisodeResult
- [x] Handle edge cases:
  - Player removed (collision)
  - Max steps reached (timeout)
  - Empty state encoding
  - Invalid actions
- [x] Add docstrings and type hints
- [x] Add logging (optional, for debugging)

**Verification**: EpisodeRunner can run episodes, returns EpisodeResult, handles all termination conditions

### Step 5: Create simple test agent

**Intent**: Create a simple agent for testing EpisodeRunner

**Implementation:**

- [ ] Create `training/base/test_agent.py` (or in tests/)
- [ ] Implement `TestAgent(BaseAgent)`:
  - Returns random actions for testing
  - Implements get_action() and reset()
- [ ] Use for testing EpisodeRunner

**Verification**: TestAgent works with EpisodeRunner, episodes complete successfully

### Step 6: Refactor train_agent.py

**Intent**: Integrate EpisodeRunner into training loop

**Implementation:**

- [ ] Read current `train_agent.py` structure
- [ ] Create new training loop using EpisodeRunner:
  - Initialize game
  - Create state_encoder (VectorEncoder for GA)
  - Create action_interface
  - Create reward_calculator (with components)
  - Create EpisodeRunner
  - For each episode:
    - Create agent (for now, use TestAgent or random)
    - Run episode using EpisodeRunner
    - Log results
- [ ] Remove legacy AIDriver class
- [ ] Remove direct arcade.schedule usage (EpisodeRunner handles stepping)
- [ ] Keep arcade.run() for rendering (if needed) or remove if headless training
- [ ] Add command-line arguments (optional):
  - Number of episodes
  - Max steps per episode
  - Render flag
- [ ] Add logging/progress tracking

**Verification**: Can run training loop, episodes execute correctly, results logged

### Step 7: Integration testing

**Intent**: Verify all infrastructure components work together

**Implementation:**

- [ ] Test with VectorEncoder (from plan 004)
- [ ] Test with ActionInterface (boolean and continuous modes)
- [ ] Test with RewardCalculator (all components enabled)
- [ ] Test with EnvironmentTracker and MetricsTracker
- [ ] Verify metrics are collected correctly
- [ ] Verify rewards are calculated correctly
- [ ] Verify episode termination works (collision, timeout)

**Verification**: All components integrate correctly, no errors, metrics/rewards accurate

### Step 8: Documentation and cleanup

**Intent**: Document usage and ensure code quality

**Implementation:**

- [ ] Add usage examples to docstrings
- [ ] Document episode lifecycle in EpisodeRunner docstring
- [ ] Document BaseAgent interface requirements
- [ ] Add type hints to all public methods
- [ ] Ensure code follows project standards
- [ ] Remove any debug/print statements (use logging)

**Verification**: Documentation is clear, code is clean and well-typed

## Testing and Validation

**Unit Tests:**

- [ ] BaseAgent: cannot instantiate (abstract), can create subclass, interface methods work
- [ ] EpisodeResult: can create instances, all fields accessible, string representation
- [ ] EpisodeRunner: initialization works, run_episode() executes correctly
- [ ] Episode lifecycle: reset works, step loop works, done conditions detected

**Integration Tests:**

- [ ] EpisodeRunner with TestAgent: episodes complete, results valid
- [ ] EpisodeRunner with VectorEncoder: state encoding works
- [ ] EpisodeRunner with ActionInterface: action conversion works
- [ ] EpisodeRunner with RewardCalculator: rewards calculated correctly
- [ ] EpisodeRunner with MetricsTracker: metrics collected correctly
- [ ] Episode termination: collision detected, timeout works

**Manual Testing:**

```python
# Test EpisodeRunner with simple agent
from Asteroids import AsteroidsGame, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from training.base.episode_runner import EpisodeRunner
from training.base.agent import BaseAgent
from interfaces.encoders.VectorEncoder import VectorEncoder
from interfaces.ActionInterface import ActionInterface
from interfaces.RewardCalculator import ComposableRewardCalculator
import random

class RandomAgent(BaseAgent):
    def get_action(self, state):
        return [random.random() for _ in range(4)]

    def reset(self):
        pass

# Setup
game = AsteroidsGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
game.setup()

state_encoder = VectorEncoder()
action_interface = ActionInterface("boolean")
reward_calculator = ComposableRewardCalculator()
# ... add reward components ...

episode_runner = EpisodeRunner(
    game=game,
    state_encoder=state_encoder,
    action_interface=action_interface,
    reward_calculator=reward_calculator
)

# Run episode
agent = RandomAgent()
result = episode_runner.run_episode(agent, max_steps=100)

print(result)
assert result.steps > 0
assert result.total_reward is not None
```

**Expected Signals:**

- Episodes run without errors
- EpisodeResult contains valid data
- Metrics are collected correctly
- Rewards are calculated correctly
- Episode termination works (collision, timeout)
- All infrastructure components integrate correctly

## Risks and Failure Modes

**Game Stepping Issues:**

- **Risk**: Manual stepping (game.on_update()) may not work correctly with arcade scheduling
- **Mitigation**: Ensure no arcade.schedule() calls interfere, test thoroughly
- **Detection**: Episodes don't progress, game state doesn't update

**Action Application Issues:**

- **Risk**: Actions not applied correctly to game (key states not set)
- **Mitigation**: Verify game_input conversion, test action application
- **Detection**: Agent actions don't affect game behavior

**State Encoding Issues:**

- **Risk**: State encoding fails or returns invalid format
- **Mitigation**: StateEncoder handles edge cases, validate encoding
- **Detection**: Agent receives invalid state, encoding errors

**Reward Calculation Issues:**

- **Risk**: Rewards not calculated correctly or at wrong time
- **Mitigation**: Verify RewardCalculator integration, test reward values
- **Detection**: Rewards are zero or incorrect, episode rewards not added

**Episode Termination Issues:**

- **Risk**: Episodes don't terminate correctly (infinite loops)
- **Mitigation**: Always check max_steps, verify collision detection
- **Detection**: Episodes run forever, timeout not working

**Tracker Update Issues:**

- **Risk**: Trackers not updated correctly, stale state
- **Mitigation**: Update trackers after game step, verify update() calls
- **Detection**: Metrics incorrect, state encoding uses stale data

**Performance Issues:**

- **Risk**: Episode execution too slow (encoding, stepping)
- **Mitigation**: Profile episode execution, optimize bottlenecks
- **Detection**: Episodes take too long, training is slow

## Exit Criteria

**Correctness:**

- [ ] BaseAgent interface implemented correctly (abstract, cannot instantiate)
- [ ] EpisodeRunner executes episodes correctly
- [ ] EpisodeResult contains all needed data
- [ ] Episode lifecycle works (reset, step, done)
- [ ] All termination conditions handled (collision, timeout)

**Integration:**

- [ ] Works with all infrastructure (EnvironmentTracker, MetricsTracker, RewardCalculator, StateEncoder, ActionInterface)
- [ ] EpisodeRunner integrates all components correctly
- [ ] Metrics collected correctly
- [ ] Rewards calculated correctly
- [ ] State encoding works
- [ ] Action conversion works

**Functionality:**

- [ ] Can run episodes with any BaseAgent
- [ ] Episodes terminate correctly
- [ ] EpisodeResult contains accurate statistics
- [ ] Training loop refactored to use EpisodeRunner
- [ ] Ready for GA implementation (plan 007)

**Code Quality:**

- [ ] All classes have comprehensive docstrings
- [ ] Type hints added to all public methods
- [ ] Code is testable (can create test agents)
- [ ] Follows project coding standards
- [ ] No direct game access in BaseAgent/EpisodeRunner (uses interfaces)

**Documentation:**

- [ ] `plans/README.md` updated with plan status
- [ ] `plans/ARCHITECTURE.md` updated with BaseAgent/EpisodeRunner
- [ ] Usage examples in docstrings
- [ ] Episode lifecycle documented

## Future Considerations

**Immediate Follow-ons:**

- GA implementation (plan 007) will use BaseAgent and EpisodeRunner
- Configuration system (plan 006) will configure EpisodeRunner components
- Test with real GA agent (after plan 007)

**Phase 2+ Enhancements:**

- **Episode callbacks/hooks**: Allow custom code to run at episode start/end
- **Parallel episode execution**: Run multiple episodes in parallel for faster training
- **Episode replay/recording**: Save and replay episodes for analysis
- **Advanced episode management**: Episode queues, prioritization, etc.
- **RL agent support**: Add optional `update()` method to BaseAgent for RL methods
- **Rendering support**: Add render flag to EpisodeRunner for visualization

**Advanced Features:**

- Episode statistics aggregation across multiple episodes
- Episode comparison utilities
- Episode visualization/debugging tools
- Performance profiling and optimization

---

**Status**: planned

**Dependencies:**

- Plans 001-004 must be complete before starting this plan
- All infrastructure components must be implemented and tested

**Implementation Phases:**

- **Phase 1 (Current)**: GA-focused implementation (BaseAgent for GA, EpisodeRunner for GA)
- **Phase 2+ (Future)**: Additional agent types will implement BaseAgent as other AI methods are added

**Last Updated**: 2025-01-XX
