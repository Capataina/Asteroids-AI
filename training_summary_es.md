# Training Summary Report

**Generated:** 2026-01-31 23:44:26
**Schema Version:** 2.3

## Table of Contents

- [Quick Trend Overview](#quick-trend-overview)
- [Report Takeaways (All Sections)](#report-takeaways-all-sections)
- [Training Configuration](#training-configuration)
- [Overall Summary](#overall-summary)
- [Best Agent Deep Profile](#best-agent-deep-profile)
- [Generation Highlights](#generation-highlights)
- [Milestone Timeline](#milestone-timeline)
- [Training Progress by Phase](#training-progress-by-phase)
- [Distribution Analysis](#distribution-analysis)
- [Kill Efficiency Analysis](#kill-efficiency-analysis)
- [Learning Velocity](#learning-velocity)
- [Reward Component Evolution](#reward-component-evolution)
- [Reward Balance Analysis](#reward-balance-analysis)
- [Population Health Dashboard](#population-health-dashboard)
- [Stagnation Analysis](#stagnation-analysis)
- [Generalization Analysis (Fresh Game)](#generalization-analysis-fresh-game)
- [Correlation Analysis](#correlation-analysis)
- [Survival Distribution](#survival-distribution)
- [Behavioral Summary](#behavioral-summary-last-10-generations)
- [Learning Progress](#learning-progress)
- [Neural & Behavioral Complexity](#neural--behavioral-complexity)
- [Risk Profile Analysis](#risk-profile-analysis)
- [Control Diagnostics](#control-diagnostics)
- [Convergence Analysis](#convergence-analysis)
- [Behavioral Trends](#behavioral-trends)
- [Recent Generations](#recent-generations-last-30)
- [Top 10 Best Generations](#top-10-best-generations)
- [Trend Analysis](#trend-analysis)
- [Fitness Progression](#fitness-progression-ascii-chart)
- [Technical Appendix](#technical-appendix)

---

## Quick Trend Overview

```
Best Fitness     130 -> 213  [: +:+=.@]  breakout improvement (high confidence)
Avg Fitness      -2 -> 76  [ ...=-.@]  breakout improvement (low confidence (noisy))
Min Fitness      -80 -> -50  [ -..:*-@]  breakout improvement (moderate confidence)
Fitness Spread   59 -> 74  [: =:@-.+]  slight regression (moderate confidence)
Avg Kills        3.5 -> 7.3  [ :..+-:@]  breakout improvement (high confidence)
Avg Accuracy     32% -> 36%  [ -  %-:@]  volatile (low confidence (noisy))
Avg Steps        618 -> 737  [ =. =. @]  steady improvement (moderate confidence)
Action Entropy   1.58 -> 1.33  [=%: @%: ]  volatile (low confidence (noisy))
Output Saturation 0% -> 3%  [      .@]  stagnation (low confidence)
Frontness Avg    48% -> 50%  [ **+@*%+]  stagnation (low confidence)
Danger Exposure  16% -> 15%  [:@+ : .*]  stagnation (low confidence)
Seed Fitness Std 66.1 -> 99.0  [ =-.+=:@]  sharp regression (high confidence)
```

### Quick Trend Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Average kills:** Mean kills per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Average steps:** Mean steps survived per episode across the population.
- **Action entropy:** Entropy of action combinations (higher = more varied control).
- **Output saturation:** Share of NN outputs near 0 or 1 (binary control tendency).
- **Frontness average:** Alignment of nearest asteroid with ship heading (1 ahead, 0 behind).
- **Danger exposure rate:** Fraction of frames with a nearby asteroid inside danger radius.
- **Soft-min TTC:** Weighted time-to-collision proxy that emphasizes the nearest threats (seconds).
- **Seed fitness std:** Average per-agent fitness std dev across seeds (evaluation noise proxy).

## Report Takeaways (All Sections)

- Quick Trend Overview: sparklines summarize phase-based metric direction and confidence.
- Training Configuration: report includes a full hyperparameter snapshot for reproducibility.
- Overall Summary: best fitness 281.52 at Gen 8.
- Best Agent Deep Profile: Gen 8 with 15.333333333333334 kills.
- Heatmaps: spatial patterns available for best agent and population.
- Generation Highlights: top improvements/regressions and record runs flagged.
- Milestone Timeline: milestones are run-relative (percent-of-peak thresholds).
- Training Progress by Phase: 4 equal phases used for normalized comparisons.
- Distribution Analysis: fitness spread trend is slight regression.
- Kill Efficiency: phase-level kill rates and shot efficiency tracked.
- Learning Velocity: phase-based fitness deltas and acceleration reported.
- Reward Component Evolution: per-component shifts tracked across 4 phases.
- Reward Balance Analysis: dominance, entropy, and penalty skew checked.
- Population Health Dashboard: diversity, elite gap, and floor trends summarized.
- Stagnation Analysis: plateau lengths compared to run history.
- Generalization Analysis: fresh-game ratios and reward transfer gaps reported.
- Correlation Analysis: fitness vs kills/survival/accuracy correlations reported.
- Survival Distribution: phase-level survival averages and max survival summarized.
- Behavioral Summary: recent kills, steps, and accuracy summarized.
- Learning Progress: phase comparisons for best/avg/min fitness.
- Neural & Behavioral Complexity: saturation and entropy trends reported.
- Risk Profile Analysis: proximity trends and archetypes reported.
- Control Diagnostics: turn bias, frontness, danger, and movement diagnostics reported.
- GNN-SAC Diagnosis: no SAC-specific diagnostics recorded.
- Convergence Analysis: recent diversity and range trends summarized.
- Behavioral Trends: action mix and intra-episode scoring patterns reported.
- Recent Generations: last 8 gens tabulated.
- Top Generations: best run is Gen 8.
- Trend Analysis: phase-based fitness trend table provided.
- ASCII Chart: best vs avg fitness progression visualized.
- Technical Appendix: runtime costs, operator stats, and ES optimizer diagnostics reported when available.

## Training Configuration

```
method: Evolution Strategies
optimizer: cmaes
population_size: 10
num_generations: 500
cmaes_sigma: 0.15
cmaes_mu: auto
cmaes_cov_min: 1e-06
cmaes_cov_target_rate: 0.001
cmaes_cov_max_scale: 10000.0
sigma_min: 0.02
use_antithetic: True
seeds_per_agent: 3
use_common_seeds: True
noise_handling_enabled: True
noise_handling_top_k: 5
noise_handling_extra_seeds: 1
noise_handling_seed_offset: 100000
restart_enabled: True
restart_patience: 12
restart_min_generations: 5
restart_cooldown: 5
restart_sigma_multiplier: 1.0
restart_use_best_candidate: True
max_workers: 16
temporal_stack_enabled: True
temporal_stack_size: 4
temporal_stack_include_deltas: True
pareto_enabled: True
pareto_objectives: ['hits', 'time_alive', 'softmin_ttc']
pareto_accuracy_min_shots: 5
pareto_accuracy_zero_below_min_shots: True
pareto_frame_delay: 0.016666666666666666
pareto_risk_ttc_max: 5.0
pareto_risk_tau: 1.0
pareto_fitness_tiebreaker: True
```

### Config Takeaways

- Configuration snapshot captures the exact training parameters for reproducibility.

### Config Glossary

- **Config value:** Literal hyperparameter or run setting recorded at training start.

## Overall Summary

- **Total Generations:** 8
- **Training Duration:** 0:04:22.897112
- **All-Time Best Fitness:** 281.52
- **Best Generation:** 8
- **Final Best Fitness:** 281.52
- **Final Average Fitness:** 136.92
- **Avg Improvement (Phase 1->Phase 4):** 78.30
- **Stagnation:** 0 generations since improvement

**Generalization (Fresh Game Performance):**
- Avg Generalization Ratio: 0.47
- Best Fresh Fitness: 95.61 (Gen 6)
- Episode Completion Rate: 0.0%

### Takeaways

- Best fitness achieved: 281.52 (Gen 8).
- Final avg fitness: 136.92.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Avg improvement (Phase 1->Phase 4):** Difference between average fitness in the first and last 25% of training.
- **Generalization ratio:** Fresh-game fitness divided by training fitness (averaged across fresh runs).
- **Episode completion rate:** Share of fresh-game episodes that completed the full max-step window.

## Best Agent Deep Profile

The most fit agent appeared in **Generation 8** with a fitness of **281.52**.

### Combat Efficiency

- **Total Kills:** 15.333333333333334
- **Survival Time:** 19.4 seconds (1161.0 steps)
- **Accuracy:** 44.9%
- **Shots per Kill:** 2.2
- **Time per Kill:** 1.26 seconds

### Behavioral Signature

**Classification:** `Sniper`

| Action | Rate (per step) | Description |
|--------|-----------------|-------------|
| **Thrust** | 6.0% | Movement frequency |
| **Turn** | 100.0% | Rotation frequency |
| **Shoot** | 81.4% | Trigger discipline |

### Takeaways

- Best agent achieved 15.333333333333334 kills with 44.9% accuracy.
- Behavioral classification: Sniper.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Average steps:** Mean steps survived per episode across the population.
- **Shots per kill:** Shots fired divided by kills (lower is more efficient).

### Spatial Analytics (Best Agent - Generations 1-8)

**Position Heatmap (Where does it fly?)**
```
|                                                                                                                        |
|                    .                                                                                                   |
|                                                                                                                        |
|                                   .                                                                                    |
|                                                                                                                        |
|                                                                                                                        |
|                                             .                                                                          |
|                                                                                                                        |
|                                                                                                                        |
|                                                   .                                                                    |
|                                                      ...  .                                                            |
|                                     :       .  .     :        .                                                        |
|                                            :  .   .      .  .  :                                                       |
|                                                           . :   :          .                                           |
|               .  .                                    . ..=@:.:  ..    .    .                                          |
|                     .                .                 .:===- .   :::   .                                              |
|                             . .                     .=:  -.   :::.  ..   ..                                            |
|                           ..        .           .       .      :       ..             .                                |
|                          . .           .:-: .      .   .    .  .        .    .                                         |
|                     .      .                  .         .... .      ..                                                 |
|                                       .                  .        ..      .                                            |
|               .                                               .::..       .       .     .                              |
|           .        .   .    :     .    .                    .         .                                                |
|                      .                          .               .                                                      |
|                        .           .                                         .     .                                   |
|                           .             .                                         .                                    |
|                                    :                 .                         .                                       |
|                                                     .          .        .                                              |
|                                                                                                                        |
|                                                                                                                        |
```

**Kill Zone Heatmap (Where does it kill?)**
```
|                                                                                                                        |
|                .                                                                                                       |
|                       .                                                                                                |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                .                                                                       |
|                                                                                                                        |
|                                                  .                                                                     |
|                                         .             .                                                                |
|                                                    . .      .                                                          |
|                                                .   :    .      .                                                       |
|                                                             =.  :                                                      |
|                                                           +@:.:         .                                              |
|                                                        .-+-=: ..  ::::                                                 |
|                     .                                +:  =.   .-.     ... .                                            |
|                                               . : .            ..       :.                                             |
|                   .        .          ...=             .       .     .   .                                             |
|                               .                 .       .: ..        .   .     .         .                             |
|             .         .  .                              ..          .   .                                              |
|                                 . .                            ..:.                                                    |
|              .             .  .    .                            .      .                                               |
|                      .   .            .  .                                                                             |
|                                     .     .     .       .                   .                                          |
|                                       .                                            .                                   |
|                                    .                                          .                                        |
|                                           .                                 .                                          |
|                                                                                                                        |
|                                             .                                                                          |
```

### Spatial Analytics (Population Average - Generations 1-8)

**Position Heatmap (Where do they fly?)**
```
|                                                                 .                                                      |
|                               .                                                                                        |
|                                                                                    .                                   |
|                      .                      .                                                                          |
|                                   .          .              . .                                                        |
|                                                                     ...                      .                         |
|                                             :.   .     .      .  .                        .                            |
|                      .                    .   .                  .                                                     |
|                                       .   .                . .         .                               .               |
|                                           .   ..  .      ..   . .                                                      |
|                                                .   .   .  ..   ..          .    .                                      |
|                                     :       : :. :.  . :   .. . . ..   :    .   :.       .                             |
|             .                              .:..   :. .: ::  . ::.. .    .  ..  .                .                      |
|                                               . :..:.: ::.-.-: .:.:.... .. .                                           |
|                       .                   . .     :. ::::-=@=:: .:          .                                          |
|                                                   . .:-:-==+=:::. :.. . .             .                                |
|                   .     .  .. .                .   .:-..:-.-:::-:   ..    .                                            |
|                            . .      ..                  .::..:::   ..  :.: .          .  . .                           |
|                      .     .           ..:.  ..    .    .   :.     :       .                                           |
|                        .       .     .                 .. .. .      .. .                                               |
|                         .                                          .      .            . .                             |
|                                                                ..                 .      .                             |
|            .                .                  .   .           .      .                                          .     |
|                                                                ..                                                      |
|                                                                             .     .      .                             |
|                                                         .                                                              |
|                     .              .  .                  .                     .                                       |
|                                                                         .                                              |
|                                              .                                                        .                |
|                              .                           .                                                             |
```

**Kill Zone Heatmap (Where do they kill?)**
```
|              .                 .  .               .  .          . . .                                               .  |
|            .   .     .       .         .                         .                   .              .                  |
|                       .  .           .          .      .                      .      ..    .             .             |
|           .  .                .            .          .                                           .     . ..           |
|                                        .  .   . .   .        ...             .                       . .  .            |
|            .              .      .               :   .           .. ...            .  .  .:             .              |
|   .. .          .     .               .    . ..     ...    ...  .      .                      ..                       |
|        .    .    .          .             .  ...         ..  .  .          . .  .  ..  .  .   .         .              |
|    .                 .           .   ..   .   ..   .       ... ..   : ..          ..   .                           . . |
|           .                            .    . .  .   .  .  .  ..      .           .     ..    ...   .    .  ...       .|
|             .        .                  .       ..  . .    . .  ..  . ...  .    .     .    .  .                        |
|                                              .  .... . : . .. ... .   .  .  .         ..                 . .           |
|         .  . .   .                    .   . .. .. .: ...:.   ... ...   .                         ..    .  .            |
|   ...  . .                  .        .       . . .: .:..:.:.-:..: .. . : .   .     .    .           .       .          |
|              .   .                    .    .   .. . ....::=@=.:.... .   .            .   .  .          .               |
|     ..     .       .   . .             .          .. :---==+=:::. .:.:. :     .     .    .         .              .    |
|                    ..   . . . .    .   .       . . ..-...=.=:::-. . ..... .      . ..                 .                |
|             .       .      ...       .    .   . : .     . .. --:.  . . .:. .   .       .  .                    .       |
|                   .       ..          ...- . ::        ..  .....   . : . . .  .                        .               |
|        .               .      .       ..       ..   . . .: ....  .   .  ..     .. .      .          .         .        |
|.     .      .         . ..                            . ..     .    ..  .  . .      . .     .                          |
|    .            .               . .               .       .    ..:..     .   .   ..  ....     .           ..      .    |
|  .           .   .         .  .    .           .        .     . .   .  ..   . ..    .  . .  .               .          |
|                  .   .   .            .  .   .     .   . ..   .        .       ..          .  .                        |
|   ..  .          .. .              ..  .  .     ..  ..  . .          .   .  ..     .. .                          .   . |
|                  .                  . .       .       .  .    .                    .                 .  ..             |
|                           .   .    ..     .               .  ..  .            ..   .                                   |
|                                      .    .              .  . .             .      .     .   .          .              |
|               .         .                                     .                    .                                   |
|            . .        .    .  .  .          .        .         ...                      .                              |
```

### Heatmap Takeaways

- Heatmaps aggregate spatial samples over the last 8 generations.
- Best-agent and population heatmaps highlight spatial biases and kill zones.

### Heatmap Glossary

- **Position heatmap:** Density of sampled player positions during evaluation.
- **Kill heatmap:** Density of player positions at kill events (proxy for engagement zones).

## Generation Highlights

### Best Improvement

**Generation 8**: Best fitness jumped +137.1 (+95.0%)
- New best fitness: 281.5

### Worst Regression

**Generation 7**: Best fitness dropped -58.9 (-29.0%)
- New best fitness: 144.4
- Note: this can be normal variation after a lucky outlier

### Most Accurate Generation

**Generation 8**: Population accuracy reached 39.8%

### Most Kills (Single Agent)

**Generation 5**: An agent achieved 16 kills

### First Viable Population

**Generation 2**: Average fitness first became positive

### Most Diverse Generation

**Generation 3**: Diversity index 15.90

### Most Converged Generation

**Generation 8**: Diversity index 0.63

### Takeaways

- Best improvement at Gen 8 (+137.1).
- Worst regression at Gen 7 (-58.9).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Max kills:** Highest kills achieved by any agent in the generation.
- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).

## Milestone Timeline

| Generation | Category | Value | Description |
|------------|----------|-------|-------------|
| 1 | Fitness | 152 | Best fitness reached 25% of run peak |
| 1 | Fitness | 152 | Best fitness reached 50% of run peak |
| 1 | Kills | 6 | Max kills reached 25% of run peak |
| 2 | Kills | 12 | Max kills reached 50% of run peak |
| 2 | Kills | 12 | Max kills reached 75% of run peak |
| 2 | Viability | 14 | Average fitness turned positive |
| 3 | Fitness | 212 | Best fitness reached 75% of run peak |
| 5 | Avg Fitness | 65 | Avg fitness reached 25% of run peak |
| 5 | Kills | 16 | Max kills reached 90% of run peak |
| 8 | Fitness | 282 | Best fitness reached 90% of run peak |
| 8 | Fitness | 282 | Best fitness reached 95% of run peak |
| 8 | Fitness | 282 | Best fitness reached 98% of run peak |
| 8 | Avg Fitness | 137 | Avg fitness reached 50% of run peak |
| 8 | Avg Fitness | 137 | Avg fitness reached 75% of run peak |
| 8 | Avg Fitness | 137 | Avg fitness reached 90% of run peak |

### Takeaways

- Total milestones reached: 15.
- Latest milestone at Gen 8 (Avg Fitness).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Max kills:** Highest kills achieved by any agent in the generation.

## Training Progress by Phase

| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|------|----------|---------|-----------|---------|-----------|----------|
| Phase 1 (0-25%) | 1-2 | 152 | -2 | 3.5 | 32% | 618 | 59 |
| Phase 2 (25-50%) | 3-4 | 212 | 8 | 3.6 | 30% | 513 | 73 |
| Phase 3 (50-75%) | 5-6 | 207 | 52 | 6.2 | 37% | 656 | 90 |
| Phase 4 (75-100%) | 7-8 | 282 | 76 | 7.3 | 36% | 737 | 74 |

### Takeaways

- Phase breakdown uses equal 25% blocks for run-normalized comparisons.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Average kills:** Mean kills per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Average steps:** Mean steps survived per episode across the population.
- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).

## Distribution Analysis

### Metric Distributions (Last 8 Generations)

Visualizing population consistency: `|---O---|` represents Mean +/- 1 StdDev.
- **Narrow bar**: Consistent population (convergence)
- **Wide bar**: Diverse or noisy population

**Accuracy Distribution**
```
Gen   1:     |-----------------O----------------|            30.1% +/- 11.3%
Gen   2:          |-----------------O------------------|     33.6% +/- 11.8%
Gen   3: |---------------------O----------------------|      30.5% +/- 14.7%
Gen   4:        |--------------O-------------|               29.9% +/-  9.2%
Gen   5:                        |------------O------------|  39.2% +/-  8.6%
Gen   6:                 |-----------O-----------|           33.9% +/-  7.7%
Gen   7:               |-----------O-----------|             32.8% +/-  7.9%
Gen   8:                             |--------O--------|     39.8% +/-  5.7%
```

**Survival Steps Distribution**
```
Gen   1:            |--------O--------|                      505.0 +/- 221.9
Gen   2:                  |-----------O-----------|          731.7 +/- 292.6
Gen   3:               |-------O-------|                     551.5 +/- 193.4
Gen   4:            |-------O------|                         475.0 +/- 181.2
Gen   5:                |-------------O-------------|        732.0 +/- 339.6
Gen   6:                 |------O------|                     579.9 +/- 174.7
Gen   7:              |------O------|                        512.9 +/- 170.0
Gen   8:                                 |-----O------|      961.3 +/- 161.1
```

**Kills Distribution**
```
Gen   1: |--------O--------|                                   2.4 +/-   2.8
Gen   2:         |-------O-------|                             4.6 +/-   2.5
Gen   3:   |----------O----------|                             3.8 +/-   3.4
Gen   4:    |--------O--------|                                3.4 +/-   2.8
Gen   5:           |------------O-------------|                6.9 +/-   4.2
Gen   6:          |---------O---------|                        5.4 +/-   3.0
Gen   7:        |--------O-------|                             4.5 +/-   2.7
Gen   8:                       |----------O-----------|       10.0 +/-   3.6
```

**Fitness Distribution**
```
Gen   1: |---------O---------|                               -18.6 +/-  66.3
Gen   2:        |-------O-------|                             14.3 +/-  52.6
Gen   3:  |-----------O-----------|                            5.0 +/-  80.1
Gen   4:     |---------O---------|                            10.0 +/-  66.8
Gen   5:       |---------------O---------------|              65.0 +/- 104.2
Gen   6:        |----------O-----------|                      38.6 +/-  74.8
Gen   7:      |---------O--------|                            15.4 +/-  62.6
Gen   8:                     |------------O------------|     136.9 +/-  85.6
```

**Aim Frontness Distribution**
```
Gen   1: |-------------O--------------|                      46.1% +/-  6.4%
Gen   2:             |---------O----------|                  49.7% +/-  4.6%
Gen   3:               |-------O-------|                     49.5% +/-  3.5%
Gen   4:             |---------O---------|                   49.3% +/-  4.4%
Gen   5:  |-----------------------O-----------------------|  50.9% +/- 10.4%
Gen   6:                 |------O-----|                      49.8% +/-  2.9%
Gen   7:               |----------O----------|               50.9% +/-  4.8%
Gen   8:        |-------------O--------------|               49.2% +/-  6.2%
```

**Danger Exposure Distribution**
```
Gen   1:        |----------O-----------|                     14.2% +/-  4.0%
Gen   2:              |-----------------O-----------------|  18.6% +/-  6.3%
Gen   3:              |-----------O-----------|              16.5% +/-  4.3%
Gen   4: |------------O------------|                         12.3% +/-  4.6%
Gen   5:      |------------O------------|                    14.0% +/-  4.5%
Gen   6:    |---------O----------|                           12.4% +/-  3.7%
Gen   7:         |--------O-------|                          13.6% +/-  2.8%
Gen   8:              |------------O------------|            16.8% +/-  4.5%
```

**Turn Deadzone Distribution**
```
Gen   1: O                                                    0.0% +/-  0.0%
Gen   2: O                                                    0.0% +/-  0.0%
Gen   3: O                                                    0.0% +/-  0.0%
Gen   4: O                                                    0.0% +/-  0.0%
Gen   5: O                                                    0.0% +/-  0.0%
Gen   6: O                                                    0.0% +/-  0.0%
Gen   7: O                                                    0.0% +/-  0.0%
Gen   8: O                                                    0.0% +/-  0.0%
```

**Coverage Ratio Distribution**
```
Gen   1:                       |-------O--------|            38.9% +/-  8.9%
Gen   2:              |-----------------O-----------------|  40.0% +/- 19.6%
Gen   3:   |------------O------------|                       22.5% +/- 14.2%
Gen   4: |----------O-----------|                            18.1% +/- 12.6%
Gen   5:             |---------------O--------------|        35.8% +/- 16.6%
Gen   6:          |-------------O------------|               30.6% +/- 14.7%
Gen   7:    |-----O-----|                                    15.8% +/-  6.4%
Gen   8:   |---------O----------|                            19.4% +/- 11.3%
```

**Seed Fitness Std Distribution**
```
Gen   1:      |-------O------|                                49.5 +/-  29.0
Gen   2:           |----------O-----------|                   82.7 +/-  41.9
Gen   3:      |-------------O-------------|                   74.3 +/-  51.9
Gen   4:         |--------O-------|                           64.6 +/-  32.7
Gen   5:              |----------O-----------|                93.8 +/-  44.3
Gen   6:           |-------------O------------|               90.5 +/-  50.9
Gen   7:          |---------O---------|                       74.1 +/-  36.8
Gen   8:                     |-----------O------------|      123.9 +/-  47.3
```

### Takeaways

- Fitness spread trend: slight regression (moderate confidence).
- Seed variance trend: sharp regression (high confidence).

### Warnings

- Fitness spread is widening or volatile; convergence is weak.
- Seed-to-seed variance is rising; evaluation noise may mask true improvements.

### Glossary

- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Seed fitness std:** Average per-agent fitness std dev across seeds (evaluation noise proxy).
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Accuracy std dev:** Standard deviation of accuracy across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Steps std dev:** Standard deviation of survival steps across the population.
- **Average kills:** Mean kills per episode across the population.
- **Kills std dev:** Standard deviation of kills across the population.
- **Frontness average:** Alignment of nearest asteroid with ship heading (1 ahead, 0 behind).
- **Frontness std dev:** Standard deviation of frontness across the population.
- **Danger exposure rate:** Fraction of frames with a nearby asteroid inside danger radius.
- **Danger exposure std dev:** Standard deviation of danger exposure across the population.
- **Soft-min TTC:** Weighted time-to-collision proxy that emphasizes the nearest threats (seconds).
- **Soft-min TTC std dev:** Standard deviation of soft-min TTC across the population.
- **Turn deadzone rate:** Fraction of frames where signed turn input is exactly zero (deadzone currently disabled).
- **Deadzone std dev:** Standard deviation of the per-agent zero-turn rate across the population (deadzone currently disabled).
- **Coverage ratio:** Fraction of spatial grid cells visited (0 to 1).
- **Coverage std dev:** Standard deviation of coverage ratio across the population.

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 0.99 (Phase 1: 0.57)
- **Shots per Kill:** 6.01 (Phase 1: 6.74)
- **Kill Conversion Rate:** 16.6% (Phase 1: 14.8%)
- **Average Kills per Episode:** 7.3

### Efficiency Trend (Phase Averages)

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 (0-25%) | 0.57 | 6.74 | 14.8% |
| Phase 2 (25-50%) | 0.70 | 7.25 | 13.8% |
| Phase 3 (50-75%) | 0.94 | 6.08 | 16.5% |
| Phase 4 (75-100%) | 0.99 | 6.01 | 16.6% |

### Takeaways

- Kill rate changed from 0.57 to 0.99 kills/100 steps.
- Shots per kill moved from 6.74 to 6.01.

### Glossary

- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Average shots:** Mean shots fired per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Shots per kill:** Shots fired divided by kills (lower is more efficient).

## Learning Velocity

Not enough data for velocity analysis (need at least 10 generations).

## Reward Component Evolution

| Component | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Trend | Status |
|-----------|---------|---------|---------|---------|-------|--------|
| DistanceBasedKillReward | +52.5 | +53.8 | +92.2 | +109.0 | ++ +108% | Learned |
| DeathPenalty | -76.1 | -82.1 | -74.8 | -71.3 | ~ +6% | Improving penalty |
| ConservingAmmoBonus | +11.5 | +12.6 | +24.7 | +25.6 | +++ +123% | Learned |
| TargetLockReward | +14.5 | +13.5 | +16.4 | +20.9 | + +44% | Learned |

### Takeaways

- DistanceBasedKillReward shifted up by +108% from Phase 1 to Phase 4.
- ConservingAmmoBonus shifted up by +123% from Phase 1 to Phase 4.

### Glossary

- **Reward breakdown:** Per-component average reward contribution per episode.

## Reward Balance Analysis

### Balance Metrics (Latest Generation)

- Reward dominance index (HHI): 0.53
- Reward entropy (normalized): 0.75
- Max component share: 69.8%
- Positive component count: 3

### Takeaways

- Reward mix is broadly stable with no major dominance spikes.

### Warnings

- Max component share is high (69.8%).
- DeathPenalty remains negative on average (behavior may be over-penalized).

### Glossary

- **Reward breakdown:** Per-component average reward contribution per episode.
- **Reward dominance index:** HHI-style dominance of positive rewards (higher = more concentrated).
- **Reward entropy:** Normalized entropy of positive reward components (balance proxy).
- **Reward max share:** Share of total positive reward from the largest component.
- **Positive component count:** Number of reward components with positive contribution.

## Population Health Dashboard

### Current Status: Warning

| Metric | Value | Trend (Recent) |
|--------|-------|----------------|
| Diversity Index | 0.97 | Increasing |
| Elite Gap | 1.80 | Stable |
| Min Fitness Trend | +29.9 | Up |
| Max Fitness Trend | +83.4 | Up |
| IQR (p75-p25) | 112 | Widening |

### Takeaways

- Health status is Warning.
- Diversity index at 0.97 with increasing spread.
- Fitness floor trend +29.9, ceiling trend +83.4.

### Warnings

- Diversity compressed vs run baseline (risk of premature convergence)

### Glossary

- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Average fitness:** Mean fitness across the population for a generation.
- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Fitness p25:** 25th percentile of population fitness.
- **Fitness p75:** 75th percentile of population fitness.

## Stagnation Analysis

- **Current Stagnation:** 0 generations
- **Average Stagnation Period:** 2.5 generations
- **Longest Stagnation:** 4 generations
- **Number of Stagnation Periods:** 2

### Takeaways

- Stagnation periods average 2.5 generations.
- Longest plateau reached 4 generations.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Accuracy | Ratio | Grade | Cause of Death |
|-----|--------------|-----------|----------|-------|-------|----------------|
| 1 | 152 | -81 | 0.0% | 0.00 | F | asteroid_collision |
| 2 | 107 | -57 | 21.1% | -1.04 | F | asteroid_collision |
| 3 | 212 | -18 | 22.5% | 0.00 | F | asteroid_collision |
| 4 | 161 | -40 | 20.0% | -72.27 | F | asteroid_collision |
| 5 | 207 | -10 | 35.5% | -0.09 | F | asteroid_collision |
| 6 | 203 | 96 | 33.9% | 0.47 | D | asteroid_collision |
| 7 | 144 | -66 | 26.7% | -1.62 | F | asteroid_collision |
| 8 | 282 | -83 | 11.1% | -0.29 | F | asteroid_collision |

### Generalization Summary

- **Average Fitness Ratio:** 0.47
- **Best Ratio:** 0.47
- **Worst Ratio:** 0.47

**Grade Distribution:** D:1 F:7 

### Reward Transfer Gap (Fresh vs Training)

| Gen | Share Shift | Largest Share Deltas |
|-----|-------------|----------------------|
| 1 |   78.3% | TargetLockReward +78%, DistanceBasedKillReward -60%, ConservingAmmoBonus -18% |
| 2 |   28.3% | TargetLockReward +28%, DistanceBasedKillReward -16%, ConservingAmmoBonus -12% |
| 3 |   18.7% | ConservingAmmoBonus -19%, TargetLockReward +15%, DistanceBasedKillReward +4% |
| 4 |   13.7% | DistanceBasedKillReward +14%, ConservingAmmoBonus -12%, TargetLockReward -1% |
| 5 |    9.2% | TargetLockReward +9%, DistanceBasedKillReward -7%, ConservingAmmoBonus -3% |
| 6 |   20.9% | TargetLockReward +21%, DistanceBasedKillReward -17%, ConservingAmmoBonus -4% |
| 7 |   24.1% | TargetLockReward +24%, DistanceBasedKillReward -13%, ConservingAmmoBonus -11% |
| 8 |   17.1% | ConservingAmmoBonus -17%, DistanceBasedKillReward +12%, TargetLockReward +5% |

### Takeaways

- Average fitness ratio 0.47 (range 0.47 to 0.47).

### Glossary

- **Fitness ratio:** Fresh-game fitness divided by training fitness for the same generation.
- **Generalization grade:** Letter grade derived from generalization ratios.
- **Reward breakdown:** Per-component average reward contribution per episode.

## Correlation Analysis

Not enough data for correlation analysis.

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 737 steps (49.1% of max)
- **Max Survival:** 1166 steps

### Survival Progression (Phase Averages)

| Phase | Mean Steps | Change vs Prior |
|-------|------------|-----------------|
| Phase 1 (0-25%) | 618 |  |
| Phase 2 (25-50%) | 513 | -105 |
| Phase 3 (50-75%) | 656 | +143 |
| Phase 4 (75-100%) | 737 | +81 |

### Takeaways

- Final-phase survival averages 737 steps.
- Best survival reached 1166 steps.

### Warnings

- Average survival remains below half of max steps; survivability is still limited.

### Glossary

- **Average steps:** Mean steps survived per episode across the population.
- **Max steps:** Highest steps survived by any agent in the generation.

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 5.12
- **Avg Steps Survived:** 631
- **Avg Accuracy:** 33.7%
- **Max Kills (Any Agent Ever):** 15.666666666666666
- **Max Steps (Any Agent Ever):** 1215.6666666666667

### Takeaways

- Recent average kills: 5.12.
- Recent average accuracy: 33.7%.

### Glossary

- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).

## Learning Progress

| Phase | Gens | Avg Best | Avg Mean | Avg Min |
|-------|------|----------|----------|---------|
| Phase 1 (0-25%) | 1-2 | 129.6 | -2.1 | -80.1 |
| Phase 2 (25-50%) | 3-4 | 186.6 | 7.5 | -81.9 |
| Phase 3 (50-75%) | 5-6 | 205.0 | 51.8 | -61.4 |
| Phase 4 (75-100%) | 7-8 | 213.0 | 76.2 | -50.3 |

### Takeaways

- Best fitness trend: breakout improvement (high confidence).
- Average fitness trend: breakout improvement (low confidence (noisy)).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.

## Neural & Behavioral Complexity

| Gen | Saturation | Entropy | Control Style |
|-----|------------|---------|---------------|
| 1 |   0.0% |  1.50 | Analog-leaning |
| 2 |   0.0% |  1.66 | Analog-leaning / Exploratory |
| 3 |   0.0% |  1.36 | Balanced / Repetitive |
| 4 |   0.0% |  1.26 | Analog-leaning / Repetitive |
| 5 |   0.0% |  1.70 | Balanced / Exploratory |
| 6 |   0.3% |  1.68 | Binary-leaning / Exploratory |
| 7 |   0.7% |  1.37 | Binary-leaning |
| 8 |   5.2% |  1.30 | Binary-leaning / Repetitive |

### Takeaways

- Output saturation trend: stagnation (low confidence).
- Action entropy trend: volatile (low confidence (noisy)).

### Warnings

- High saturation with low entropy suggests rigid, repetitive control.

### Glossary

- **Output saturation:** Share of NN outputs near 0 or 1 (binary control tendency).
- **Action entropy:** Entropy of action combinations (higher = more varied control).

## Risk Profile Analysis

Analysis of how close agents let asteroids get before reacting or killing them.

| Gen | Avg Min Dist | Fitness | Kills | Archetype |
|-----|--------------|---------|-------|-----------|
| 1 |   16.7px |  -18.6 |  2.4 | Cautious Underperformer |
| 2 |   15.8px |   14.3 |  4.6 | Balanced |
| 3 |   16.2px |    5.0 |  3.8 | Cautious Underperformer |
| 4 |   13.3px |   10.0 |  3.4 | Overexposed |
| 5 |   16.7px |   65.0 |  6.9 | Sniper |
| 6 |   14.6px |   38.6 |  5.4 | Daredevil |
| 7 |   14.0px |   15.4 |  4.5 | Balanced |
| 8 |   15.8px |  136.9 | 10.0 | Balanced |

### Takeaways

- Min-distance trend: volatile (low confidence (noisy)).
- Danger exposure trend: stagnation (low confidence).

### Glossary

- **Min asteroid distance:** Closest distance to an asteroid during an episode (pixels).
- **Average asteroid distance:** Mean distance to nearest asteroid over time (pixels).
- **Danger exposure rate:** Fraction of frames with a nearby asteroid inside danger radius.
- **Soft-min TTC:** Weighted time-to-collision proxy that emphasizes the nearest threats (seconds).

## Control Diagnostics

### Control Snapshot (Latest Generation)

| Category | Metric | Value |
|----------|--------|-------|
| Turn | Deadzone Rate | 0.0% |
| Turn | Turn Balance (R-L) | +0.39 |
| Turn | Switch Rate | 35.3% |
| Turn | Avg Streak | 18.3f |
| Turn | Max Streak | 108f |
| Aim | Frontness Avg | 49.2% |
| Aim | Frontness at Shot | 48.3% |
| Aim | Frontness at Hit | 55.0% |
| Aim | Shot Distance | 134.2px |
| Aim | Hit Distance | 112.5px |
| Danger | Exposure Rate | 16.8% |
| Danger | Entries | 3.8 |
| Danger | Reaction Time | 0.0f |
| Danger | Wraps in Danger | 0.0 |
| Movement | Distance Traveled | 312.0px |
| Movement | Avg Speed | 0.34 |
| Movement | Speed Std | 0.22 |
| Movement | Coverage Ratio | 19.4% |
| Shooting | Shots per Kill | 6.34 |
| Shooting | Shots per Hit | 2.50 |
| Shooting | Cooldown Usage | 68.7% |
| Shooting | Cooldown Ready | 8.7% |
| Stability | Fitness Std (Seeds) | 123.9 |

### Recent Control Trends (Last 8)

| Gen | Deadzone | Turn Bias | Switch | Frontness | Danger | Coverage |
|-----|----------|-----------|--------|-----------|--------|----------|
| 1 |    0.0% |  -0.03 |   23.9% |   46.1% |   14.2% |   38.9% |
| 2 |    0.0% |  -0.02 |   34.3% |   49.7% |   18.6% |   40.0% |
| 3 |    0.0% |  +0.30 |   28.6% |   49.5% |   16.5% |   22.5% |
| 4 |    0.0% |  +0.49 |   17.1% |   49.3% |   12.3% |   18.1% |
| 5 |    0.0% |  +0.19 |   36.6% |   50.9% |   14.0% |   35.8% |
| 6 |    0.0% |  +0.19 |   34.6% |   49.8% |   12.4% |   30.6% |
| 7 |    0.0% |  +0.51 |   35.5% |   50.9% |   13.6% |   15.8% |
| 8 |    0.0% |  +0.39 |   35.3% |   49.2% |   16.8% |   19.4% |

### Takeaways

- Turn balance trend: sharp regression (low confidence (noisy)).
- Aim alignment trend: stagnation (low confidence).
- Danger exposure trend: stagnation (low confidence).

### Glossary

- **Turn deadzone rate:** Fraction of frames where signed turn input is exactly zero (deadzone currently disabled).
- **Turn balance:** Right-turn frames minus left-turn frames divided by total turning.
- **Turn switch rate:** Rate of turn direction switches per signed turn.
- **Average turn streak:** Average consecutive frames turning in the same direction.
- **Max turn streak:** Longest consecutive turn streak per episode (averaged).
- **Frontness average:** Alignment of nearest asteroid with ship heading (1 ahead, 0 behind).
- **Frontness at shot:** Frontness measured at shot times (aim alignment during firing).
- **Frontness at hit:** Frontness measured at hit times (aim alignment on hits).
- **Shot distance:** Distance to nearest asteroid when firing (pixels).
- **Hit distance:** Distance to nearest asteroid when hits occur (pixels).
- **Danger exposure rate:** Fraction of frames with a nearby asteroid inside danger radius.
- **Danger entries:** Average number of entries into the danger zone per episode.
- **Danger reaction time:** Average frames to react after entering danger.
- **Danger wraps:** Screen-wrap count while in danger zones (mobility under threat).
- **Distance traveled:** Total distance traveled per episode (pixels).
- **Average speed:** Mean movement speed per episode.
- **Speed std dev:** Standard deviation of movement speed per episode.
- **Coverage ratio:** Fraction of spatial grid cells visited (0 to 1).
- **Shots per kill:** Shots fired divided by kills (lower is more efficient).
- **Shots per hit:** Shots fired divided by hits (lower is more efficient).
- **Seed fitness std:** Average per-agent fitness std dev across seeds (evaluation noise proxy).

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 74.13
- Average Range (Best-Min): 251.97
- Diversity Change: +24.5%
- **Status:** Population has balanced diversity

### Takeaways

- Convergence status: balanced.
- Diversity change: +24.5%.

### Glossary

- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Minimum fitness:** Lowest fitness in the population for a generation.

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Safe Dist | Max Kills |
|--------|-----------|-----------|--------------|-----------|----------|
| Q1 | 3.50 | 618 | 31.8% | 163.1px | 12.0 |
| Q2 | 3.58 | 513 | 30.2% | 189.8px | 11.333333333333334 |
| Q3 | 6.15 | 656 | 36.5% | 175.9px | 15.666666666666666 |
| Q4 | 7.27 | 737 | 36.3% | 157.7px | 15.333333333333334 |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
|--------|----------|--------|---------|-------------------|
| Q1 | 33.7% | 100.0% | 41.3% | **Skirmisher** |
| Q2 | 8.1% | 100.0% | 55.0% | **Balanced** |
| Q3 | 15.4% | 100.0% | 75.2% | **Balanced** |
| Q4 | 5.8% | 100.0% | 82.1% | **Sniper** |

### Input Control Style

| Period | Thrust Dur | Turn Dur | Shoot Dur | Idle Rate | Wraps |
|--------|------------|----------|-----------|-----------|-------|
| Q1 | 9.4f | 618.3f | 41.8f | 0.0% | 1.3 |
| Q2 | 1.0f | 513.3f | 23.2f | 0.0% | 0.3 |
| Q3 | 2.4f | 656.0f | 28.6f | 0.0% | 0.5 |
| Q4 | 1.0f | 737.1f | 112.9f | 0.0% | 0.2 |

### Takeaways

- Kills trend: breakout improvement.
- Accuracy trend: volatile.
- Idle rate trend: stagnation.

### Glossary

- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Average asteroid distance:** Mean distance to nearest asteroid over time (pixels).
- **Thrust frames:** Average frames with thrust active per episode.
- **Turn frames:** Average frames with turn input active per episode.
- **Shoot frames:** Average frames with shooting active per episode.
- **Thrust duration:** Average consecutive frames per thrust burst.
- **Turn duration:** Average consecutive frames per turning burst.
- **Shoot duration:** Average consecutive frames per shooting burst.
- **Idle rate:** Fraction of frames with no action input.
- **Screen wraps:** Average number of screen-edge wraps per episode.

### Intra-Episode Score Breakdown

Analysis of when agents earn their reward during an episode (Early vs Late game).

| Quarter | Avg Score | Share of Total | Play Style |
|---------|-----------|----------------|------------|
| Start (0-25%) | 30.5 | 19.6% | Balanced |
| Mid-Game (25-50%) | 56.7 | 36.5% | Balanced |
| Late-Game (50-75%) | 62.0 | 39.9% | Mid-loaded |
| End-Game (75-100%) | 6.1 | 4.0% | Balanced |

### Intra-Episode Takeaways

- Highest scoring quarter: Late-Game (50-75%) (39.9% of episode reward).

### Intra-Episode Glossary

- **Quarterly scores:** Average reward earned in each episode quarter (0-25%, 25-50%, 50-75%, 75-100%).

## Recent Generations (Last 30)

<details>
<summary>Click to expand Recent Generations table</summary>

| Gen   | Best   | Avg    | StdDev | Kills  | Steps  | Acc%   | Stag   |
|-------|--------|--------|--------|--------|--------|--------|--------|
| 1     | 152    | -19    | 66     | 2.4    | 505    | 30     | 0      |
| 2     | 107    | 14     | 53     | 4.6    | 732    | 34     | 1      |
| 3     | 212    | 5      | 80     | 3.8    | 552    | 30     | 0      |
| 4     | 161    | 10     | 67     | 3.4    | 475    | 30     | 1      |
| 5     | 207    | 65     | 104    | 6.9    | 732    | 39     | 2      |
| 6     | 203    | 39     | 75     | 5.4    | 580    | 34     | 3      |
| 7     | 144    | 15     | 63     | 4.5    | 513    | 33     | 4      |
| 8     | 282    | 137    | 86     | 10.0   | 961    | 40     | 0      |

</details>

### Recent Table Takeaways

- Recent table covers 8 generations ending at Gen 8.
- Latest best fitness: 281.5.

### Recent Table Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Median fitness:** Median population fitness (robust central tendency).
- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Best improvement:** Change in best fitness compared to the previous generation.
- **Average improvement:** Change in average fitness compared to the previous generation.
- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).


## Top 10 Best Generations

<details>
<summary>Click to expand Top 10 Best Generations table</summary>

| Rank | Gen   | Best   | Avg    | Kills  | Steps  | Accuracy |
|------|-------|--------|--------|--------|--------|----------|
| 1    | 8     | 282    | 137    | 15.3   | 1161   | 44.9     |
| 2    | 3     | 212    | 5      | 11.3   | 885    | 43.7     |
| 3    | 5     | 207    | 65     | 15.7   | 1216   | 48.1     |
| 4    | 6     | 203    | 39     | 10.7   | 758    | 47.6     |
| 5    | 4     | 161    | 10     | 7.3    | 649    | 34.8     |
| 6    | 1     | 152    | -19    | 5.7    | 624    | 41.0     |
| 7    | 7     | 144    | 15     | 8.7    | 697    | 42.9     |
| 8    | 2     | 107    | 14     | 12.0   | 1021   | 27.4     |

</details>

### Top Generations Takeaways

- Top generation is Gen 8 with best fitness 281.5.

### Top Generations Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Accuracy:** Hits divided by shots fired (0 to 1).


## Trend Analysis

Not enough data for trend analysis.


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

     282 |       *
     262 |        
     242 |        
     222 |        
     201 |  * **  
     181 |        
     161 |        
     141 |*  *  * 
     121 |       o
     101 | *      
      81 |        
      61 |    o   
      41 |        
      21 |     o  
       1 | ooo  o 
     -19 |o       
         --------
         Gen 1Gen 8
```

### Takeaways

- Best fitness trend: breakout improvement (high confidence).
- Average fitness trend: breakout improvement (low confidence (noisy)).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.


---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 0.00s
- **Evaluation (Simulation):** 21.21s (0.0%)
- **Evolution (Operators):** 0.0000s (0.0%)

| Phase | Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
|-------|-----------|---------------|---------------|------------|
| Phase 1 (0-25%) | 1-2 | 19.40s | 0.0000s | 0.00s |
| Phase 2 (25-50%) | 3-4 | 17.46s | 0.0000s | 0.00s |
| Phase 3 (50-75%) | 5-6 | 22.85s | 0.0000s | 0.00s |
| Phase 4 (75-100%) | 7-8 | 25.14s | 0.0000s | 0.00s |

### Takeaways

- Evaluation accounts for 0.0% of generation time.
- Evolution accounts for 0.0% of generation time.

### Glossary

- **Evaluation duration:** Wall time spent evaluating a generation.
- **Evolution duration:** Wall time spent evolving a generation.
- **Total generation duration:** Combined evaluation and evolution wall time.

## ES Optimizer Diagnostics

**Recent Averages (Last 10 Generations):**
- **Sigma:** 0.13093
- **Cov diag mean:** 0.87392
- **Cov diag std:** 0.000571
- **Cov diag mean abs dev:** 0.000902
- **Cov diag max abs dev:** 0.003348
- **Cov lr scale:** 8750.00
- **Cov lr effective rate:** 0.000680

### Optimizer Takeaways

- CMA-ES step-size and diagonal covariance movement are tracked across recent generations.

### Optimizer Glossary

- **Sigma:** CMA-ES global step size controlling exploration radius.
- **Cov diag mean:** Mean diagonal covariance value (per-parameter variance).
- **Cov diag std:** Standard deviation of diagonal covariance values.
- **Cov diag mean abs dev:** Mean absolute deviation of diagonal covariance from 1.0.
- **Cov diag max abs dev:** Largest absolute deviation of diagonal covariance from 1.0.
- **Cov lr scale:** Scaling factor applied to CMA-ES covariance learning rates (c1/cmu).
- **Cov lr effective rate:** Effective c1 + cmu rate used for diagonal covariance update.

