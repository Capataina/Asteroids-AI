# Analytics & Data Schema: Implemented vs. Planned

## 1. Introduction

This document provides a comprehensive overview of the Asteroids AI project's analytics and data collection systems. It serves as a unified reference, merging the original enhancement proposals with a clear-eyed assessment of the current implementation.

The guiding philosophy is that **if we observe it during training, we should be able to analyze it later.** This document outlines what we currently track and what is planned for the future to achieve a deeper, more actionable understanding of agent behavior and training dynamics.

---

## 2. Current Implemented System

A significant portion of the proposed analytics and data schema has already been implemented. The system is designed to be modular, with data collection handled by `training/analytics/collectors` and report generation by `training/analytics/reporting`.

### 2.1. Implemented Data Schema

The current data schema (`version 2.0`) is defined in `training/analytics/collection/models.py` and captured in `training_data.json`. The following data categories are **fully implemented and collected** during every training run:

| Data Category | Schema Fields | Status | Notes |
| :--- | :--- | :--- | :--- |
| **Core Aggregates** | `best_fitness`, `avg_fitness`, `min_fitness`, `median_fitness`, `std_dev`, `percentiles` | ✅ **Implemented** | Basic population statistics per generation. |
| **Behavioral Aggregates** | `avg_kills`, `avg_steps`, `avg_accuracy`, `avg_shots` | ✅ **Implemented** | Population-wide average behaviors. |
| **Reward Breakdown** | `avg_reward_breakdown` | ✅ **Implemented** | Per-component reward averages for the population. |
| **Fresh Game Performance** | `fresh_game` object, `generalization_metrics` object | ✅ **Implemented** | **CRITICAL**: Captures the best agent's performance in an unseeded game to test generalization. |
| **Population Distributions**| `distributions` object containing arrays for `fitness_values`, `kills_values`, etc. | ✅ **Implemented** | Captures the full data for every agent in a generation, not just averages. Enables deep statistical analysis. |

### 2.2. Implemented Analytics Report

The `training_summary.md` report is automatically generated and already includes the majority of the proposed analytics sections. The following features are **fully implemented**:

-   **Quick Trend Overview**: ASCII sparklines for at-a-glance trend visualization.
-   **Overall Summary**: High-level training outcomes, including generalization performance.
-   **Generation Highlights**: Tables of the best-performing generations.
-   **Temporal Analysis (Deciles/Trends)**: Multiple views breaking down the training run into phases to show how performance and behavior evolved over time.
-   **Kill Efficiency Analysis**: Metrics like "Kills per 100 Steps" and "Shots per Kill" to distinguish skillful from lucky agents.
-   **Learning Velocity**: Analysis of the rate of improvement.
-   **Reward Component Evolution**: A table showing how the agent's sources of reward changed over the course of training.
-   **Reward Balance Warnings**: Automated checks for potential issues in the reward structure (e.g., one component dominating all others).
-   **Population Health & Convergence**: Analysis of population diversity (`std_dev`) and convergence status.
-   **Stagnation Analysis**: Detection of learning plateaus.
-   **Generalization Analysis**: A dedicated section analyzing the `fresh_game` data to assess how well the agent's skills transfer to new scenarios.
-   **Correlation Analysis**: A matrix showing the statistical correlation between various metrics and fitness.
-   **Survival Distribution**: Analysis of when and how often agents die.
-   **Detailed Tables**: Breakdowns of the most recent and all-time best generations.
-   **ASCII Fitness Chart**: A simple plot of fitness progression.

---

## 3. Planned Enhancements

This section details the features and data structures that have **not yet been implemented**. It provides a clear, prioritized roadmap for future development.

### 3.1. Planned Data Schema Expansions

The following data types need to be added to the data collection pipeline. They are prerequisites for several of the most valuable planned analytics features.

| Priority | Data Category | Proposed Fields | Status | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **P1** | **Action-Level Metrics** | `action_metrics` object with fields like `avg_thrust_frequency`, `avg_turn_frequency`, etc. | ❌ **Not Implemented** | Moves from *inferring* agent behavior to *observing* it directly. Essential for accurate behavioral classification. |
| **P2** | **Computational Metadata**| `timing` object with `generation_duration`, `evaluation_duration`, etc. | ❌ **Not Implemented** | Provides data for performance profiling and identifying bottlenecks in the training pipeline. |
| **P3** | **Genetic Operator Stats** | `operator_stats` object with `crossovers_performed`, `mutation_impact`, etc. | ❌ **Not Implemented** | Helps in debugging the GA itself and tuning hyperparameters like mutation and crossover rates. |

### 3.2. Planned Analytics Report Enhancements

The implementation of the features below is blocked by the missing data collection described above.

| Priority | Enhancement | Description | Status | **Prerequisite** |
| :--- | :--- | :--- | :--- | :--- |
| **P1** | **Behavioral Classification** | Automatically classify the agent's emergent strategy (e.g., "Camper", "Hunter", "Sniper") based on its actions. | ❌ **Not Implemented** | **Action-Level Metrics** |
| **P2** | **Best Agent Deep Profile** | An expanded profile of the all-time best agent, including its action profile and a more detailed dominance analysis. | ⚠️ **Partially Implemented** | **Action-Level Metrics** |
| **P3** | **Milestone Timeline** | A timeline showing when the training run first achieved key milestones (e.g., "First 10-kill agent at Gen 12"). | ❌ **Not Implemented** | **Computational Metadata** (for timestamps) |
| **P4** | **Action Distribution Estimates**| A more accurate estimation of agent action patterns. | ❌ **Not Implemented** | **Action-Level Metrics** |

### 3.3. Implementation Roadmap

Development should proceed in the following order to satisfy dependencies.

#### **Phase 1: Implement Action Metrics Collection**

1.  **Modify `parallel_evaluator.py`**: In the `evaluate_single_agent` loop, add counters for each action type (`thrust`, `turn`, `shoot`, `idle`).
2.  **Return Action Data**: Have the evaluation function return these action counts along with other metrics.
3.  **Update `AnalyticsData` Model**: Add the `action_metrics` dictionary to the schema in `models.py`.
4.  **Update `record_generation`**: The collector function needs to accept and store this new data.
5.  **Implement Analytics**: Once the data is flowing, implement the **Behavioral Classification** and enhance the **Best Agent Profile** sections in the `MarkdownReporter`.

#### **Phase 2: Implement Computational & Operator Metadata Collection**

1.  **Modify `train_ga_parallel.py`**: Add `time()` captures around the evaluation, evolution, and display phases within the main `update` loop. Count the applications of crossover and mutation.
2.  **Update `AnalyticsData` Model**: Add the `timing` and `operator_stats` dictionaries to the schema.
3.  **Update `record_generation`**: Pass the new data to the collector.
4.  **Implement Analytics**: Implement the **Milestone Timeline** section in the `MarkdownReporter`.
