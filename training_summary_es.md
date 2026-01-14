# Training Summary Report

**Generated:** 2026-01-14 21:00:21
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
Best Fitness: 687 → 1059   [▃▁▅▆▅▆█▆▆▅] +54%
Avg Fitness:  58 → 522   [▁▁▅▅▅▄▅▆█▅] +795%
Avg Kills:    2.9 → 10.6   [▁▁▅▅▅▄▅▆█▅] +268%
Avg Accuracy: 21% → 46%   [▁▁▅▅▅▆▇▇█▆] +120%
Avg Steps:    553 → 797   [▃▁▇▆▆▃▅▇█▅] +44%
Diversity:    161 → 201   [▃▁▅▅▇▅█▅▆▆] +24%
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

- **Total Generations:** 105
- **Training Duration:** 2:02:17.097641
- **All-Time Best Fitness:** 1626.40
- **Best Generation:** 54
- **Final Best Fitness:** 1058.71
- **Final Average Fitness:** 521.66
- **Avg Improvement (Early->Late):** 404.78
- **Stagnation:** 51 generations since improvement

**Generalization (Fresh Game Performance):**

- Avg Generalization Ratio: 0.61
- Best Fresh Fitness: 1820.63 (Gen 44)
- Episode Completion Rate: 9.6%

## Best Agent Deep Profile

The most fit agent appeared in **Generation 54** with a fitness of **1626.40**.

### Combat Efficiency

- **Total Kills:** 27.666666666666668
- **Survival Time:** 25.0 seconds (1500.0 steps)
- **Accuracy:** 62.1%
- **Shots per Kill:** 1.6
- **Time per Kill:** 0.90 seconds

### Behavioral Signature

**Classification:** `Spinner`

| Action     | Rate (per step) | Description        |
| ---------- | --------------- | ------------------ |
| **Thrust** | 2.8%            | Movement frequency |
| **Turn**   | 36.5%           | Rotation frequency |
| **Shoot**  | 99.5%           | Trigger discipline |

### Spatial Analytics (Best Agent - Generations 96-105)

**Position Heatmap (Where does it fly?)**

```
|                                               .                 .             .             .                          |
|                                                                           .        .     .     .                .      |
|                                                      .                ..                           .                   |
|                                                                        .                                               |
|                                                       .                                      .                       . |
|                            .                                .                                                          |
|                                       .    .             .  .           .                                              |
|  .                   .                 .    .              .             .   .             .                           |
|                         .                .               . .     .    .   .      .. .          .                       |
|                           .                   .: ..      ...  ...      .  .. .                  .  . .. .              |
|                            .             . ..   ....   . .. ..   .             ..                      .               |
|         .                  .        .    .  ..:... ...   ...  .  ..      .     .                                       |
|        . .   .      .             .  . .   .    ..    .. ...     ... .  ..    .             .   .                      |
|                               . . .      ..        .....  .  ... .  .   . .         .                                  |
|                     .               . ... .  .  ..... ..=:=@=:... ...         .           .                            |
|                      .. .          ..    .   ..   .  ..:.--=.:.- .. . .   .. .    .                                    |
|                      .    ..       .         ...  : .   ..::::.  :....            .    ..       .    .   .             |
|                                     .  ... .  ..  .    :. . :. ::.. ..  . ..         .                                 |
|                                ..             . .  .    ... :   ........ . .     .  ... .                              |
|                        ..  .                  .      .      ..  . .  .  .  . .       .              .         .   .    |
|                                        .                      ..  ....  .  .   ..                                      |
|                                      .. .                .... :. .  ...   .      ...            .                  .   |
|                                       .  .           .  . .   ...    .     .  .   .     .                            . |
|                                        .     . .    .          .   . .... .  .      ...                                |
|                                     .                      .  . .                           .                          |
|                           .                                  .              .   .                                      |
|                               .   .                 .    .   . . .   .    .                .    ..  .                  |
|                                        .              .          .                                                     |
|                                                      .   .           .                     .                           |
|                                                                               .  .                                     |
```

**Kill Zone Heatmap (Where does it kill?)**

```
|                                                          .      .            .       .                                 |
|                                                        .                               .  .   .  .                     |
|                                                        .               . :                        .                    |
|                                                                        .      .                                        |
|                                                                                                .                     . |
|                            ..                              ..              .                      .                    |
|.                                                            :.           .                                             |
|                      .                      .  .          .:   .                                                       |
|                        . .             .                .. :        .      . .                                         |
|     .                    .              .   . .:  .  .  . ::.  .       .    .  . . :                 :::.              |
|                            :              . : . .  :.  . - :.  . .  ::        ...  .          .        :               |
|                            . .        .      ::.: ..:.   .-- ..   .     :     .:                   .                   |
|          ::   .     .             :    .  ..     .   ....:..:.    .: .   .    :                                        |
|             .                 ..:.    ...       ..  :: :  :   :: .         . .                                         |
|                     ..              :  .  :.     :: .:::- =@=-.:. .: .     : .      .                                  |
|                  ..  . .                .  .:.:       ..:--+:.-::...  .       .     .                                  |
|                           :   . ..          ..:-  ::    .. -=-:: :- :  : ..:    ..              .  .        .          |
|                                      .  : ..    ..-    -- : : :.-  ..    . .        .   .  .              .            |
|                                 ..   .      . .: .   .  :.-.: ...   :.:  .    .   .  . ..                              |
|                         .     .            .           .    .   .:  .. . .: .:.      .              .                  |
|                                                           ...    ... . ..     .   .       .                       .    |
|                                      :..                 . :  : . . .:. .  : .   :                                 :   |
|                                       .               .  . .    ..:...    .   :.       .                            :  |
|                                               .    .    .      .    .: .:....      :. .:                              .|
|                                             .      .         .. : .     .            ..                                |
|                                    :.          .      ......  . . .       .                                            |
|                                 . .                           .  .     .                      .  .:                    |
|                                                        ..        .    .   .            .        .          .           |
|                                                                              .                                         |
|                                                       .                                     ..                 .       |
```

### Spatial Analytics (Population Average - Generations 96-105)

**Position Heatmap (Where do they fly?)**

```
|                  .   .        ..               .                    .      .  .  .   .                                 |
|                                           .. . .   .    .     ..   .   .   .   .. . .  .                               |
|                                       .                     . .  .     . . . ..     .                                  |
|                       ..              ...     .         . .   .   .  .  . . .   .   .                                  |
|                                .       .   .   . ..     ...     ... .  .           .. . .             .                |
|    .            .       .       ..    .                . ..... ..              .. ... .        .                       |
|                       .         .  .       .   ..  ....... . .... .. ..  . .   .  . . .             .                  |
|                      .. .              .. .... .. .  :.   :  ... ...     .   . ...           .        .                |
|                        .      .    .   .    .  ...   .  ... :...... ....... ...  ...      .    . .      .      .       |
|                           .      . . .  .  : . :.:.. ......:.... . .. . .. .. .   ..  ...    .             .           |
|                  .   ..  ...    .. ..  ...:..... ..:.::......: . ..:... . .   ...  :   .   .                     .     |
|                 ..       . ..  . . .... .::..::.:::.::: ::..:..:.::.:..............  .     ....        ..              |
|          .   .  .   ..  ... .   .. .... .::....::.:::.:::::.::::.-::::::::..::. :....  .  .        .    . .  .         |
|                    .       .. .. ....  .::::..:::::-------------::-::::::.:: :..:. .....     .  .     .     .          |
|          .    .      .  . .   .  .  . .:.....::::::-:--==++@+===---:::::.:.::.:... .. ....  . ..        .           .  |
|.     ..  . .      .  .. .  . .   . .... ..:::::::::----==++*===-----:::::. .:... .       ..... ... .. .   .   . .      |
|     .                      ..   .  ..   . :...:::::::------=---::--::-::....  .:.. ..  . .. .. ...                     |
|       .           .. . .   ...   .. .. ::: ..:::.::::-::---------::..::::-::.:.. ...:.       .  .                 ..   |
|        ..                 .   ...   .... .:....:.:.::::.:-:-::::.::::.:.::. .:..... . . ... .  .     .      .          |
|             .                ..  ..  .. ....:..:::.::::..:.:::::..::::.... ..:.... ....  .   . .   .                   |
|          .      .    .     .  .   ...... ....: ..........:.:......::-. .. ..  ..: .           . .         ..           |
|          .       .  .  .   .      ... ..... ..  . .. .....::..............:.:. .. .      ..     .                      |
|             .                    . .  .    .   . .... ....... .. ....:... . .   .. .    . ...    .                 .   |
|   .  .                           ....  ..    ...  .. :......:.. .:  ::. . . .    . . ..   . . .           .  .         |
|.                                         .   . . ..  ... .     ....... .. ...  ...    .     .  .                       |
|                       .  ..           .    .   . ..  .       ..   . ..... .    . .  .     .       .    .               |
|                   .   .    .           .   .   .  .  .   .. .     ..   .. .   ....     ...   . .                       |
|                   .       . .. .   .  .. .     .  . .   . . .  .  .     .  . .        .  ..                            |
|          .                        ..           .   .      . . . .... .   .                     .                       |
|                                .   .      ..            .   . .    .     .   ..  .            .                        |
```

**Kill Zone Heatmap (Where do they kill?)**

```
|             .              .   ..                .    .    ..     . .     ....   ..                                    |
|      .           .         .    .         ...       ..  .  . . :   .    .       ...           .  .                     |
|                   .  .    .     .       ..  .  .. .         . ..       . .      .      .                               |
|                                    .          ..         .       .      . .  .              .                      .   |
|                      .  .           . .  .      . .     ... . ...     .     .       ... . .  .                         |
|                           .  .         . .     .    .    ..  . ..     . ..   ..... . .       .                         |
|                       ..      .  .         ..   .. ..:: . ..   ...  ..   :  . ... ..  .  .           .                 |
|                                  . .   .  .  . ... :.::.  . .... .: .   . . .. . ..       .          .                 |
|                     .. . .     . . .. ....: . ..:.. : ......::: . . . .:.... :.. .. ... ..      .                .     |
|                          .      .  :  ..::. :.::.....  .:::::.:  ... : ... .. . . .. . .:                      .       |
|.                 .   ..   ..   . .... . . :..:: . .::::....:...:.::. :..:   . .:. ...    .  .                  .   . . |
|      .           .     . ...  .  ..  :. :.:::-::..::::...:::.:.:.::......:.:... :....  .    .. .                       |
|     .    ..     . ..  .. .. .  ..:....:. .:.::.::.::::::::::-::::-:::::--:.:. .  ....  .     .    ..  . .   .          |
|     .          .    . .. ..  .. :. .  .::-:::::::------:-=------:---::::::.:..:.:.. :.:   .                          . |
|.   ..    .       .   .  .     . . ......... ...:::----===++@+===---:-:.::::::.::. .:......  ...   ..         .         |
|      . ..  .      .  .          .. ...:. .:.::-:-:::---==++*+==----:::.::::....:.  .. .   ..: ... ...          ..      |
|     .   ..          ..   .. : .    :  . ....:.:.-::::------===--.::--:::.:.:. .  ....    ..... ...         .    .   .  |
|     .       .  . . : . ..      ......:..:.::::::::--:-::---------::::::::::.::. .  ....     . .           . .     . .  |
|    .   .    .                . .      .. .:...:::::::::.----::----:-::.:.-:::- :::: . ..    .    .      .              |
|       .               .  .    :. ....:..:.:.:.::-.::::::::.::.::::: :::..:. .::.. . ..   .  .  ..        .        .    |
|  .     .        ..  . . .  .      ....  ... ..:: . : :..:..::.::..:::.... ... .... .  ..    ...   .      .  .          |
|            . .   .     ..  .     .: ........ ... ..: : .::.::.......::  . .::  ...  .    .  .   .      .  .  .         |
|                .          .      ......  .  ...  ..::::...: : ...:::.: ..  .     .. .  .            .       .       .  |
|                   .                  ..   . . ... : ... .. .:.  :: . .... .. :     .....   ..        .          .      |
|           .     .   .                       ..  .    . ....    . ..... ...... .....  ..         .           .          |
|                           .     .            . .           ..  . ..... ... .   . ..  .      . .                        |
|.                .           .   ..     .     . .   . .   .   ...  .. .  .    . ...  .    :  .. ..                      |
|.     .               .    : .  .  . .         .      . ..  . ... . .       .  ..     . .      .  .     .               |
|                               . . ...     .   :   .:       .. :   . ...    . .  .                        .             |
|                              . . .    .   .   .   .  .. ....  . . : .   .    .                                         |
```

## Generation Highlights

### Best Improvement

**Generation 74**: Best fitness jumped +625.0 (+69.9%)

- New best fitness: 1518.7

### Worst Regression

**Generation 17**: Best fitness dropped -573.6 (-49.8%)

- New best fitness: 578.7
- _Note: This may be normal variation after a lucky outlier_

### Most Accurate Generation

**Generation 75**: Population accuracy reached 59.5%

### Most Kills (Single Agent)

**Generation 54**: An agent achieved 29 kills

### First Viable Population

**Generation 1**: Average fitness first became positive

### Most Diverse Generation

**Generation 11**: Diversity index 7.52

### Most Converged Generation

**Generation 99**: Diversity index 0.31

## Milestone Timeline

| Generation | Category | Value              | Description                     |
| ---------- | -------- | ------------------ | ------------------------------- |
| 1          | Fitness  | 687                | Best fitness crossed 100        |
| 1          | Fitness  | 687                | Best fitness crossed 500        |
| 1          | Kills    | 13.0               | First agent to achieve 1 kills  |
| 1          | Kills    | 13.0               | First agent to achieve 5 kills  |
| 1          | Kills    | 13.0               | First agent to achieve 10 kills |
| 6          | Fitness  | 1010               | Best fitness crossed 1000       |
| 21         | Kills    | 21.666666666666668 | First agent to achieve 20 kills |

## Training Progress by Decile

| Phase   | Gens   | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
| ------- | ------ | -------- | ------- | --------- | ------- | --------- | --------- |
| 0-10%   | 1-10   | 1010     | 137     | 4.5       | 28%     | 607       | 188       |
| 10-20%  | 11-20  | 1152     | 211     | 6.4       | 31%     | 653       | 163       |
| 20-30%  | 21-30  | 1214     | 376     | 9.2       | 38%     | 802       | 206       |
| 30-40%  | 31-40  | 1183     | 353     | 8.5       | 38%     | 747       | 225       |
| 40-50%  | 41-50  | 1506     | 525     | 11.4      | 45%     | 863       | 256       |
| 50-60%  | 51-60  | 1626     | 592     | 12.5      | 49%     | 833       | 265       |
| 60-70%  | 61-70  | 1499     | 509     | 11.0      | 47%     | 785       | 245       |
| 70-80%  | 71-80  | 1519     | 528     | 11.4      | 48%     | 789       | 260       |
| 80-90%  | 81-90  | 1444     | 459     | 10.2      | 43%     | 762       | 239       |
| 90-100% | 91-105 | 1452     | 520     | 11.2      | 46%     | 803       | 237       |

### Metric Distributions (Last 10 Generations)

Visualizing population consistency: `|---O---|` represents Mean ± 1 StdDev.

- **Narrow bar**: Consistent population (Convergence)
- **Wide bar**: Chaotic/Diverse population

**Accuracy Distribution**

```
Gen  96:                       |---------O---------|         49.5% ±  5.3%
Gen  97:            |---------O---------|                    43.3% ±  5.3%
Gen  98:                        |---------O----------|       49.9% ±  5.6%
Gen  99:                            |--------O---------|     51.5% ±  5.1%
Gen 100:                 |------------O------------|         47.5% ±  6.9%
Gen 101:                          |-----------O-----------|  52.1% ±  6.3%
Gen 102: |----------O----------|                             38.2% ±  6.0%
Gen 103:                     |---------O----------|          48.3% ±  5.5%
Gen 104:      |-----------O----------|                       41.3% ±  6.1%
Gen 105:                 |---------O----------|              46.3% ±  5.6%
```

**Survival Steps Distribution**

```
Gen  96:                             |------O------|         905.5 ± 175.3
Gen  97:                         |--------O-------|          843.2 ± 214.2
Gen  98:                             |------O-------|        904.4 ± 195.7
Gen  99:                                |------O------|      973.0 ± 176.5
Gen 100:                   |--------O-------|                685.9 ± 219.8
Gen 101:                         |-------O-------|           815.3 ± 201.6
Gen 102:                  |-------O------|                   640.7 ± 192.4
Gen 103:                       |--------O--------|           804.2 ± 226.4
Gen 104:                     |-------O--------|              729.9 ± 220.2
Gen 105:                          |-----O-----|              796.8 ± 162.6
```

**Kills Distribution**

```
Gen  96:                       |---------O---------|          13.1 ±   4.1
Gen  97:                   |---------O--------|               11.3 ±   3.9
Gen  98:                        |---------O---------|         13.4 ±   4.0
Gen  99:                           |---------O--------|       14.5 ±   3.8
Gen 100:               |----------O---------|                 10.1 ±   4.3
Gen 101:                      |----------O---------|          12.9 ±   4.3
Gen 102:          |---------O---------|                        7.9 ±   3.9
Gen 103:                  |----------O----------|             11.6 ±   4.3
Gen 104:                |--------O---------|                  10.0 ±   3.8
Gen 105:                   |-------O-------|                  10.6 ±   3.3
```

**Fitness Distribution**

```
Gen  96:                   |----------O-----------|          628.5 ± 232.5
Gen  97:             |----------O----------|                 500.4 ± 231.0
Gen  98:                   |-----------O-----------|         640.2 ± 247.8
Gen  99:                        |----------O----------|      728.1 ± 225.5
Gen 100:         |-----------O------------|                  439.9 ± 255.5
Gen 101:                  |-----------O------------|         624.4 ± 263.7
Gen 102:     |-----------O----------|                        337.9 ± 238.3
Gen 103:               |-----------O------------|            557.1 ± 262.7
Gen 104:          |----------O-----------|                   438.0 ± 233.3
Gen 105:                |--------O---------|                 521.7 ± 200.7
```

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 1.42 (up from 0.74 in Phase 1)
- **Shots per Kill:** 4.42 (down from 6.79 in Phase 1)
- **Kill Conversion Rate:** 22.6% (up from 14.7% in Phase 1)
- **Average Kills per Episode:** 11.5

### Efficiency Trend

| Phase   | Kills/100 Steps | Shots/Kill | Conversion Rate |
| ------- | --------------- | ---------- | --------------- |
| Phase 1 | 0.89            | 6.41       | 15.6%           |
| Phase 2 | 1.15            | 5.46       | 18.3%           |
| Phase 3 | 1.44            | 4.37       | 22.9%           |
| Phase 4 | 1.43            | 4.38       | 22.8%           |
| Phase 5 | 1.34            | 4.69       | 21.3%           |

**Assessment:** Agent has improved efficiency moderately. Shots per kill dropped 35%.

## Learning Velocity

### Velocity by Phase

| Phase   | Fitness Delta | Delta/Gen | Velocity | Trend          |
| ------- | ------------- | --------- | -------- | -------------- |
| Phase 1 | +394          | +18.8     | Moderate |                |
| Phase 2 | +452          | +21.5     | Fast     | ↑ Accelerating |
| Phase 3 | +202          | +9.6      | Moderate | ↓ Slowing      |
| Phase 4 | +466          | +22.2     | Fast     | ↑ Accelerating |
| Phase 5 | +41           | +1.9      | Slow     | ↓ Slowing      |

### Current Velocity

- **Recent Improvement Rate:** +1.9 fitness/generation
- **Acceleration:** -8.9 (learning slowing down)
- **Projected Generations to +50% Fitness:** ~272 generations

### Velocity Assessment

Learning is slow. The population may be approaching a local optimum. Consider:

- Increasing mutation rate to escape plateau
- Adding diversity through fresh random individuals

## Reward Component Evolution

| Component               | Phase 1 | Mid    | Final  | Trend     | Status    |
| ----------------------- | ------- | ------ | ------ | --------- | --------- |
| ConservingAmmoBonus     | +119.7  | +389.8 | +353.3 | ↑↑↑ +195% | Learned   |
| DistanceBasedKillReward | +111.7  | +311.3 | +288.4 | ↑↑↑ +158% | Learned   |
| DeathPenalty            | -142.1  | -131.8 | -133.3 | → +6%     | Improving |
| ExplorationBonus        | +22.8   | +14.5  | +18.5  | ↓ -19%    | Stable    |
| VelocitySurvivalBonus   | +24.7   | +8.4   | +14.7  | ↓ -41%    | Stable    |

**Exploration Efficiency (Final Phase):** 0.0228 score/step

- _Note: A higher rate indicates faster map traversal, independent of survival time._

## Reward Balance Analysis

### Warnings

- **DeathPenalty consistently negative** - This component has been negative throughout training, averaging -133.3/episode. The intended behavior may not be incentivized strongly enough, or there may be a conflict with other rewards.

- **DistanceBasedKillReward is dominant (43%)** - This component accounts for a large portion of positive reward. Consider if this is intentional.

- **ConservingAmmoBonus is dominant (53%)** - This component accounts for a large portion of positive reward. Consider if this is intentional.

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

### Current Status: 🔴 Warning

| Metric            | Value  | Trend (Recent) | Status  |
| ----------------- | ------ | -------------- | ------- |
| Diversity Index   | 0.44   | ↑ Increasing   | 🟢 Good |
| Elite Gap         | 1.28   | →              | 🟢 Good |
| Min Fitness Trend | +220.1 | ↑              | 🟢 Good |
| Max Fitness Trend | +482.4 | ↑              | 🟢 Good |
| IQR (p75-p25)     | 326    | ↑ 89           | 🟢      |

### Warnings

- ⚠️ High stagnation (51 gens) - population stuck

## Stagnation Analysis

- **Current Stagnation:** 51 generations
- **Average Stagnation Period:** 16.2 generations
- **Longest Stagnation:** 51 generations
- **Number of Stagnation Periods:** 6

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Accuracy | Ratio | Grade | Cause of Death     |
| --- | ------------ | --------- | -------- | ----- | ----- | ------------------ |
| 95  | 1255         | 367       | 14.9%    | 0.29  | F     | asteroid_collision |
| 96  | 1226         | 472       | 20.7%    | 0.38  | D     | asteroid_collision |
| 97  | 1189         | 958       | 29.7%    | 0.81  | B     | asteroid_collision |
| 98  | 1230         | 1804      | 33.0%    | 1.47  | A     | completed_episode  |
| 99  | 1329         | 1197      | 21.3%    | 0.90  | A     | completed_episode  |
| 100 | 1378         | -44       | 20.0%    | -0.03 | F     | asteroid_collision |
| 101 | 1452         | 166       | 22.2%    | 0.11  | F     | asteroid_collision |
| 102 | 1189         | 608       | 26.7%    | 0.51  | C     | asteroid_collision |
| 103 | 1318         | 1065      | 21.3%    | 0.81  | B     | asteroid_collision |
| 104 | 1003         | 492       | 20.4%    | 0.49  | D     | asteroid_collision |

### Generalization Summary

- **Average Fitness Ratio:** 0.61
- **Best Ratio:** 1.80
- **Worst Ratio:** 0.02

**Grade Distribution:** A:20 B:10 C:11 D:18 F:45

## Correlation Analysis

### Fitness Correlations

| Metric         | Correlation | Strength |
| -------------- | ----------- | -------- |
| Kills          | +0.99       | Strong   |
| Steps Survived | +0.94       | Strong   |
| Accuracy       | +0.90       | Strong   |

### Interpretation

Fitness is most strongly predicted by kills (r=0.99).

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 810 steps (54.0% of max)
- **Max Survival:** 1476 steps

### Survival Progression

| Phase   | Mean Steps | Change |
| ------- | ---------- | ------ |
| Phase 1 | 645        |        |
| Phase 2 | 779        | +134   |
| Phase 3 | 824        | +45    |
| Phase 4 | 817        | -7     |
| Phase 5 | 765        | -52    |

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 11.54
- **Avg Steps Survived:** 810
- **Avg Accuracy:** 46.8%
- **Max Kills (Any Agent Ever):** 29.333333333333332
- **Max Steps (Any Agent Ever):** 1500.0

## Learning Progress

**Comparing First 10 vs Last 10 Generations:**

| Metric       | Early | Late   | Change  |
| ------------ | ----- | ------ | ------- |
| Best Fitness | 754.8 | 1237.2 | +63.9%  |
| Avg Fitness  | 136.8 | 541.6  | +295.8% |

**Verdict:** Strong learning - both best and average fitness improved significantly.

## Neural & Behavioral Complexity

| Gen | Saturation | Entropy | Control Style   |
| --- | ---------- | ------- | --------------- |
| 76  | 0.0%       | 1.74    | Analog (Smooth) |
| 77  | 0.1%       | 1.76    | Analog (Smooth) |
| 78  | 0.1%       | 1.77    | Analog (Smooth) |
| 79  | 0.1%       | 1.80    | Analog (Smooth) |
| 80  | 0.1%       | 1.64    | Analog (Smooth) |
| 81  | 0.1%       | 1.71    | Analog (Smooth) |
| 82  | 0.3%       | 1.60    | Analog (Smooth) |
| 83  | 0.4%       | 1.54    | Analog (Smooth) |
| 84  | 0.4%       | 1.46    | Analog (Smooth) |
| 85  | 0.4%       | 1.16    | Analog (Smooth) |
| 86  | 0.4%       | 0.90    | Analog (Smooth) |
| 87  | 0.4%       | 1.12    | Analog (Smooth) |
| 88  | 0.4%       | 0.76    | Analog (Smooth) |
| 89  | 0.7%       | 1.27    | Analog (Smooth) |
| 90  | 1.1%       | 1.52    | Analog (Smooth) |
| 91  | 1.1%       | 1.58    | Analog (Smooth) |
| 92  | 1.2%       | 1.40    | Analog (Smooth) |
| 93  | 1.4%       | 1.21    | Analog (Smooth) |
| 94  | 1.4%       | 1.03    | Analog (Smooth) |
| 95  | 1.2%       | 0.90    | Analog (Smooth) |
| 96  | 0.9%       | 0.86    | Analog (Smooth) |
| 97  | 0.6%       | 0.95    | Analog (Smooth) |
| 98  | 0.5%       | 1.03    | Analog (Smooth) |
| 99  | 0.6%       | 1.15    | Analog (Smooth) |
| 100 | 0.4%       | 1.11    | Analog (Smooth) |
| 101 | 0.6%       | 1.29    | Analog (Smooth) |
| 102 | 0.6%       | 1.25    | Analog (Smooth) |
| 103 | 1.0%       | 1.54    | Analog (Smooth) |
| 104 | 0.8%       | 1.50    | Analog (Smooth) |
| 105 | 1.0%       | 1.68    | Analog (Smooth) |

**Metrics Explanation:**

- **Saturation**: % of time neurons are stuck at hard limits (0 or 1). High (>80%) means binary control; Low means analog control.
- **Entropy**: Measure of input unpredictability. Low = simple loops; High = random/complex.

## Risk Profile Analysis

Analysis of how close agents let asteroids get before reacting or killing them.

| Gen | Avg Min Dist | Fitness | Kills | Archetype |
| --- | ------------ | ------- | ----- | --------- |
| 76  | 15.0px       | 478.5   | 11.5  | Victim    |
| 77  | 15.7px       | 703.4   | 13.9  | Daredevil |
| 78  | 14.8px       | 393.6   | 9.1   | Victim    |
| 79  | 14.9px       | 628.1   | 13.1  | Daredevil |
| 80  | 15.0px       | 540.3   | 12.2  | Daredevil |
| 81  | 15.6px       | 771.4   | 16.2  | Daredevil |
| 82  | 14.5px       | 695.1   | 14.1  | Daredevil |
| 83  | 14.9px       | 685.8   | 13.5  | Daredevil |
| 84  | 15.0px       | 451.5   | 10.6  | Victim    |
| 85  | 13.4px       | 370.0   | 8.4   | Victim    |
| 86  | 14.1px       | 148.6   | 5.0   | Victim    |
| 87  | 15.3px       | 458.4   | 10.3  | Victim    |
| 88  | 13.2px       | 91.9    | 3.5   | Victim    |
| 89  | 13.8px       | 428.0   | 9.3   | Victim    |
| 90  | 14.8px       | 490.2   | 11.0  | Victim    |
| 91  | 14.8px       | 508.0   | 10.9  | Daredevil |
| 92  | 14.5px       | 443.5   | 9.9   | Victim    |
| 93  | 15.3px       | 401.1   | 9.1   | Victim    |
| 94  | 14.4px       | 514.5   | 11.5  | Daredevil |
| 95  | 14.6px       | 512.5   | 11.6  | Daredevil |
| 96  | 15.3px       | 628.5   | 13.1  | Daredevil |
| 97  | 16.1px       | 500.4   | 11.3  | Daredevil |
| 98  | 14.7px       | 640.2   | 13.4  | Daredevil |
| 99  | 15.0px       | 728.1   | 14.5  | Daredevil |
| 100 | 14.5px       | 439.9   | 10.1  | Victim    |
| 101 | 14.7px       | 624.4   | 12.9  | Daredevil |
| 102 | 13.9px       | 337.9   | 7.9   | Victim    |
| 103 | 14.4px       | 557.1   | 11.6  | Daredevil |
| 104 | 14.0px       | 438.0   | 10.0  | Victim    |
| 105 | 14.7px       | 521.7   | 10.6  | Daredevil |

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 234.34
- Average Range (Best-Min): 1132.62
- Diversity Change: +27.1%
- **Status:** Population is converging (low diversity)

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Safe Dist | Max Kills          |
| ------ | --------- | --------- | ------------ | --------- | ------------------ |
| Q1     | 6.30      | 670       | 31.4%        | 167.2px   | 21.666666666666668 |
| Q2     | 9.89      | 797       | 41.6%        | 157.4px   | 28.0               |
| Q3     | 11.65     | 807       | 47.8%        | 156.4px   | 29.333333333333332 |
| Q4     | 10.94     | 789       | 45.4%        | 159.0px   | 27.666666666666668 |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
| ------ | -------- | ------ | ------- | ----------------- |
| Q1     | 7.1%     | 72.1%  | 88.9%   | **Spinner**       |
| Q2     | 3.4%     | 53.2%  | 99.4%   | **Spinner**       |
| Q3     | 3.7%     | 56.3%  | 96.8%   | **Spinner**       |
| Q4     | 6.2%     | 44.9%  | 98.7%   | **Spinner**       |

### Input Control Style

| Period | Thrust Dur | Turn Dur | Shoot Dur | Idle Rate | Wraps |
| ------ | ---------- | -------- | --------- | --------- | ----- |
| Q1     | 0.0f       | 0.0f     | 0.0f      | 2.3%      | 0.5   |
| Q2     | 0.0f       | 0.0f     | 0.0f      | 0.2%      | 0.1   |
| Q3     | 0.0f       | 0.0f     | 0.0f      | 0.3%      | 0.2   |
| Q4     | 0.0f       | 0.0f     | 0.0f      | 0.2%      | 0.3   |

### Intra-Episode Score Breakdown

Analysis of when agents earn their reward during an episode (Early vs Late game).

| Quarter            | Avg Score | Share of Total | Play Style |
| ------------------ | --------- | -------------- | ---------- |
| Start (0-25%)      | 97.2      | 18.6%          | Balanced   |
| Mid-Game (25-50%)  | 144.7     | 27.7%          | Balanced   |
| Late-Game (50-75%) | 193.2     | 37.0%          | Balanced   |
| End-Game (75-100%) | 86.5      | 16.6%          | Balanced   |

## Recent Generations (Last 30)

<details>
<summary>Click to expand Recent Generations table</summary>

| Gen | Best | Avg | StdDev | Kills | Steps | Acc% | Stag |
| --- | ---- | --- | ------ | ----- | ----- | ---- | ---- |
| 76  | 1010 | 479 | 265    | 11.5  | 702   | 47   | 22   |
| 77  | 1449 | 703 | 247    | 13.9  | 922   | 55   | 23   |
| 78  | 1276 | 394 | 249    | 9.1   | 622   | 52   | 24   |
| 79  | 1296 | 628 | 272    | 13.1  | 836   | 53   | 25   |
| 80  | 1480 | 540 | 283    | 12.2  | 802   | 48   | 26   |
| 81  | 1298 | 771 | 249    | 16.2  | 1034  | 51   | 27   |
| 82  | 1435 | 695 | 256    | 14.1  | 918   | 54   | 28   |
| 83  | 1409 | 686 | 261    | 13.5  | 910   | 54   | 29   |
| 84  | 1354 | 451 | 250    | 10.6  | 733   | 45   | 30   |
| 85  | 1018 | 370 | 242    | 8.4   | 679   | 42   | 31   |
| 86  | 729  | 149 | 186    | 5.0   | 499   | 34   | 32   |
| 87  | 1130 | 458 | 226    | 10.3  | 880   | 41   | 33   |
| 88  | 605  | 92  | 166    | 3.5   | 403   | 30   | 34   |
| 89  | 1178 | 428 | 279    | 9.3   | 751   | 40   | 35   |
| 90  | 1444 | 490 | 276    | 11.0  | 811   | 42   | 36   |
| 91  | 1045 | 508 | 257    | 10.9  | 793   | 44   | 37   |
| 92  | 1172 | 444 | 217    | 9.9   | 739   | 44   | 38   |
| 93  | 1068 | 401 | 226    | 9.1   | 819   | 38   | 39   |
| 94  | 1312 | 514 | 227    | 11.5  | 831   | 45   | 40   |
| 95  | 1255 | 513 | 235    | 11.6  | 769   | 52   | 41   |
| 96  | 1226 | 629 | 233    | 13.1  | 906   | 49   | 42   |
| 97  | 1189 | 500 | 231    | 11.3  | 843   | 43   | 43   |
| 98  | 1230 | 640 | 248    | 13.4  | 904   | 50   | 44   |
| 99  | 1329 | 728 | 225    | 14.5  | 973   | 51   | 45   |
| 100 | 1378 | 440 | 255    | 10.1  | 686   | 48   | 46   |
| 101 | 1452 | 624 | 264    | 12.9  | 815   | 52   | 47   |
| 102 | 1189 | 338 | 238    | 7.9   | 641   | 38   | 48   |
| 103 | 1318 | 557 | 263    | 11.6  | 804   | 48   | 49   |
| 104 | 1003 | 438 | 233    | 10.0  | 730   | 41   | 50   |
| 105 | 1059 | 522 | 201    | 10.6  | 797   | 46   | 51   |

</details>

## Top 10 Best Generations

<details>
<summary>Click to expand Top 10 Best Generations table</summary>

| Rank | Gen | Best | Avg | Kills | Steps | Accuracy |
| ---- | --- | ---- | --- | ----- | ----- | -------- |
| 1    | 54  | 1626 | 769 | 27.7  | 1500  | 62.1     |
| 2    | 74  | 1519 | 482 | 28.3  | 1500  | 55.3     |
| 3    | 45  | 1506 | 496 | 27.0  | 1500  | 56.7     |
| 4    | 61  | 1499 | 492 | 26.7  | 1383  | 63.3     |
| 5    | 75  | 1497 | 729 | 28.3  | 1293  | 66.8     |
| 6    | 48  | 1485 | 693 | 27.7  | 1489  | 58.5     |
| 7    | 80  | 1480 | 540 | 27.7  | 1500  | 56.0     |
| 8    | 46  | 1455 | 508 | 26.3  | 1500  | 55.0     |
| 9    | 101 | 1452 | 624 | 25.3  | 1364  | 62.5     |
| 10   | 77  | 1449 | 703 | 25.7  | 1499  | 59.1     |

</details>

## Trend Analysis

| Period | Avg Best | Avg Mean | Avg Min | Improvement |
| ------ | -------- | -------- | ------- | ----------- |
| Q1     | 798.9    | 220.3    | -77.3   |             |
| Q2     | 1130.7   | 433.8    | 7.5     | +331.8      |
| Q3     | 1265.7   | 543.9    | 64.5    | +134.9      |
| Q4     | 1207.4   | 502.0    | 51.8    | -58.3       |

## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

    1506 |                      *
    1404 |                        *  *  **     **  *        *
    1303 |                             *  *                * *
    1202 |            *        *   *       *     **      *
    1100 |              **  ***     * *     **       **   *
     999 |          ** *         *                  *  **     *
     898 |   *             *
     797 |         *      *                   *
     695 | *     *                        o    oo o        o
     594 |*   *                   o  ooo     o   o o        o
     493 |  *   * * o  o      o o   o    o  o          o oo  oo
     391 |           oo  o  o  o o      o  o         oo o
     290 |     *   o    o  o o     o          o     o
     189 |    o oo
      87 |   o    o       o
     -14 |ooo  o
         -----------------------------------------------------
         Gen 1                                      Gen 105
```

---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 0.00s

- **Evaluation (Simulation):** 61.09s (0.0%)
- **Evolution (GA Operators):** 0.0000s (0.0%)

| Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
| --------- | ------------- | ------------- | ---------- |
| 1-10      | 41.16s        | 0.0000s       | 0.00s      |
| 11-20     | 46.65s        | 0.0000s       | 0.00s      |
| 21-30     | 58.43s        | 0.0000s       | 0.00s      |
| 31-40     | 54.28s        | 0.0000s       | 0.00s      |
| 41-50     | 63.98s        | 0.0000s       | 0.00s      |
| 51-60     | 62.75s        | 0.0000s       | 0.00s      |
| 61-70     | 58.34s        | 0.0000s       | 0.00s      |
| 71-80     | 59.35s        | 0.0000s       | 0.00s      |
| 81-90     | 56.48s        | 0.0000s       | 0.00s      |
| 91-100    | 61.56s        | 0.0000s       | 0.00s      |
| 101-105   | 56.57s        | 0.0000s       | 0.00s      |
