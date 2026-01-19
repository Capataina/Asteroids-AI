# Training Summary Report

**Generated:** 2026-01-15 18:19:23
**Schema Version:** 2.1

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
Best Fitness     -60 -> -32  [# =-=+=@-+=-+=%+]  great improvement (low confidence (noisy))
Avg Fitness      -152 -> -113  [. ..-=+@+#**+*%*]  breakout improvement (high confidence)
Min Fitness      -217 -> -181  [=:= -=#@**#%=+%*]  breakout improvement (moderate confidence)
Fitness Spread   39 -> 39  [# +*@*:*.:- =-*+]  volatile (low confidence (noisy))
Avg Kills        3.6 -> 6.5  [ .:-=+#%#%###%@#]  breakout improvement (high confidence)
Avg Accuracy     30% -> 34%  [.:: -=#%%@#%##%%]  stagnation (low confidence)
Avg Steps        547 -> 713  [.. .=**@#%##*###]  breakout improvement (moderate confidence)
Action Entropy   1.55 -> 0.65  [#*@*#*-=:::.    ]  slight regression (moderate confidence)
Output Saturation 39% -> 72%  [ : :::++***%%%%@]  regression (low confidence)
Frontness Avg    51% -> 50%  [@ **%=:-.:.::-.:]  stagnation (low confidence)
Danger Exposure  14% -> 16%  [::. -=#@+%#+=**=]  stagnation (low confidence)
Seed Fitness Std 111.7 -> 164.8  [   -=+#%**#**#@#]  sharp regression (high confidence)
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
- **Seed fitness std:** Average per-agent fitness std dev across seeds (evaluation noise proxy).

## Report Takeaways (All Sections)

- Quick Trend Overview: sparklines summarize phase-based metric direction and confidence.
- Training Configuration: report includes a full hyperparameter snapshot for reproducibility.
- Overall Summary: best fitness 4.81 at Gen 8.
- Best Agent Deep Profile: Gen 8 with 10.2 kills.
- Heatmaps: spatial patterns available for best agent and population.
- Generation Highlights: top improvements/regressions and record runs flagged.
- Milestone Timeline: milestones are run-relative (percent-of-peak thresholds).
- Training Progress by Phase: 4 equal phases used for normalized comparisons.
- Distribution Analysis: fitness spread trend is volatile.
- Kill Efficiency: phase-level kill rates and shot efficiency tracked.
- Learning Velocity: phase-based fitness deltas and acceleration reported.
- Reward Component Evolution: per-component shifts tracked across 4 phases.
- Reward Balance Analysis: dominance, entropy, and penalty skew checked.
- Population Health Dashboard: diversity, elite gap, and floor trends summarized.
- Stagnation Analysis: plateau lengths compared to run history.
- Generalization Analysis: no fresh-game data recorded.
- Correlation Analysis: fitness vs kills/survival/accuracy correlations reported.
- Survival Distribution: phase-level survival averages and max survival summarized.
- Behavioral Summary: recent kills, steps, and accuracy summarized.
- Learning Progress: phase comparisons for best/avg/min fitness.
- Neural & Behavioral Complexity: saturation and entropy trends reported.
- Risk Profile Analysis: proximity trends and archetypes reported.
- Control Diagnostics: turn bias, frontness, danger, and movement diagnostics reported.
- Convergence Analysis: recent diversity and range trends summarized.
- Behavioral Trends: action mix and intra-episode scoring patterns reported.
- Recent Generations: last 16 gens tabulated.
- Top Generations: best run is Gen 8.
- Trend Analysis: phase-based fitness trend table provided.
- ASCII Chart: best vs avg fitness progression visualized.
- Technical Appendix: runtime costs and operator stats reported when available.

## Training Configuration

```
population_size: 15
num_generations: 500
mutation_probability: 0.05
max_workers: 16
```

### Config Takeaways

- Configuration snapshot captures the exact training parameters for reproducibility.

### Config Glossary

- **Config value:** Literal hyperparameter or run setting recorded at training start.

## Overall Summary

- **Total Generations:** 16
- **Training Duration:** 0:17:43.640689
- **All-Time Best Fitness:** 4.81
- **Best Generation:** 8
- **Final Best Fitness:** -34.89
- **Final Average Fitness:** -113.03
- **Avg Improvement (Phase 1->Phase 4):** 39.79
- **Stagnation:** 8 generations since improvement

### Takeaways

- Best fitness achieved: 4.81 (Gen 8).
- Final avg fitness: -113.03.
- Current stagnation: 8 generations without improvement.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Avg improvement (Phase 1->Phase 4):** Difference between average fitness in the first and last 25% of training.

## Best Agent Deep Profile

The most fit agent appeared in **Generation 8** with a fitness of **4.81**.

### Combat Efficiency

- **Total Kills:** 10.2
- **Survival Time:** 16.4 seconds (983.5 steps)
- **Accuracy:** 37.1%
- **Shots per Kill:** 2.6
- **Time per Kill:** 1.61 seconds

### Behavioral Signature

**Classification:** `Sniper`

| Action | Rate (per step) | Description |
|--------|-----------------|-------------|
| **Thrust** | 0.3% | Movement frequency |
| **Turn** | 75.7% | Rotation frequency |
| **Shoot** | 87.6% | Trigger discipline |

### Takeaways

- Best agent achieved 10.2 kills with 37.1% accuracy.
- Behavioral classification: Sniper.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Average steps:** Mean steps survived per episode across the population.
- **Shots per kill:** Shots fired divided by kills (lower is more efficient).

### Spatial Analytics (Best Agent - Generations 7-16)

**Position Heatmap (Where does it fly?)**
```
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                       ..                                                               |
|                                                             .                                                          |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                     -.:                                                                |
|                                                        .     : .                                                       |
|                                                          :. ::.                                                        |
|                                                  ..  .:::--@=::.                                                       |
|                                                         -==-:.::..                                                     |
|                                                        : ..::. ::.:   .-        .                                      |
|                                                       :     .:.                                                        |
|                                                             .  : .:.                                                   |
|                                                              .:                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                   .                                                    |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
```

**Kill Zone Heatmap (Where does it kill?)**
```
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                       :.                                                               |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                     - :                                                                |
|                                                              : .                                                       |
|                                     .                    :  ::.                                                        |
|                                                  ...:.:::--@+-:                                                        |
|                                                       . ==+:..::                                                       |
|                                                        ::  -:..::::    -                                               |
|                                                       :  .  .:.                                                        |
|                                                             :  :  :.                                                   |
|                                                               .                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                  .                                                     |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
```

### Spatial Analytics (Population Average - Generations 7-16)

**Position Heatmap (Where do they fly?)**
```
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                       .                                                                |
|                                                                                                                        |
|                                                                                                                        |
|                                                           .                                                            |
|                                                                                                                        |
|                                   .         :.                                                                         |
|                                               .         :  .. .  .... .            .                                   |
|                         .                          .  : .. :.  . .  ..                                                 |
|                                                   . :..:..... .. .......:.... . .                                      |
|                                                   .:.:.:::::-:::.:..:.....                                             |
|                               .              .  ..:::..::------:-::.::..:.    .                                        |
|                                             .    .:.::--==+@+==-:-::.......   ..                                       |
|                                           . .  :....::-==+++=---:.....     .                                           |
|                                  .          .  .:::::::-------:::.::. .: .      .                                      |
|                           .                 . .::.:...:..:.-::..:. .                                                   |
|                           ...           ...    ..:.. .: .:  ::.: .:.    .                                              |
|                                        .        ...:.  ..  . .:.   ..     .                                            |
|                                                 . ..             ...     .                                             |
|                                                  .                                                                     |
|                                                                                                                        |
|                                                                                                                        |
|                                  ....                                                                                  |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
```

**Kill Zone Heatmap (Where do they kill?)**
```
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                       ..                                                               |
|                                                                                                                        |
|                                                                            .                                           |
|                                                           .     .                                                      |
|                                                                        .           .                                   |
|                                   . .       ..                                                                         |
|                        .                      ..  .  .  :  .. .  :..: .            .                                   |
|                         .                             : .. :.  . .  ... .      . .                                     |
|                         .                           : .:.. ..    .... ..:.... . ..                                     |
|                                                   .:..::::.:-:::.:..:: ...  .                                          |
|                               .     .      ...  ....:..::------:-::..:  ....  . .                                      |
|                               .            .   . :::::--=++@+==-:-.:... :...  ..             .                         |
|                                           .  . :....-:-==+++=---:.....     .   .         .                             |
|                                             ....:.:::::----=--:-:::: . : .     .  ..                                   |
|                             .     .    ...   . .. -.:.: .: -.:..: ..                                                   |
|                           ...  .  .     . . .. ...  .....:  ...:  ...  ..                ..                            |
|                                   .   .         ...:.....  .  :.   ..  .                                               |
|                                                   ..          .  ...   . .                                             |
|                                 .             ...               .        .                                             |
|                                                                  .                                                     |
|                                                                                                                        |
|                                  .            .                                                                        |
|                                                                            .                                           |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                               .                                                        |
```

### Heatmap Takeaways

- Heatmaps aggregate spatial samples over the last 10 generations.
- Best-agent and population heatmaps highlight spatial biases and kill zones.

### Heatmap Glossary

- **Position heatmap:** Density of sampled player positions during evaluation.
- **Kill heatmap:** Density of player positions at kill events (proxy for engagement zones).

## Generation Highlights

### Best Improvement

**Generation 3**: Best fitness jumped +63.2 (+57.3%)
- New best fitness: -47.1

### Worst Regression

**Generation 2**: Best fitness dropped -94.0 (--573.7%)
- New best fitness: -110.4
- Note: this can be normal variation after a lucky outlier

### Most Accurate Generation

**Generation 10**: Population accuracy reached 34.2%

### Most Kills (Single Agent)

**Generation 15**: An agent achieved 10 kills

### Most Diverse Generation

**Generation 8**: Diversity index 0.45

### Most Converged Generation

**Generation 2**: Diversity index 0.18

### Takeaways

- Best improvement at Gen 3 (+63.2).
- Worst regression at Gen 2 (-94.0).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Max kills:** Highest kills achieved by any agent in the generation.
- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).

## Milestone Timeline

| Generation | Category | Value | Description |
|------------|----------|-------|-------------|
| 1 | Kills | 8 | Max kills reached 25% of run peak |
| 1 | Kills | 8 | Max kills reached 50% of run peak |
| 1 | Kills | 8 | Max kills reached 75% of run peak |
| 8 | Fitness | 5 | Best fitness reached 25% of run peak |
| 8 | Fitness | 5 | Best fitness reached 50% of run peak |
| 8 | Fitness | 5 | Best fitness reached 75% of run peak |
| 8 | Fitness | 5 | Best fitness reached 90% of run peak |
| 8 | Fitness | 5 | Best fitness reached 95% of run peak |
| 8 | Fitness | 5 | Best fitness reached 98% of run peak |
| 8 | Kills | 10 | Max kills reached 90% of run peak |

### Takeaways

- Total milestones reached: 10.
- Latest milestone at Gen 8 (Kills).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Max kills:** Highest kills achieved by any agent in the generation.

## Training Progress by Phase

| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|------|----------|---------|-----------|---------|-----------|----------|
| Phase 1 (0-25%) | 1-4 | -16 | -152 | 3.6 | 30% | 547 | 39 |
| Phase 2 (25-50%) | 5-8 | 5 | -121 | 5.9 | 32% | 695 | 42 |
| Phase 3 (50-75%) | 9-12 | -45 | -115 | 6.4 | 34% | 720 | 32 |
| Phase 4 (75-100%) | 13-16 | 1 | -113 | 6.5 | 34% | 713 | 39 |

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

### Metric Distributions (Last 10 Generations)

Visualizing population consistency: `|---O---|` represents Mean +/- 1 StdDev.
- **Narrow bar**: Consistent population (convergence)
- **Wide bar**: Diverse or noisy population

**Accuracy Distribution**
```
Gen   7: |-----------------------O-----------------------|   33.3% +/-  3.4%
Gen   8:            |-----------------O----------------|     34.0% +/-  2.4%
Gen   9:             |--------------O---------------|        33.9% +/-  2.1%
Gen  10:               |---------------O---------------|     34.2% +/-  2.3%
Gen  11:         |--------------O--------------|             33.2% +/-  2.1%
Gen  12:          |-------------------O-------------------|  34.2% +/-  2.8%
Gen  13:            |------------O------------|              33.5% +/-  1.8%
Gen  14:        |----------------O---------------|           33.4% +/-  2.3%
Gen  15:              |---------------O----------------|     34.1% +/-  2.3%
Gen  16:             |--------------O-------------|          33.8% +/-  2.0%
```

**Survival Steps Distribution**
```
Gen   7:                                 |---O----|          698.1 +/-  85.3
Gen   8:                                   |----O-----|      758.0 +/- 106.4
Gen   9:                                   |--O---|          715.0 +/-  68.3
Gen  10:                                  |----O----|        733.4 +/-  89.1
Gen  11:                                 |----O----|         715.8 +/-  93.9
Gen  12:                                  |---O---|          714.3 +/-  74.5
Gen  13:                                |----O----|          692.5 +/-  98.5
Gen  14:                                  |---O---|          708.9 +/-  74.3
Gen  15:                                  |----O---|         729.9 +/-  87.2
Gen  16:                                  |---O----|         718.9 +/-  80.8
```

**Kills Distribution**
```
Gen   7:                            |-----O----|               6.2 +/-   1.0
Gen   8:                              |-------O-------|        6.9 +/-   1.5
Gen   9:                             |----O-----|              6.2 +/-   1.0
Gen  10:                              |-----O-----|            6.6 +/-   1.1
Gen  11:                             |-----O-----|             6.4 +/-   1.1
Gen  12:                              |----O----|              6.5 +/-   0.9
Gen  13:                            |-----O------|             6.3 +/-   1.2
Gen  14:                             |-----O------|            6.5 +/-   1.2
Gen  15:                              |-------O-------|        7.0 +/-   1.5
Gen  16:                            |------O------|            6.5 +/-   1.3
```

**Fitness Distribution**
```
Gen   7:   |----------------O---------------|               -120.0 +/-  33.3
Gen   8:         |---------------------O------------------|  -96.7 +/-  43.6
Gen   9:    |--------------O---------------|                -120.2 +/-  30.5
Gen  10:       |----------------O----------------|          -111.0 +/-  33.1
Gen  11:     |-----------------O------------------|         -112.4 +/-  36.2
Gen  12:        |------------O-------------|                -116.2 +/-  27.2
Gen  13: |-----------------O------------------|             -120.6 +/-  37.4
Gen  14:    |-----------------O-----------------|           -115.8 +/-  35.8
Gen  15:        |--------------------O--------------------| -100.9 +/-  42.2
Gen  16:   |-------------------O-------------------|        -113.0 +/-  40.1
```

**Aim Frontness Distribution**
```
Gen   7:               |------------O------------|           49.7% +/-  0.9%
Gen   8:              |----------------O----------------|    49.9% +/-  1.1%
Gen   9: |------------------O------------------|             49.1% +/-  1.3%
Gen  10:                 |----------O----------|             49.7% +/-  0.7%
Gen  11:     |---------------O--------------|                49.2% +/-  1.0%
Gen  12:          |---------------O---------------|          49.5% +/-  1.1%
Gen  13:     |------------------O-------------------|        49.4% +/-  1.3%
Gen  14:           |-------------------O------------------|  49.8% +/-  1.3%
Gen  15:      |-------------O------------|                   49.1% +/-  0.9%
Gen  16:               |------------O-------------|          49.7% +/-  0.9%
```

**Danger Exposure Distribution**
```
Gen   7:    |----------------------O----------------------|  16.4% +/-  2.1%
Gen   8:              |-----------------O-----------------|  16.9% +/-  1.7%
Gen   9: |-----------------O-----------------|               15.7% +/-  1.6%
Gen  10:           |------------------O-----------------|    16.7% +/-  1.7%
Gen  11:      |-------------------O-------------------|      16.3% +/-  1.9%
Gen  12:    |----------------O-----------------|             15.9% +/-  1.6%
Gen  13: |---------------O---------------|                   15.6% +/-  1.5%
Gen  14:   |-------------------O-------------------|         16.1% +/-  1.8%
Gen  15:     |------------------O-------------------|        16.2% +/-  1.8%
Gen  16: |--------------O---------------|                    15.5% +/-  1.5%
```

**Turn Deadzone Distribution**
```
Gen   7:                   |-------------O--------------|    20.1% +/-  5.9%
Gen   8:                        |------------O------------|  21.7% +/-  5.5%
Gen   9:           |--------------O---------------|          17.3% +/-  6.6%
Gen  10:       |----------------O----------------|           16.2% +/-  7.1%
Gen  11:               |----------O-----------|              17.3% +/-  4.8%
Gen  12:      |---------O---------|                          13.0% +/-  4.1%
Gen  13: |-------O-------|                                   10.2% +/-  3.2%
Gen  14:      |-----O-----|                                  11.4% +/-  2.5%
Gen  15: |--------------O-------------|                      12.8% +/-  6.1%
Gen  16: |-----O------|                                       9.3% +/-  2.7%
```

**Coverage Ratio Distribution**
```
Gen   7:             |------------------O-----------------|  10.8% +/-  1.2%
Gen   8:                    |------------O-------------|     10.9% +/-  0.9%
Gen   9:         |--------------O---------------|            10.3% +/-  1.0%
Gen  10:                    |------------O------------|      10.9% +/-  0.9%
Gen  11:           |------------------O------------------|   10.7% +/-  1.3%
Gen  12:            |-----------O----------|                 10.2% +/-  0.8%
Gen  13:       |----------------O----------------|           10.2% +/-  1.1%
Gen  14: |----------------O----------------|                  9.8% +/-  1.1%
Gen  15:                     |------O-----|                  10.5% +/-  0.4%
Gen  16:       |-----------O----------|                       9.9% +/-  0.8%
```

**Seed Fitness Std Distribution**
```
Gen   7:                            |-----O------|           159.4 +/-  32.5
Gen   8:                                |-----O-----|        175.0 +/-  29.6
Gen   9:                          |-------O-------|          155.2 +/-  37.4
Gen  10:                           |-----O------|            154.7 +/-  30.7
Gen  11:                             |------O------|         166.5 +/-  33.1
Gen  12:                          |------O------|            152.0 +/-  33.7
Gen  13:                           |------O------|           158.8 +/-  33.1
Gen  14:                            |------O-----|           159.7 +/-  29.0
Gen  15:                              |-------O-------|      175.0 +/-  38.1
Gen  16:                            |-------O------|         165.6 +/-  36.0
```

### Takeaways

- Fitness spread trend: volatile (low confidence (noisy)).
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
- **Turn deadzone rate:** Fraction of frames where signed turn input is within the deadzone.
- **Deadzone std dev:** Standard deviation of turn deadzone rate across the population.
- **Coverage ratio:** Fraction of spatial grid cells visited (0 to 1).
- **Coverage std dev:** Standard deviation of coverage ratio across the population.

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 0.92 (Phase 1: 0.65)
- **Shots per Kill:** 6.74 (Phase 1: 7.66)
- **Kill Conversion Rate:** 14.8% (Phase 1: 13.1%)
- **Average Kills per Episode:** 6.5

### Efficiency Trend (Phase Averages)

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 (0-25%) | 0.65 | 7.66 | 13.1% |
| Phase 2 (25-50%) | 0.84 | 6.90 | 14.5% |
| Phase 3 (50-75%) | 0.89 | 6.84 | 14.6% |
| Phase 4 (75-100%) | 0.92 | 6.74 | 14.8% |

### Takeaways

- Kill rate changed from 0.65 to 0.92 kills/100 steps.
- Shots per kill moved from 7.66 to 6.74.

### Glossary

- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Average shots:** Mean shots fired per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Shots per kill:** Shots fired divided by kills (lower is more efficient).

## Learning Velocity

### Velocity by Phase

| Phase | Fitness Delta | Delta/Gen | Velocity Band |
|-------|---------------|-----------|---------------|
| Phase 1 (0-25%) | -51 | -12.7 | Slow |
| Phase 2 (25-50%) | +60 | +15.0 | Fast |
| Phase 3 (50-75%) | -6 | -1.4 | Slow |
| Phase 4 (75-100%) | +6 | +1.6 | Fast |

### Current Velocity

- **Recent Improvement Rate:** +1.6 fitness/generation
- **Acceleration:** -1.1 (positive = speeding up)

### Takeaways

- Velocity mean +0.6 with std 9.9 across phases.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).

## Reward Component Evolution

| Component | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Trend | Status |
|-----------|---------|---------|---------|---------|-------|--------|
| DeathPenalty | -240.1 | -216.9 | -216.4 | -216.0 | ~ +10% | Improving penalty |
| DistanceBasedKillReward | +64.5 | +105.4 | +115.7 | +117.9 | ++ +83% | Learned |
| ConservingAmmoBonus | -17.0 | -20.6 | -21.1 | -21.0 | - -23% | Worsening penalty |
| ExplorationBonus | +21.7 | +8.6 | +6.3 | +6.1 | -- -72% | Neutral |
| VelocitySurvivalBonus | +18.6 | +3.0 | +0.5 | +0.5 | -- -98% | Neutral |

**Exploration Efficiency (Final Phase):** 0.0083 score/step
- *A higher rate indicates faster map traversal, independent of survival time.*

### Takeaways

- DistanceBasedKillReward shifted up by +83% from Phase 1 to Phase 4.
- ExplorationBonus shifted down by -72% from Phase 1 to Phase 4.
- VelocitySurvivalBonus shifted down by -98% from Phase 1 to Phase 4.

### Warnings

- ConservingAmmoBonus penalty deepened (more negative over time).

### Glossary

- **Reward breakdown:** Per-component average reward contribution per episode.

## Reward Balance Analysis

### Balance Metrics (Latest Generation)

- Reward dominance index (HHI): 0.90
- Reward entropy (normalized): 0.20
- Max component share: 94.8%
- Positive component count: 3

### Takeaways

- Reward mix is broadly stable with no major dominance spikes.

### Warnings

- Max component share is high (94.8%).
- VelocitySurvivalBonus is volatile across the run (high variance vs mean).
- ConservingAmmoBonus remains negative on average (behavior may be over-penalized).
- DeathPenalty remains negative on average (behavior may be over-penalized).
- Penalty ratio is high (1.92), negative rewards dominate.

### Glossary

- **Reward breakdown:** Per-component average reward contribution per episode.
- **Reward dominance index:** HHI-style dominance of positive rewards (higher = more concentrated).
- **Reward entropy:** Normalized entropy of positive reward components (balance proxy).
- **Reward max share:** Share of total positive reward from the largest component.
- **Positive component count:** Number of reward components with positive contribution.

## Population Health Dashboard

### Current Status: Healthy

| Metric | Value | Trend (Recent) |
|--------|-------|----------------|
| Diversity Index | 0.35 | Decreasing |
| Elite Gap | 0.71 | Stable |
| Min Fitness Trend | +36.1 | Up |
| Max Fitness Trend | +28.1 | Up |
| IQR (p75-p25) | 55 | Widening |

### Takeaways

- Health status is Healthy.
- Diversity index at 0.35 with decreasing spread.
- Fitness floor trend +36.1, ceiling trend +28.1.

### Glossary

- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Average fitness:** Mean fitness across the population for a generation.
- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Fitness p25:** 25th percentile of population fitness.
- **Fitness p75:** 75th percentile of population fitness.

## Stagnation Analysis

- **Current Stagnation:** 8 generations
- **Average Stagnation Period:** 7.0 generations
- **Longest Stagnation:** 8 generations
- **Number of Stagnation Periods:** 2

### Takeaways

- Stagnation periods average 7.0 generations.
- Longest plateau reached 8 generations.

### Warnings

- Current stagnation is in the top 10% of historical plateaus.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).

## Correlation Analysis

### Fitness Correlations

| Metric | Correlation | Strength |
|--------|-------------|----------|
| Kills | +0.93 | Strong |
| Steps Survived | +0.91 | Strong |
| Accuracy | +0.87 | Strong |

### Interpretation

Fitness is most strongly predicted by kills (r=0.93).

### Takeaways

- Strongest fitness driver: kills (r=0.93).

### Glossary

- **Average fitness:** Mean fitness across the population for a generation.
- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 713 steps (47.5% of max)
- **Max Survival:** 897 steps

### Survival Progression (Phase Averages)

| Phase | Mean Steps | Change vs Prior |
|-------|------------|-----------------|
| Phase 1 (0-25%) | 547 |  |
| Phase 2 (25-50%) | 695 | +148 |
| Phase 3 (50-75%) | 720 | +25 |
| Phase 4 (75-100%) | 713 | -7 |

### Takeaways

- Final-phase survival averages 713 steps.
- Best survival reached 897 steps.

### Warnings

- Average survival remains below half of max steps; survivability is still limited.

### Glossary

- **Average steps:** Mean steps survived per episode across the population.
- **Max steps:** Highest steps survived by any agent in the generation.

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 6.50
- **Avg Steps Survived:** 718
- **Avg Accuracy:** 33.8%
- **Max Kills (Any Agent Ever):** 10.4
- **Max Steps (Any Agent Ever):** 983.5

### Takeaways

- Recent average kills: 6.50.
- Recent average accuracy: 33.8%.

### Glossary

- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).

## Learning Progress

| Phase | Gens | Avg Best | Avg Mean | Avg Min |
|-------|------|----------|----------|---------|
| Phase 1 (0-25%) | 1-4 | -60.3 | -152.4 | -216.9 |
| Phase 2 (25-50%) | 5-8 | -34.8 | -120.6 | -184.8 |
| Phase 3 (50-75%) | 9-12 | -56.7 | -115.0 | -174.7 |
| Phase 4 (75-100%) | 13-16 | -32.2 | -112.6 | -180.8 |

### Takeaways

- Best fitness trend: great improvement (low confidence (noisy)).
- Average fitness trend: breakout improvement (high confidence).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.

## Neural & Behavioral Complexity

| Gen | Saturation | Entropy | Control Style |
|-----|------------|---------|---------------|
| 1 |  33.5% |  1.55 | Analog-leaning / Exploratory |
| 2 |  42.5% |  1.44 | Analog-leaning / Exploratory |
| 3 |  35.8% |  1.73 | Analog-leaning / Exploratory |
| 4 |  43.2% |  1.47 | Analog-leaning / Exploratory |
| 5 |  43.9% |  1.52 | Analog-leaning / Exploratory |
| 6 |  45.9% |  1.38 | Balanced |
| 7 |  57.6% |  1.05 | Balanced |
| 8 |  58.2% |  1.11 | Balanced |
| 9 |  61.7% |  0.96 | Balanced |
| 10 |  62.1% |  0.94 | Balanced |
| 11 |  61.5% |  0.96 | Balanced |
| 12 |  68.7% |  0.77 | Binary-leaning / Repetitive |
| 13 |  72.3% |  0.64 | Binary-leaning / Repetitive |
| 14 |  71.3% |  0.68 | Binary-leaning / Repetitive |
| 15 |  70.4% |  0.70 | Binary-leaning / Repetitive |
| 16 |  72.7% |  0.59 | Binary-leaning / Repetitive |

### Takeaways

- Output saturation trend: regression (low confidence).
- Action entropy trend: slight regression (moderate confidence).

### Warnings

- High saturation with low entropy suggests rigid, repetitive control.

### Glossary

- **Output saturation:** Share of NN outputs near 0 or 1 (binary control tendency).
- **Action entropy:** Entropy of action combinations (higher = more varied control).

## Risk Profile Analysis

Analysis of how close agents let asteroids get before reacting or killing them.

| Gen | Avg Min Dist | Fitness | Kills | Archetype |
|-----|--------------|---------|-------|-----------|
| 1 |   16.3px | -150.5 |  2.7 | Cautious Underperformer |
| 2 |   15.5px | -161.8 |  3.4 | Overexposed |
| 3 |   15.7px | -149.4 |  3.7 | Balanced |
| 4 |   15.1px | -147.8 |  4.5 | Overexposed |
| 5 |   16.5px | -137.2 |  4.8 | Cautious Underperformer |
| 6 |   15.8px | -128.5 |  5.5 | Balanced |
| 7 |   15.7px | -120.0 |  6.2 | Balanced |
| 8 |   16.1px |  -96.7 |  6.9 | Sniper |
| 9 |   15.5px | -120.2 |  6.2 | Balanced |
| 10 |   15.9px | -111.0 |  6.6 | Balanced |
| 11 |   15.5px | -112.4 |  6.4 | Daredevil |
| 12 |   15.6px | -116.2 |  6.5 | Balanced |
| 13 |   16.0px | -120.6 |  6.3 | Balanced |
| 14 |   15.4px | -115.8 |  6.5 | Balanced |
| 15 |   15.9px | -100.9 |  7.0 | Balanced |
| 16 |   16.2px | -113.0 |  6.5 | Sniper |

### Takeaways

- Min-distance trend: volatile (low confidence (noisy)).
- Danger exposure trend: stagnation (low confidence).

### Glossary

- **Min asteroid distance:** Closest distance to an asteroid during an episode (pixels).
- **Average asteroid distance:** Mean distance to nearest asteroid over time (pixels).
- **Danger exposure rate:** Fraction of frames with a nearby asteroid inside danger radius.

## Control Diagnostics

### Control Snapshot (Latest Generation)

| Category | Metric | Value |
|----------|--------|-------|
| Turn | Deadzone Rate | 9.3% |
| Turn | Turn Balance (R-L) | +1.00 |
| Turn | Switch Rate | 0.1% |
| Turn | Avg Streak | 71.6f |
| Turn | Max Streak | 239f |
| Aim | Frontness Avg | 49.7% |
| Aim | Frontness at Shot | 49.8% |
| Aim | Frontness at Hit | 53.4% |
| Aim | Shot Distance | 171.8px |
| Aim | Hit Distance | 130.1px |
| Danger | Exposure Rate | 15.5% |
| Danger | Entries | 3.0 |
| Danger | Reaction Time | 1.1f |
| Danger | Wraps in Danger | 0.0 |
| Movement | Distance Traveled | 18.5px |
| Movement | Avg Speed | 0.02 |
| Movement | Speed Std | 0.03 |
| Movement | Coverage Ratio | 9.9% |
| Shooting | Shots per Kill | 7.04 |
| Shooting | Shots per Hit | 2.64 |
| Shooting | Cooldown Usage | 64.0% |
| Shooting | Cooldown Ready | 1.5% |
| Stability | Fitness Std (Seeds) | 165.6 |

### Recent Control Trends (Last 10)

| Gen | Deadzone | Turn Bias | Switch | Frontness | Danger | Coverage |
|-----|----------|-----------|--------|-----------|--------|----------|
| 7 |   20.1% |  +0.99 |    0.4% |   49.7% |   16.4% |   10.8% |
| 8 |   21.7% |  +0.99 |    0.4% |   49.9% |   16.9% |   10.9% |
| 9 |   17.3% |  +0.99 |    0.3% |   49.1% |   15.7% |   10.3% |
| 10 |   16.2% |  +0.99 |    0.2% |   49.7% |   16.7% |   10.9% |
| 11 |   17.3% |  +0.99 |    0.3% |   49.2% |   16.3% |   10.7% |
| 12 |   13.0% |  +1.00 |    0.2% |   49.5% |   15.9% |   10.2% |
| 13 |   10.2% |  +1.00 |    0.1% |   49.4% |   15.6% |   10.2% |
| 14 |   11.4% |  +1.00 |    0.2% |   49.8% |   16.1% |    9.8% |
| 15 |   12.8% |  +1.00 |    0.2% |   49.1% |   16.2% |   10.5% |
| 16 |    9.3% |  +1.00 |    0.1% |   49.7% |   15.5% |    9.9% |

### Takeaways

- Turn balance trend: sharp regression (moderate confidence).
- Aim alignment trend: stagnation (low confidence).
- Danger exposure trend: stagnation (low confidence).

### Warnings

- Turn bias is high vs run baseline (one-direction dominance).

### Glossary

- **Turn deadzone rate:** Fraction of frames where signed turn input is within the deadzone.
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

- Average Standard Deviation: 37.93
- Average Range (Best-Min): 143.31
- Diversity Change: -0.5%
- **Status:** Population has balanced diversity

### Takeaways

- Convergence status: balanced.
- Diversity change: -0.5%.

### Glossary

- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Minimum fitness:** Lowest fitness in the population for a generation.

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Safe Dist | Max Kills |
|--------|-----------|-----------|--------------|-----------|----------|
| Q1 | 3.58 | 547 | 29.7% | 173.7px | 8.35 |
| Q2 | 5.85 | 695 | 32.4% | 167.2px | 10.2 |
| Q3 | 6.43 | 720 | 33.9% | 162.1px | 8.9 |
| Q4 | 6.55 | 713 | 33.7% | 164.8px | 10.4 |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
|--------|----------|--------|---------|-------------------|
| Q1 | 26.5% | 61.2% | 64.4% | **Skirmisher** |
| Q2 | 2.0% | 70.6% | 82.5% | **Sniper** |
| Q3 | 0.3% | 81.7% | 90.1% | **Sniper** |
| Q4 | 0.2% | 86.8% | 94.4% | **Sniper** |

### Input Control Style

| Period | Thrust Dur | Turn Dur | Shoot Dur | Idle Rate | Wraps |
|--------|------------|----------|-----------|-----------|-------|
| Q1 | 18.6f | 57.7f | 83.1f | 12.1% | 0.8 |
| Q2 | 3.4f | 26.8f | 35.2f | 9.8% | 0.1 |
| Q3 | 0.8f | 46.4f | 51.3f | 5.1% | 0.0 |
| Q4 | 0.7f | 66.3f | 89.4f | 2.7% | 0.0 |

### Takeaways

- Kills trend: breakout improvement.
- Accuracy trend: stagnation.
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
| Start (0-25%) | 5.2 | -4.6% | Balanced |
| Mid-Game (25-50%) | 21.6 | -19.1% | Balanced |
| Late-Game (50-75%) | 33.5 | -29.6% | Balanced |
| End-Game (75-100%) | -173.3 | 153.3% | Back-loaded |

### Intra-Episode Takeaways

- Highest scoring quarter: Late-Game (50-75%) (-29.6% of episode reward).

### Intra-Episode Glossary

- **Quarterly scores:** Average reward earned in each episode quarter (0-25%, 25-50%, 50-75%, 75-100%).

## Recent Generations (Last 30)

<details>
<summary>Click to expand Recent Generations table</summary>

| Gen   | Best   | Avg    | StdDev | Kills  | Steps  | Acc%   | Stag   |
|-------|--------|--------|--------|--------|--------|--------|--------|
| 1     | -16    | -151   | 46     | 2.7    | 549    | 30     | 0      |
| 2     | -110   | -162   | 28     | 3.4    | 566    | 30     | 1      |
| 3     | -47    | -149   | 39     | 3.7    | 515    | 30     | 2      |
| 4     | -67    | -148   | 42     | 4.5    | 559    | 29     | 3      |
| 5     | -55    | -137   | 49     | 4.8    | 637    | 31     | 4      |
| 6     | -42    | -128   | 43     | 5.5    | 686    | 32     | 5      |
| 7     | -47    | -120   | 33     | 6.2    | 698    | 33     | 6      |
| 8     | 5      | -97    | 44     | 6.9    | 758    | 34     | 0      |
| 9     | -60    | -120   | 31     | 6.2    | 715    | 34     | 1      |
| 10    | -45    | -111   | 33     | 6.6    | 733    | 34     | 2      |
| 11    | -55    | -112   | 36     | 6.4    | 716    | 33     | 3      |
| 12    | -66    | -116   | 27     | 6.5    | 714    | 34     | 4      |
| 13    | -41    | -121   | 37     | 6.3    | 692    | 33     | 5      |
| 14    | -54    | -116   | 36     | 6.5    | 709    | 33     | 6      |
| 15    | 1      | -101   | 42     | 7.0    | 730    | 34     | 7      |
| 16    | -35    | -113   | 40     | 6.5    | 719    | 34     | 8      |

</details>

### Recent Table Takeaways

- Recent table covers 16 generations ending at Gen 16.
- Latest best fitness: -34.9.

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
| 1    | 8     | 5      | -97    | 10.2   | 984    | 37.1     |
| 2    | 15    | 1      | -101   | 10.4   | 897    | 39.3     |
| 3    | 1     | -16    | -151   | 8.3    | 885    | 35.3     |
| 4    | 16    | -35    | -113   | 9.0    | 866    | 35.2     |
| 5    | 13    | -41    | -121   | 8.8    | 871    | 34.7     |
| 6    | 6     | -42    | -128   | 8.8    | 978    | 35.0     |
| 7    | 10    | -45    | -111   | 8.9    | 932    | 39.9     |
| 8    | 7     | -47    | -120   | 8.7    | 869    | 39.0     |
| 9    | 3     | -47    | -149   | 8.0    | 880    | 35.8     |
| 10   | 14    | -54    | -116   | 8.7    | 794    | 38.5     |

</details>

### Top Generations Takeaways

- Top generation is Gen 8 with best fitness 4.8.

### Top Generations Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Accuracy:** Hits divided by shots fired (0 to 1).


## Trend Analysis

| Phase | Avg Best | Avg Mean | Avg Min | Improvement |
|-------|----------|----------|---------|-------------|
| Phase 1 (0-25%) | -60.3 | -152.4 | -216.9 |  |
| Phase 2 (25-50%) | -34.8 | -120.6 | -184.8 | +25.4 |
| Phase 3 (50-75%) | -56.7 | -115.0 | -174.7 | -21.9 |
| Phase 4 (75-100%) | -32.2 | -112.6 | -180.8 | +24.5 |

### Takeaways

- Best fitness: great improvement (low confidence (noisy)).
- Average fitness: breakout improvement (high confidence).
- Minimum fitness: breakout improvement (moderate confidence).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

       5 |       *        
      -6 |              * 
     -17 |*               
     -29 |                
     -40 |               *
     -51 |  *  **  *  *   
     -62 |    *   * *  *  
     -73 |   *       *    
     -84 |                
     -95 |                
    -106 |       o      o 
    -117 | *       ooo o o
    -128 |      o o   o   
    -140 |    oo          
    -151 |o oo            
    -162 | o              
         ----------------
         Gen 1 Gen 16
```

### Takeaways

- Best fitness trend: great improvement (low confidence (noisy)).
- Average fitness trend: breakout improvement (high confidence).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.


---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 0.00s
- **Evaluation (Simulation):** 60.50s (0.0%)
- **Evolution (GA Operators):** 0.0091s (0.0%)

| Phase | Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
|-------|-----------|---------------|---------------|------------|
| Phase 1 (0-25%) | 1-4 | 42.16s | 0.0039s | 0.00s |
| Phase 2 (25-50%) | 5-8 | 57.49s | 0.0065s | 0.00s |
| Phase 3 (50-75%) | 9-12 | 58.57s | 0.0065s | 0.00s |
| Phase 4 (75-100%) | 13-16 | 62.55s | 0.0130s | 0.00s |

### Takeaways

- Evaluation accounts for 0.0% of generation time.
- Evolution accounts for 0.0% of generation time.

### Glossary

- **Evaluation duration:** Wall time spent evaluating a generation.
- **Evolution duration:** Wall time spent evolving a generation.
- **Total generation duration:** Combined evaluation and evolution wall time.

## Genetic Operator Statistics

**Recent Averages (Population: 15)**
- **Crossovers:** 5.6 (37.3%)
- **Mutations:** 15.0 (100.0%)
- **Elites Preserved:** 2.0

### Operator Takeaways

- Recent crossover rate: 37.3%.
- Recent mutation rate: 100.0%.

### Operator Glossary

- **Crossovers:** Number of crossover events per generation.
- **Mutations:** Number of mutation events per generation.
- **Elites:** Individuals preserved without mutation.

