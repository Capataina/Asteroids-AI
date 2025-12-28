# Reward System Abstraction

## Goal and Scope

**Deliverables:**

- `interfaces/RewardCalculator` base class and interface
- Multiple reward function implementations (Survival, Accuracy, Aggression, Risk, Hybrid)
- Removal of score calculation from game core
- Integration with EnvironmentTracker and MetricsTracker
- Swappable reward functions for experimentation

**Out of Scope:**

- Specific reward function formulas (will be refined during implementation)
- Historical reward tracking (future enhancement)
- Reward visualization (future enhancement)

## Context and Justification

**Why Now:**

- Score calculation currently embedded in game logic (Asteroids.py)
- AI wrappers duplicate reward logic (env_wrapper.py modifies score directly)
- Need swappable reward functions for experimentation
- All 5 AI methods need consistent reward interface
- Reward shaping is a first-class experimental variable (per README)

**What It Enables:**

- Game core focuses only on physics/simulation
- Easy experimentation with different reward functions
- No duplication of reward logic
- Clean separation: game → tracker → reward → AI
- Foundation for reward shaping experiments

**Key Requirements:**

- Must use EnvironmentTracker and MetricsTracker as inputs
- Must support both step-level and episode-level rewards
- Must be swappable without modifying game or AI code
- Must handle edge cases gracefully

## Interfaces and Contracts

### RewardCalculator Base Interface

**Core Methods:**

- `calculate_step_reward(env_tracker, metrics_tracker, prev_state, current_state)` - Per-step reward
- `calculate_episode_reward(metrics_tracker)` - Episode-level reward
- `reset()` - Reset any internal state (called at episode start)

**Reward Function Types:**

1. **SurvivalReward** - Time-based rewards, survival focus
2. **AccuracyReward** - Hits/shots ratio focus, efficiency emphasis
3. **AggressionReward** - Kill-focused, rewards destruction
4. **RiskReward** - Near-miss focused, rewards close encounters
5. **HybridReward** - Weighted combination of multiple reward types

**Invariants:**

- Reward functions are pure (no side effects)
- Use only EnvironmentTracker and MetricsTracker as inputs
- Handle edge cases (empty lists, zero metrics, etc.)

## Impacted Areas

**Files to Create:**

- `interfaces/RewardCalculator.py` (base class)
- `interfaces/rewards/` directory with individual reward functions:
  - `survival.py`
  - `accuracy.py`
  - `aggression.py`
  - `risk.py`
  - `hybrid.py`

**Files to Modify:**

- `Asteroids.py` - Remove score calculation logic, optionally use RewardCalculator for display
- `ai_agents/reinforcement_learning/gnn_and_sac/env_wrapper.py` - Remove score modification, use RewardCalculator
- `train_agent.py` - Integrate RewardCalculator into training loop

**Dependencies:**

- Requires EnvironmentTracker (complete)
- Requires MetricsTracker (plan 002)
- Will be used by all AI methods

## Implementation Notes

**Score Removal:**

- Extract all score logic from `Asteroids.py.on_update()`
- Current score sources: survival time, movement distance, asteroid kills
- Move to appropriate RewardCalculator implementations

**Reward Function Design:**

- Each reward function should be independently testable
- Formulas can be refined during implementation
- Should support configurable weights/parameters

**Integration:**

- RewardCalculator used by training loops, not game core
- Game can optionally display reward for debugging
- AI methods receive rewards from RewardCalculator

## Testing and Validation

**Unit Tests:**

- Each reward function independently
- Edge cases (no events, zero metrics)
- Reward scaling and normalization

**Integration Tests:**

- Works with EnvironmentTracker and MetricsTracker
- Game no longer calculates score
- Training loops receive correct rewards

## Exit Criteria

**Correctness:**

- All score logic removed from game
- Reward functions compute correctly
- No duplication of reward logic

**Integration:**

- Works with tracking infrastructure
- Ready for AI method use
- Swappable reward functions work

## Future Considerations

**Follow-ons:**

- More reward function types
- Reward visualization/debugging
- Historical reward analysis
- Automatic reward function discovery
- Curriculum learning with reward shaping

---

**Note:** This is a skeleton plan file. Once plans 001 (EnvironmentTracker) and 002 (MetricsTracker) are completed, this plan will be expanded into a full implementation plan with detailed steps, reward function specifications, and risk analysis.
