# Shared Training Components (Novelty & Diversity)

## Scope / Purpose

This document covers training components designed to be reusable across **all optimization methods** (GA now, ES/NEAT later). These components encourage human-like play and reduce convergence to degenerate local minima by shaping selection pressure using behavior novelty and reward diversity signals in addition to raw fitness.

## Current Implemented System

### Implemented Modules (Implemented)

| Module           | File                               | Granular Responsibility                                                                             |
| ---------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------- |
| Behavior vector  | `training/components/novelty.py`   | Converts per-agent metrics into a normalized 7D behavior vector and computes kNN novelty distances. |
| Reward diversity | `training/components/diversity.py` | Computes entropy-based reward diversity score from per-agent reward breakdown dictionaries.         |
| Behavior archive | `training/components/archive.py`   | Maintains a bounded archive of historically novel behaviors for novelty distance comparisons.       |
| Selection score  | `training/components/selection.py` | Combines fitness + novelty + diversity into a single scalar score for parent selection.             |
| Configuration    | `training/config/novelty.py`       | Provides weights and archive parameters via `NoveltyConfig`.                                        |

### Inputs Required From Evaluation (Implemented)

The novelty/diversity system is based on **reward-agnostic** behavior signals and the per-agent reward breakdown:

| Input Signal        | Source (Current)                        | Meaning                                                         |
| ------------------- | --------------------------------------- | --------------------------------------------------------------- |
| `thrust_frames`     | `training/core/population_evaluator.py` | How often the agent thrusts (movement tendency).                |
| `turn_frames`       | `training/core/population_evaluator.py` | How often the agent turns (rotation tendency).                  |
| `shoot_frames`      | `training/core/population_evaluator.py` | How often the agent shoots (aggression).                        |
| `accuracy`          | `training/core/population_evaluator.py` | Hits/shots (precision proxy).                                   |
| `idle_rate`         | `training/core/population_evaluator.py` | Fraction of frames with no input (passivity proxy).             |
| `avg_asteroid_dist` | `training/core/population_evaluator.py` | Engagement distance proxy (how close it stays to threats).      |
| `screen_wraps`      | `training/core/population_evaluator.py` | Area coverage proxy (how much it traverses the toroidal world). |
| `reward_breakdown`  | `training/core/population_evaluator.py` | Per-component reward totals used for diversity entropy.         |

### Behavior Vector (Implemented)

`training/components/novelty.py:compute_behavior_vector(metrics, steps)` produces a 7D vector with each element normalized to `0..1`:

- Thrust rate: `thrust_frames / steps` (clamped).
- Turn rate: `turn_frames / steps` (clamped).
- Shoot rate: `shoot_frames / steps` (clamped).
- Accuracy: `accuracy` (clamped).
- Idle rate: `idle_rate` (clamped).
- Engagement distance: `avg_asteroid_dist / 400` (clamped).
- Screen coverage: `screen_wraps / 20` (clamped).

### Novelty Scoring (Implemented)

- `compute_behavior_novelty(behavior, population, archive, k)`:
  - Computes Euclidean distances to other population behaviors plus archive behaviors.
  - Returns average distance to the `k` nearest neighbors.
- `compute_population_novelty(population, archive, k)`:
  - Computes novelty for each agent while excluding itself from population comparisons.

### Reward Diversity Scoring (Implemented)

`training/components/diversity.py:compute_reward_diversity(reward_breakdown)`:

- Considers only **positive reward components** (penalties are excluded from entropy).
- Returns `0.0` when:
  - There is no reward breakdown,
  - Total positive reward is `<= 0`,
  - There is only 1 positive reward source (no diversity possible).
- Otherwise returns Shannon entropy normalized to `0..1` by maximum entropy of the positive components.

### Behavior Archive (Implemented)

`training/components/archive.py:BehaviorArchive`:

- Stores `behaviors: List[List[float]]` up to `max_size`.
- Adds behaviors when novelty score exceeds `novelty_threshold`.
- Evicts by random replacement when full.
- Exposes `get_behaviors()` for distance calculations and `size()` for monitoring.

### Combined Selection Score (Implemented)

`training/components/selection.py:compute_selection_score(fitness, novelty, diversity, config)`:

- Base score starts as raw `fitness`.
- Novelty bonus (when enabled):
  - `behavior_novelty_weight * novelty * novelty_fitness_scale`
- Diversity bonus (when enabled):
  - `diversity_weight * reward_diversity * max(1, abs(fitness))`

### GA Integration (Implemented)

| Integration Point             | File                                              | Granular Behavior                                                                                                           |
| ----------------------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Behavior/diversity extraction | `training/core/population_evaluator.py`           | Computes `behavior_vector` and `reward_diversity` per agent (averaged across seeds).                                        |
| Archive + novelty scoring     | `training/methods/genetic_algorithm/driver.py`    | Computes population novelty vs archive, updates archive, and builds combined selection scores.                              |
| Parent selection              | `training/methods/genetic_algorithm/selection.py` | Tournament selection uses the combined selection scores (not raw fitness).                                                  |
| Operator stats passthrough    | `training/methods/genetic_algorithm/driver.py`    | Records `avg_novelty`, `avg_diversity`, `archive_size` into `last_evolution_stats` (merged into analytics generation data). |

## Implemented Outputs / Artifacts (if applicable)

- In-memory per-agent novelty inputs:
  - `behavior_vector` (7D) and `reward_diversity` (scalar) are produced during evaluation and passed into `GADriver.evolve(...)`.
- Per-generation operator fields (recorded into analytics when provided):
  - `avg_novelty`, `avg_diversity`, `archive_size` (plus `crossover_events`, `mutation_events`, `elite_count`).

## In Progress / Partially Implemented

- [ ] Analytics reporting integration: `avg_novelty/avg_diversity/archive_size` are stored in generation data, but the markdown report does not yet visualize them.
- [ ] Novelty/diversity distributions: Analytics exports do not currently include distributions of `reward_diversity` or any per-dimension `behavior_vector` statistics.
- [ ] `NoveltyConfig.normalize_scores`: Configuration flag exists but is not currently used in selection score computation (scores are combined in raw scale).
- [ ] `NoveltyConfig.min_positive_components`: Configuration value exists but is not explicitly enforced by selection scoring (diversity returns 0.0 for <=1 positive component implicitly).

## Planned / Missing / To Be Changed

- [ ] Add report sections for novelty/diversity: Visualize archive growth, novelty trends, and diversity trends alongside fitness.
- [ ] Adaptive archive threshold: Adjust novelty threshold dynamically based on archive fill rate and population novelty statistics.
- [ ] Behavior clustering: Cluster behavior vectors to identify distinct strategies and track their population share over time.
- [ ] Extend behavior characterization: Add additional behavior dimensions (e.g., risk appetite, ray hit distribution summaries) while maintaining normalization.
- [ ] Method parity integration: Ensure ES/NEAT selection/update logic can reuse the same novelty/diversity signals for fair comparison.

## Notes / Design Considerations (optional)

- Novelty and diversity address different failure modes:
  - Behavior novelty discourages population collapse into identical action patterns.
  - Reward diversity discourages single-component reward exploitation.
- Both systems are designed to be reward-preset agnostic:
  - Behavior novelty uses action/engagement metrics independent of reward values.
  - Diversity uses entropy over whatever reward components are active.

## Discarded / Obsolete / No Longer Relevant

- State encoder designs are documented in `plans/STATE_REPRESENTATION.md`; this shared-components plan focuses strictly on method-agnostic training/selection components.
