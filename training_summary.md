# Training Summary Report

**Generated:** 2026-01-13 17:34:43
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
Best Fitness: 390 → 1262   [▁▅▅█▅▅▄▄▄▆] +224%
Avg Fitness:  74 → 701   [▁▆▅▇▆▇▅▆█▆] +853%
Avg Kills:    1.8 → 8.6   [▁▇▆▇▆▇▅▆█▆] +382%
Avg Accuracy: 20% → 39%   [▁▇▅█▆▆▅▇▆▆] +96%
Avg Steps:    372 → 789   [▁▆▆▇▆▇▅▇█▆] +112%
Diversity:    149 → 282   [▁▅▃█▆▆▄▄▃▇] +89%
```

## Training Configuration

```
population_size: 10
num_generations: 500
mutation_probability: 0.05
max_workers: 16
```

## Overall Summary

- **Total Generations:** 22
- **Training Duration:** 0:06:57.321746
- **All-Time Best Fitness:** 1483.94
- **Best Generation:** 7
- **Final Best Fitness:** 1262.30
- **Final Average Fitness:** 700.75
- **Avg Improvement (Early->Late):** 84.08
- **Stagnation:** 15 generations since improvement

**Generalization (Fresh Game Performance):**

- Avg Generalization Ratio: 0.77
- Best Fresh Fitness: 2255.51 (Gen 17)
- Episode Completion Rate: 9.5%

## Best Agent Deep Profile

The most fit agent appeared in **Generation 7** with a fitness of **1483.94**.

### Combat Efficiency

- **Total Kills:** 16.4
- **Survival Time:** 21.3 seconds (1275.2 steps)
- **Accuracy:** 48.3%
- **Shots per Kill:** 2.0
- **Time per Kill:** 1.30 seconds

### Behavioral Signature

**Classification:** `Spinner`

| Action     | Rate (per step) | Description        |
| ---------- | --------------- | ------------------ |
| **Thrust** | 0.9%            | Movement frequency |
| **Turn**   | 97.3%           | Rotation frequency |
| **Shoot**  | 84.5%           | Trigger discipline |

### Spatial Analytics (Best Agent - Generations 13-22)

**Position Heatmap (Where does it fly?)**

```
|                                                                                                                 ...    |
|                                                                                                                   .    |
|                                                                                                                  .     |
|                                                                                     .                          .       |
|                                             .  .                                 .                                     |
|                                             .   ..                         .                              .            |
|                                                                                                                        |
|                                             .                       .....           . .:.                              |
|                                                                   .    .. .:    .         .                            |
|                                              .                 ..                                                      |
|                                               .      .       .  .         .                                            |
|                                        :.    :..   .   .   .. : .       ...                                            |
|                                          .. :.:... . . . .    .       .    .                                           |
|                                   .           :... .   ...:-:..    .   .   .:                                          |
|                                                   ...:.---=@=... ..    .  .                                            |
|                                            ... .  ... ---====-:.:::=..  .                                              |
|                                         . .        .:. :.... :.-..       ..                                            |
|                                            .   ..:-.-. ... ::    . ..    .                                             |
|                                            :::.   ....  . .: ..     .                                                  |
|                                             .           .::..-.                                                        |
|                                                           :   ...                                                      |
|                                                             .  .   .                                                   |
|                                                              .   :                        .                            |
|                                                              .  :....                                                  |
|                                                              .                                      . .:.              |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                            .           |
|                                                                                                                .       |
```

**Kill Zone Heatmap (Where does it kill?)**

```
|                                                                                                                  ..    |
|                                                                                                                   :    |
|                                                                                     .                           ...    |
|                                                                                    .                                   |
|                                               .                                .                             .         |
|                                                 ..                         .                                           |
|                                             .                             .                                            |
|                                                                     .... .          . ...                              |
|                                                                   .   ... ..   .                                       |
|                                                                ..                        .                             |
|                                                              . ..        ..                                            |
|                                        :    .:     .        . . .       ..                                             |
|                                     . .  .  ..:..:     ...    .         .  .                                           |
|                                    .          :  .:.   . ::::::            .:                                          |
|                                                   . .: :-==@=..  .      .                                              |
|                                            :    .  .. --===+-. ....=.... .                                             |
|                                                    .: .. ....:.=. .      ..                                            |
|                                          .     ...= :    . -.    .  ..                                                 |
|                                            -:: .. ..:.   . -..      .      .                                           |
|                                             .            -:..: ..                                                      |
|                                                           ..  ..                                                       |
|                                                             .    .                                                     |
|                                                             .   . .                                                    |
|                                                              .  : . .                         . .                      |
|                                                                                                        ..              |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                            .           |
|                                                                                                              .         |
|                                                                                                                        |
```

### Spatial Analytics (Population Average - Generations 13-22)

**Position Heatmap (Where do they fly?)**

```
|                                                          .                      ..                                     |
|                                     .                       .                                                          |
|                                 .                                                                                      |
|                 ..                                                                                                     |
|                 .                           .                  .:                                                      |
|                                         .   .   ..                            :                                        |
|               .                                           .                  .                                         |
|                    .                                    ..            . .   .        ...                               |
|                                     :       .       . . .  .  .        .  ...                                          |
|                                      ..    .      .     ..               .                                             |
|           .                   ..      .....   .    .        . .  .  .. .  .    .:                               .      |
|                                 ..  . .:. . .:...:.. ...  .:.::-:.:.  ..  .  . .        .:                             |
|                                  :... .  .. ::::.:::::-.:...:::    ::.:.: .. .  .       .                              |
|                ..           .        :. .  :..:...::::-:-:---:-....::.::. ..:..  .:     .                              |
|                              .     . :.       :.:.:::--===+@=--:.:-:.: ::  .  . .                       .              |
|                         ...        .      ..:  . ::-:--====++---:-:=::  .  .  .                          .             |
|                           :.    .     . . : .: .:.::-:..:.--:-----::.... .:  .. .         :                            |
|                                         .  .   . .:::. .:..::.:::::::.   ..                                            |
|                                            :...    .:.. . .::....:: :  ..   ... ::                                 .   |
|                                                 .   . ......:-:  .::.: .     ..                                        |
|                                       :   .        . :.  ::.  . .  . :  ...    .:                                      |
|                                                    .               :   ..: .   .    .                                  |
|                                                 .                ..                   .:                               |
|                                                       .      .  ...                                                    |
|                                             .             .  . ..                      ..             ..               |
|                                                             .   .                                ..                    |
|                                                            .                                                           |
|                                               ..         .                                                             |
|                                                                                                                        |
|                                                                                                                        |
```

**Kill Zone Heatmap (Where do they kill?)**

```
|                                                          .                      ..                               .     |
|                                     .                       :                                                     .    |
|                                                                                     ..                                 |
|                 ..                                                                                                     |
|                                                                 :                                                      |
|                                  .      .                                     :                                        |
|                                         .                                     .                                        |
|                    .               .                   . :    .        .   . .        .                                |
|                     .               :.              ..  .  .           .. .. .                                         |
|                                            .      .     ..                                                             |
|                               :       .. .  .   .  .         . ..  .. ..       .:                                      |
|                                 .. .   :.   ::...:..  .  . ::..::.:.. ..   . . .        .:                             |
|                                . . .: .  ..  ::..::::.-::: .-:::  .::...:    .        . .                              |
|                : .              .          :..:.:.:::::--:--:::....::..:.  .:    .:   . .                              |
|                            .         :.       ....--:-=-===@=-=.: ::.. .:           .                                  |
|                          ..            .   :    :.:-:--===+++----:-=::..                                               |
|                       .   :           .   : .:  . :.-....:--:--=:::-:. ..:-              .                             |
|                                                  .:..:  ::.::.:-::..:   .    .   .                                 .   |
|                             . .            ::.    .::..  ..::.:  :.    .   .:   .:                            .    .   |
|                                             .       : .. :..-:.  .:::. .                                               |
|                                       :              .. .:..  ..    .:   .      :                                      |
|                                                             .    ..: .   :..         .                                 |
|                                                  .                :                    .                               |
|                                             .             .     .                       .       .  .                   |
|                                              .                  :                  .  . :        .    ...              |
|                                                            .    :                                ..                    |
|                               .                           ..                                                           |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
```

## Generation Highlights

### Best Improvement

**Generation 7**: Best fitness jumped +606.2 (+69.1%)

- New best fitness: 1483.9

### Worst Regression

**Generation 8**: Best fitness dropped -894.8 (-60.3%)

- New best fitness: 589.1
- _Note: This may be normal variation after a lucky outlier_

### Most Accurate Generation

**Generation 7**: Population accuracy reached 41.5%

### Most Kills (Single Agent)

**Generation 7**: An agent achieved 16 kills

### First Viable Population

**Generation 1**: Average fitness first became positive

### Most Diverse Generation

**Generation 1**: Diversity index 2.03

### Most Converged Generation

**Generation 6**: Diversity index 0.31

## Milestone Timeline

| Generation | Category | Value | Description                     |
| ---------- | -------- | ----- | ------------------------------- |
| 1          | Fitness  | 390   | Best fitness crossed 100        |
| 1          | Kills    | 6.0   | First agent to achieve 1 kills  |
| 1          | Kills    | 6.0   | First agent to achieve 5 kills  |
| 2          | Fitness  | 877   | Best fitness crossed 500        |
| 2          | Kills    | 10.8  | First agent to achieve 10 kills |
| 3          | Fitness  | 1029  | Best fitness crossed 1000       |

## Training Progress by Decile

| Phase   | Gens  | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
| ------- | ----- | -------- | ------- | --------- | ------- | --------- | --------- |
| 0-10%   | 1-2   | 877      | 244     | 3.6       | 28%     | 517       | 217       |
| 10-20%  | 3-4   | 1029     | 558     | 7.1       | 38%     | 743       | 273       |
| 20-30%  | 5-6   | 1065     | 524     | 6.8       | 37%     | 735       | 207       |
| 30-40%  | 7-8   | 1484     | 525     | 6.8       | 40%     | 703       | 253       |
| 40-50%  | 9-10  | 1091     | 525     | 6.8       | 38%     | 716       | 291       |
| 50-60%  | 11-12 | 1078     | 563     | 7.2       | 36%     | 761       | 265       |
| 60-70%  | 13-14 | 1085     | 510     | 6.8       | 37%     | 682       | 246       |
| 70-80%  | 15-16 | 953      | 580     | 7.1       | 39%     | 756       | 273       |
| 80-90%  | 17-18 | 1029     | 600     | 7.4       | 38%     | 747       | 252       |
| 90-100% | 19-22 | 1262     | 553     | 7.1       | 37%     | 718       | 304       |

### Metric Distributions (Last 10 Generations)

Visualizing population consistency: `|---O---|` represents Mean ± 1 StdDev.

- **Narrow bar**: Consistent population (Convergence)
- **Wide bar**: Chaotic/Diverse population

**Accuracy Distribution**

```
Gen  13:      |---------------O---------------|              35.3% ±  4.8%
Gen  14:                 |--------------O---------------|    38.5% ±  4.6%
Gen  15:                     |-----------O------------|      38.8% ±  3.7%
Gen  16:                  |--------------O-------------|     38.6% ±  4.3%
Gen  17:          |-----------------O-----------------|      37.2% ±  5.3%
Gen  18:              |-----------------O-----------------|  38.4% ±  5.5%
Gen  19:      |--------------------O--------------------|    36.9% ±  6.3%
Gen  20:                   |---------O--------|              37.4% ±  2.8%
Gen  21: |-----------------O-----------------|               34.4% ±  5.5%
Gen  22:                         |---------O----------|      39.4% ±  3.1%
```

**Survival Steps Distribution**

```
Gen  13:                     |------O------|                 620.1 ± 155.4
Gen  14:                          |-------O-------|          743.0 ± 173.2
Gen  15:                           |------O------|           739.1 ± 160.3
Gen  16:                         |---------O----------|      772.8 ± 238.2
Gen  17:                              |-----O------|         794.8 ± 148.3
Gen  18:                         |------O------|             698.4 ± 153.3
Gen  19:                       |---------O--------|          712.7 ± 206.8
Gen  20:                      |-------O-------|              652.4 ± 183.2
Gen  21:                      |----------O---------|         718.8 ± 237.0
Gen  22:                           |--------O--------|       789.1 ± 202.3
```

**Kills Distribution**

```
Gen  13:              |---------O----------|                   5.9 ±   2.6
Gen  14:                       |-------O--------|              7.7 ±   2.1
Gen  15:                  |---------O---------|                6.9 ±   2.4
Gen  16:                   |----------O----------|             7.4 ±   2.7
Gen  17:                        |--------O-------|             8.0 ±   2.1
Gen  18:                  |---------O---------|                6.9 ±   2.5
Gen  19:             |--------------O-------------|            6.8 ±   3.6
Gen  20:               |----------O----------|                 6.4 ±   2.7
Gen  21:               |------------O-----------|              6.8 ±   3.0
Gen  22:                        |----------O----------|        8.6 ±   2.7
```

**Fitness Distribution**

```
Gen  13:        |----------O-----------|                     409.6 ± 251.8
Gen  14:                  |----------O----------|            611.2 ± 241.2
Gen  15:               |----------O-----------|              558.9 ± 251.8
Gen  16:               |------------O-------------|          601.0 ± 293.3
Gen  17:                   |----------O----------|           647.3 ± 237.1
Gen  18:              |-----------O-----------|              552.6 ± 266.1
Gen  19:        |---------------O---------------|            511.8 ± 352.9
Gen  20:          |-----------O------------|                 474.8 ± 263.4
Gen  21:          |--------------O-------------|             524.8 ± 317.3
Gen  22:                    |------------O------------|      700.8 ± 282.3
```

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 1.02 (up from 0.70 in Phase 1)
- **Shots per Kill:** 6.05 (down from 7.23 in Phase 1)
- **Kill Conversion Rate:** 16.5% (up from 13.8% in Phase 1)
- **Average Kills per Episode:** 7.7

### Efficiency Trend

| Phase   | Kills/100 Steps | Shots/Kill | Conversion Rate |
| ------- | --------------- | ---------- | --------------- |
| Phase 1 | 0.85            | 6.47       | 15.4%           |
| Phase 2 | 0.95            | 6.23       | 16.0%           |
| Phase 3 | 0.95            | 6.27       | 15.9%           |
| Phase 4 | 0.97            | 6.17       | 16.2%           |
| Phase 5 | 0.99            | 6.14       | 16.3%           |

**Assessment:** Agent shows slight efficiency improvement. Shots per kill dropped 16%.

## Learning Velocity

### Velocity by Phase

| Phase   | Fitness Delta | Delta/Gen | Velocity | Trend          |
| ------- | ------------- | --------- | -------- | -------------- |
| Phase 1 | +481          | +120.2    | Fast     |                |
| Phase 2 | -476          | -119.0    | Stalled  | ↓ Slowing      |
| Phase 3 | -278          | -69.5     | Stalled  | ↑ Accelerating |
| Phase 4 | -53           | -13.2     | Stalled  | ↑ Accelerating |
| Phase 5 | +289          | +48.1     | Fast     | ↑ Accelerating |

### Current Velocity

- **Recent Improvement Rate:** +48.1 fitness/generation
- **Acceleration:** -12.1 (learning slowing down)
- **Projected Generations to +50% Fitness:** ~13 generations

### Velocity Assessment

Learning is progressing at a moderate pace. Consider if further training is worthwhile.

## Reward Component Evolution

| Component               | Phase 1 | Mid    | Final  | Trend     | Status    |
| ----------------------- | ------- | ------ | ------ | --------- | --------- |
| DistanceBasedKillReward | +227.4  | +457.9 | +488.8 | ↑↑↑ +115% | Learned   |
| ConservingAmmoBonus     | +111.2  | +227.6 | +242.0 | ↑↑↑ +118% | Learned   |
| DeathPenalty            | -145.5  | -135.0 | -132.0 | → +9%     | Improving |
| ExplorationBonus        | +26.9   | +9.7   | +10.4  | ↓↓ -61%   | Stable    |
| VelocitySurvivalBonus   | +24.2   | +3.1   | +3.5   | ↓↓ -85%   | Stable    |

**Exploration Efficiency (Final Phase):** 0.0138 score/step

- _Note: A higher rate indicates faster map traversal, independent of survival time._

## Reward Balance Analysis

### Warnings

- **DeathPenalty consistently negative** - This component has been negative throughout training, averaging -132.0/episode. The intended behavior may not be incentivized strongly enough, or there may be a conflict with other rewards.

- **DistanceBasedKillReward is dominant (59%)** - This component accounts for a large portion of positive reward. Consider if this is intentional.

- **VelocitySurvivalBonus declining** - This component dropped from 24.2 to 3.5. The agent may be trading off this behavior for others.

- **ExplorationBonus declining** - This component dropped from 26.9 to 10.4. The agent may be trading off this behavior for others.

### Confirmations

- **Reward reasonably balanced** - No single component >60%
- **VelocitySurvivalBonus positive** - Agents are learning to stay alive
- **Penalty ratio healthy** - Negative rewards are not overwhelming positive

### Recommendations

- Consider increasing the magnitude of consistently negative reward components
- Check if there are conflicting incentives preventing the behavior
- Review if other behaviors need stronger incentives
- Consider reducing the dominant component or boosting others

## Population Health Dashboard

### Current Status: 🟢 Healthy

| Metric            | Value  | Trend (Recent) | Status  |
| ----------------- | ------ | -------------- | ------- |
| Diversity Index   | 0.49   | ↑ Increasing   | 🟢 Good |
| Elite Gap         | 0.90   | →              | 🟢 Good |
| Min Fitness Trend | +39.4  | ↑              | 🟢 Good |
| Max Fitness Trend | +142.4 | ↑              | 🟢 Good |
| IQR (p75-p25)     | 386    | ↑ 31           | 🟢      |

## Stagnation Analysis

- **Current Stagnation:** 15 generations
- **Average Stagnation Period:** 5.7 generations
- **Longest Stagnation:** 15 generations
- **Number of Stagnation Periods:** 3

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Accuracy | Ratio | Grade | Cause of Death     |
| --- | ------------ | --------- | -------- | ----- | ----- | ------------------ |
| 12  | 813          | 200       | 6.5%     | 0.25  | F     | asteroid_collision |
| 13  | 1006         | 3         | 4.2%     | 0.00  | F     | asteroid_collision |
| 14  | 1085         | 619       | 18.4%    | 0.57  | C     | asteroid_collision |
| 15  | 932          | 280       | 11.1%    | 0.30  | D     | asteroid_collision |
| 16  | 953          | -66       | 0.0%     | -0.07 | F     | asteroid_collision |
| 17  | 974          | 2256      | 25.0%    | 2.32  | A     | completed_episode  |
| 18  | 1029         | -38       | 6.2%     | -0.04 | F     | asteroid_collision |
| 19  | 1250         | 204       | 13.8%    | 0.16  | F     | asteroid_collision |
| 20  | 1025         | 169       | 14.3%    | 0.16  | F     | asteroid_collision |
| 21  | 1123         | 823       | 15.5%    | 0.73  | B     | asteroid_collision |

### Generalization Summary

- **Average Fitness Ratio:** 0.77
- **Best Ratio:** 3.15
- **Worst Ratio:** 0.00

**Grade Distribution:** A:4 B:2 C:2 D:1 F:12

## Correlation Analysis

### Fitness Correlations

| Metric         | Correlation | Strength |
| -------------- | ----------- | -------- |
| Kills          | +0.99       | Strong   |
| Steps Survived | +0.96       | Strong   |
| Accuracy       | +0.85       | Strong   |

### Interpretation

Fitness is most strongly predicted by kills (r=0.99).

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 754 steps (50.3% of max)
- **Max Survival:** 1187 steps

### Survival Progression

| Phase   | Mean Steps | Change |
| ------- | ---------- | ------ |
| Phase 1 | 630        |        |
| Phase 2 | 719        | +89    |
| Phase 3 | 738        | +19    |
| Phase 4 | 719        | -19    |
| Phase 5 | 728        | +9     |

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 7.13
- **Avg Steps Survived:** 724
- **Avg Accuracy:** 37.5%
- **Max Kills (Any Agent Ever):** 16.4
- **Max Steps (Any Agent Ever):** 1275.2

## Learning Progress

**Comparing First 2 vs Last 2 Generations:**

| Metric       | Early | Late   | Change  |
| ------------ | ----- | ------ | ------- |
| Best Fitness | 633.3 | 1192.8 | +88.4%  |
| Avg Fitness  | 244.3 | 612.8  | +150.9% |

**Verdict:** Strong learning - both best and average fitness improved significantly.

## Neural & Behavioral Complexity

| Gen | Saturation | Entropy | Control Style      |
| --- | ---------- | ------- | ------------------ |
| 1   | 33.3%      | 2.01    | Balanced / Chaotic |
| 2   | 38.9%      | 1.92    | Balanced           |
| 3   | 46.3%      | 1.47    | Balanced           |
| 4   | 46.8%      | 1.38    | Balanced           |
| 5   | 46.6%      | 1.43    | Balanced           |
| 6   | 46.3%      | 1.48    | Balanced           |
| 7   | 45.4%      | 1.51    | Balanced           |
| 8   | 46.3%      | 1.44    | Balanced           |
| 9   | 44.7%      | 1.51    | Balanced           |
| 10  | 45.8%      | 1.43    | Balanced           |
| 11  | 43.9%      | 1.50    | Balanced           |
| 12  | 45.3%      | 1.45    | Balanced           |
| 13  | 42.1%      | 1.63    | Balanced           |
| 14  | 44.1%      | 1.50    | Balanced           |
| 15  | 45.6%      | 1.51    | Balanced           |
| 16  | 44.5%      | 1.55    | Balanced           |
| 17  | 47.2%      | 1.28    | Balanced           |
| 18  | 48.9%      | 1.22    | Balanced           |
| 19  | 47.0%      | 1.28    | Balanced           |
| 20  | 45.7%      | 1.31    | Balanced           |
| 21  | 50.1%      | 1.17    | Balanced           |
| 22  | 50.0%      | 1.23    | Balanced           |

**Metrics Explanation:**

- **Saturation**: % of time neurons are stuck at hard limits (0 or 1). High (>80%) means binary control; Low means analog control.
- **Entropy**: Measure of input unpredictability. Low = simple loops; High = random/complex.

## Risk Profile Analysis

Analysis of how close agents let asteroids get before reacting or killing them.

| Gen | Avg Min Dist | Fitness | Kills | Archetype |
| --- | ------------ | ------- | ----- | --------- |
| 1   | 15.1px       | 73.5    | 1.8   | Victim    |
| 2   | 15.2px       | 415.0   | 5.5   | Victim    |
| 3   | 15.4px       | 556.4   | 7.2   | Daredevil |
| 4   | 16.0px       | 560.3   | 7.0   | Daredevil |
| 5   | 16.6px       | 457.5   | 6.2   | Victim    |
| 6   | 15.4px       | 590.5   | 7.5   | Daredevil |
| 7   | 15.9px       | 627.8   | 7.7   | Daredevil |
| 8   | 16.5px       | 421.4   | 5.8   | Victim    |
| 9   | 15.6px       | 516.8   | 6.8   | Daredevil |
| 10  | 15.6px       | 532.5   | 6.7   | Daredevil |
| 11  | 15.9px       | 572.2   | 7.3   | Daredevil |
| 12  | 15.6px       | 554.3   | 7.2   | Daredevil |
| 13  | 15.5px       | 409.6   | 5.9   | Victim    |
| 14  | 15.2px       | 611.2   | 7.7   | Daredevil |
| 15  | 16.0px       | 558.9   | 6.9   | Daredevil |
| 16  | 15.2px       | 601.0   | 7.4   | Daredevil |
| 17  | 16.8px       | 647.3   | 8.0   | Daredevil |
| 18  | 16.5px       | 552.6   | 6.9   | Daredevil |
| 19  | 15.8px       | 511.8   | 6.8   | Daredevil |
| 20  | 14.8px       | 474.8   | 6.4   | Victim    |
| 21  | 16.1px       | 524.8   | 6.8   | Daredevil |
| 22  | 15.3px       | 700.8   | 8.6   | Daredevil |

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 266.62
- Average Range (Best-Min): 870.31
- Diversity Change: +11.1%
- **Status:** Population is converging (low diversity)

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Safe Dist | Max Kills |
| ------ | --------- | --------- | ------------ | --------- | --------- |
| Q1     | 5.55      | 639       | 33.5%        | 173.9px   | 12.2      |
| Q2     | 6.91      | 726       | 38.7%        | 162.2px   | 16.4      |
| Q3     | 7.00      | 725       | 37.1%        | 163.8px   | 12.6      |
| Q4     | 7.25      | 734       | 37.5%        | 163.6px   | 14.6      |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
| ------ | -------- | ------ | ------- | ----------------- |
| Q1     | 6.5%     | 93.0%  | 79.1%   | **Spinner**       |
| Q2     | 1.0%     | 97.5%  | 86.2%   | **Spinner**       |
| Q3     | 1.3%     | 97.2%  | 87.6%   | **Spinner**       |
| Q4     | 1.4%     | 97.2%  | 91.6%   | **Spinner**       |

### Input Control Style

| Period | Thrust Dur | Turn Dur | Shoot Dur | Idle Rate | Wraps |
| ------ | ---------- | -------- | --------- | --------- | ----- |
| Q1     | 0.0f       | 0.0f     | 0.0f      | 2.1%      | 0.5   |
| Q2     | 0.0f       | 0.0f     | 0.0f      | 0.2%      | 0.0   |
| Q3     | 0.0f       | 0.0f     | 0.0f      | 0.3%      | 0.0   |
| Q4     | 0.0f       | 0.0f     | 0.0f      | 0.1%      | 0.0   |

### Intra-Episode Score Breakdown

Analysis of when agents earn their reward during an episode (Early vs Late game).

| Quarter            | Avg Score | Share of Total | Play Style |
| ------------------ | --------- | -------------- | ---------- |
| Start (0-25%)      | 87.2      | 12.4%          | Balanced   |
| Mid-Game (25-50%)  | 178.3     | 25.5%          | Balanced   |
| Late-Game (50-75%) | 254.9     | 36.4%          | Balanced   |
| End-Game (75-100%) | 180.3     | 25.7%          | Balanced   |

## Recent Generations (Last 30)

<details>
<summary>Click to expand Recent Generations table</summary>

| Gen | Best | Avg | StdDev | Kills | Steps | Acc% | Stag |
| --- | ---- | --- | ------ | ----- | ----- | ---- | ---- |
| 1   | 390  | 74  | 149    | 1.8   | 372   | 20   | 0    |
| 2   | 877  | 415 | 285    | 5.5   | 662   | 36   | 0    |
| 3   | 1029 | 556 | 296    | 7.2   | 731   | 39   | 0    |
| 4   | 870  | 560 | 249    | 7.0   | 755   | 38   | 1    |
| 5   | 1065 | 458 | 230    | 6.2   | 677   | 35   | 0    |
| 6   | 878  | 590 | 184    | 7.5   | 793   | 39   | 1    |
| 7   | 1484 | 628 | 374    | 7.7   | 773   | 41   | 0    |
| 8   | 589  | 421 | 133    | 5.8   | 632   | 38   | 1    |
| 9   | 1091 | 517 | 322    | 6.8   | 685   | 38   | 2    |
| 10  | 942  | 532 | 259    | 6.7   | 747   | 38   | 3    |
| 11  | 1078 | 572 | 325    | 7.3   | 757   | 36   | 4    |
| 12  | 813  | 554 | 204    | 7.2   | 764   | 37   | 5    |
| 13  | 1006 | 410 | 252    | 5.9   | 620   | 35   | 6    |
| 14  | 1085 | 611 | 241    | 7.7   | 743   | 38   | 7    |
| 15  | 932  | 559 | 252    | 6.9   | 739   | 39   | 8    |
| 16  | 953  | 601 | 293    | 7.4   | 773   | 39   | 9    |
| 17  | 974  | 647 | 237    | 8.0   | 795   | 37   | 10   |
| 18  | 1029 | 553 | 266    | 6.9   | 698   | 38   | 11   |
| 19  | 1250 | 512 | 353    | 6.8   | 713   | 37   | 12   |
| 20  | 1025 | 475 | 263    | 6.4   | 652   | 37   | 13   |
| 21  | 1123 | 525 | 317    | 6.8   | 719   | 34   | 14   |
| 22  | 1262 | 701 | 282    | 8.6   | 789   | 39   | 15   |

</details>

## Top 10 Best Generations

<details>
<summary>Click to expand Top 10 Best Generations table</summary>

| Rank | Gen | Best | Avg | Kills | Steps | Accuracy |
| ---- | --- | ---- | --- | ----- | ----- | -------- |
| 1    | 7   | 1484 | 628 | 16.4  | 1275  | 48.3     |
| 2    | 22  | 1262 | 701 | 13.6  | 1155  | 42.3     |
| 3    | 19  | 1250 | 512 | 14.6  | 1138  | 43.0     |
| 4    | 21  | 1123 | 525 | 12.2  | 1187  | 46.5     |
| 5    | 9   | 1091 | 517 | 12.8  | 1032  | 42.0     |
| 6    | 14  | 1085 | 611 | 12.2  | 1115  | 41.1     |
| 7    | 11  | 1078 | 572 | 12.6  | 1096  | 43.9     |
| 8    | 5   | 1065 | 458 | 12.2  | 1116  | 43.1     |
| 9    | 3   | 1029 | 556 | 12.2  | 1147  | 43.2     |
| 10   | 18  | 1029 | 553 | 11.4  | 829   | 51.4     |

</details>

## Trend Analysis

| Period | Avg Best | Avg Mean | Avg Min | Improvement |
| ------ | -------- | -------- | ------- | ----------- |
| Q1     | 846.2    | 412.6    | 76.9    |             |
| Q2     | 996.6    | 537.8    | 156.9   | +150.5      |
| Q3     | 982.7    | 541.2    | 135.4   | -13.9       |
| Q4     | 1087.9   | 573.3    | 164.4   | +105.2      |

## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

    1484 |      *
    1385 |
    1286 |
    1187 |                  *  *
    1088 |        *           *
     989 |  * *     * **   * *
     890 |         *    ***
     791 | * * *     *
     693 |                     o
     594 |      o      o oo
     495 |  oo o *oooo  o  oo o
     396 | o  o  o    o      o
     297 |*
     198 |
      99 |
       0 |o
         ----------------------
         Gen 1       Gen 22
```

---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 0.00s

- **Evaluation (Simulation):** 7.25s (0.0%)
- **Evolution (GA Operators):** 0.0036s (0.0%)

| Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
| --------- | ------------- | ------------- | ---------- |
| 1-2       | 5.09s         | 0.0010s       | 0.00s      |
| 3-4       | 7.21s         | 0.0033s       | 0.00s      |
| 5-6       | 7.19s         | 0.0025s       | 0.00s      |
| 7-8       | 7.03s         | 0.0035s       | 0.00s      |
| 9-10      | 7.00s         | 0.0035s       | 0.00s      |
| 11-12     | 7.72s         | 0.0040s       | 0.00s      |
| 13-14     | 6.61s         | 0.0030s       | 0.00s      |
| 15-16     | 7.55s         | 0.0032s       | 0.00s      |
| 17-18     | 7.36s         | 0.0035s       | 0.00s      |
| 19-20     | 6.95s         | 0.0038s       | 0.00s      |
| 21-22     | 7.76s         | 0.0043s       | 0.00s      |

## Genetic Operator Statistics

**Recent Averages (Population: 10)**

- **Crossovers:** 3.4 (34.0%)
- **Mutations:** 10.0 (100.0%)
- **Elites Preserved:** 2.0
