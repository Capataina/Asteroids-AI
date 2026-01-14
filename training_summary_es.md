# Training Summary Report

**Generated:** 2026-01-14 23:24:56
**Schema Version:** 2.0

## Table of Contents

- [Quick Trend Overview](#quick-trend-overview)
- [Training Configuration](#training-configuration)
- [Overall Summary](#overall-summary)
- [Best Agent Deep Profile](#best-agent-deep-profile)
- [Generation Highlights](#generation-highlights)
- [Milestone Timeline](#milestone-timeline)
- [Training Progress by Decile](#training-progress-by-decile)
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
Best Fitness: 56 → 164   [▄▁▁▃▃▂▂▇▄█] +194%
Avg Fitness:  -200 → -180   [▂▃▁▄▃▁▄█▁▆] +10%
Avg Kills:    1.3 → 3.6   [▁▁▂▃▄▃▅█▃▆] +170%
Avg Accuracy: 12% → 24%   [▁▁▁▃▄▃▆▆▃█] +90%
Avg Steps:    428 → 541   [▃▃▁▆▆▃▆▇▁█] +27%
Diversity:    54 → 79   [▂▁▂▃▄▁▃▄▄█] +46%
```

## Training Configuration

```
method: Evolution Strategies
population_size: 100
num_generations: 500
sigma: 0.15
sigma_decay: 0.99
sigma_min: 0.02
adaptive_sigma: True
learning_rate: 0.03
use_antithetic: True
use_rank_transformation: True
weight_decay: 0.0025
seeds_per_agent: 3
use_common_seeds: True
enable_novelty: True
enable_diversity: True
novelty_weight: 0.1
diversity_weight: 0.1
use_adamw: True
adamw_beta1: 0.9
adamw_beta2: 0.999
enable_elitism: True
elite_pull_enabled: True
max_workers: 16
```

## Overall Summary

- **Total Generations:** 11
- **Training Duration:** 0:08:08.171191
- **All-Time Best Fitness:** 165.47
- **Best Generation:** 10
- **Final Best Fitness:** 164.34
- **Final Average Fitness:** -180.02
- **Avg Improvement (Early->Late):** 1.95
- **Stagnation:** 1 generations since improvement

**Generalization (Fresh Game Performance):**
- Avg Generalization Ratio: 5.61
- Best Fresh Fitness: 247.22 (Gen 9)
- Episode Completion Rate: 0.0%

## Best Agent Deep Profile

The most fit agent appeared in **Generation 10** with a fitness of **165.47**.

### Combat Efficiency

- **Total Kills:** 15.333333333333334
- **Survival Time:** 16.1 seconds (967.0 steps)
- **Accuracy:** 41.5%
- **Shots per Kill:** 2.3
- **Time per Kill:** 1.05 seconds

### Behavioral Signature

**Classification:** `Aggressive`

| Action | Rate (per step) | Description |
|--------|-----------------|-------------|
| **Thrust** | 7.4% | Movement frequency |
| **Turn** | 14.5% | Rotation frequency |
| **Shoot** | 82.4% | Trigger discipline |

### Spatial Analytics (Best Agent - Generations 2-11)

**Position Heatmap (Where does it fly?)**
```
|                                                            :      .                                                    |
|                                                .                     .                    .                .           |
|                                                            :                                                           |
|      .                                                     -  =       .                                                |
|                                                          . -  .                  .                                     |
|                              .                             . .             .                .        .                 |
|                                                            -.          :.                                              |
|                                                            -     .    .                    .      .    . .             |
|                                                            -.        .                 .                               |
|                       . .                                  = ..  . . .                       .                 ..      |
|                                          .                 -..          .                                         .   .|
|                                               .            -. .            .       .          .                    .   |
|                                               .    .       =  .   .          .              .                          |
|      .                   .                        .        -                                                     .   . |
|             .      .         .                             @:.       .           .     .  . .                          |
|   .      .                       .        .              . .. .                .                         .             |
|            . .       .                                 .   : .    .               .                                    |
|          .                            .               .    :          .      .       .               .                 |
|   .  .                                        .  .      .  :                            .     .   .  .       .         |
|                                    .           .           .                     .                  .                  |
|        .                          .           .    .       .      . .      .                ...                       .|
|  ..                                   .  .          .             .                    .   .                           |
|         ..    .          .                               . -      .                     .                              |
|                                            .               - .                 .                                       |
|           .        .                                       .     . .              .                         .          |
|                                                            :                   .                                       |
|                                                            -   .                                                       |
|                                                            -            .                                              |
|                                    .                       .                                                           |
|                                                            : . .         .                 .                           |
```

**Kill Zone Heatmap (Where does it kill?)**
```
|                                             :              :      .                                                    |
|                                                            :           .                    .                          |
|                                                            .         .                                                 |
|                                                            :  +                                                        |
|                                                            -  :                .                                       |
|                                                          .                                                             |
|                             .                              -.          :                    .  .      .                |
|                                                            =    .   . .                   ..              .            |
|                 .                              .           =     .           .                  .          .           |
|                      :   .                   ..            + :                                  .                .     |
|                                 .                          :::    .    ..          .           .       .        .     .|
|                                  .                 .       :                       .       .  .                  .. .  |
|                                               .            :      ..                                                   |
|        .      .                                    .       :             .                                        .    |
|                     .. .   . .                   .         @: .            .              .: .                         |
|           :         .             .     .                  :                                .              .           |
|                                                  .         :.                    .                         .           |
|                                       .              .     :                 .                     ..                  |
|   .  .                                     .    .          :        .                  .         .                     |
|    :                                .            .         -                                                           |
|    .   .                                                                                      .            .   .     . |
|       .                                .        .               . :                        :                           |
|                 .      .                                 . :      .                    .                               |
|                                           ..               :.                      .                          .        |
|                                                            -                                                           |
|                        .                                   .                    .                                      |
|                                                            :   .           :                                           |
|                                                            :             .                                             |
|                                                            :    .    :                                                 |
|                                                            .        .                                                  |
```

### Spatial Analytics (Population Average - Generations 2-11)

**Position Heatmap (Where do they fly?)**
```
|                                                            =                                                           |
|                                                            -   .                                                       |
|                                                            =                                            .              |
|                                                  .    .  . +.  . .  .     .                                            |
|                               .                .  .        =    .:   .              .   .              .               |
|                         .                                  = . . .                    .                                |
|                                                            =. .                  . .                                   |
|                                                    .      .+. . ..                        .                            |
|                                                          . =: ..       ..  .                                           |
|                       .                              .     =.  ...    .        .    . .                     .          |
|                                                            = ..       .           .                                    |
|                                             .   .          +.    . .   ..    .   .  .                                  |
|                                                        .  .+.    ....   .                          .                   |
|                                           .             ..:+.... .  .                          .                       |
|                                                    .:    ::@-:::                              .    .                   |
|                                                . .  .......-::..                                                       |
|                                                .  .   .   .-              ..      .            ..                      |
|                                                    ..      -:. ..   .            .    .     .                          |
|                                                         .  -.    .                  .                      .           |
|                                                       ... .-     .                                                     |
|                                               .            -                           .                               |
|                                                            -  .                            .                           |
|                                                            -  .      .                     .                           |
|                                                            =  .      .  .      .                                       |
|                                             . .            -. .                                                        |
|                                                            -         .    .                            .               |
|                                                ..         .=.       .                               .                  |
|                                                            =        .        .                                         |
|                                                            -      .                                                    |
|                                                  ..        =                .                                          |
```

**Kill Zone Heatmap (Where do they kill?)**
```
|                                                            =                         .               .                 |
|                                                  .         -    .                                                      |
|                                                            -   .   .                                                   |
|                                                            =                                                           |
|                                                            =    .:   .                                                 |
|                                                            =   ...                  .                                  |
|                                             .              =.  .            .                                          |
|                                                            -                                                           |
|                                                            =                            .  .                   .       |
|                                                            =    .                                                      |
|    .                                                       = ..       .                                                |
|                                             .   . .     .  +     . . ....          .                                   |
|                                                            +.  ..  :                            .                      |
|               .                           .       .      ..+   . .                  . .           .                    |
|                                                           :@:..:                                   ..                  |
|                                                .      . .. -.                                                          |
|                                                            :.             ..  .               .                        |
|                                                     . .    -   ..                                    .                 |
|                    .                                  . :  -                                                  .        |
|                                             .          ..  -                                                           |
|                                                         .  -                                                           |
|                                                            -                                                           |
|                                                            :         :        .                                        |
|                                                            -         .  :                                              |
|                                             .              -               .                                           |
|                                               .            -         .                                                 |
|                                                            -        .                                                  |
|                                                            -                                                           |
|                                                            -   .                                                       |
|                                                            -                                 .                         |
```

## Generation Highlights

### Best Improvement

**Generation 8**: Best fitness jumped +138.1 (+8121.0%)
- New best fitness: 139.8

### Worst Regression

**Generation 9**: Best fitness dropped -95.7 (-68.5%)
- New best fitness: 44.0
- *Note: This may be normal variation after a lucky outlier*

### Most Accurate Generation

**Generation 10**: Population accuracy reached 25.3%

### Most Kills (Single Agent)

**Generation 8**: An agent achieved 16 kills

### Most Diverse Generation

**Generation 10**: Diversity index 0.62

### Most Converged Generation

**Generation 2**: Diversity index 0.20

## Milestone Timeline

| Generation | Category | Value | Description |
|------------|----------|-------|-------------|
| 1 | Kills | 10.333333333333334 | First agent to achieve 1 kills |
| 1 | Kills | 10.333333333333334 | First agent to achieve 5 kills |
| 1 | Kills | 10.333333333333334 | First agent to achieve 10 kills |
| 8 | Fitness | 140 | Best fitness crossed 100 |

## Training Progress by Decile

| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|------|----------|---------|-----------|---------|-----------|----------|
| 0-10% | 1-1 | 56 | -200 | 1.3 | 12% | 428 | 54 |
| 10-20% | 2-2 | -30 | -192 | 1.5 | 14% | 455 | 38 |
| 20-30% | 3-3 | -62 | -206 | 2.0 | 13% | 361 | 53 |
| 30-40% | 4-4 | 3 | -176 | 2.7 | 17% | 535 | 57 |
| 40-50% | 5-5 | 19 | -184 | 3.2 | 19% | 533 | 65 |
| 50-60% | 6-6 | -17 | -209 | 2.5 | 16% | 445 | 45 |
| 60-70% | 7-7 | 2 | -175 | 3.7 | 22% | 567 | 60 |
| 70-80% | 8-8 | 140 | -142 | 5.1 | 23% | 602 | 70 |
| 80-90% | 9-9 | 44 | -213 | 2.8 | 16% | 353 | 70 |
| 90-100% | 10-11 | 165 | -170 | 4.1 | 24% | 573 | 89 |

### Metric Distributions (Last 10 Generations)

Visualizing population consistency: `|---O---|` represents Mean ± 1 StdDev.
- **Narrow bar**: Consistent population (Convergence)
- **Wide bar**: Chaotic/Diverse population

**Accuracy Distribution**
```
Gen   2: |------------------O--------------------|           14.1% ± 14.7%
Gen   3:    |-------------O-------------|                    12.7% ± 10.0%
Gen   4:       |----------------O-----------------|          17.0% ± 12.7%
Gen   5:          |-----------------O----------------|       19.2% ± 12.6%
Gen   6:          |------------O------------|                16.2% ±  9.3%
Gen   7:                  |-------------O-------------|      22.3% ± 10.1%
Gen   8:                  |--------------O-------------|     22.8% ± 10.4%
Gen   9:           |------------O-----------|                16.4% ±  9.0%
Gen  10:                      |-------------O-------------|  25.3% ± 10.2%
Gen  11:                 |----------------O---------------|  23.5% ± 11.9%
```

**Survival Steps Distribution**
```
Gen   2:                |----------O---------|               454.8 ± 183.2
Gen   3:              |------O-------|                       361.1 ± 132.2
Gen   4:                   |-----------O------------|        535.1 ± 220.2
Gen   5:                     |---------O----------|          533.3 ± 180.2
Gen   6:                  |-------O-------|                  445.4 ± 136.8
Gen   7:                      |----------O----------|        566.7 ± 195.0
Gen   8:                         |---------O----------|      601.9 ± 183.0
Gen   9:           |---------O---------|                     352.9 ± 170.6
Gen  10:                         |---------O----------|      604.5 ± 183.5
Gen  11:                     |----------O---------|          541.3 ± 182.8
```

**Kills Distribution**
```
Gen   2: |----------O----------|                               1.5 ±   2.2
Gen   3:   |----------O----------|                             2.0 ±   2.2
Gen   4:    |------------O-------------|                       2.7 ±   2.7
Gen   5:      |-------------O-------------|                    3.2 ±   2.7
Gen   6:      |----------O---------|                           2.5 ±   2.1
Gen   7:         |-------------O------------|                  3.7 ±   2.7
Gen   8:             |----------------O---------------|        5.1 ±   3.2
Gen   9:      |-----------O-----------|                        2.8 ±   2.3
Gen  10:         |-----------------O-----------------|         4.6 ±   3.6
Gen  11:      |---------------O---------------|                3.6 ±   3.2
```

**Fitness Distribution**
```
Gen   2:             |--------O-------|                     -191.8 ±  37.9
Gen   3:      |-----------O------------|                    -206.2 ±  53.0
Gen   4:            |------------O------------|             -176.0 ±  57.0
Gen   5:        |--------------O---------------|            -183.7 ±  64.8
Gen   6:       |----------O---------|                       -209.1 ±  45.1
Gen   7:            |-------------O------------|            -175.0 ±  60.3
Gen   8:                 |---------------O---------------|  -142.5 ±  70.1
Gen   9: |---------------O---------------|                  -213.5 ±  69.6
Gen  10:      |----------------------O--------------------| -159.5 ±  98.4
Gen  11:      |-----------------O------------------|        -180.0 ±  79.4
```

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 0.66 (up from 0.31 in Phase 1)
- **Shots per Kill:** 8.33 (down from 10.15 in Phase 1)
- **Kill Conversion Rate:** 12.0% (up from 9.9% in Phase 1)
- **Average Kills per Episode:** 3.6

### Efficiency Trend

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 | 0.33 | 10.52 | 9.5% |
| Phase 2 | 0.52 | 8.44 | 11.8% |
| Phase 3 | 0.58 | 8.28 | 12.1% |
| Phase 4 | 0.76 | 7.07 | 14.1% |
| Phase 5 | 0.73 | 7.60 | 13.1% |

**Assessment:** Agent shows slight efficiency improvement. Shots per kill dropped 18%.

## Learning Velocity

### Velocity by Phase

| Phase | Fitness Delta | Delta/Gen | Velocity | Trend |
|-------|---------------|-----------|----------|-------|
| Phase 1 | -86 | -42.8 | Stalled |  |
| Phase 2 | +65 | +32.7 | Fast | ↑ Accelerating |
| Phase 3 | -37 | -18.3 | Stalled | ↓ Slowing |
| Phase 4 | +138 | +69.0 | Fast | ↑ Accelerating |
| Phase 5 | +120 | +40.1 | Fast | ↓ Slowing |

### Current Velocity

- **Recent Improvement Rate:** +40.1 fitness/generation
- **Acceleration:** +35.3 (learning speeding up)
- **Projected Generations to +50% Fitness:** ~2 generations

### Velocity Assessment

Learning is progressing well with good velocity. Continue training.

## Reward Component Evolution

| Component | Phase 1 | Mid | Final | Trend | Status |
|-----------|---------|-----|-------|-------|--------|
| DeathPenalty | -254.2 | -255.5 | -243.9 | → +4% | Improving |
| DistanceBasedKillReward | +24.0 | +45.5 | +64.7 | ↑↑↑ +170% | Learned |
| ConservingAmmoBonus | -15.7 | -23.2 | -25.8 | ↓↓ -65% | Not learned |
| VelocitySurvivalBonus | +32.1 | +14.0 | +13.8 | ↓↓ -57% | Stable |
| ExplorationBonus | +14.2 | +10.0 | +11.1 | ↓ -22% | Stable |

**Exploration Efficiency (Final Phase):** 0.0205 score/step
- *Note: A higher rate indicates faster map traversal, independent of survival time.*

## Reward Balance Analysis

### Warnings

- **ConservingAmmoBonus consistently negative** - This component has been negative throughout training, averaging -25.8/episode. The intended behavior may not be incentivized strongly enough, or there may be a conflict with other rewards.

- **DeathPenalty consistently negative** - This component has been negative throughout training, averaging -243.9/episode. The intended behavior may not be incentivized strongly enough, or there may be a conflict with other rewards.

- **DistanceBasedKillReward dominates reward (72%)** - This single component accounts for most of all positive reward. Other behaviors may be under-incentivized.

- **VelocitySurvivalBonus declining** - This component dropped from 32.1 to 13.8. The agent may be trading off this behavior for others.

- **High penalty ratio (300.7%)** - Negative rewards are 301% of positive rewards. Agents may be struggling to achieve net positive fitness.

### Confirmations

- **VelocitySurvivalBonus positive** - Agents are learning to stay alive

### Recommendations

- Consider increasing the magnitude of consistently negative reward components
- Check if there are conflicting incentives preventing the behavior
- Review if other behaviors need stronger incentives
- Consider reducing the dominant component or boosting others

## Population Health Dashboard

### Current Status: 🟡 Watch

| Metric | Value | Trend (Recent) | Status |
|--------|-------|----------------|--------|
| Diversity Index | 0.35 | ↑ Increasing | 🟢 Good |
| Elite Gap | 1.23 | → | 🟢 Good |
| Min Fitness Trend | -2.6 | ↓ | 🟡 Watch |
| Max Fitness Trend | +10.8 | ↑ | 🟢 Good |
| IQR (p75-p25) | 74 | ↑ 4 | 🟢 |

### Warnings

- ⚠️ Floor declining - worst agents getting worse

## Stagnation Analysis

- **Current Stagnation:** 1 generations
- **Average Stagnation Period:** 2.7 generations
- **Longest Stagnation:** 6 generations
- **Number of Stagnation Periods:** 3

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Accuracy | Ratio | Grade | Cause of Death |
|-----|--------------|-----------|----------|-------|-------|----------------|
| 1 | 56 | -265 | 3.8% | -4.74 | F | asteroid_collision |
| 2 | -30 | -261 | 7.7% | 0.00 | F | asteroid_collision |
| 3 | -62 | 81 | 18.0% | 0.00 | F | asteroid_collision |
| 4 | 3 | -171 | 5.6% | -50.04 | F | asteroid_collision |
| 5 | 19 | -156 | 11.8% | -8.02 | F | asteroid_collision |
| 6 | -17 | 17 | 18.2% | 0.00 | F | asteroid_collision |
| 7 | 2 | -132 | 15.2% | -77.40 | F | asteroid_collision |
| 8 | 140 | -103 | 11.5% | -0.74 | F | asteroid_collision |
| 9 | 44 | 247 | 24.7% | 5.61 | A | asteroid_collision |
| 10 | 165 | -246 | 5.3% | -1.49 | F | asteroid_collision |

### Generalization Summary

- **Average Fitness Ratio:** 5.61
- **Best Ratio:** 5.61
- **Worst Ratio:** 5.61

**Grade Distribution:** A:1 F:9 

## Correlation Analysis

### Fitness Correlations

| Metric | Correlation | Strength |
|--------|-------------|----------|
| Kills | +0.94 | Strong |
| Steps Survived | +0.90 | Strong |
| Accuracy | +0.85 | Strong |

### Interpretation

Fitness is most strongly predicted by kills (r=0.94).

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 541 steps (36.1% of max)
- **Max Survival:** 1165 steps

### Survival Progression

| Phase | Mean Steps | Change |
|-------|------------|--------|
| Phase 1 | 441 |  |
| Phase 2 | 448 | +7 |
| Phase 3 | 489 | +41 |
| Phase 4 | 584 | +95 |
| Phase 5 | 500 | -85 |

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 3.18
- **Avg Steps Survived:** 500
- **Avg Accuracy:** 18.9%
- **Max Kills (Any Agent Ever):** 15.666666666666666
- **Max Steps (Any Agent Ever):** 1229.6666666666667

## Learning Progress

**Comparing First 1 vs Last 1 Generations:**

| Metric | Early | Late | Change |
|--------|-------|------|--------|
| Best Fitness | 55.9 | 164.3 | +194.2% |
| Avg Fitness | -199.6 | -180.0 | +9.8% |

**Verdict:** Moderate learning - some improvement but room for more training.

## Neural & Behavioral Complexity

| Gen | Saturation | Entropy | Control Style |
|-----|------------|---------|---------------|
| 1 |   0.0% |  0.64 | Analog (Smooth) |
| 2 |   0.0% |  0.62 | Analog (Smooth) |
| 3 |   0.0% |  0.63 | Analog (Smooth) |
| 4 |   0.0% |  0.68 | Analog (Smooth) |
| 5 |   0.0% |  0.54 | Analog (Smooth) |
| 6 |   0.0% |  0.62 | Analog (Smooth) |
| 7 |   0.0% |  0.62 | Analog (Smooth) |
| 8 |   0.0% |  0.60 | Analog (Smooth) |
| 9 |   0.0% |  0.52 | Analog (Smooth) |
| 10 |   0.0% |  0.61 | Analog (Smooth) |
| 11 |   0.0% |  0.67 | Analog (Smooth) |

**Metrics Explanation:**
- **Saturation**: % of time neurons are stuck at hard limits (0 or 1). High (>80%) means binary control; Low means analog control.
- **Entropy**: Measure of input unpredictability. Low = simple loops; High = random/complex.

## Risk Profile Analysis

Analysis of how close agents let asteroids get before reacting or killing them.

| Gen | Avg Min Dist | Fitness | Kills | Archetype |
|-----|--------------|---------|-------|-----------|
| 1 |   13.0px | -199.6 |  1.3 | Victim |
| 2 |   13.7px | -191.8 |  1.5 | Victim |
| 3 |   12.8px | -206.2 |  2.0 | Victim |
| 4 |   14.4px | -176.0 |  2.7 | Victim |
| 5 |   14.5px | -183.7 |  3.2 | Victim |
| 6 |   15.7px | -209.1 |  2.5 | Victim |
| 7 |   16.5px | -175.0 |  3.7 | Victim |
| 8 |   13.9px | -142.5 |  5.1 | Victim |
| 9 |   14.0px | -213.5 |  2.8 | Victim |
| 10 |   17.1px | -159.5 |  4.6 | Victim |
| 11 |   17.6px | -180.0 |  3.6 | Victim |

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 62.72
- Average Range (Best-Min): 310.85
- Diversity Change: +0.0%
- **Status:** Population is converging (low diversity)

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Safe Dist | Max Kills |
|--------|-----------|-----------|--------------|-----------|----------|
| Q1 | 1.44 | 441 | 13.2% | 199.8px | 10.333333333333334 |
| Q2 | 2.35 | 448 | 14.9% | 191.1px | 9.666666666666666 |
| Q3 | 2.86 | 489 | 17.7% | 183.7px | 10.666666666666666 |
| Q4 | 3.96 | 533 | 22.0% | 175.6px | 15.666666666666666 |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
|--------|----------|--------|---------|-------------------|
| Q1 | 32.6% | 2.0% | 45.3% | **Dogfighter** |
| Q2 | 22.5% | 2.6% | 60.2% | **Dogfighter** |
| Q3 | 12.6% | 4.7% | 70.3% | **Dogfighter** |
| Q4 | 10.3% | 11.7% | 81.9% | **Dogfighter** |

### Input Control Style

| Period | Thrust Dur | Turn Dur | Shoot Dur | Idle Rate | Wraps |
|--------|------------|----------|-----------|-----------|-------|
| Q1 | 0.0f | 0.0f | 0.0f | 26.7% | 2.4 |
| Q2 | 0.0f | 0.0f | 0.0f | 26.8% | 1.6 |
| Q3 | 0.0f | 0.0f | 0.0f | 23.0% | 1.0 |
| Q4 | 0.0f | 0.0f | 0.0f | 14.4% | 0.8 |

### Intra-Episode Score Breakdown

Analysis of when agents earn their reward during an episode (Early vs Late game).

| Quarter | Avg Score | Share of Total | Play Style |
|---------|-----------|----------------|------------|
| Start (0-25%) | -0.6 | 0.3% | Balanced |
| Mid-Game (25-50%) | 8.2 | -4.6% | Balanced |
| Late-Game (50-75%) | 22.6 | -12.6% | Balanced |
| End-Game (75-100%) | -210.3 | 116.8% | Survivor |

## Recent Generations (Last 30)

<details>
<summary>Click to expand Recent Generations table</summary>

| Gen   | Best   | Avg    | StdDev | Kills  | Steps  | Acc%   | Stag   |
|-------|--------|--------|--------|--------|--------|--------|--------|
| 1     | 56     | -200   | 54     | 1.3    | 428    | 12     | 0      |
| 2     | -30    | -192   | 38     | 1.5    | 455    | 14     | 1      |
| 3     | -62    | -206   | 53     | 2.0    | 361    | 13     | 2      |
| 4     | 3      | -176   | 57     | 2.7    | 535    | 17     | 3      |
| 5     | 19     | -184   | 65     | 3.2    | 533    | 19     | 4      |
| 6     | -17    | -209   | 45     | 2.5    | 445    | 16     | 5      |
| 7     | 2      | -175   | 60     | 3.7    | 567    | 22     | 6      |
| 8     | 140    | -142   | 70     | 5.1    | 602    | 23     | 0      |
| 9     | 44     | -213   | 70     | 2.8    | 353    | 16     | 1      |
| 10    | 165    | -159   | 98     | 4.6    | 604    | 25     | 0      |
| 11    | 164    | -180   | 79     | 3.6    | 541    | 24     | 1      |

</details>


## Top 10 Best Generations

<details>
<summary>Click to expand Top 10 Best Generations table</summary>

| Rank | Gen   | Best   | Avg    | Kills  | Steps  | Accuracy |
|------|-------|--------|--------|--------|--------|----------|
| 1    | 10    | 165    | -159   | 15.3   | 967    | 41.5     |
| 2    | 11    | 164    | -180   | 14.7   | 1165   | 45.7     |
| 3    | 8     | 140    | -142   | 15.7   | 1124   | 42.9     |
| 4    | 1     | 56     | -200   | 10.3   | 982    | 29.3     |
| 5    | 9     | 44     | -213   | 9.7    | 1011   | 25.3     |
| 6    | 5     | 19     | -184   | 5.3    | 1230   | 34.3     |
| 7    | 4     | 3      | -176   | 9.7    | 854    | 32.4     |
| 8    | 7     | 2      | -175   | 10.3   | 867    | 33.0     |
| 9    | 6     | -17    | -209   | 9.7    | 877    | 31.3     |
| 10   | 2     | -30    | -192   | 7.3    | 944    | 34.9     |

</details>


## Trend Analysis

| Period | Avg Best | Avg Mean | Avg Min | Improvement |
|--------|----------|----------|---------|-------------|
| Q1 | 13.1 | -195.7 | -260.0 |  |
| Q2 | -29.3 | -191.1 | -275.5 | -42.4 |
| Q3 | 1.1 | -196.4 | -268.5 | +30.4 |
| Q4 | 103.1 | -174.1 | -265.2 | +101.9 |


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

     165 |         * 
     140 |          *
     115 |       *   
      90 |           
      64 |           
      39 |*       *  
      14 |    *      
     -11 |   *  *    
     -37 | *   *     
     -62 |           
     -87 |  *        
    -112 |           
    -138 |           
    -163 |       o o 
    -188 |   oo o   o
    -213 |ooo  o  o  
         -----------
         Gen 1Gen 11
```


---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 0.00s
- **Evaluation (Simulation):** 32.31s (0.0%)
- **Evolution (GA Operators):** 0.0000s (0.0%)

| Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
|-----------|---------------|---------------|------------|
| 1-1 | 26.53s | 0.0000s | 0.00s |
| 2-2 | 28.47s | 0.0000s | 0.00s |
| 3-3 | 21.23s | 0.0000s | 0.00s |
| 4-4 | 34.55s | 0.0000s | 0.00s |
| 5-5 | 34.84s | 0.0000s | 0.00s |
| 6-6 | 27.66s | 0.0000s | 0.00s |
| 7-7 | 37.28s | 0.0000s | 0.00s |
| 8-8 | 40.92s | 0.0000s | 0.00s |
| 9-9 | 21.95s | 0.0000s | 0.00s |
| 10-10 | 39.91s | 0.0000s | 0.00s |
| 11-11 | 36.26s | 0.0000s | 0.00s |

