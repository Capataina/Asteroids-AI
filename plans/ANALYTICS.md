# Analytics & Data Schema

## Scope / Purpose

The analytics system captures, aggregates, and exports training metrics so AsteroidsAI experiments can be compared beyond a single “fitness number”. It exists to make training behavior observable (what agents do, how populations shift, and whether improvements generalize) and to provide machine-readable artifacts for later analysis.

## Current Implemented System

### Core Data Model (`training/analytics/collection/models.py`)

- **`AnalyticsData.SCHEMA_VERSION = "2.0"`**: A schema tag written into JSON exports for compatibility tracking.
- **`AnalyticsData.generations_data`**: Ordered list of per-generation dictionaries (fitness stats + optional behavioral/spatial data).
- **`AnalyticsData.fresh_game_data`**: Mapping `generation -> {fresh_game, generalization_metrics}` recorded from windowed playback.
- **`AnalyticsData.distributions_data`**: Mapping `generation -> {distributions, distribution_stats}` for per-agent value lists.
- **`AnalyticsData.config`**: Training configuration metadata recorded once at startup.
- **`AnalyticsData.start_time`**: Start timestamp used for duration computations.
- **`AnalyticsData.all_time_best_fitness`**: Running best fitness value.
- **`AnalyticsData.all_time_best_generation`**: Generation index where the all-time best occurred.
- **`AnalyticsData.generations_since_improvement`**: Stagnation counter incremented when best fitness does not improve.

### Collection API (`training/analytics/analytics.py`, `training/analytics/collection/collectors.py`)

- **`TrainingAnalytics.set_config(...)`**: Records run metadata (population size, generations, mutation probability, workers).
- **`TrainingAnalytics.record_generation(...)`**: Appends generation fitness stats and attaches aggregated metrics when provided.
- **`TrainingAnalytics.record_distributions(...)`**: Stores sorted per-agent value lists, basic distribution health stats, and standard deviations for reporting.
- **`TrainingAnalytics.record_fresh_game(...)`**: Stores windowed “fresh game” results plus generalization ratios/grade.

### What Gets Recorded Per Generation (Observed Keys)

Fitness and run health (always recorded when `fitness_scores` provided):

- **`best_fitness` / `avg_fitness` / `min_fitness` / `median_fitness`**: Summary fitness statistics.
- **`std_dev`**: Standard deviation of fitnesses.
- **`p25_fitness` / `p75_fitness` / `p90_fitness`**: Percentiles for skew/long-tail visibility.
- **`best_improvement` / `avg_improvement`**: Delta versus previous generation.
- **`all_time_best` / `generations_since_improvement`**: Global best/stagnation tracking.
- **`evaluation_duration` / `evolution_duration`** (if provided): Timing metrics from the training script.
- **`crossover_events` / `mutation_events` / `elite_count`** (if provided): GA operator accounting.

Behavioral and spatial metrics (recorded when `behavioral_metrics` is provided by the evaluator):

- **Combat**: `avg_kills`, `max_kills`, `avg_accuracy`, `avg_shots`, `total_kills`, `total_shots`.
- **Survival**: `avg_steps`, `max_steps`.
- **Action rates**: `avg_thrust_frames`, `avg_turn_frames`, `avg_shoot_frames`.
- **Action durations**: `avg_thrust_duration`, `avg_turn_duration`, `avg_shoot_duration`.
- **Idle/engagement**: `avg_idle_rate`, `avg_asteroid_dist`, `avg_screen_wraps`.
- **Risk Profiling**: `avg_min_dist` (average closest approach to an asteroid).
- **Neural Health**: `avg_output_saturation` (percentage of outputs saturated at 0 or 1).
- **Behavioral Complexity**: `avg_action_entropy` (Shannon entropy of input combinations).
- **Reward anatomy**: `avg_reward_breakdown` (per-component totals), `avg_quarterly_scores` (episode score quarters).
- **Heatmap inputs**:
  - `best_agent_positions` / `best_agent_kill_events` (aggregated across best agent seeds)
  - `population_positions` / `population_kill_events` (sampled across the population)

### Distributions (Per-Agent Lists)

Stored in `AnalyticsData.distributions_data[generation]`:

- **Value lists**: `fitness_values`, `kills_values`, `steps_values`, `accuracy_values`, `shots_values`, `thrust_values`, `turn_values`, `shoot_values`.
- **Stats**: `fitness_skewness`, `fitness_kurtosis`, `viable_agent_count`, `failed_agent_count`.

### Analysis Utilities (Implemented)

- **Fitness stats** (`training/analytics/analysis/fitness.py`): `median`, `std_dev`, skewness/kurtosis, Pearson correlation.
- **Report-level analyses** (`training/analytics/reporting/sections/`): deciles, kill efficiency, reward balance warnings, stagnation analysis, correlations, survival distributions, learning progress, convergence analysis, trend tables, ASCII charts, heatmaps, distributions, neural analysis, and risk analysis.

### Configuration (`training/config/analytics.py`)

- **`AnalyticsConfig`**: Centralized configuration class.
  - Toggles for all report sections (`ENABLE_DISTRIBUTIONS`, `ENABLE_HEATMAPS`, `ENABLE_RISK_ANALYSIS`, etc.).
  - Configurable window sizes for analysis (`HEATMAP_WINDOW`, `RECENT_TABLE_WINDOW`, `DISTRIBUTION_WINDOW`).

### Reporting/Export (Implemented)

- **Markdown report** (`training/analytics/reporting/markdown.py`): Orchestrates sections into `training_summary.md`, respecting `AnalyticsConfig` toggles.
- **JSON export** (`training/analytics/reporting/json_export.py`): Writes `training_data.json` (schema + all stored data).

## Implemented Outputs / Artifacts

- **`training_summary.md`**: Generated by `TrainingAnalytics.generate_markdown_report(...)`. Includes:
  - **Distribution Charts**: ASCII Mean ± StdDev charts for Fitness, Accuracy, Steps, and Kills.
  - **Heatmaps**: Aggregated spatial heatmaps (positions/kills) over the last `HEATMAP_WINDOW` generations.
  - **Neural Analysis**: Table showing output saturation and action entropy.
  - **Risk Profile**: Analysis of minimum proximity to asteroids ("Sniper" vs "Daredevil").
  - Tables, trends, warnings, and other summary statistics.
- **`training_data.json`**: Generated by `TrainingAnalytics.save_json(...)` and includes config, summary, generations, fresh-game data, and distribution data.

## In Progress / Partially Implemented

- [ ] Sparkline/arrow glyph rendering: Report sparklines use non-ASCII glyphs which can display as mojibake depending on terminal encoding/font.
- [ ] Fresh-game record alignment: `DisplayManager` infers the generation number as `len(generations_data)`; this works in the current flow but is brittle if the training loop changes ordering.

## Planned / Missing / To Be Changed

- [ ] Reaction-time metrics: Record delay between a threat entering a danger zone and the agent producing a corrective action.
- [ ] Feature-importance tooling: Attribute fitness/behavior outcomes to parts of the state vector (currently `VectorEncoder`).
- [ ] Lineage/ancestry graphs: Track parentage across generations to visualize genetic drift and “founder effects”.
- [ ] Per-seed variance reporting: Export mean/std across the `seeds_per_agent` evaluations for robustness tracking.
- [ ] Long-run storage strategy: Add optional compression or chunked exports when `training_data.json` grows large.

## Notes / Design Considerations

- Data growth is dominated by heatmap inputs (`*_positions`, `*_kill_events`) because they are stored per generation.
- Many report sections require a minimum number of generations (often `>= 10`) to produce meaningful trend/correlation outputs.

## Discarded / Obsolete / No Longer Relevant

- No analytics features have been formally removed; items not currently implemented should live under "Planned / Missing / To Be Changed".
