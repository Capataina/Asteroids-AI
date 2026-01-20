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

NEAT operator stats (recorded when provided by the NEAT driver):

- `species_count`, `species_min_size`, `species_max_size`, `species_median_size`
- `species_pruned` (stagnation-based pruning count)
- `avg_nodes`, `avg_connections`
- `best_nodes`, `best_connections`
- `compatibility_threshold`, `compatibility_mean`, `compatibility_p10`, `compatibility_p90`
- `add_node_events`, `add_connection_events`, `weight_mutation_events`, `crossover_events`
- `innovation_survival_rate`

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
- `training_summary_es.md`: ES run report produced by the same analytics exporter pipeline.
- `training_data_es.json`: ES run JSON export produced by the same analytics exporter pipeline.
- `training_summary_neat.md`: NEAT run report produced by the same analytics exporter pipeline.
- `training_data_neat.json`: NEAT run JSON export produced by the same analytics exporter pipeline.
- `training_summary_sac.md`: SAC run report produced by the same analytics exporter pipeline.
- `training_data_sac.json`: SAC run JSON export produced by the same analytics exporter pipeline.

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

### RL Method Support (Planned)

- [ ] RL action health metrics: Record continuous action statistics (turn/thrust magnitude + saturation + entropy) as first-class generation/interval keys.
- [ ] RL embedding health metrics: Record state-embedding variance and similarity diagnostics so embedding collapse can be detected without manual inspection.
- [ ] RL learner stability metrics: Record actor/critic losses, Q-value scale, alpha (temperature), and gradient norms so training instability is visible in reports.
- [ ] RL replay health metrics: Record replay size, warmup/learn start progress, and episode-length/reward distribution snapshots so data quality can be diagnosed.
- [ ] RL report sections: Add dedicated report sections (or append blocks) for action health, embedding health, and learner stability alongside existing fitness/generalization sections.

### RL Metrics (Planned: Concrete Keys)

These keys are intended to be emitted by `train_gnn_sac.py` via `TrainingAnalytics.record_generation(...)` (or a periodic “interval” record) and exported in `training_data_sac.json`.

- [ ] RL “generation” meaning: When reusing the GA/ES/NEAT `generations_data` schema, treat “generation” as a **reporting interval index** for RL (e.g., every N environment steps) rather than an evolutionary generation.
- [ ] RL timebase keys: Record the absolute RL timebase alongside each interval so plots can be interpreted correctly.

#### RL Action Health (Continuous-Control)

- [ ] `turn_abs_mean`: Mean absolute `turn_value` over the logging window (detects “never turns” vs active control).
- [ ] `turn_abs_p90`: 90th percentile absolute `turn_value` (detects whether high authority is ever used).
- [ ] `turn_near_zero_rate`: Fraction of steps with `|turn_value| < eps` (detects turn collapse).
- [ ] `turn_saturation_rate`: Fraction of steps with `|turn_value| > 0.95` (detects “always max turn” degeneracy).
- [ ] `thrust_mean`: Mean `thrust_value` (detects always-on vs always-off thrust).
- [ ] `thrust_zero_rate`: Fraction of steps with `thrust_value < eps` (detects “never thrust” collapse).
- [ ] `thrust_saturation_rate`: Fraction of steps with `thrust_value > 0.95` (detects always-on thrust).
- [ ] `shoot_prob_mean`: Mean shoot probability/logit-derived probability (detects shoot collapse).
- [ ] `shoot_rate`: Fraction of steps where a shot is actually fired (environment-level realization).
- [ ] `shoot_saturation_rate`: Fraction of steps with `shoot_prob < eps` or `shoot_prob > 1-eps` (detects probability collapse).
- [ ] `policy_entropy_mean`: Mean policy entropy (continuous + shoot head) to detect exploration collapse.

#### RL Timebase / Progress (Schema Compatibility)

- [ ] `env_steps_total`: Total environment steps collected so far (monotonic).
- [ ] `updates_total`: Total learner update steps performed so far (monotonic).
- [ ] `episodes_total`: Total completed episodes so far (monotonic).

#### RL Embedding Health (GNN Representation)

- [ ] `state_emb_mean_norm`: Mean L2 norm of the state embedding batch (detects scale drift).
- [ ] `state_emb_std_mean`: Mean per-dimension std of embeddings across batch/time (low values indicate collapse).
- [ ] `state_emb_cosine_sim_mean`: Mean pairwise cosine similarity across a sampled embedding batch (high values indicate collapse).
- [ ] `state_emb_cosine_sim_p90`: 90th percentile pairwise cosine similarity (detects partial collapse).

#### RL Learner Stability (Optimization Diagnostics)

- [ ] `critic_loss_mean`: Mean critic TD loss over the logging window.
- [ ] `actor_loss_mean`: Mean actor loss over the logging window.
- [ ] `alpha_value`: Current entropy temperature value (auto-tuning health).
- [ ] `alpha_loss_mean`: Mean alpha loss over the logging window (auto-tuning stability).
- [ ] `q1_mean`: Mean Q1 value on a sampled training batch (scale sanity).
- [ ] `q2_mean`: Mean Q2 value on a sampled training batch (scale sanity).
- [ ] `q_target_mean`: Mean target Q value on a sampled training batch (bootstrapping sanity).
- [ ] `td_error_mean`: Mean TD error magnitude (learning progress proxy).
- [ ] `td_error_std`: Stddev of TD error magnitude (instability proxy).
- [ ] `actor_grad_norm`: Gradient norm of actor parameters (explosion/vanishing detection).
- [ ] `critic_grad_norm`: Gradient norm of critic parameters (explosion/vanishing detection).
- [ ] `grad_clip_hit_rate`: Fraction of updates where gradient clipping activated (too-hot learning detection).

#### RL Replay / Data Health (Off-Policy Data Quality)

- [ ] `replay_size`: Current number of transitions in replay (warmup visibility).
- [ ] `learn_start_progress`: Fraction of warmup completed (`steps / LEARN_START_STEPS`).
- [ ] `episode_len_mean`: Mean episode length over completed episodes (survivability proxy).
- [ ] `episode_len_p90`: 90th percentile episode length (tail survivability proxy).
- [ ] `reward_mean`: Mean reward per step over collected transitions (scale sanity).
- [ ] `reward_std`: Stddev reward per step over collected transitions (noise proxy).

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

### NEAT Reporting Support (Medium / Hard)

#### Medium

- [x] Species count series: Record the number of species per generation as a diversity signal for topology-growth runs.
- [x] Species size distribution: Record per-generation min/median/max species sizes to detect collapse into a single species.
- [x] Topology growth series: Record average node count per generation to measure structural growth over time.
- [x] Topology growth series: Record average connection count per generation to measure structural growth over time.
- [x] Operator event counts: Record per-generation counts of add-node, add-connection, crossover, and weight-mutation events.
- [x] Compatibility threshold telemetry: Record the active compatibility threshold per generation to explain speciation dynamics.
- [x] Species stagnation telemetry: Record the number of stagnant species pruned per generation to explain population resets.

#### Hard

- [ ] Genome identity tracking: Store a stable identifier (e.g., genome hash) for the fresh-tested genome to improve generalization provenance.
- [ ] Genome artifact links: Store paths/filenames for best-genome JSON/DOT artifacts in the analytics export for replay and inspection.
- [ ] Species-level dashboards: Add report tables/plots for best fitness per species and species lifetime to support debugging selection pressure.

## Notes / Design Considerations (optional)

- Data growth is dominated by heatmap inputs because they store spatial samples per generation.
- Many report sections require a minimum number of generations to produce meaningful trend/correlation outputs.
- Trend tags are phase-based and designed to be scale-invariant across reward reweights.

## Discarded / Obsolete / No Longer Relevant

- No analytics features have been formally removed; metrics not currently implemented should live under "Planned / Missing / To Be Changed" rather than being implied elsewhere.
