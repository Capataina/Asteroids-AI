# Analytics & Data Schema

## Scope / Purpose

The analytics system captures, aggregates, and exports training metrics so AsteroidsAI experiments can be compared beyond a single fitness number. It exists to make training behavior observable (what agents do, how populations shift, and whether improvements generalize) and to provide machine-readable artifacts for later analysis.

## Current Implemented System

### Core Data Model (`training/analytics/collection/models.py`)

| Field | Type | Granular Meaning |
|---|---|---|
| `SCHEMA_VERSION` | `str` | Schema tag written into JSON exports for compatibility tracking (`"2.1"`). |
| `generations_data` | `List[dict]` | Ordered per-generation records (fitness stats + optional behavior/spatial/operator/timing keys). |
| `fresh_game_data` | `Dict[int, dict]` | Mapping `generation -> {fresh_game, generalization_metrics}` from windowed playback. |
| `distributions_data` | `Dict[int, dict]` | Mapping `generation -> {distributions, distribution_stats}` with sorted per-agent value lists. |
| `config` | `dict` | Training run metadata (recorded once at startup). |
| `start_time` | `datetime` | Start timestamp for duration computations and report headers. |
| `all_time_best_fitness` | `float` | Running best fitness across all generations. |
| `all_time_best_generation` | `int` | Generation index where the all-time best occurred. |
| `generations_since_improvement` | `int` | Stagnation counter incremented when best fitness does not improve. |

### Collection API (`training/analytics/analytics.py`, `training/analytics/collection/collectors.py`)

| API | Granular Responsibility |
|---|---|
| `TrainingAnalytics.set_config(...)` | Records run metadata (population size, generations, mutation prob, workers, etc.). |
| `TrainingAnalytics.record_generation(...)` | Appends generation fitness stats and merges optional timing/operator/behavior metrics into the generation record. |
| `TrainingAnalytics.record_distributions(...)` | Stores per-generation sorted lists (fitness/kills/steps/etc.) plus skewness/kurtosis and “viable vs failed” counts. |
| `TrainingAnalytics.record_fresh_game(...)` | Stores windowed “fresh game” performance and generalization ratios/grade. |

### Generation Records: Observed Keys (Implemented)

Fitness and run health (always recorded):

- `generation`: 1-based generation index as passed by the training script.
- `best_fitness`: max fitness among population.
- `avg_fitness`: mean fitness among population.
- `min_fitness`: min fitness among population.
- `median_fitness`: median fitness among population.
- `std_dev`: standard deviation of fitnesses.
- `population_size`: population size for this generation.
- `p25_fitness`, `p75_fitness`, `p90_fitness`: fitness percentiles for skew/long-tail visibility.
- `best_improvement`, `avg_improvement`: deltas versus previous generation.
- `all_time_best`: running best fitness.
- `generations_since_improvement`: stagnation counter.

Timing stats (recorded when provided by the training script):

- `evaluation_duration`: wall time spent evaluating the population.
- `evolution_duration`: wall time spent evolving the population.

Genetic operator stats (recorded when provided by the method driver):

- `crossover_events`: number of crossover applications performed.
- `mutation_events`: number of mutation applications performed.
- `elite_count`: elites preserved into the next generation.
- `avg_novelty`: average novelty score used for selection (when novelty is enabled).
- `avg_diversity`: average reward diversity score used for selection (when diversity is enabled).
- `archive_size`: current size of the behavior archive (novelty history).

Behavioral and spatial metrics (recorded when evaluator provides `behavioral_metrics`):

- Combat:
  - `avg_kills`, `max_kills`, `total_kills`
  - `avg_accuracy`, `avg_hits`, `avg_shots`
  - `avg_shots_per_kill`, `avg_shots_per_hit`
- Survival:
  - `avg_steps`, `max_steps`
- Action rates:
  - `avg_thrust_frames`, `avg_turn_frames`, `avg_shoot_frames`
  - `avg_left_only_frames`, `avg_right_only_frames`, `avg_both_turn_frames` (detailed turn metrics)
- Action durations:
  - `avg_thrust_duration`, `avg_turn_duration`, `avg_shoot_duration`
- Turn dynamics:
  - `avg_turn_value_mean`, `avg_turn_value_std`, `avg_turn_abs_mean`
  - `avg_turn_deadzone_rate`, `avg_turn_switch_rate`
  - `avg_turn_balance`, `avg_turn_left_rate`, `avg_turn_right_rate`
  - `avg_turn_streak`, `avg_max_turn_streak`
- Aim alignment:
  - `avg_frontness`, `avg_frontness_at_shot`, `avg_frontness_at_hit`
  - `avg_shot_distance`, `avg_hit_distance`
- Shooting cadence:
  - `avg_cooldown_ready_rate`, `avg_cooldown_usage_rate`
- Engagement / movement:
  - `avg_idle_rate`
  - `avg_asteroid_dist`
  - `avg_screen_wraps`
  - `avg_distance_traveled`, `avg_speed`, `avg_speed_std`
  - `avg_coverage_ratio`
- Risk profiling:
  - `avg_min_dist`
  - `avg_danger_exposure_rate`, `avg_danger_entries`, `avg_danger_reaction_time`, `avg_danger_wraps`
- Robustness:
  - `avg_fitness_std` (seed variance per agent)
- Neural/behavior health:
  - `avg_output_saturation`
  - `avg_action_entropy`
- Reward anatomy:
  - `avg_reward_breakdown`
  - `avg_quarterly_scores`
  - `reward_component_shares`, `reward_entropy`, `reward_dominance_index`, `reward_max_share`, `reward_positive_component_count`
- Heatmap inputs:
  - `best_agent_positions`, `best_agent_kill_events`
  - `population_positions`, `population_kill_events`

Fresh-game generalization (recorded when a generation has windowed playback captured):

- `fresh_game`: dict of fresh-game performance (`fitness`, `kills`, `steps_survived`, `shots_fired`, `accuracy`, `cause_of_death`, `reward_breakdown`, etc.).
- `generalization_metrics`: dict of ratios/deltas (`fitness_ratio`, `kills_ratio`, `steps_ratio`, `accuracy_delta`, `generalization_grade`).

### Distributions (Implemented)

Stored in `AnalyticsData.distributions_data[generation]` and mirrored into `generations_data[generation]['distributions']`:

| Distribution Key | Meaning |
|---|---|
| `fitness_values` | Sorted per-agent fitness values. |
| `kills_values` | Sorted per-agent kills values. |
| `steps_values` | Sorted per-agent steps survived values. |
| `accuracy_values` | Sorted per-agent accuracy values. |
| `shots_values` | Sorted per-agent shots fired values. |
| `thrust_values` | Sorted per-agent thrust frame counts. |
| `turn_values` | Sorted per-agent turn frame counts. |
| `shoot_values` | Sorted per-agent shoot frame counts. |
| `turn_deadzone_rate_values` | Sorted per-agent turn deadzone rates. |
| `turn_balance_values` | Sorted per-agent turn balance values (right-left bias). |
| `turn_switch_rate_values` | Sorted per-agent turn switch rates. |
| `frontness_values` | Sorted per-agent aim frontness averages. |
| `frontness_at_shot_values` | Sorted per-agent frontness at shot averages. |
| `danger_exposure_rate_values` | Sorted per-agent danger exposure rates. |
| `reaction_time_values` | Sorted per-agent danger reaction times. |
| `coverage_ratio_values` | Sorted per-agent coverage ratios. |
| `distance_traveled_values` | Sorted per-agent distance traveled totals. |
| `avg_speed_values` | Sorted per-agent average speeds. |
| `cooldown_usage_rate_values` | Sorted per-agent cooldown usage rates. |
| `shots_per_kill_values` | Sorted per-agent shots-per-kill ratios. |
| `shots_per_hit_values` | Sorted per-agent shots-per-hit ratios. |
| `fitness_std_values` | Sorted per-agent fitness std across seeds. |

Additional distribution stats:

- `fitness_skewness`: skewness of the fitness distribution.
- `fitness_kurtosis`: kurtosis of the fitness distribution.
- `viable_agent_count`: number of agents with `fitness > 0`.
- `failed_agent_count`: number of agents with `fitness <= 0`.
- `std_dev_kills`, `std_dev_steps`, `std_dev_accuracy`: std-dev snapshots for core performance metrics.
- `std_dev_frontness`, `std_dev_danger_exposure_rate`, `std_dev_turn_deadzone_rate`: std-dev snapshots for control diagnostics.
- `std_dev_coverage_ratio`, `std_dev_fitness_std`: std-dev snapshots for traversal and seed variance.

### Reporting & Export (Implemented)

| Artifact | Produced By | Notes |
|---|---|---|
| `training_summary.md` | `training/analytics/reporting/markdown.py:MarkdownReporter` | Markdown report with configurable sections via `training/config/analytics.py:AnalyticsConfig` (includes control diagnostics + reward transfer gaps when enabled). |
| `training_data.json` | `training/analytics/reporting/json_export.py:save_json` | JSON export containing schema, config, summary, generations, fresh-game and distributions data. |

## Implemented Outputs / Artifacts (if applicable)

- `training_summary.md`: Comprehensive report including control diagnostics, reward balance, generalization transfer gaps, trends, distributions, heatmaps, risk, and neural sections (as enabled by `AnalyticsConfig`).
- `training_data.json`: Machine-readable export of all recorded analytics data for offline analysis.

## In Progress / Partially Implemented

- [ ] Novelty/diversity visualization: GA records `avg_novelty/avg_diversity/archive_size` into generation data, but the markdown report does not yet have dedicated sections/plots for them.
- [ ] Fresh-game generation alignment: `DisplayManager` infers generation as `len(generations_data)`; this is correct in the current flow but brittle if ordering changes.
- [ ] Sparkline glyph rendering: Some report sections use non-ASCII glyphs which can display as mojibake depending on terminal encoding/font.
- [ ] Novelty/diversity distributions: Per-agent `behavior_vector` and `reward_diversity` exist during evaluation but are not exported as distributions.
- [ ] Evaluation seed traceability: Evaluator chooses a `generation_seed` and prints it as debug output, but the seed is not stored in analytics exports for reproducibility or CRN experiments.

## Planned / Missing / To Be Changed

- [ ] Feature-importance tooling: Attribute outcomes to parts of the current state vector (currently `HybridEncoder` output).
- [ ] Lineage/ancestry graphs: Track parentage across generations to visualize genetic drift and founder effects.
- [ ] Evaluation seed-policy metadata: Record whether a generation used per-candidate seeds or common-random-numbers (CRN), and persist the exact seed set used.
- [ ] Long-run storage strategy: Optional compression or chunked exports when `training_data.json` grows large.

## Notes / Design Considerations (optional)

- Data growth is dominated by heatmap inputs because they store spatial samples per generation.
- Many report sections require a minimum number of generations to produce meaningful trend/correlation outputs.

## Discarded / Obsolete / No Longer Relevant

- No analytics features have been formally removed; metrics not currently implemented should live under “Planned / Missing / To Be Changed” rather than being implied elsewhere.
