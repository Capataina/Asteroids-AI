# Analytics & Data Schema

## Scope / Purpose

The analytics system captures, aggregates, and exports training metrics so AsteroidsAI experiments can be compared beyond a single fitness number. It exists to make training behavior observable (what agents do, how populations shift, and whether improvements generalize) and to provide machine-readable artifacts for later analysis.

## Current Implemented System

### Core Data Model (`training/analytics/collection/models.py`)

| Field | Type | Granular Meaning |
|---|---|---|
| `SCHEMA_VERSION` | `str` | Schema tag written into JSON exports for compatibility tracking (`"2.1"`). |
| `generations_data` | `List[dict]` | Ordered per-generation records (fitness stats plus optional behavior/spatial/operator/timing keys). |
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
| `TrainingAnalytics.record_distributions(...)` | Stores per-generation sorted lists (fitness/kills/steps/etc.) plus skewness/kurtosis and viable vs failed counts. |
| `TrainingAnalytics.record_fresh_game(...)` | Stores windowed fresh-game performance and generalization ratios/grade. |

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

ES optimizer diagnostics (recorded when provided by CMA-ES):

- `sigma`: CMA-ES global step size.
- `mean_param_norm`: L2 norm of the CMA-ES mean vector.
- `cov_diag_mean`: Mean diagonal covariance value.
- `cov_diag_min`: Minimum diagonal covariance value.
- `cov_diag_max`: Maximum diagonal covariance value.
- `cov_diag_std`: Standard deviation of diagonal covariance values.
- `cov_diag_mean_abs_dev`: Mean absolute deviation of diagonal covariance from 1.0.
- `cov_diag_max_abs_dev`: Largest absolute deviation of diagonal covariance from 1.0.
- `cov_lr_scale`: Scaling factor applied to `c1/cmu` for diagonal covariance adaptation.
- `cov_lr_effective_rate`: Effective `c1 + cmu` rate after scaling/clamping.

Behavioral and spatial metrics (recorded when evaluator provides `behavioral_metrics`):

- Combat:
  - `avg_kills`, `max_kills`, `total_kills`
  - `avg_accuracy`, `avg_hits`, `avg_shots`
  - `avg_shots_per_kill`, `avg_shots_per_hit`
- Survival:
  - `avg_steps`, `avg_time_alive`, `max_steps`
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
  - `avg_softmin_ttc`
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

- `fresh_game`: dict of fresh-game performance (`fitness`, `kills`, `steps_survived`, `shots_fired`, `hits`, `accuracy`, `time_alive_seconds`, `cause_of_death`, `reward_breakdown`, etc.).
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
| `softmin_ttc_values` | Sorted per-agent soft-min TTC values. |
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
- `std_dev_frontness`, `std_dev_danger_exposure_rate`, `std_dev_softmin_ttc`, `std_dev_turn_deadzone_rate`: std-dev snapshots for control diagnostics.
- `std_dev_coverage_ratio`, `std_dev_fitness_std`: std-dev snapshots for traversal and seed variance.

### Reporting & Export (Implemented)

| Artifact | Produced By | Notes |
|---|---|---|
| `training_summary.md` | `training/analytics/reporting/markdown.py:MarkdownReporter` | Markdown report with configurable sections via `training/config/analytics.py:AnalyticsConfig` (includes control diagnostics + reward transfer gaps when enabled). |
| `training_data.json` | `training/analytics/reporting/json_export.py:save_json` | JSON export containing schema, config, summary, generations, fresh-game and distributions data. |

### Report Structure & Interpretation (Implemented)

- Quick trend overview uses 20-column ASCII sparklines (5% bins) with phase-based tags and confidence.
- Report takeaways block summarizes every major report section with a single bullet.
- Per-section takeaways and warnings are emitted for each analytics section.
- Per-section glossary blocks define all metrics shown in that section.
- Training phases use 4 equal slices (25% each) for normalized comparisons.
- Milestones are run-relative (percent-of-peak thresholds) rather than fixed numeric thresholds.
- Reward evolution uses 4 phases and marks trends using relative percent change.
- Reward balance warnings use dominance/entropy baselines and component volatility checks.
- Distribution analysis includes mean +/- std dev charts plus spread/seed-noise trend tags.

## Implemented Outputs / Artifacts (if applicable)

- `training_summary.md`: Comprehensive report including control diagnostics, reward balance, generalization transfer gaps, trends, distributions, heatmaps, risk, and neural sections (as enabled by `AnalyticsConfig`).
- `training_data.json`: Machine-readable export of all recorded analytics data for offline analysis.

## In Progress / Partially Implemented

- [ ] Novelty/diversity visualization: GA records `avg_novelty/avg_diversity/archive_size` into generation data, but the markdown report does not yet have dedicated sections/plots for them.
- [ ] Fresh-game generation alignment: `DisplayManager` infers generation as `len(generations_data)`; this is correct in the current flow but brittle if ordering changes.
- [ ] Novelty/diversity distributions: Per-agent `behavior_vector` and `reward_diversity` exist during evaluation but are not exported as distributions.
- [ ] Evaluation seed traceability: Evaluator chooses a `generation_seed` and prints it as debug output, but the seed is not stored in analytics exports for reproducibility or CRN experiments.
- [ ] Generalization report “training fit” mismatch: `training/analytics/reporting/sections/generalization.py` prints `best_fitness` as “Training Fit”, which may not match the candidate that was actually fresh-tested.
- [ ] Generalization ratio filtering bias: `training/analytics/reporting/sections/generalization.py` computes ratio summaries using only `fitness_ratio > 0`, which can hide frequent failures.
- [ ] Generalization ratio near-zero instability: Generalization ratios are not explicitly marked `N/A` when training fitness is near zero, which can make ratios numerically misleading.
- [ ] System performance totals inconsistency: The markdown report can show large evaluation durations while showing `0.00s` total times, indicating missing/incorrect aggregation in performance reporting.

## Planned / Missing / To Be Changed

- [ ] Feature-importance tooling: Attribute outcomes to parts of the current state vector (currently `HybridEncoder` output).
- [ ] Lineage/ancestry graphs: Track parentage across generations to visualize genetic drift and founder effects.
- [ ] Evaluation seed-policy metadata: Record whether a generation used per-candidate seeds or common-random-numbers (CRN), and persist the exact seed set used.
- [ ] Long-run storage strategy: Optional compression or chunked exports when `training_data.json` grows large.

### Reporting Correctness & Interpretability (Easy)

- [ ] Fresh-game training-fitness provenance: Store and print the exact scalar fitness value used as the denominator for `fitness_ratio` in each fresh-game record.
- [ ] Fresh-game candidate identity: Store and print a stable identifier for the candidate that was fresh-tested (e.g., parameter hash or source index).
- [ ] Generalization table dual columns: Show both `best_fitness` (population best) and “fresh-tested candidate training fitness” with explicit labels.
- [ ] Generalization ratios “all vs positive-only”: Compute and print ratio summaries for all ratios and for ratios filtered to `> 0`, clearly labeled.
- [ ] Generalization ratio N/A rules: Render ratios as `N/A` when training fitness is below a configurable threshold to prevent blow-ups and misleading grades.
- [ ] Generalization grade definition: Print the exact grade thresholds/logic used to compute `generalization_grade` so report readers can interpret grades.
- [ ] Ratio sign handling: Include negative ratios in “all ratio” summaries as explicit failure signals instead of silently excluding them.
- [ ] Metric-definition note: Add a report note clarifying whether training fitness and fresh-game fitness use identical reward accounting (step + episode reward).

### Robust Descriptive Statistics (Easy)

- [ ] Fitness quantile tracking: Add p10/p25/p50/p75/p90 for population fitness into trend and phase summaries.
- [ ] Kills quantile tracking: Add p10/p25/p50/p75/p90 for population kills into distribution summaries.
- [ ] Survival quantile tracking: Add p10/p25/p50/p75/p90 for survival steps/time into survival and distribution summaries.
- [ ] Accuracy quantile tracking: Add p10/p25/p50/p75/p90 for accuracy into distribution summaries.
- [ ] Trimmed-mean fitness: Add a trimmed-mean fitness statistic (e.g., 10% trimmed) to reduce outlier sensitivity.
- [ ] Rolling-window stability: Add rolling-window mean/std and rolling slope for best/avg fitness (window size configurable via `AnalyticsConfig`).
- [ ] Outlier counts (fitness): Count agents above/below configurable fitness thresholds per generation and report as a time series.
- [ ] Outlier counts (kills): Count agents meeting configurable kill thresholds per generation and report as a time series.
- [ ] Tail-shape surfacing: Surface existing skewness/kurtosis values with short interpretation guidance per metric.

### Pareto Diagnostics (Medium; No New Rollouts)

- [ ] Pareto front0 size series: Compute and store the number of candidates in Pareto front 0 per generation.
- [ ] Pareto front rank histogram: Compute and store counts of candidates per Pareto front rank (front0/front1/…).
- [ ] Pareto crowding stats: Compute and store mean/median/percentiles for crowding distance and count of infinite crowding values.
- [ ] Objective summary stats: Store mean/median/p10/p90 for each objective (`hits`, `time_alive`, `softmin_ttc`) per generation.
- [ ] Front0 objective summary: Store objective summary stats computed only over the Pareto front0 set per generation.
- [ ] Pareto winner explanation: Print the selected candidate’s objective vector plus its front rank and crowding distance in the report.
- [ ] Objective correlation block: Add an objective-to-objective correlation matrix to show redundancy/conflict between objectives.
- [ ] Pareto-vs-fitness consistency: Track how often the Pareto-selected candidate is also top-k by scalar fitness (and vice versa).
- [ ] Fitness tie-break activation: Track and report how often Pareto tie-breaking by fitness was applied during ordering/selection.

### ES Optimizer Reporting Upgrades (Easy/Medium; No New Rollouts)

- [ ] Mean step length: Log and report `||Δmean||` per generation to show distribution movement magnitude.
- [ ] Sigma change rate: Log and report `Δsigma/sigma` per generation to show step-size dynamics.
- [ ] Covariance percentiles: Log and report p1/p50/p99 of `cov_diag` per generation to detect partial collapse/explosion.
- [ ] Covariance floor hits: Log and report the count/fraction of `cov_diag` elements at `CMAES_COV_MIN` per generation.
- [ ] Evolution path norms: Log and report `||p_sigma||` and `||p_c||` per generation to diagnose stalled adaptation.
- [ ] Restart annotations: Add restart markers to the report timeline including before/after `sigma` and key performance stats.
- [ ] Noise-handling impact flag: Log and report whether top-k confirmation changed the ordering/winner for a generation.

### Evaluation Noise & Measurement Quality (Easy; No New Rollouts)

- [ ] Seed-variance percentiles: Report p50/p90/p99 of per-agent `fitness_std` across seeds per generation as a stability summary.
- [ ] Signal-to-noise proxy: Report `(best_improvement) / (median fitness_std)` per generation as an update reliability proxy.
- [ ] Fragile-elite warning: Warn when top candidates have unusually high seed variance relative to the generation median.
- [ ] Winner-volatility tag: Tag generations where the winner’s variance overlaps heavily with the population, indicating ambiguous ranking.

### Reward-System Deepening (Easy; No New Rollouts)

- [ ] Reward concentration time series: Track and plot reward dominance (HHI), reward entropy, and max-share across generations (not only latest).
- [ ] Penalty ratio time series: Track and plot penalty ratio across generations to show how negative components dominate over time.
- [ ] Component share per generation: Convert `avg_reward_breakdown` into normalized component shares per generation for comparability.
- [ ] Component volatility ranking: Compute per-component volatility over a rolling window and list the most volatile components.
- [ ] Reward-share distributions (where available): Add distributions of component shares for top candidates when per-agent breakdowns are available.

### Control & Behavior Diagnostics Expansion (Easy; No New Rollouts)

- [ ] Turn precision proxy: Summarize control precision using `turn_abs_mean` and related turn dynamics distributions.
- [ ] Action-combo frequency table: Report top-N most common action combinations per generation (derived from existing action diagnostics).
- [ ] Smoothness trend summaries: Add rolling summaries for turn switch rate, streak length, and turn balance.
- [ ] Movement regime classification: Add a derived “movement regime” label per generation using coverage, distance traveled, and speed stats.
- [ ] Aim quality delta: Report and trend `(frontness_at_hit - frontness_at_shot)` as a targeting-quality proxy.
- [ ] Efficiency distributions: Add explicit distributions for `shots_per_kill` and `shots_per_hit` alongside kills/accuracy distributions.

### Fresh-Game Analysis Improvements (Easy; No New Rollouts)

- [ ] Cause-of-death distribution: Summarize fresh-game `cause_of_death` counts/percentages across the run.
- [ ] Fresh-game robust stats: Report median/IQR for fresh-game fitness, kills, steps, and accuracy across recorded fresh-game runs.
- [ ] Fresh-vs-training deltas: Report absolute deltas (fresh minus training) for kills/accuracy/steps in addition to ratios.
- [ ] Reward transfer phase summary: Aggregate reward share-shift metrics by phase to summarize transfer stability beyond last-10 snapshots.
- [ ] Reward transfer outlier flags: Flag generations with extreme share-shifts (configurable threshold) for immediate inspection.

### Data Quality, Sanity Checks & Provenance (Easy; No New Rollouts)

- [ ] Missing-key rates: Track and report missing rates for optional keys in per-agent metrics and generation aggregates.
- [ ] Range sanity checks: Validate metrics fall within expected ranges (e.g., accuracy in [0,1], steps ≤ max_steps) and emit warnings on violations.
- [ ] Non-finite accounting: Report counts of NaN/Inf replacements performed during JSON export sanitization and list affected fields.
- [ ] Config delta display: Print a compact “config echo” and highlight missing/unknown config keys for schema compatibility tracking.
- [ ] Metric definition appendix: Add an appendix mapping report fields to their computation sources (evaluator vs display vs config) for high-risk metrics like fitness and ratios.

### ES Upgrade Reporting Support (Medium / Hard)

#### Medium

- [ ] Two-stage evaluation telemetry: Export “screening” vs “confirmation” fitness for top-K candidates so update trustworthiness is measurable.
- [ ] Validation seed set artifacts: Export held-out seed-set results as a separate time series so generalization is tracked without mixing into training curves.
- [ ] Update stability tags: Emit a per-generation “update accepted / update gated” marker when ES skips or shrinks an update due to unstable ranking.

#### Hard

- [ ] Multi-objective exports (method-agnostic): Extend schema to store per-candidate objective vectors and per-generation Pareto front summaries (front size, archetype mix, best-by-objective).
- [ ] Pareto report sections (method-agnostic): Add report sections that summarize Pareto fronts and trade-offs (objective correlations, front progression, stability under validation seeds).

## Notes / Design Considerations (optional)

- Data growth is dominated by heatmap inputs because they store spatial samples per generation.
- Many report sections require a minimum number of generations to produce meaningful trend/correlation outputs.
- Trend tags are phase-based and designed to be scale-invariant across reward reweights.

## Discarded / Obsolete / No Longer Relevant

- No analytics features have been formally removed; metrics not currently implemented should live under "Planned / Missing / To Be Changed" rather than being implied elsewhere.
