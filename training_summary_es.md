# Training Summary Report

**Generated:** 2026-01-14 00:10:53
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
Best Fitness: 705 → 899   [▅▅▂▅▅█▇▁▄▆] +27%
Avg Fitness:  156 → 313   [▁▂▁█▂▇▂▂▃▄] +101%
Avg Kills:    2.6 → 4.6   [▁▁▁█▃▇▂▂▅▆] +77%
Avg Accuracy: 21% → 30%   [▁▁▅▆█▆▆▇▅▃] +42%
Avg Steps:    559 → 663   [▆▁▂▆█▆▆▃▅▅] +18%
Diversity:    261 → 245   [█▇▃▅▇▆▇▁▆▆] -6%
```

## Training Configuration

```
method: Evolution Strategies
population_size: 25
num_generations: 500
sigma: 0.1
learning_rate: 0.01
use_antithetic: True
use_rank_transformation: True
weight_decay: 0.005
seeds_per_agent: 12
max_workers: 16
```

## Overall Summary

- **Total Generations:** 78
- **Training Duration:** 0:58:56.809005
- **All-Time Best Fitness:** 1041.15
- **Best Generation:** 60
- **Final Best Fitness:** 899.21
- **Final Average Fitness:** 313.40
- **Avg Improvement (Early->Late):** 110.24
- **Stagnation:** 18 generations since improvement

**Generalization (Fresh Game Performance):**
- Avg Generalization Ratio: 1.00
- Best Fresh Fitness: 2358.39 (Gen 65)
- Episode Completion Rate: 10.4%

## Best Agent Deep Profile

The most fit agent appeared in **Generation 60** with a fitness of **1041.15**.

### Combat Efficiency

- **Total Kills:** 11.916666666666666
- **Survival Time:** 16.9 seconds (1014.5833333333334 steps)
- **Accuracy:** 43.3%
- **Shots per Kill:** 2.3
- **Time per Kill:** 1.42 seconds

### Behavioral Signature

**Classification:** `Dogfighter`

| Action | Rate (per step) | Description |
|--------|-----------------|-------------|
| **Thrust** | 18.7% | Movement frequency |
| **Turn** | 74.4% | Rotation frequency |
| **Shoot** | 72.4% | Trigger discipline |

### Spatial Analytics (Best Agent - Generations 69-78)

**Position Heatmap (Where does it fly?)**
```
|                                                                                                                        |
|                                                                                                                        |
|                                                   .                                                                    |
|                                                   .                                                                    |
|                                                                                                                        |
|                                                   .                                                                    |
|                                    .                     :  .                       .                                  |
|                                               :                                .                                       |
|                                                .  .      :                                                             |
|                                                  .        :                                                            |
|               .                                     . -   -:                                                           |
|                                 .    .     .      .      .::                                                           |
|                             .      . ...        .    ....: :                                 .                         |
|                    :.       .              ..         . :.-:           .                                               |
|                                                   :..:..:--@.                                                          |
|                                .                  : ..  ::..                                                           |
|                                  :   :.        .          ..   .  . .                                                  |
|                                       :                            :..                                                 |
|                                       .                                                                                |
|                                                                                                                        |
|                                                .          . .                                                          |
|                                                                                                                        |
|                                                       .           .                                                    |
|                                                                                                                        |
|                                   ..                             .                                                     |
|                                                                                                                        |
|                                          .                                                                             |
|                                   .                                                                                    |
|                                           .                           .                                                |
|                                                                                                                        |
```

**Kill Zone Heatmap (Where does it kill?)**
```
|                                                                                                                        |
|                                                   .                                                                    |
|                                                   .     .                                                              |
|                                                   :     .                                                              |
|                                                    .                                                                   |
|                                               .                                                                        |
|                                          .               :                                                             |
|                              .        .   .   .                                .                                       |
|                       .                       ..  :      :                                                             |
|         .                   .                  .    .     :                   .                                        |
|               :                                       :   -.                                                           |
|                                 .                        .:                                           .                |
|                                      . :        . .   . ..:.                                    .                      |
|                    -.       :                           : :.                                                           |
|.                        .               .         :.  . .--@                                                           |
|                               .       .     .     .  .  :::                                                            |
|                                  .   .:        .          .      .. .                                                  |
|                                       :                            : .                                                 |
|                                                                                                                        |
|                                                                        ..        .                                     |
|                                                                                                                        |
|                                                                                                         .              |
|                                                            .                                                           |
|                                                                                                         .              |
|                                   :.                      .                         .          .                       |
|                                                                .                                                       |
|                                                                                                                        |
|                                              .     ..                    .                                             |
|                                           .                                                                            |
|                                                            .                 .                                         |
```

### Spatial Analytics (Population Average - Generations 69-78)

**Position Heatmap (Where do they fly?)**
```
|       .          .  .     ...  ... .  .. .  .   .  ..    ..:..  ..  .  .... . .     ....         ..            .       |
|.                 . .    ..         . .    . ..    . ...   .: .       .. . ..  ... .  .  .    .  .    .                .|
|           .                 . .     .....  ..  ..........::=::.: .....  . .   .  ..   ..  . .  .     .      .          |
| .           .    .          . . . ...  . ...   . ........::+:..: ....... .. ...      .   .   .    .      ...     .     |
|             .   .    . .   . . ... ..   . . .  ...:.  .....-:............ ....    . .    ..  . .. .   .  .... .        |
|                     .  .       .  .   . .... . ...... .....-..... .. ..........   .  .    .  . .   .     . ..          |
|  .   .          . .  .....  .... . . ..... ....... ......:.-:.....   .  ..........  . ...        .  . .....   .    .   |
|                .  ..    .   .  .  . ...  .. . :... ..:.:.::+...:::.....   ....... .  .    ....    .  ..   ..      .. . |
|..   . .  . ..  ...   .  .  .    ....   .... . ..::.......::-...:..:..   .. ......:   .     .........    . .... .... . .|
|  ..    .. ... .   ... . ..   ...    ... .... . .:..:....:::-.:::....: ...........:.   .. ..... ..  .  .                |
|...  .  .   .  ...  . .. . .    ....:.  . ...:  ...:...-::::-.::.... . ..... ..:....  ... ... . .....  .  ....  ..     .|
|.    .    .     ...... .  .     ...  -. ... ......::..:.::::-:.:::.....:.. .:..:.:=....  .... .  ... ....  ...          |
| .     .. . ..  . . . ... .... ...  ........ .::::::-::::-:-=:-::..:..:....::......  . ...........-...:.:...  ..       .|
|   .      .  .     .:.. ........  . .. .....:::....::::::---=--::::::::....:......: ..  . .. ..  . .:. ..... ..  .   .  |
|. .....     .   ....   .. ...  .     ..... ..:..:.::::-:-==+@=--::::::...............  ..... .  . ....... ..     .  .. .|
|   .. . .  . ...  . :     . . ...  ... ..  ........::::::-====--:::...:::. .  .  .  .. . . ...... .... ..   . ...... .  |
|. . . ..  . .. ..         ... .  ..............:::.::.:::::---::::::.:........ ...  .  .. .......:......... .   ..      |
|.        . .    ..   ..   .......  .  ... ......:.::...:.::.:::::. .:.:... .... ..  .. .-........: ::..   .     .. . .  |
|.   .. .  . .  . ..        ........... .. .. ...............:..:..:................ . ... .. ..  .......... .   .  .    |
|  .   .  . .            . ..     .. ... ... .... ...  .. ...:......... .... .......  . ..  ......  . ..       .  .    . |
|... ..   .  ..  ... ..  ... ..  . . ...    .   ... .. ......::......... ... ... ...    .   .  ........ .       .  .  ...|
| .          . .     .....     .. .... .. ..... .. .....  :. :.... .. . ... .... . ....         ...  ..  ..   .    .   . |
|.   ..       . ..       ....  .  .   .    .... ..... ...... :.. .:.......  .     .  . ....    .    .       .  ..  . ..  |
|     .     .  . .       .  ......   . . . .  .. . ..........-. .......     .. .. ...... . . . ..    .    .          .   |
|                       ...     .   ...  . .   . .     ..  . -........ .. . ....  . . ..  .. .   ...      .              |
|                .      .. .  . .  .       . . . ..     ..  .: .. .. ...:.   . . ...... .  ..          .   .        .    |
|       .          .  .  . .   . .. ..  .. .  ... .. .      .:.......   ....   .   .     .  ..          ..    . .      . |
|.                  .          .. . . . .. .. .. ..  .  . . .:.....  .....    ..... ..... ..   .           .    .        |
|        . .    .   .  ...  .      .. .     . .     ... .... :..... ....... ..  ..... ..    .          .    .  .  .     .|
|.            .   .         .    . .   ....... ..   ..  . . .-..... .  ..  . .  . .. ..     .            .   ..    .    .|
```

**Kill Zone Heatmap (Where do they kill?)**
```
|                                  . .       .      .       ..  .    .        .       ..             .                .  |
|       .                    .       .      .  .    .     .  :.     .           .    .        .                        . |
|  .  .                  .   ....    .  .         ... .  .. .. ...      .              ..          .    .  ..            |
|                    .              ...    ... . . ..   . .  :. ..                     .   .     .                       |
|                        .     .              .   ....       . .. .    .       . . .  .                    . .           |
|.                                    .   ..   ... . .... .. :  . .   ..    ..     .                 .       .           |
|                        .        .       ...   ...      . : :.. .  . .  ..       . ..    .   .        ..  .             |
|                   .          . . .    ..  .   ..:. .  ... .:...:..       ..  . .   .      .                        .   |
|      .                ..    .  .  .     .     ....:...: .:.:..... :.        ...  .             .  .           .     .. |
|        .. . .       .  .    ..          ....   .. ....: ..::...: .  . . .. :. .  .   .  ..     . .  .  ..      .      .|
|    .         ....                    .      .    .....:.. ::...... .    . . .         ..     .   . . .     .      .    |
| ..             .             .  ..   .   .........:...::.:::........... .. :.    ...  ..   .     ... ..      .    .    |
|    .    .     ..     .     .         ....     ....::..::::--:::....... .....     .      .... . .... . ..      .    .   |
|.   .  .  ..    .   :..    . . .  .  . . . ...::  .:::::--:-=:-.:.:..::. ..::  . ...  ... .. ..   ..  ... ..           .|
|.  ..      ..       .    ...        .. ... ..... ..:.::::-==@=--:.::.:. .   ... .. . ..    .    . .      .. ...     . . |
| .    .  .     ..   .    ...  ... .  . .    .. ... ::.:::-====::.....:::.     . .  . ..   ... . .   .   ..   .. .   ..  |
|                            .  . .. . ..      . .:.:..:::-:::--:...:.. ..... .. . .    .  . .  . .      ..   ..         |
|          .               .    .. .    ..  ... .:.-:...:....::......: .. .. .    .. .     .. .. .. ...  .  ..   .       |
|         ..            .    . .  .. . . .     .. . .   . ...:...  ..  ...  .  . ...    .  . .        .    .          .  |
|.        .       .      .  . .    .   . .. .  . ..       .. :..... ...  ..    ..  .         .      .        .        . .|
|         ..  .         .    . ....  ...         .       . ....:    . .. ..  .. .  . .      .                  .         |
|                 . .. .  .   ...  .. .    .   . ..  .  .    :.  ...       .  ...     .     .             .     .        |
|              ...... .  .   .   .   .        :    .... . .  :    :...    .                       .                      |
|                        . ..   .                   .. .     :. ..            . . .       .  ... . .      ..    .       .|
|.   .                     .    .   ...               .   . .. . .. .  .          .   .   .    . .  .      .             |
|                 .    ..      .            .. .       . .  .:. .. .  . .   .   .   .   . ..   .                 .       |
|                   .       .    . ...     .   .   ..   . . .:   . .                    .        .       .      .        |
|                 .                   .       ...    ..      :  ..   .. .  . ....                    .     .       .     |
|   .  .               .     . ...  .       .          ..    :  .   ... . . .....   ..     .            ..  .            |
|         .             . .       .   .                   .  -   ..    .  .    . ..      .  .                   .   .  . |
```

## Generation Highlights

### Best Improvement

**Generation 5**: Best fitness jumped +573.9 (+170.3%)
- New best fitness: 910.8

### Worst Regression

**Generation 40**: Best fitness dropped -526.5 (-51.0%)
- New best fitness: 505.9
- *Note: This may be normal variation after a lucky outlier*

### Most Accurate Generation

**Generation 78**: Population accuracy reached 30.1%

### Most Kills (Single Agent)

**Generation 39**: An agent achieved 12 kills

### First Viable Population

**Generation 1**: Average fitness first became positive

### Most Diverse Generation

**Generation 4**: Diversity index 3.51

### Most Converged Generation

**Generation 55**: Diversity index 0.68

## Milestone Timeline

| Generation | Category | Value | Description |
|------------|----------|-------|-------------|
| 1 | Fitness | 705 | Best fitness crossed 100 |
| 1 | Fitness | 705 | Best fitness crossed 500 |
| 1 | Kills | 8.5 | First agent to achieve 1 kills |
| 1 | Kills | 8.5 | First agent to achieve 5 kills |
| 5 | Kills | 10.25 | First agent to achieve 10 kills |
| 39 | Fitness | 1032 | Best fitness crossed 1000 |

## Training Progress by Decile

| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|------|----------|---------|-----------|---------|-----------|----------|
| 0-10% | 1-7 | 911 | 131 | 2.3 | 22% | 478 | 212 |
| 10-20% | 8-14 | 920 | 179 | 2.9 | 23% | 487 | 245 |
| 20-30% | 15-21 | 809 | 162 | 2.8 | 24% | 510 | 222 |
| 30-40% | 22-28 | 970 | 159 | 2.7 | 24% | 517 | 238 |
| 40-50% | 29-35 | 936 | 188 | 3.0 | 24% | 504 | 236 |
| 50-60% | 36-42 | 1032 | 187 | 3.0 | 25% | 532 | 242 |
| 60-70% | 43-49 | 996 | 191 | 3.1 | 25% | 515 | 230 |
| 70-80% | 50-56 | 961 | 219 | 3.5 | 24% | 533 | 226 |
| 80-90% | 57-63 | 1041 | 240 | 3.8 | 26% | 575 | 241 |
| 90-100% | 64-78 | 899 | 241 | 3.8 | 25% | 566 | 252 |

### Metric Distributions (Last 10 Generations)

Visualizing population consistency: `|---O---|` represents Mean ± 1 StdDev.
- **Narrow bar**: Consistent population (Convergence)
- **Wide bar**: Chaotic/Diverse population

**Accuracy Distribution**
```
Gen  69:    |----------------O----------------|              22.9% ± 10.1%
Gen  70:      |------------------O------------------|        25.1% ± 11.2%
Gen  71: |--------------------O--------------------|         23.5% ± 12.6%
Gen  72:  |--------------------O--------------------|        23.9% ± 12.4%
Gen  73:            |----------------O---------------|       27.4% ±  9.6%
Gen  74:         |----------------O----------------|         25.9% ±  9.9%
Gen  75:     |--------------------O-------------------|      25.8% ± 12.1%
Gen  76:    |-------------------O--------------------|       24.9% ± 12.1%
Gen  77:     |------------------O-------------------|        24.9% ± 11.6%
Gen  78:                |----------------O----------------|  30.1% ± 10.2%
```

**Survival Steps Distribution**
```
Gen  69:                       |-------O-------|             553.1 ± 148.4
Gen  70:                  |-----------O-----------|          549.4 ± 220.3
Gen  71:                       |--------O--------|           579.4 ± 165.9
Gen  72:                |-----------O------------|           509.9 ± 231.7
Gen  73:                      |-----------O-----------|      610.5 ± 219.7
Gen  74:                   |------------O------------|       585.4 ± 238.2
Gen  75:                      |----------O---------|         594.2 ± 195.3
Gen  76:                   |-------------O------------|      588.1 ± 246.7
Gen  77:                    |----------O----------|          560.0 ± 200.3
Gen  78:                            |--------O-------|       662.7 ± 157.5
```

**Kills Distribution**
```
Gen  69:     |-----------O------------|                        3.1 ±   2.4
Gen  70:   |----------------O-----------------|                3.7 ±   3.3
Gen  71:      |----------------O----------------|              4.1 ±   3.2
Gen  72:  |--------------O--------------|                      3.0 ±   2.8
Gen  73:           |-----------------O----------------|        5.2 ±   3.2
Gen  74:    |----------------O----------------|                3.9 ±   3.2
Gen  75:           |-------------O-------------|               4.6 ±   2.7
Gen  76:   |-----------------O----------------|                3.7 ±   3.3
Gen  77:       |-------------O--------------|                  3.8 ±   2.7
Gen  78:          |--------------O--------------|              4.6 ±   2.8
```

**Fitness Distribution**
```
Gen  69:   |------------O-----------|                        164.8 ± 201.9
Gen  70:  |-----------------O------------------|             243.2 ± 291.6
Gen  71:   |-----------------O-----------------|             256.3 ± 283.2
Gen  72: |--------------O---------------|                    177.8 ± 250.9
Gen  73:           |-----------------O----------------|      377.1 ± 277.1
Gen  74:    |----------------O-----------------|             258.1 ± 274.3
Gen  75:          |--------------O--------------|            314.7 ± 242.9
Gen  76:  |-----------------O-----------------|              239.5 ± 285.7
Gen  77:      |--------------O-------------|                 246.1 ± 226.1
Gen  78:         |---------------O--------------|            313.4 ± 245.4
```

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 0.70 (up from 0.49 in Phase 1)
- **Shots per Kill:** 7.05 (down from 7.72 in Phase 1)
- **Kill Conversion Rate:** 14.2% (up from 13.0% in Phase 1)
- **Average Kills per Episode:** 4.1

### Efficiency Trend

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 | 0.54 | 7.62 | 13.1% |
| Phase 2 | 0.53 | 7.41 | 13.5% |
| Phase 3 | 0.59 | 7.29 | 13.7% |
| Phase 4 | 0.65 | 7.33 | 13.7% |
| Phase 5 | 0.66 | 7.11 | 14.1% |

**Assessment:** Agent shows slight efficiency improvement. Shots per kill dropped 9%.

## Learning Velocity

### Velocity by Phase

| Phase | Fitness Delta | Delta/Gen | Velocity | Trend |
|-------|---------------|-----------|----------|-------|
| Phase 1 | -154 | -10.3 | Stalled |  |
| Phase 2 | -57 | -3.8 | Stalled | ↑ Accelerating |
| Phase 3 | +84 | +5.6 | Moderate | ↑ Accelerating |
| Phase 4 | +284 | +18.9 | Moderate | ↑ Accelerating |
| Phase 5 | +192 | +10.7 | Moderate | ↓ Slowing |

### Current Velocity

- **Recent Improvement Rate:** +10.7 fitness/generation
- **Acceleration:** +18.8 (learning speeding up)
- **Projected Generations to +50% Fitness:** ~42 generations

### Velocity Assessment

Learning is progressing well with good velocity. Continue training.

## Reward Component Evolution

| Component | Phase 1 | Mid | Final | Trend | Status |
|-----------|---------|-----|-------|-------|--------|
| DistanceBasedKillReward | +150.9 | +190.4 | +266.7 | ↑↑ +77% | Learned |
| DeathPenalty | -145.8 | -143.4 | -141.0 | → +3% | Improving |
| ConservingAmmoBonus | +61.2 | +80.0 | +106.4 | ↑↑ +74% | Learned |
| VelocitySurvivalBonus | +35.9 | +30.1 | +24.0 | ↓ -33% | Stable |
| ExplorationBonus | +28.5 | +24.7 | +19.1 | ↓ -33% | Stable |

**Exploration Efficiency (Final Phase):** 0.0325 score/step
- *Note: A higher rate indicates faster map traversal, independent of survival time.*

## Reward Balance Analysis

### Warnings

- **DeathPenalty consistently negative** - This component has been negative throughout training, averaging -141.0/episode. The intended behavior may not be incentivized strongly enough, or there may be a conflict with other rewards.

- **DistanceBasedKillReward is dominant (59%)** - This component accounts for a large portion of positive reward. Consider if this is intentional.

### Confirmations

- **Reward reasonably balanced** - No single component >60%
- **VelocitySurvivalBonus positive** - Agents are learning to stay alive

### Recommendations

- Consider increasing the magnitude of consistently negative reward components
- Check if there are conflicting incentives preventing the behavior
- Review if other behaviors need stronger incentives
- Consider reducing the dominant component or boosting others

## Population Health Dashboard

### Current Status: 🟢 Healthy

| Metric | Value | Trend (Recent) | Status |
|--------|-------|----------------|--------|
| Diversity Index | 1.00 | ↑ Increasing | 🟡 Watch |
| Elite Gap | 2.05 | → | 🟡 Watch |
| Min Fitness Trend | +1.6 | ↑ | 🟢 Good |
| Max Fitness Trend | +92.1 | ↑ | 🟢 Good |
| IQR (p75-p25) | 409 | ↑ 103 | 🟢 |

## Stagnation Analysis

- **Current Stagnation:** 18 generations
- **Average Stagnation Period:** 12.0 generations
- **Longest Stagnation:** 20 generations
- **Number of Stagnation Periods:** 6

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Accuracy | Ratio | Grade | Cause of Death |
|-----|--------------|-----------|----------|-------|-------|----------------|
| 68 | 696 | 486 | 12.0% | 0.70 | C | asteroid_collision |
| 69 | 551 | 319 | 15.8% | 0.58 | C | asteroid_collision |
| 70 | 749 | 551 | 12.5% | 0.74 | B | asteroid_collision |
| 71 | 799 | 49 | 3.3% | 0.06 | F | asteroid_collision |
| 72 | 728 | -92 | 4.8% | -0.13 | F | asteroid_collision |
| 73 | 825 | 1854 | 26.7% | 2.25 | A | asteroid_collision |
| 74 | 894 | 223 | 9.1% | 0.25 | F | asteroid_collision |
| 75 | 825 | -174 | 0.0% | -0.21 | F | asteroid_collision |
| 76 | 892 | 267 | 19.2% | 0.30 | F | asteroid_collision |
| 77 | 727 | 40 | 8.0% | 0.06 | F | asteroid_collision |

### Generalization Summary

- **Average Fitness Ratio:** 1.00
- **Best Ratio:** 4.14
- **Worst Ratio:** 0.01

**Grade Distribution:** A:26 B:6 C:6 D:3 F:36 

## Correlation Analysis

### Fitness Correlations

| Metric | Correlation | Strength |
|--------|-------------|----------|
| Kills | +0.99 | Strong |
| Steps Survived | +0.93 | Strong |
| Accuracy | +0.86 | Strong |

### Interpretation

Fitness is most strongly predicted by kills (r=0.99).

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 587 steps (39.2% of max)
- **Max Survival:** 1134 steps

### Survival Progression

| Phase | Mean Steps | Change |
|-------|------------|--------|
| Phase 1 | 482 |  |
| Phase 2 | 519 | +38 |
| Phase 3 | 518 | -1 |
| Phase 4 | 536 | +18 |
| Phase 5 | 568 | +32 |

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 3.98
- **Avg Steps Survived:** 579
- **Avg Accuracy:** 25.4%
- **Max Kills (Any Agent Ever):** 12.25
- **Max Steps (Any Agent Ever):** 1134.0

## Learning Progress

**Comparing First 7 vs Last 7 Generations:**

| Metric | Early | Late | Change |
|--------|-------|------|--------|
| Best Fitness | 650.3 | 827.1 | +27.2% |
| Avg Fitness | 130.7 | 275.2 | +110.6% |

**Verdict:** Moderate learning - some improvement but room for more training.

## Neural & Behavioral Complexity

| Gen | Saturation | Entropy | Control Style |
|-----|------------|---------|---------------|
| 49 |   0.0% |  1.24 | Analog (Smooth) |
| 50 |   0.0% |  1.32 | Analog (Smooth) |
| 51 |   0.0% |  1.21 | Analog (Smooth) |
| 52 |   0.0% |  1.08 | Analog (Smooth) |
| 53 |   0.0% |  1.01 | Analog (Smooth) |
| 54 |   0.0% |  1.24 | Analog (Smooth) |
| 55 |   0.0% |  1.16 | Analog (Smooth) |
| 56 |   0.0% |  1.18 | Analog (Smooth) |
| 57 |   0.0% |  1.02 | Analog (Smooth) |
| 58 |   0.0% |  1.07 | Analog (Smooth) |
| 59 |   0.0% |  1.09 | Analog (Smooth) |
| 60 |   0.0% |  1.19 | Analog (Smooth) |
| 61 |   0.0% |  1.42 | Analog (Smooth) |
| 62 |   0.0% |  1.02 | Analog (Smooth) |
| 63 |   0.0% |  1.25 | Analog (Smooth) |
| 64 |   0.0% |  1.02 | Analog (Smooth) |
| 65 |   0.0% |  1.06 | Analog (Smooth) |
| 66 |   0.0% |  1.13 | Analog (Smooth) |
| 67 |   0.0% |  1.17 | Analog (Smooth) |
| 68 |   0.0% |  1.16 | Analog (Smooth) |
| 69 |   0.0% |  0.98 | Analog (Smooth) |
| 70 |   0.0% |  1.18 | Analog (Smooth) |
| 71 |   0.0% |  0.93 | Analog (Smooth) |
| 72 |   0.0% |  1.17 | Analog (Smooth) |
| 73 |   0.0% |  0.92 | Analog (Smooth) |
| 74 |   0.0% |  1.24 | Analog (Smooth) |
| 75 |   0.0% |  0.86 | Analog (Smooth) |
| 76 |   0.0% |  1.05 | Analog (Smooth) |
| 77 |   0.0% |  1.03 | Analog (Smooth) |
| 78 |   0.0% |  1.21 | Analog (Smooth) |

**Metrics Explanation:**
- **Saturation**: % of time neurons are stuck at hard limits (0 or 1). High (>80%) means binary control; Low means analog control.
- **Entropy**: Measure of input unpredictability. Low = simple loops; High = random/complex.

## Risk Profile Analysis

Analysis of how close agents let asteroids get before reacting or killing them.

| Gen | Avg Min Dist | Fitness | Kills | Archetype |
|-----|--------------|---------|-------|-----------|
| 49 |   15.2px |  240.2 |  3.8 | Victim |
| 50 |   15.5px |  169.1 |  2.8 | Victim |
| 51 |   15.3px |  165.7 |  2.9 | Victim |
| 52 |   14.8px |  179.5 |  3.1 | Victim |
| 53 |   15.0px |  117.5 |  2.4 | Victim |
| 54 |   15.9px |  258.8 |  3.8 | Victim |
| 55 |   15.9px |  334.8 |  5.0 | Victim |
| 56 |   15.6px |  309.1 |  4.6 | Victim |
| 57 |   15.7px |  175.0 |  3.1 | Victim |
| 58 |   15.5px |  204.2 |  3.5 | Victim |
| 59 |   15.6px |  338.4 |  4.9 | Victim |
| 60 |   15.3px |  278.1 |  4.1 | Victim |
| 61 |   15.3px |  211.8 |  3.4 | Victim |
| 62 |   15.4px |  248.3 |  4.0 | Victim |
| 63 |   15.6px |  225.7 |  3.5 | Victim |
| 64 |   15.0px |  191.8 |  3.2 | Victim |
| 65 |   15.7px |  259.0 |  4.1 | Victim |
| 66 |   15.8px |  230.9 |  3.5 | Victim |
| 67 |   15.8px |  146.7 |  2.6 | Victim |
| 68 |   16.1px |  200.6 |  3.4 | Victim |
| 69 |   15.9px |  164.8 |  3.1 | Victim |
| 70 |   15.5px |  243.2 |  3.7 | Victim |
| 71 |   15.3px |  256.3 |  4.1 | Victim |
| 72 |   15.0px |  177.8 |  3.0 | Victim |
| 73 |   15.8px |  377.1 |  5.2 | Victim |
| 74 |   15.8px |  258.1 |  3.9 | Victim |
| 75 |   15.4px |  314.7 |  4.6 | Victim |
| 76 |   15.3px |  239.5 |  3.7 | Victim |
| 77 |   15.1px |  246.1 |  3.8 | Victim |
| 78 |   15.8px |  313.4 |  4.6 | Victim |

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 251.70
- Average Range (Best-Min): 908.77
- Diversity Change: +14.3%
- **Status:** Population is converging (low diversity)

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Safe Dist | Max Kills |
|--------|-----------|-----------|--------------|-----------|----------|
| Q1 | 2.66 | 489 | 23.0% | 183.3px | 10.583333333333334 |
| Q2 | 2.88 | 516 | 24.0% | 180.3px | 11.5 |
| Q3 | 3.26 | 525 | 24.6% | 179.3px | 12.25 |
| Q4 | 3.81 | 571 | 25.4% | 176.6px | 11.916666666666666 |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
|--------|----------|--------|---------|-------------------|
| Q1 | 32.9% | 71.5% | 54.6% | **Dogfighter** |
| Q2 | 27.6% | 70.6% | 55.1% | **Dogfighter** |
| Q3 | 24.7% | 70.8% | 63.8% | **Dogfighter** |
| Q4 | 17.2% | 69.9% | 67.6% | **Dogfighter** |

### Input Control Style

| Period | Thrust Dur | Turn Dur | Shoot Dur | Idle Rate | Wraps |
|--------|------------|----------|-----------|-----------|-------|
| Q1 | 0.0f | 0.0f | 0.0f | 9.1% | 1.4 |
| Q2 | 0.0f | 0.0f | 0.0f | 9.4% | 1.4 |
| Q3 | 0.0f | 0.0f | 0.0f | 7.6% | 1.2 |
| Q4 | 0.0f | 0.0f | 0.0f | 7.3% | 1.0 |

### Intra-Episode Score Breakdown

Analysis of when agents earn their reward during an episode (Early vs Late game).

| Quarter | Avg Score | Share of Total | Play Style |
|---------|-----------|----------------|------------|
| Start (0-25%) | 29.3 | 9.4% | Balanced |
| Mid-Game (25-50%) | 107.2 | 34.2% | Balanced |
| Late-Game (50-75%) | 136.0 | 43.4% | Balanced |
| End-Game (75-100%) | 40.8 | 13.0% | Balanced |

## Recent Generations (Last 30)

<details>
<summary>Click to expand Recent Generations table</summary>

| Gen   | Best   | Avg    | StdDev | Kills  | Steps  | Acc%   | Stag   |
|-------|--------|--------|--------|--------|--------|--------|--------|
| 49    | 669    | 240    | 183    | 3.8    | 540    | 27     | 10     |
| 50    | 487    | 169    | 164    | 2.8    | 481    | 26     | 11     |
| 51    | 740    | 166    | 233    | 2.9    | 561    | 21     | 12     |
| 52    | 602    | 180    | 218    | 3.1    | 473    | 22     | 13     |
| 53    | 741    | 118    | 225    | 2.4    | 488    | 20     | 14     |
| 54    | 961    | 259    | 277    | 3.8    | 540    | 24     | 15     |
| 55    | 696    | 335    | 227    | 5.0    | 626    | 27     | 16     |
| 56    | 774    | 309    | 239    | 4.6    | 563    | 29     | 17     |
| 57    | 670    | 175    | 239    | 3.1    | 539    | 25     | 18     |
| 58    | 553    | 204    | 194    | 3.5    | 564    | 25     | 19     |
| 59    | 847    | 338    | 248    | 4.9    | 620    | 26     | 20     |
| 60    | 1041   | 278    | 265    | 4.1    | 575    | 27     | 0      |
| 61    | 707    | 212    | 234    | 3.4    | 541    | 26     | 1      |
| 62    | 830    | 248    | 267    | 4.0    | 614    | 25     | 2      |
| 63    | 758    | 226    | 240    | 3.5    | 573    | 26     | 3      |
| 64    | 734    | 192    | 235    | 3.2    | 526    | 23     | 4      |
| 65    | 701    | 259    | 227    | 4.1    | 602    | 27     | 5      |
| 66    | 846    | 231    | 279    | 3.5    | 558    | 24     | 6      |
| 67    | 830    | 147    | 240    | 2.6    | 451    | 24     | 7      |
| 68    | 696    | 201    | 220    | 3.4    | 565    | 26     | 8      |
| 69    | 551    | 165    | 202    | 3.1    | 553    | 23     | 9      |
| 70    | 749    | 243    | 292    | 3.7    | 549    | 25     | 10     |
| 71    | 799    | 256    | 283    | 4.1    | 579    | 23     | 11     |
| 72    | 728    | 178    | 251    | 3.0    | 510    | 24     | 12     |
| 73    | 825    | 377    | 277    | 5.2    | 611    | 27     | 13     |
| 74    | 894    | 258    | 274    | 3.9    | 585    | 26     | 14     |
| 75    | 825    | 315    | 243    | 4.6    | 594    | 26     | 15     |
| 76    | 892    | 240    | 286    | 3.7    | 588    | 25     | 16     |
| 77    | 727    | 246    | 226    | 3.8    | 560    | 25     | 17     |
| 78    | 899    | 313    | 245    | 4.6    | 663    | 30     | 18     |

</details>


## Top 10 Best Generations

<details>
<summary>Click to expand Top 10 Best Generations table</summary>

| Rank | Gen   | Best   | Avg    | Kills  | Steps  | Accuracy |
|------|-------|--------|--------|--------|--------|----------|
| 1    | 60    | 1041   | 278    | 11.9   | 1015   | 43.3     |
| 2    | 39    | 1032   | 282    | 12.2   | 937    | 38.0     |
| 3    | 44    | 996    | 215    | 11.8   | 916    | 43.9     |
| 4    | 25    | 970    | 127    | 11.5   | 925    | 35.5     |
| 5    | 54    | 961    | 259    | 10.8   | 1001   | 41.4     |
| 6    | 32    | 936    | 230    | 11.3   | 801    | 45.7     |
| 7    | 13    | 920    | 174    | 10.6   | 968    | 34.9     |
| 8    | 5     | 911    | 197    | 10.2   | 896    | 43.2     |
| 9    | 78    | 899    | 313    | 11.2   | 851    | 34.4     |
| 10   | 74    | 894    | 258    | 9.9    | 893    | 36.3     |

</details>


## Trend Analysis

| Period | Avg Best | Avg Mean | Avg Min | Improvement |
|--------|----------|----------|---------|-------------|
| Q1 | 694.4 | 156.1 | -115.0 |  |
| Q2 | 734.6 | 174.4 | -112.5 | +40.1 |
| Q3 | 737.6 | 200.5 | -116.2 | +3.0 |
| Q4 | 782.5 | 244.1 | -115.6 | +44.9 |


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

    1041 |                                                           *                  
     972 |                                      *    *                                  
     902 |    *       *           *      *                     *                        
     833 |        **            *             *       *             *      *       * * *
     764 |          *    *              *   **    * *            *     *    *   * * *   
     694 |*    * *          *  *     * *               **   * * *     * ***  * * *    * 
     625 | *    *             *    ** *    *              *       *                     
     555 |  *        * *  ** *   *             *   *     *   *                          
     486 |              *                 *      *         *       *          *         
     416 |                                                                              
     347 |                                                                        o     
     278 |   *                                  o               oo  oo              o  o
     208 |      o o o         ooo        o ooo     o oo   o    o      ooo oo   oo  o oo 
     139 |o   o  o o  oooooo       o  ooo     o   o o  oo  ooo    oo     o  ooo  o      
      69 | oo  o     o      oo   oo oo    o    o o       o    o                         
       0 |   o                                                                          
         ------------------------------------------------------------------------------
         Gen 1                                                               Gen 78
```


---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 0.00s
- **Evaluation (Simulation):** 37.59s (0.0%)
- **Evolution (GA Operators):** 0.0000s (0.0%)

| Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
|-----------|---------------|---------------|------------|
| 1-7 | 29.13s | 0.0000s | 0.00s |
| 8-14 | 30.65s | 0.0000s | 0.00s |
| 15-21 | 31.61s | 0.0000s | 0.00s |
| 22-28 | 32.07s | 0.0000s | 0.00s |
| 29-35 | 31.50s | 0.0000s | 0.00s |
| 36-42 | 33.31s | 0.0000s | 0.00s |
| 43-49 | 32.25s | 0.0000s | 0.00s |
| 50-56 | 34.08s | 0.0000s | 0.00s |
| 57-63 | 36.80s | 0.0000s | 0.00s |
| 64-70 | 34.77s | 0.0000s | 0.00s |
| 71-77 | 37.36s | 0.0000s | 0.00s |
| 78-78 | 44.51s | 0.0000s | 0.00s |

