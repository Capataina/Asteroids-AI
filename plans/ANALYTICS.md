# Analytics & Data Schema

## Scope / Purpose

The analytics system provides a comprehensive window into the training process, capturing detailed metrics on agent behavior, population health, and learning dynamics. Its purpose is to move beyond simple "fitness scores" and allow researchers to understand *how* and *why* agents are learning (or failing), enabling data-driven decisions for reward shaping and hyperparameter tuning.

## Current Implemented System

The system is fully modular, with data collection handled by `training/analytics/collection` and reporting by `training/analytics/reporting`.

- **Data Collection Infrastructure**
    - **`TrainingAnalytics` Facade**: Central entry point that delegates to specialized collectors.
    - **Generation Collector**: Captures fitness stats, behavioral aggregates, and timing data per generation.
    - **Fresh Game Collector**: Captures performance on unseen seeds to measure generalization.
    - **Distribution Collector**: Captures per-agent metrics to analyze population skewness and diversity.

- **Data Schema (Version 2.0)**
    - **Core Aggregates**: `best_fitness`, `avg_fitness`, `min_fitness`, `median_fitness`, `std_dev`, `percentiles`.
    - **Behavioral Aggregates**:
        - `avg_kills`, `avg_steps`, `avg_accuracy`, `avg_shots`.
        - `avg_thrust_frames`, `avg_turn_frames`, `avg_shoot_frames` (Input distribution).
        - `avg_thrust_duration`, `avg_turn_duration`, `avg_idle_rate` (Input style).
    - **Spatial Metrics**:
        - `avg_asteroid_dist`, `avg_screen_wraps`.
        - `best_agent_positions` & `best_agent_kill_events` (List of coordinates).
        - `population_positions` & `population_kill_events` (Sampled list from 30 agents).
    - **Reward Breakdown**: Per-component score averages (e.g., `SurvivalBonus`, `KillAsteroid`).
    - **Fresh Game Data**: `fresh_game` object containing performance on a new seed, and `generalization_metrics` (Grade A-F).
    - **Distributions**: Full arrays of `fitness_values`, `kills_values`, etc., for histogram generation.
    - **Performance Metadata**: `timing_stats` (eval/evolve duration) and `operator_stats` (crossover/mutation counts).

## Implemented Outputs / Artifacts

- **`training_summary.md` (Markdown Report)**
    - **Executive Summary**: High-level stats, generalization grade, and best agent profile.
    - **Sparklines**: ASCII trend lines for fitness, kills, and accuracy trends.
    - **Spatial Heatmaps**:
        - **Best Agent**: Position and Kill Zone heatmaps.
        - **Population Average**: Heatmaps derived from a random sample of 30 agents to show herd behavior.
    - **Behavioral Analysis**: Breakdowns of input styles, safe distances, and action distributions.
    - **Population Health**: Stagnation warnings, diversity analysis, and convergence tracking.
    - **Technical Appendix**: Computational performance and genetic operator stats.

- **`training_data.json` (Raw Data)**
    - Complete, machine-readable history of the entire training run for external analysis (e.g., Jupyter notebooks).

- **Console Output**
    - **Generation Summary**: Structured table with Best/Avg/Std fitness and key behavioral metrics.
    - **Fresh Game Report**: Formatted table comparing training performance vs. fresh seed performance.

## In Progress / Partially Implemented

- **Trend Indicators**: Basic trend analysis exists, but visual indicators (arrows) in section headers are not yet consistent.

## Planned / Missing / To Be Changed

- **Reaction Time Metric**: Measure the time delta between an asteroid entering "Danger Radius" and the agent changing inputs.
- **Neuron Saturation**: Track the percentage of time hidden neurons are stuck at -1 or 1 (tanh saturation) to diagnose dead networks.
- **Lineage Tracking**: Track "Parent ID" to visualize genetic drift and identify "Eve" agents.
- **Input Feature Importance**: Correlate specific inputs (e.g., "Bullet Cooldown") with action intensity.

## Notes / Design Considerations

- **Data Volume**: Storing full distribution data for every generation can be large. The JSON file size should be monitored for very long runs (1000+ generations).
- **Sampling Strategy**: Population heatmaps use a sample of 30 agents to balance accuracy with file size and processing speed.
- **Data Integrity**: Bugs involving >100% action percentages (due to incorrect key lookups) and 0.0s input durations have been resolved. The system now correctly normalizes aggregated frame counts against the appropriate step metrics.

## Discarded / Obsolete

- **Sequential Logging**: Old flat-file logging was replaced by the structured JSON/Markdown system.
- **Manual "Best Agent" Replay**: Replaced by "Fresh Game" testing to enforce generalization checks.