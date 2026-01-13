# Shared Training Components

## Scope / Purpose

This document covers generic training components that apply to **all AI methods** (GA, ES, NEAT, RL, etc.) regardless of their optimization approach. These components encourage human-like play patterns and prevent degenerate strategies that exploit single reward sources or repetitive action patterns.

The goal is to produce agents that:
- Utilize all aspects of gameplay (shooting, dodging, positioning)
- Exhibit varied, context-appropriate behavior
- Generalize well to unseen scenarios
- Resist convergence to simplistic local minima

---

## Current Implemented System

### Existing Infrastructure (Available for Novelty Systems)

The following metrics are already collected per agent during evaluation (`training/core/population_evaluator.py`):

| Metric | Type | Description |
|--------|------|-------------|
| `thrust_frames` | int | Number of frames where thrust was active |
| `turn_frames` | int | Number of frames where left/right rotation was active |
| `shoot_frames` | int | Number of frames where shoot was active |
| `idle_rate` | float | Proportion of frames with no input |
| `accuracy` | float | Hits / shots fired |
| `avg_asteroid_dist` | float | Average distance to nearest asteroid |
| `screen_wraps` | int | Number of times agent crossed screen boundary |
| `position_history` | list | Sampled (x, y) positions throughout episode |
| `reward_breakdown` | dict | Per-component reward totals |

These metrics are **reward-agnostic** and describe observable behavior regardless of what reward preset is active.

### Behavior Novelty System (Implemented)

Located in `training/components/novelty.py`:

- **`compute_behavior_vector(metrics, steps)`**: Converts agent metrics into a 7-dimensional normalized behavior vector representing action patterns.
- **`compute_behavior_novelty(behavior, population, archive, k)`**: Calculates novelty as average distance to k-nearest neighbors in behavior space.
- **`compute_population_novelty(population, archive, k)`**: Batch novelty computation for entire population.

### Reward Diversity System (Implemented)

Located in `training/components/diversity.py`:

- **`compute_reward_diversity(reward_breakdown)`**: Shannon entropy-based diversity score measuring how evenly rewards are distributed across components. Returns 0-1 where 1 = perfectly balanced.
- **`compute_population_diversity_stats(breakdowns)`**: Population-level diversity statistics.
- **`get_reward_balance_warnings(breakdown)`**: Analyzes reward breakdown and returns warnings about imbalances.

### Behavior Archive (Implemented)

Located in `training/components/archive.py`:

- **`BehaviorArchive`**: Maintains historical archive of novel behaviors encountered during training.
  - `maybe_add(behavior, population)`: Add behavior if novelty exceeds threshold.
  - `add_batch(behaviors, novelty_scores)`: Batch addition based on pre-computed scores.
  - Configurable max size with random eviction when full.

### Combined Selection Scoring (Implemented)

Located in `training/components/selection.py`:

- **`compute_selection_score(fitness, novelty, diversity, config)`**: Combines fitness, behavior novelty, and reward diversity into a single selection score.
- **`compute_population_selection_scores(...)`**: Batch computation for population.

### Novelty Configuration (Implemented)

Located in `training/config/novelty.py`:

- **`NoveltyConfig`**: Dataclass containing all novelty/diversity parameters.
  - `enable_behavior_novelty`: Toggle behavior novelty (default: True)
  - `enable_reward_diversity`: Toggle reward diversity (default: True)
  - `behavior_novelty_weight`: Weight in selection (default: 0.15)
  - `diversity_weight`: Weight in selection (default: 0.2)
  - Preset methods: `disabled()`, `novelty_only()`, `diversity_only()`, `aggressive()`

### GA Integration (Implemented)

- `population_evaluator.py`: Now computes `behavior_vector` and `reward_diversity` per agent.
- `driver.py`: `GADriver` accepts `NoveltyConfig`, maintains `BehaviorArchive`, and uses combined selection scores.
- `train_ga.py`: Passes `per_agent_metrics` to `evolve()` for novelty/diversity calculation.

---

## Implemented Outputs / Artifacts

- **Per-agent metrics** now include `behavior_vector` and `reward_diversity` fields.
- **GA evolution stats** now include `avg_novelty`, `avg_diversity`, and `archive_size`.

---

## In Progress / Partially Implemented

- [ ] Analytics integration: Add novelty/diversity metrics to training reports and visualizations.

---

## Planned / Missing / To Be Changed

### Future Enhancements

- [ ] **Analytics integration**: Add novelty/diversity metrics to markdown reports and visualizations.
- [ ] **ES integration**: Ensure Evolution Strategies uses novelty/diversity when implemented.
- [ ] **NEAT integration**: Ensure NEAT uses novelty/diversity when implemented.
- [ ] **Adaptive thresholds**: Automatically adjust novelty threshold based on archive fill rate.
- [ ] **Behavior clustering**: Group similar behaviors to identify distinct strategies.

---

## Notes / Design Considerations

### Why Both Novelty Types?

| Novelty Type | What It Prevents | What It Encourages |
|--------------|------------------|-------------------|
| **Behavior Novelty** | Population convergence to identical action patterns | Exploration of different play styles |
| **Reward Diversity** | Single-reward exploitation | Well-rounded gameplay using all mechanics |

They address different failure modes:
- Behavior novelty prevents everyone copying the "best" strategy.
- Reward diversity prevents that "best" strategy from being one-dimensional.

### Reward-Agnostic Design

Both systems are designed to work with **any reward preset**:
- Behavior vectors use raw action counts and spatial metrics, not reward values.
- Reward diversity uses entropy over whatever components are active, adapting automatically.

Changing `training/config/rewards.py` does not require changes to novelty systems.

### Computational Cost

- Behavior novelty requires O(n*k) distance calculations per agent (n = population + archive size).
- Reward diversity is O(c) per agent where c = number of reward components.
- Both are negligible compared to episode simulation time.

### Human-Like Play

The combination pushes agents toward human-like play:
- Humans don't repeat the same input sequence forever (behavior novelty).
- Humans engage with all game mechanics, not just survival (reward diversity).
- Humans exhibit varied strategies based on context.

### Tuning Considerations

- If `behavior_novelty_weight` is too high, agents may explore useless behaviors.
- If `diversity_weight` is too high, weak generalists may beat strong specialists.
- Start with low weights (0.1-0.2) and increase if convergence remains problematic.

---

## Discarded / Obsolete / No Longer Relevant

- None yet. This is a new planned component.
