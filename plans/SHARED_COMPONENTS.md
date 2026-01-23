# Shared Training Components (Novelty & Diversity)

## Scope / Purpose

This document covers training components designed to be reusable across **evolutionary / selection-based optimization methods** (GA now, ES/NEAT later). These components encourage human-like play and reduce convergence to degenerate local minima by shaping **selection pressure** using behavior novelty and reward diversity signals in addition to raw fitness.

- RL note: SAC-based RL does not use these signals for gradient updates, but it can still log compatible behavioral metrics for analysis and comparability.

## Current Implemented System

### Implemented Modules (Implemented)

| Module           | File                               | Granular Responsibility                                                                             |
| ---------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------- |
| Behavior vector  | `training/components/novelty.py`   | Converts per-agent metrics into a normalized 7D behavior vector and computes kNN novelty distances. |
| Reward diversity | `training/components/diversity.py` | Computes entropy-based reward diversity score from per-agent reward breakdown dictionaries.         |
| Behavior archive | `training/components/archive.py`   | Maintains a bounded archive of historically novel behaviors for novelty distance comparisons.       |
| Selection score  | `training/components/selection.py` | Combines fitness + novelty + diversity into a single scalar score for parent selection.             |
| Configuration    | `training/config/novelty.py`       | Provides weights and archive parameters via `NoveltyConfig`.                                        |

### Pareto Objective Modules (Implemented)

| Module | File | Granular Responsibility |
| --- | --- | --- |
| Pareto config | `training/config/pareto.py` | Defines objective list and accuracy threshold for Pareto ranking. |
| Objective extraction | `training/components/pareto/objectives.py` | Builds per-candidate objective vectors (`kills`, `time_alive`, `softmin_ttc`, `accuracy`). |
| Pareto ranking | `training/components/pareto/ranking.py` | Computes Pareto fronts and crowding distance. |
| Pareto ordering | `training/components/pareto/utility.py` | Orders candidates by Pareto front + crowding for method adapters. |

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

### Pareto Inputs (Implemented)

| Input Signal | Source (Current) | Meaning |
| --- | --- | --- |
| `hits` | `training/core/population_evaluator.py` | Total bullet hits per episode (averaged across seeds). |
| `kills` | `training/core/population_evaluator.py` | Total kills per episode (averaged across seeds). |
| `time_alive` | `training/core/population_evaluator.py` | Time alive per episode (seconds, averaged). |
| `accuracy` | `training/core/population_evaluator.py` | Hits/shots ratio with minimum-shot threshold handling. |
| `softmin_ttc` | `training/core/population_evaluator.py` | Soft-min time-to-collision proxy that weights all asteroids (seconds, averaged). |

- `softmin_ttc` blends all asteroid TTCs using an exponential weighting so the closest threat dominates without ignoring others.

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
- [ ] ES parity of scoring semantics: GA uses `compute_selection_score(...)` with fitness-relative scaling, while ES applies novelty/diversity bonuses scaled by fitness spread (stddev with a floor) pre-rank-shaping in `training/methods/evolution_strategies/driver.py:_apply_novelty_diversity(...)`.
- [ ] ES bonus-scale validation: ES rank transformation discards magnitude information, so novelty/diversity bonus weights must be tuned with shaping behavior in mind (currently enabled in `ESConfig`).

## Planned / Missing / To Be Changed

- [ ] Add report sections for novelty/diversity: Visualize archive growth, novelty trends, and diversity trends alongside fitness.
- [ ] Adaptive archive threshold: Adjust novelty threshold dynamically based on archive fill rate and population novelty statistics.
- [ ] Adaptive novelty-weight schedule: Adjust `NoveltyConfig.behavior_novelty_weight` based on behavior collapse signals (e.g., low population novelty, low action entropy).
- [ ] Adaptive diversity-weight schedule: Adjust `NoveltyConfig.diversity_weight` based on reward concentration signals (high dominance / low entropy).
- [ ] Adaptive novelty scaling: Adjust `NoveltyConfig.novelty_fitness_scale` so novelty bonuses remain rank-effective under changing fitness magnitudes.
- [ ] Adaptive k-nearest schedule: Adjust `NoveltyConfig.k_nearest` based on population size and archive density (stability vs sensitivity).
- [ ] Adaptive archive capacity schedule: Adjust `NoveltyConfig.archive_max_size` based on run length to avoid early saturation.
- [ ] Behavior clustering: Cluster behavior vectors to identify distinct strategies and track their population share over time.
- [ ] Extend behavior characterization (turn asymmetry): Add left-only/right-only/both-turn rates as explicit behavior dimensions to detect and penalize one-direction collapse in novelty pressure.
- [ ] Extend behavior characterization (turn streaks): Add longest/mean same-direction turn streak length as a behavior dimension to distinguish "continuous spinner" from agile turning.
- [ ] Extend behavior characterization (danger exposure): Add a danger-exposure metric (e.g., fraction of steps where min ray distance < threshold or min TTC < threshold) as a behavior dimension.
- [ ] Extend behavior characterization (aim alignment): Add an aim-alignment metric (e.g., time with an asteroid in the front rays / best-ray index distribution) as a behavior dimension.
- [ ] Extend behavior characterization (output saturation): Incorporate `output_saturation` into the behavior vector so novelty can discourage always-on saturated control policies.
- [ ] Method parity integration: Ensure ES/NEAT selection/update logic can reuse the same novelty/diversity signals for fair comparison.
- [ ] Adaptive Pareto objective schedule (shared): Rotate or reweight `ParetoConfig.OBJECTIVES` across training phases while logging the active objective set.
- [ ] Adaptive Pareto risk sensitivity: Schedule `ParetoConfig.RISK_TAU` and `ParetoConfig.RISK_TTC_MAX` as difficulty changes or as policies become more stable.

### NEAT-Oriented Integration Roadmap (Easy / Medium / Hard)

#### Easy

- [x] NEAT novelty bonus mode: Add a NEAT selection mode that uses behavior novelty as an additive parent-selection bonus.
- [x] NEAT diversity bonus mode: Add a NEAT selection mode that uses reward diversity as an additive parent-selection bonus.
- [x] NEAT bonus diagnostics: Export per-generation novelty/diversity bonus magnitude summaries so selection pressure is measurable.
- [ ] NEAT degenerate guardrails: Add optional selection penalties for extreme spin-lock and always-shoot regimes using existing evaluator metrics.

#### Medium

- [ ] NEAT novelty-first mode: Add an optional selection mode where novelty is primary and fitness is secondary to explore watchable behaviors.
- [ ] NEAT archive admission rules: Add archive admission rules that reject behaviors that are novel but dominated by degenerate control signatures.
- [ ] NEAT behavior-descriptor stability: Version behavior-vector normalization so archives remain comparable across encoder/reward changes.

#### Hard

- [ ] NEAT quality-diversity archive: Add a MAP-Elites-style archive keyed by behavior descriptors to preserve distinct strategies.
- [ ] NEAT multi-objective adapter: Add a NEAT adapter that can use Pareto ranking utilities for reproduction allocation across species.

### ES-Oriented Integration Roadmap (Easy / Medium / Hard)

#### Easy

- [ ] ES novelty/diversity kill-switch: Add a single configuration surface to disable novelty and diversity for ES runs (true ablation, not just “weight=0.0”).
- [ ] Bonus magnitude diagnostics: Log per-generation novelty/diversity bonus means and maxes for both GA and ES so “selection pressure” is visible and comparable.
- [ ] Seed-noise penalty option: Add an optional selection penalty proportional to per-agent `fitness_std` (across seeds) to favor robust behaviors over seed-lucky ones.
- [ ] Degenerate-style guardrails: Add optional penalties for extreme `turn_balance`, near-zero `turn_switch_rate`, and near-constant shoot usage so novelty does not reward “weird but useless” behaviors.

#### Medium

- [ ] Method-parity normalization: Normalize novelty and diversity scores into a comparable scale across GA and ES so weights have consistent meaning.
- [ ] Archive hygiene rules: Add archive admission rules that reject behaviors that are novel but dominated by degenerate control signatures (spin-lock / always-shoot / never-move).
- [ ] Behavior vector temporal extensions: Extend the behavior vector with temporal stability features (turn streaks, switch frequency, cooldown usage) so novelty promotes controllable strategies, not just action-rate differences.

#### Hard

- [ ] Random scalarization schedules: Support rotating objective weights per generation as an alternative multi-objective strategy (method-agnostic; same objective vector, different scalarization).
- [ ] Method adapters: Provide explicit adapter hooks for GA and future NEAT so the same Pareto/scalarization layer can drive selection/update consistently across methods.
- [ ] Strategy clustering pipeline: Convert behavior vectors into clustered archetypes and expose cluster shares as a first-class training signal for selection pressure and analysis.

## Notes / Design Considerations (optional)

- Novelty and diversity address different failure modes:
  - Behavior novelty discourages population collapse into identical action patterns.
  - Reward diversity discourages single-component reward exploitation.
- Reward balance principle: Reward components should be weighted so no single component becomes a clear dominant driver of total fitness, preserving reward diversity/novelty and reducing degenerate exploit strategies.
- Both systems are designed to be reward-preset agnostic:
  - Behavior novelty uses action/engagement metrics independent of reward values.
  - Diversity uses entropy over whatever reward components are active.
- ES sensitivity warning: Because ES can use rank transformation, novelty/diversity bonuses must be scaled to reliably change ranks without overwhelming the base skill signal.

## Discarded / Obsolete / No Longer Relevant

- State encoder designs are documented in `plans/STATE_REPRESENTATION.md`; this shared-components plan focuses strictly on method-agnostic training/selection components.
