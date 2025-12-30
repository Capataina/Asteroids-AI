# MetricsTracker Implementation

## Goal and Scope

**Deliverables:**

- `interfaces/MetricsTracker`: Class tracking aggregated statistics over episode/lifetime
- Episode-level metrics (accuracy, kills, shots, time alive)
- Rate calculations (shots per second, kills per minute)
- Episode summary functionality
- Integration with EnvironmentTracker for data source

**Out of Scope:**

- Per-tick event detection (handled by EnvironmentTracker)
- Reward calculation (separate plan)
- Historical metrics across multiple episodes (future enhancement)

## Context and Justification

**Why Now:**

- EnvironmentTracker provides current state, but we need aggregated episode statistics
- AI methods need episode-level metrics for fitness evaluation and comparison
- Reward functions will use metrics for shaping (accuracy bonuses, efficiency rewards)
- All 5 AI methods will need consistent metrics for fair comparison

**What It Enables:**

- Episode-level statistics without modifying game code
- Consistent metrics across all AI methods
- Foundation for reward shaping experiments
- Easy comparison of agent performance

**Key Requirements:**

- Must aggregate from EnvironmentTracker events
- Must reset on episode start
- Must compute rates from totals and time
- Must handle edge cases (no shots fired, zero time, etc.)

## Interfaces and Contracts

### MetricsTracker Interface

**Core Methods:**

- `reset()` - Clear all counters (called at episode start)
- `update(env_tracker)` - Aggregate from EnvironmentTracker events
- `get_total_shots_fired()` - Total shots in episode
- `get_total_hits()` - Total successful hits
- `get_total_kills()` - Total asteroids destroyed
- `get_accuracy()` - hits / shots_fired (or 0.0 if no shots)
- `get_time_alive()` - Episode duration in seconds
- `get_episode_duration()` - Episode duration in ticks
- `get_shots_per_second()` - Rate calculation
- `get_kills_per_minute()` - Rate calculation
- `get_episode_stats()` - Dictionary of all metrics

**Invariants:**

- `reset()` clears all counters
- `update()` aggregates from `env_tracker` events
- Rates computed from totals / time_alive
- All methods handle edge cases gracefully

## Impacted Areas

**Files to Create:**

- `interfaces/MetricsTracker.py`

**Files to Modify:**

- `Asteroids.py` - Initialize MetricsTracker, call reset on episode start
- **Note**: `train_agent.py` integration is deferred to plan 005 (BaseAgent/EpisodeRunner infrastructure). MetricsTracker will be integrated via EpisodeRunner, not directly into current `train_agent.py`.

**Dependencies:**

- Requires EnvironmentTracker to be complete (event detection working)
- Will be used by RewardCalculator (next plan)

## Implementation Notes

**Event Aggregation:**

- MetricsTracker observes EnvironmentTracker events
- Tracks cumulative statistics over episode
- Computes derived metrics (rates, ratios)

**Reset Behavior:**

- Must be called at episode start
- Clears all counters to zero
- Prepares for new episode

**Edge Cases:**

- No shots fired → accuracy = 0.0 (not division by zero)
- Zero time → rates = 0.0
- Empty asteroid list → kills = 0

## Testing and Validation

**Unit Tests:**

- Counter accumulation
- Accuracy calculation (including edge cases)
- Reset behavior
- Rate calculations

**Integration Tests:**

- Works with EnvironmentTracker
- Resets correctly on episode start
- Metrics match expected values

## Exit Criteria

**Correctness:**

- All metrics accumulate correctly
- Edge cases handled
- Reset works properly
- Rates computed correctly

**Integration:**

- Works with EnvironmentTracker
- Integrates with game update loop
- Ready for RewardCalculator use

## Future Considerations

**Follow-ons:**

- Historical metrics (across multiple episodes)
- Rolling averages
- Percentile calculations
- Export metrics to file for analysis

---

**Note:** This is a skeleton plan file. Once plan 001 (EnvironmentTracker) is completed, this plan will be expanded into a full implementation plan with detailed steps, verification criteria, and risk analysis.
