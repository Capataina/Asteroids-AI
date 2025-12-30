# Base Agent and Episode Infrastructure

## Goal and Scope

**Deliverables:**

- `training/base/BaseAgent` interface
- `training/base/EpisodeRunner` shared episode execution
- Episode lifecycle management
- EpisodeResult data structure
- Refactored training loop using new infrastructure

**Out of Scope:**

- Specific AI method implementations (separate plans)
- Training dashboard (after all AIs work)
- Advanced episode features (callbacks, hooks - future enhancement)

## Context and Justification

**Why Now:**

- All 5 AI methods need consistent agent interface
- Episode execution logic is duplicated
- Need shared infrastructure for fair comparison
- Foundation for all AI implementations

**What It Enables:**

- Consistent interface for all AI methods
- Shared episode execution (fair comparison)
- Easy to add new AI methods
- Clean separation: episode execution separate from learning

**Key Requirements:**

- BaseAgent interface must support all 5 AI methods
- EpisodeRunner must work with any BaseAgent
- Must use StateEncoder, ActionInterface, RewardCalculator
- Must handle episode lifecycle (reset, step, done)

## Interfaces and Contracts

### BaseAgent Interface

**Core Methods:**
- `get_action(state) -> action` - Get action from state (all methods implement)
- `reset()` - Reset agent state (for episodic resets)
- `update(...)` - Optional, for RL methods that learn per-step

**Agent Types:**

- **Evolutionary Agents** (GA, GP, ES, NEAT): Implement `get_action()`, `reset()`
- **RL Agents** (GNN+SAC): Implement `get_action()`, `reset()`, `update()`

**Invariants:**

- All agents implement `get_action(state)`
- Actions are in standard format (via ActionInterface)
- Agents use StateEncoder for state representation

### EpisodeRunner

**Core Methods:**
- `run_episode(agent, max_steps, state_encoder, reward_calculator) -> EpisodeResult`
- Handles: reset → loop(observe → act → step → reward) → done

**EpisodeResult:**

- `total_reward` - Episode reward
- `steps` - Number of steps
- `metrics` - MetricsTracker stats
- `done_reason` - Why episode ended (collision, timeout, etc.)

**Invariants:**

- Uses StateEncoder for observations
- Uses ActionInterface for actions
- Uses RewardCalculator for rewards
- Uses EnvironmentTracker and MetricsTracker

## Impacted Areas

**Files to Create:**

- `training/base/agent.py` (BaseAgent)
- `training/base/episode_runner.py` (EpisodeRunner)
- `training/base/episode_result.py` (EpisodeResult data structure)

**Files to Modify:**

- `train_agent.py` - Refactor to use EpisodeRunner (this is where all infrastructure from plans 001-004 gets integrated: MetricsTracker, RewardCalculator, StateEncoder, ActionInterface)
- All future AI trainers will use BaseAgent and EpisodeRunner

**Integration Responsibility:**

- Plan 005 is responsible for integrating all previous infrastructure into the training loop:
  - EnvironmentTracker and MetricsTracker (plans 001-002)
  - RewardCalculator (plan 003)
  - StateEncoder and ActionInterface (plan 004)
- Plans 002-004 create the infrastructure but do NOT modify `train_agent.py` directly
- EpisodeRunner will orchestrate the full episode lifecycle using all these components

**Dependencies:**

- Requires StateEncoder (plan 004)
- Requires ActionInterface (plan 004)
- Requires RewardCalculator (plan 003)
- Requires EnvironmentTracker and MetricsTracker (plans 001-002)

## Implementation Notes

**BaseAgent Design:**

- Abstract base class or protocol
- Minimal interface (just what's needed)
- Optional methods for RL (update, etc.)
- All 5 AI methods will implement this

**EpisodeRunner Design:**

- Takes any BaseAgent
- Uses shared interfaces (StateEncoder, etc.)
- Handles episode lifecycle
- Returns EpisodeResult

**Episode Lifecycle:**

- Reset: game, trackers, agent, reward calculator
- Step loop: observe → act → step → reward
- Done conditions: collision, timeout, manual stop
- Cleanup: collect metrics, return result

## Testing and Validation

**Unit Tests:**

- BaseAgent interface
- EpisodeRunner with mock agent
- EpisodeResult structure
- Episode lifecycle

**Integration Tests:**

- Works with all interfaces
- Episode execution correct
- Metrics collected properly

## Exit Criteria

**Correctness:**

- BaseAgent interface works
- EpisodeRunner executes correctly
- EpisodeResult contains all needed data

**Integration:**

- Works with all previous plans
- Training loop refactored
- Ready for AI implementations

## Future Considerations

**Follow-ons:**

- Episode callbacks/hooks
- Parallel episode execution
- Episode replay/recording
- Advanced episode management

---

**Note:** This is a skeleton plan file. Once plans 001-004 are completed, this plan will be expanded into a full implementation plan with detailed steps, interface specifications, and risk analysis.

