# Analytics & Data Schema: Implemented vs. Planned

## 1. Introduction

This document provides a comprehensive overview of the Asteroids AI project's analytics and data collection systems. It serves as a unified reference, merging the original enhancement proposals with a clear-eyed assessment of the current implementation.

The guiding philosophy is that **if we observe it during training, we should be able to analyze it later.** This document outlines what we currently track and what is planned for the future to achieve a deeper, more actionable understanding of agent behavior and training dynamics.

---

## 2. Current Implemented System

A significant portion of the proposed analytics and data schema has already been implemented. The system is designed to be modular, with data collection handled by `training/analytics/collectors` and report generation by `training/analytics/reporting`.

### 2.1. Implemented Data Schema

The current data schema (`version 2.0`) is defined in `training/analytics/collection/models.py` and captured in `training_data.json`. The following data categories are **fully implemented and collected** during every training run:

| Data Category                | Schema Fields                                                                                        | Status             | Notes                                                                                                                |
| :--------------------------- | :--------------------------------------------------------------------------------------------------- | :----------------- | :------------------------------------------------------------------------------------------------------------------- |
| **Core Aggregates**          | `best_fitness`, `avg_fitness`, `min_fitness`, `median_fitness`, `std_dev`, `percentiles`             | ✅ **Implemented** | Basic population statistics per generation.                                                                          |
| **Behavioral Aggregates**    | `avg_kills`, `avg_steps`, `avg_accuracy`, `avg_shots`                                                | ✅ **Implemented** | Population-wide average behaviors.                                                                                   |
| **Action-Level Metrics**     | `avg_thrust_frames`, `avg_turn_frames`, `avg_shoot_frames`                                           | ✅ **Implemented** | Direct observation of input behavior (frequencies).                                                                  |
| **Input Style Metrics**      | `avg_thrust_duration`, `avg_turn_duration`, `avg_shoot_duration`, `avg_idle_rate`                    | ✅ **Implemented** | Tracks how long buttons are held (control finesse) and idle time.                                                    |
| **Spatial Metrics**          | `avg_asteroid_dist`, `avg_screen_wraps`, `best_agent_positions`, `best_agent_kill_events`            | ✅ **Implemented** | Safety margin tracking, screen usage, and heatmap data points.                                                       |
| **Reward Breakdown**         | `avg_reward_breakdown`, `avg_quarterly_scores`                                                       | ✅ **Implemented** | Per-component reward averages and intra-episode scoring timeline.                                                    |
| **Fresh Game Performance**   | `fresh_game` object, `generalization_metrics` object                                                 | ✅ **Implemented** | **CRITICAL**: Captures the best agent's performance in an unseeded game to test generalization. Includes `accuracy`. |
| **Population Distributions** | `distributions` object containing arrays for `fitness_values`, `kills_values`, `thrust_values`, etc. | ✅ **Implemented** | Captures the full data for every agent in a generation, not just averages. Enables deep statistical analysis.        |
| **Computational Metadata**   | `timing_stats` object (`evaluation_duration`, `evolution_duration`)                                  | ✅ **Implemented** | Performance profiling for the training loop.                                                                         |
| **Genetic Operator Stats**   | `operator_stats` object (`crossover_events`, `mutation_events`)                                      | ✅ **Implemented** | Tracking of GA internal mechanics.                                                                                   |

### 2.2. Implemented Analytics Report

The `training_summary.md` report is automatically generated and already includes the majority of the proposed analytics sections. The following features are **fully implemented**:

- **Table of Contents**: Auto-generated clickable index.
- **Quick Trend Overview**: ASCII sparklines for at-a-glance trend visualization.
- **Overall Summary**: High-level training outcomes, including generalization performance.
- **Best Agent Deep Profile**: Detailed stats of the all-time best agent, including efficiency metrics and **Behavioral Classification** (e.g., "Sniper", "Berzerker").
- **Spatial Heatmaps**: ASCII grids showing **Position Density** and **Kill Zones** for the best agent.
- **Generation Highlights**: Tables of the best-performing generations.
- **Milestone Timeline**: A chronological list of key achievements (e.g., "First 10-kill agent").
- **Temporal Analysis (Deciles/Trends)**: Multiple views breaking down the training run into phases to show how performance and behavior evolved over time.
- **Behavioral Trends**: Includes a table of **Action Distribution** (Thrust/Turn/Shoot frequencies), **Safe Distance**, and dominant strategy per quarter. Includes **Intra-Episode Score Breakdown** (Early vs Late game scoring) and **Input Control Style**.
- **Kill Efficiency Analysis**: Metrics like "Kills per 100 Steps" and "Shots per Kill".
- **Learning Velocity**: Analysis of the rate of improvement.
- **Reward Component Evolution**: A table showing how the agent's sources of reward changed over the course of training, including **Exploration Efficiency**.
- **Reward Balance Warnings**: Automated checks for potential issues in the reward structure (e.g., one component dominating all others).
- **Population Health & Convergence**: Analysis of population diversity (`std_dev`) and convergence status, including **Stagnation Warnings** (>20 gens).
- **Stagnation Analysis**: Detection of learning plateaus.
- **Generalization Analysis**: A dedicated section analyzing the `fresh_game` data (including **Accuracy**) to assess how well the agent's skills transfer to new scenarios.
- **Correlation Analysis**: A matrix showing the statistical correlation between various metrics and fitness.
- **Survival Distribution**: Analysis of when and how often agents die.
- **Detailed Tables**: Breakdowns of the most recent and all-time best generations (aligned for raw viewing, collapsible).
- **ASCII Fitness Chart**: A simple plot of fitness progression.
- **Technical Appendix**: Performance timings and Genetic Operator statistics.

---

## 3. Planned Enhancements

This section details the features and data structures that have **not yet been implemented**. These enhancements focus on finer-grained behavioral analysis, spatial reasoning, and neural network diagnostics.

### 3.1. Visuals & Formatting (Polishing the Report)

| Priority | Enhancement                     | Description                                                 | Rationale                   |
| :------- | :------------------------------ | :---------------------------------------------------------- | :-------------------------- |
| **P3**   | **Trend Indicators in Headers** | Add arrows (↑/↓) to section headers based on recent trends. | Provides immediate context. |

### 3.2. Intra-Episode Analysis (The "Micro" View)

| Priority | Enhancement              | Description                                                                                        | Rationale                                 |
| :------- | :----------------------- | :------------------------------------------------------------------------------------------------- | :---------------------------------------- |
| **P2**   | **Reaction Time Metric** | Measure the time delta between an asteroid entering "Danger Radius" and the agent changing inputs. | Quantifies reflexes and processing speed. |

### 3.3. Spatial & Physics Analytics

| Priority | Enhancement                     | Description                                                                         | Rationale                                 |
| :------- | :------------------------------ | :---------------------------------------------------------------------------------- | :---------------------------------------- |
| **P1**   | **Average Engagement Distance** | Calculate the average distance between Player and Asteroid at the moment of a Kill. | Quantitative measure of engagement style. |

### 3.4. Neural Network Diagnostics

| Priority | Enhancement                       | Description                                                                 | Rationale                                                          |
| :------- | :-------------------------------- | :-------------------------------------------------------------------------- | :----------------------------------------------------------------- |
| **P3**   | **Neuron Saturation Check**       | Report the % of time hidden neurons are stuck at -1 or 1 (tanh saturation). | Diagnoses "dead" networks or potential learning issues.            |
| **P3**   | **Input Feature Importance**      | Correlate specific inputs (e.g., "Bullet Cooldown") with action intensity.  | Reveals what the agent is actually "looking at" to make decisions. |
| **P3**   | **Weight Magnitude Distribution** | Histogram of network weights.                                               | Detects exploding weights that might require regularization.       |

### 3.5. Evolutionary Metrics & Robustness

| Priority | Enhancement                    | Description                                                             | Rationale                                                                   |
| :------- | :----------------------------- | :---------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| **P2**   | **Lineage/Ancestry Tracking**  | Track "Parent ID" to visualize genetic drift and identify "Eve" agents. | Helps understand diversity loss and the genealogy of successful traits.     |
| **P2**   | **Crossover Efficiency**       | Measure if Children fitness > Parent fitness on average.                | Validates if the crossover operator is actually constructive.               |
| **P2**   | **Generalization Grade Trend** | Plot the "Fresh Game Grade" (A-F) over time, not just for the last 10.  | Visualizes if the agent is becoming more robust or just overfitting harder. |
