# Training Summary Report

**Generated:** 2026-01-13 22:31:37
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
Best Fitness: 522 → 1300   [▁▅▅▅▅▆▅▅▅█] +149%
Avg Fitness:  58 → 767   [▁▆▆▆▆█▆▆▅▆] +1216%
Avg Kills:    1.4 → 9.3   [▁▆▆▆▆█▆▆▅▆] +559%
Avg Accuracy: 26% → 41%   [▁▅▅▆▅█▇▆▅▆] +53%
Avg Steps:    440 → 781   [▁▆▆▆▇█▆▆▅▅] +77%
Diversity:    136 → 244   [▁▃▆▃▅▅▂▄▄█] +79%
```

## Training Configuration

```
population_size: 25
num_generations: 500
mutation_probability: 0.05
max_workers: 16
```

## Overall Summary

- **Total Generations:** 179
- **Training Duration:** 3:30:13.842246
- **All-Time Best Fitness:** 1819.08
- **Best Generation:** 79
- **Final Best Fitness:** 1300.01
- **Final Average Fitness:** 766.55
- **Avg Improvement (Early->Late):** 436.68
- **Stagnation:** 100 generations since improvement

**Generalization (Fresh Game Performance):**
- Avg Generalization Ratio: 0.81
- Best Fresh Fitness: 2976.65 (Gen 90)
- Episode Completion Rate: 11.2%

## Best Agent Deep Profile

The most fit agent appeared in **Generation 79** with a fitness of **1819.08**.

### Combat Efficiency

- **Total Kills:** 20.25
- **Survival Time:** 20.6 seconds (1234.6666666666667 steps)
- **Accuracy:** 51.4%
- **Shots per Kill:** 1.9
- **Time per Kill:** 1.02 seconds

### Behavioral Signature

**Classification:** `Turret`

| Action | Rate (per step) | Description |
|--------|-----------------|-------------|
| **Thrust** | 0.1% | Movement frequency |
| **Turn** | 29.8% | Rotation frequency |
| **Shoot** | 99.1% | Trigger discipline |

### Spatial Analytics (Best Agent - Generations 170-179)

**Position Heatmap (Where does it fly?)**
```
|                                               .      .                                                                 |
|                                  -..                     .                                                             |
|                                 ..  .                                                  .                               |
|                                            .                                                                           |
|                                             .                                                                          |
|                 .                                                                                .                     |
|                       ..                                                                                               |
|                                                         .       .                                                      |
|                                                      .     .   . .                                                     |
|                                            .          .      . . .   :                      .                          |
|                       .       .                       ..:  : . :.    .    ..           .  .                            |
|                                              .  .  :   .:   . .:.  . .           .                                     |
|                                             .. ..  ::....  .. :-..  .  .                                               |
|                                              . .:.::--::-..:: :-...  ..  .                                             |
|                                               ::.. ...-:===@=-:....                                                    |
|                                           . .   .. : :::-====-::.                                                      |
|                              :            .  . . .. -  :::: ::::.:   . :                                               |
|                            .  . .     . . . .   .  ...  ..  .:    . .  .  .         .                                  |
|                                  .     . . .  .   .         .         .                                                |
|                                  .     .       :.     .      .                                                         |
|                                                 ....             .                                                     |
|                                         :       .   .   ..           .         . .                     .               |
|                                      . .                         .            .                                        |
|                                     .            .               :.   .                  .                             |
|                           .       :       . .                                                                          |
|                                            .             :                            .                                |
|                                              .                                                                         |
|                                  .    .                                       .                                        |
|                                                 ..                                                                     |
|                                  .   .                                                                                 |
```

**Kill Zone Heatmap (Where does it kill?)**
```
|                  .  .             .         .         .... .         .                                               . |
|    .               ..    . ....  - .....                  ..                     .            .      .  .   .   .      |
|.         .           ..          :  .: .            : .   .          .     .           . .     .             .         |
|           ..                    . . .   .  .         ...              .          .       ..                   .  .     |
|               .  .. . .                   . .          .     ..       .                   ..       .                   |
|                 ..                 . .      .   . ..      . .    .    .        .      ..  .      .                  .. |
|              .       ....             ...    ..   .   ... . .. .     .        .:         ..     .                .     |
|                     .    ...             . .   ..    .  .. .   ..   .   .     .    .      . .                          |
|       .                      . .        .       : . ...  . : .  ...     .    .           .        .                    |
|              ...  .                       ..   ..  .      .  : : :   :.    .    ..          .. ..                      |
|       :          .   .  .     .  .       .:.:   . . .  :-. ....... . :.   : .          ..  .  .                        |
|    .     .                ... .  .           ..... :....-  :-..-. ....    .  . ..-     . .                             |
|      .                       .     . .      ..:-. .-::.:.. .-::-:..:  .. . .   .   ... .                               |
|:.                   ..  ..      .           .. -: .:--.:=..:: .- -..:..      ...           .                           |
|                   . .   .  . .      .       ..::...:..::=+=@+--:::..                   ..:  .   .                   . .|
|               .      .  .         . ..    :..  . .:.:--.======-:. .                . . . ..  .                .    .   |
|     .                   . . .-.         .... .. . ..=.:.-:-...-:.:: ...-                      .                        |
|            ..         .    :  ..   .:   :.. .  .. ..:....:  -... ....   ....        ..               .           .     |
|      .          .     .  .     . : .  ..:.. .... .: .   .    .       .  . ..  .      .                  .              |
|  .                          ..     .  :. .    .-:. .. .. .    .     ..         ...   .                     .           |
|                                ..    . .    .  .:....  . ..  . . : .   .      . .  ..                           .      |
|                           .            .:.   . .:.. ...  :... . .  ....     . .::..:     .   .   .      .              |
|                         .     ..  .:...:: . .  .  ..    . .. . ...   .   .    :.       .  ..                           |
|.                     ..             ..  .  ...   .  .    . .   : :.: .. .   .  .  .      .                             |
| .            .           ..:.     :       : .      ..    .           . ...  . . .     .                   ..    .      |
| . .     : .               .      ....   .....    .     . -..          .    ..    .  . ..  . ..       . .               |
|      ..  .                                .. .      .    .   .   .  .  ..  .      .  . .  .  . ...                     |
|                          .          . .    ..    ::  ..       .      .       .      . . .  .      ..                   |
|         .                               .       :. . . ..              .  .   .       :        .                       |
|             .            .      .           .  .    . ...         .                                    ..              |
```

### Spatial Analytics (Population Average - Generations 170-179)

**Position Heatmap (Where do they fly?)**
```
|    ...   ..  .... . ..  . ... .... .. ... ..  ......... ...:.. .... ..... . . ..   . . . . . .  .      .. .        ..  |
|..      . .... . . ..   . ...... .:........ .. .. ......  ....... ..  ....... . . ..  . .. .   .     ..  .. .           |
|. .   .   ....  . ...    . .  ...:..... . .. ...... . .. ...... .  . ...........  . . ....  . .. ... . . .   .     .    |
| .   . . . ..   . .  . . ...  ........... .:...................:....... .. ... . ... .  . ... ..  .     ..   ...        |
|  .  . . ..   . ....... . .. ... ..... ......:... ....::.......:....  .....:. . . ...    ... .           .   .  ..      |
|    ...... .... .. ....  .. ... .......:.........:.:..........:  ........:... ....  . ...... ... ... . ...           ...|
| .    .   .  . . ..  ..:......... .:..... :..::...:....:.:....... :...:.. ........  . . . ..  ....        . . ..      . |
|......  ... ...   .  . .. ...  ........::.::::.......::.:.:..:.... ......:....:...... .....  .. . .             . . ....|
|..       .     ..  .. ....... ......::..:.:::::::::::::.:..:::..:..:.:..:.. .......::..:....  .... ..... .   . ...     .|
|  .. ... ....... .......................:..::::.:::.:::::::::::.:::::::.:........:::........ ........ ..   .    .     ..|
|     .. ..... .   .... ...... .. ::..::::.::::::-::-::--:-::::::::.::::::.:.:....:.::: ....: .  . . .. .. .     ..   ...|
|. .    . .   .  ....   ........:..:....::::::::::::--------:-:-:::::::::::..:.:..::.:. .. ... . .     .  . ..    . .  ..|
| .  . . .... ...   .  ....... .. ......::..::::::------=------:----:::::::::.....::...........  ...  .. . ...   . .. .. |
|...  .      . . .... .:. .. ............::::::::------========---:--:::::::::..:........... ... .... .  ...    .    . ..|
| .  .  . .. .. ......... ............::::.::.::::-:---===++*@+==-----:::::..:.:.................. .  ...   . ..   ..  ..|
|  .. . .  .  . .. ..... .......:.:.....:::::::::-:-----===++++===---:-:::::::::.::... ....... .....    . .  ... .  . . .|
| .  .   ...  . ....   . ...::.::..:.::::.::::.::::------===-===------::-:::.:..:.:.:....... ... . ...  .  .  . ..   . ..|
|. .. ...     . .. ..  .... :: ...:::::::.:::::::::::-------:--------:-::::.:.::........ .. . .. .         .  ..  .     .|
|  .        . . . .   ... . ............::..:.::::::::::::::-:-:--:-:::.:::..::...::. . ... . ...... .. ..    .  .... .  |
|   .. .  .    . ..  ... ............:...:.::::::::.:::::::::::::::::::.:::.:.....:. .... .... .....   .     .  ....     |
|.     ....  .... .:... ........:..........:..::..:.:::::.:::::::.::::::.:::.:.::......... ......  . ...  . .. .  .  .   |
|.     . ..  ... ..   .. .. ..::..... :..::::.:...:..:::: :::::::.:.::::.::........:...... .. .  . ..  ... . ..   .    . |
|  .. . .. . .. ...... . .. ...:.......:.:.:.....:..:..:..:.::::::.::::....::...:...:.. . ....... .       .  .  ...      |
|  ... . .    ..  .  ... .. .....  ...: .. ..........:.:::....:....:.:.::.:.:..:.........  .. .  .. ..        . .. .     |
|.... .    .     .. ...  .  ... .. .:.:........:..:........ ... .........::..:....:  ... .  . .....   . .    .. . .    ..|
|. ........  . . .. .     .... ... .....  .........::.................... .. .. . ..   ... .... ... ........  .       . .|
|  . . .   . .   ..... .   .. ... ......  ... ..... .:......:... .................. ...... .... .   . ..    . ...  .     |
|          .  ...  . .... .. . .. ... . ...:....::.....  ............... . ....... . ..... .... .  ..  .  ... .  . ... . |
|.  .  .  .. . .    . .  . . ...    ..... ... .:...........   .:.. ... .  .. ..  . ... .. .      .   .            .  .   |
|    .  . ..      ... ......... . ...... .  .... ....:.... .. .. .....  ...... .  .  ...  . . . .   .. .    ..           |
```

**Kill Zone Heatmap (Where do they kill?)**
```
|.   ...  ...    . .  ..  . :...  ...... .   .. .. ... .. . .....  .......  ... .   ...  .   ...  .    . ..  . .    ..   |
|. ...  .  . .  .... . .  ... .... :......  .   ....... :...:.   . .:... ..:...... . ..  . . .. .  . ....... .    .   .. |
|. .   .. .   . .. :.. ..  ..  ...:.. .:..... .... ...:... ...  ... .....   ..... ..  ... ... ..  ...  ..  .   ..       .|
|           ..  .  :.  .   :  ......:...:....:.. .:......:. . . .. ..: . ...:..:.  .  .    .. ... ..  .         .    .   |
| .. . ....  .......... :........... . .. . :...... .............. . . . .. :. .......  .. ... .. .. ..     .  .         |
| ..  . .. ..     ... ..  ...:........:.:..:. ..:::.::..:.:....:........ .:. .......... ..     .....        .         ...|
|...  ... . . .... .  ...:...  .. .. ..:.:..:.::.:.::. :::... :..... ..:....:......  ... ........... .  . .        ..   .|
|.....  ... ...       . ........ ......:..:.:::: :....:::::.....::.. .....:....::.: .. ... :.... ... . .      ...  ......|
|..  . .  .  .   ...... ....:  . ....::.:::..::::::::::::..::-.:.:...::: .. .....:..::..:.  ..  .   ..... .   ...  .   ..|
|...  .:. .: ......     ...........:::::::.:::::.::::::::::::::-:::::::::::::.....::::..... . ........      .    .       |
|..   ... .....    . ......  ..:..:..::::::-::--::::-::--:--::-::-::.::::::.:......::::... ......   ... ...    .  .   ...|
|         . . ..   ..  ........ : :::...:.::-::::--:-----------:---::::::::..:::..::::: .: .. ..  ... ...... ..   . .    |
|     .. . ..     ........ .. .........:::.:.::-:------==-=----:---:-:.:::.::....::::.:......... .... .  .. ...  . . ... |
|... ..  ..  . .......... .. .:..:.:... ..:.:::::--:-==========--------:--::::::....:..... ..:.   ..:. ...... . . . .  ..|
| ...      ...  .. .. .......::.....::::.:::::-::------===+**@+===------:::::.:::. :.:...........:.....  . .  ..     ... |
|  . . . .    . ..  ...:. .. ..........::::::::::--:--====+++*+===------::::.:.::.::.:.... ..... ... .    .    ..  .   . |
| .. ....  ....  .      ....::.:.::::::.::::-::::::------=-=======----::--::.::.:.::.....:.. .... ..   .           . ....|
|.     .. . ... .   . . ... ::..:::::::::.:.:::::--:--------------------.::.:.:.. . .... ... . ...... .       .      ..  |
|.. .. .   . ... ..   . .... ::.:..:..:.:::::::-::::-:::--:---:-:-:-:::::.::.::::.::  ..............    .   .. .    ..  .|
| ..  . .. .. .. . .... . :..... . .....:::::::::::::::::.::::::::-::-:::::::..::.:...:. .:..... ... .  .  ..... . ..   .|
| .  ....     ...... .... . . ..:........:::::::..:.::..:.:::.::::::::-:.:::::.::..: .:. ........   ..... ...   .      . |
| .   .. .   :.  .   ...  ... :::.. .....::.:.....::::::::.:::::::::..::.::.:......:..:.. ..: .... ... .  . .            |
|. .:  ....  . ..  ... . .....:......::::.:.:........:....:..::-...::.:. :......:...... .  .. .:  ..    .       ..:      |
|..  ..:.     . ... . ..... . ... ....:.:.::..:: ...::...: . ::..:.:.::::::::.:..:.... .  ... .   ..  .   . ......       |
|  ... .    .     .....  . .... ....:.:.:.  : :. ...:.:::... ....  ...:.:::...:....  ..  .  ...  .     .  . ...   .  .. .|
|.....    .      .. .  ...........  .:......:.:..:.:...:.:.:.......:. . ::.. ..    . . ...... ..   .  .....   ...    ..  |
|    .  . ..  . .......   ... . . .. . :.   ....:: ....: ............... ...:.:. ....::... ..  .  ......      ..   .   . |
|. .    .      .......:.. ....   . .. ...  . .. :...:.:.. ... ...... .......:...  .:....:...... . . ..   .   ... . ..  . |
|..       .   ... .       ... ..   ........... . ...:. .. . ...:.. ::. . .. ... .. .... . ..    ... . .. .  .          . |
|.    ... :.... . ...   ..... ..:......  ... ... . ...... ...... .... .. .. ... :...  ... . ..       ... ..  .. .        |
```

## Generation Highlights

### Best Improvement

**Generation 169**: Best fitness jumped +507.1 (+43.1%)
- New best fitness: 1684.3

### Worst Regression

**Generation 103**: Best fitness dropped -460.9 (-27.9%)
- New best fitness: 1189.9
- *Note: This may be normal variation after a lucky outlier*

### Most Accurate Generation

**Generation 87**: Population accuracy reached 50.7%

### Most Kills (Single Agent)

**Generation 79**: An agent achieved 20 kills

### First Viable Population

**Generation 1**: Average fitness first became positive

### Most Diverse Generation

**Generation 1**: Diversity index 2.34

### Most Converged Generation

**Generation 95**: Diversity index 0.13

## Milestone Timeline

| Generation | Category | Value | Description |
|------------|----------|-------|-------------|
| 1 | Fitness | 522 | Best fitness crossed 100 |
| 1 | Fitness | 522 | Best fitness crossed 500 |
| 1 | Kills | 6.166666666666667 | First agent to achieve 1 kills |
| 1 | Kills | 6.166666666666667 | First agent to achieve 5 kills |
| 5 | Kills | 10.666666666666666 | First agent to achieve 10 kills |
| 8 | Fitness | 1184 | Best fitness crossed 1000 |
| 79 | Kills | 20.25 | First agent to achieve 20 kills |

## Training Progress by Decile

| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|------|----------|---------|-----------|---------|-----------|----------|
| 0-10% | 1-17 | 1207 | 471 | 6.1 | 34% | 668 | 206 |
| 10-20% | 18-34 | 1556 | 757 | 9.4 | 41% | 770 | 217 |
| 20-30% | 35-51 | 1536 | 822 | 10.0 | 44% | 786 | 210 |
| 30-40% | 52-68 | 1381 | 785 | 9.7 | 43% | 767 | 224 |
| 40-50% | 69-85 | 1819 | 890 | 10.7 | 46% | 795 | 255 |
| 50-60% | 86-102 | 1651 | 966 | 11.5 | 49% | 819 | 222 |
| 60-70% | 103-119 | 1601 | 862 | 10.4 | 46% | 781 | 240 |
| 70-80% | 120-136 | 1649 | 789 | 9.6 | 44% | 754 | 240 |
| 80-90% | 137-153 | 1599 | 835 | 10.1 | 44% | 760 | 245 |
| 90-100% | 154-179 | 1684 | 805 | 9.8 | 43% | 747 | 244 |

### Metric Distributions (Last 10 Generations)

Visualizing population consistency: `|---O---|` represents Mean ± 1 StdDev.
- **Narrow bar**: Consistent population (Convergence)
- **Wide bar**: Chaotic/Diverse population

**Accuracy Distribution**
```
Gen 170:          |-------------------O-------------------|  43.7% ±  6.9%
Gen 171:             |-----------------O-----------------|   44.2% ±  6.2%
Gen 172:                   |------------O-----------|        44.4% ±  4.3%
Gen 173:              |--------------O-------------|         43.3% ±  5.0%
Gen 174:                 |---------------O---------------|   44.7% ±  5.6%
Gen 175:                 |--------------O--------------|     44.5% ±  5.2%
Gen 176:                 |----------------O---------------|  45.1% ±  5.7%
Gen 177:                     |-------------O--------------|  45.6% ±  4.9%
Gen 178:       |--------------------O--------------------|   43.0% ±  7.2%
Gen 179: |-------------------O-------------------|           40.6% ±  7.0%
```

**Survival Steps Distribution**
```
Gen 170:                               |-----O------|        752.8 ± 133.6
Gen 171:                              |-------O-------|      766.9 ± 158.1
Gen 172:                               |------O-----|        754.4 ± 128.2
Gen 173:                              |-----O----|           715.6 ± 116.7
Gen 174:                              |------O------|        741.7 ± 140.2
Gen 175:                             |------O-----|          713.9 ± 136.7
Gen 176:                                 |----O----|         764.9 ±  96.4
Gen 177:                                |-----O-----|        763.5 ± 126.0
Gen 178:                                 |-----O-----|       783.6 ± 122.7
Gen 179:                                |------O------|      780.7 ± 142.0
```

**Kills Distribution**
```
Gen 170:                          |--------O---------|        10.1 ±   2.8
Gen 171:                          |---------O---------|       10.2 ±   2.9
Gen 172:                            |-------O-------|         10.2 ±   2.3
Gen 173:                           |------O-----|              9.5 ±   1.9
Gen 174:                         |---------O---------|         9.9 ±   2.9
Gen 175:                      |---------O----------|           9.1 ±   2.9
Gen 176:                              |-----O-----|           10.2 ±   1.8
Gen 177:                           |--------O--------|        10.3 ±   2.6
Gen 178:                           |--------O-------|         10.1 ±   2.4
Gen 179:                        |--------O--------|            9.3 ±   2.5
```

**Fitness Distribution**
```
Gen 170:                      |----------O----------|        824.9 ± 275.4
Gen 171:                       |----------O-----------|      849.4 ± 294.7
Gen 172:                         |--------O--------|         846.1 ± 221.4
Gen 173:                        |-------O------|             784.2 ± 189.7
Gen 174:                      |----------O----------|        817.0 ± 286.1
Gen 175:                   |----------O-----------|          746.3 ± 286.1
Gen 176:                          |-------O-------|          843.3 ± 189.7
Gen 177:                        |----------O---------|       857.0 ± 270.5
Gen 178:                         |--------O--------|         844.2 ± 235.8
Gen 179:                     |---------O---------|           766.6 ± 244.3
```

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 1.31 (up from 0.92 in Phase 1)
- **Shots per Kill:** 4.77 (down from 6.25 in Phase 1)
- **Kill Conversion Rate:** 21.0% (up from 16.0% in Phase 1)
- **Average Kills per Episode:** 9.7

### Efficiency Trend

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 | 1.08 | 5.57 | 17.9% |
| Phase 2 | 1.27 | 4.91 | 20.4% |
| Phase 3 | 1.38 | 4.54 | 22.0% |
| Phase 4 | 1.31 | 4.76 | 21.0% |
| Phase 5 | 1.32 | 4.74 | 21.1% |

**Assessment:** Agent has improved efficiency moderately. Shots per kill dropped 24%.

## Learning Velocity

### Velocity by Phase

| Phase | Fitness Delta | Delta/Gen | Velocity | Trend |
|-------|---------------|-----------|----------|-------|
| Phase 1 | +710 | +20.3 | Fast |  |
| Phase 2 | -182 | -5.2 | Stalled | ↓ Slowing |
| Phase 3 | -148 | -4.2 | Stalled | ↑ Accelerating |
| Phase 4 | +305 | +8.7 | Moderate | ↑ Accelerating |
| Phase 5 | -18 | -0.5 | Stalled | ↓ Slowing |

### Current Velocity

- **Recent Improvement Rate:** -0.5 fitness/generation
- **Acceleration:** -6.2 (learning slowing down)
- **Projected Generations to +50% Fitness:** N/A (not improving)

### Velocity Assessment

Learning has stalled. Fitness is no longer improving. Consider:
- Stopping training (may have converged)
- Restarting with different hyperparameters
- Reviewing reward structure

## Reward Component Evolution

| Component | Phase 1 | Mid | Final | Trend | Status |
|-----------|---------|-----|-------|-------|--------|
| DistanceBasedKillReward | +388.0 | +721.7 | +611.8 | ↑↑ +58% | Learned |
| ConservingAmmoBonus | +186.1 | +376.5 | +297.2 | ↑↑ +60% | Learned |
| DeathPenalty | -140.6 | -133.9 | -138.7 | → +1% | Improving |
| ExplorationBonus | +20.4 | +6.2 | +17.6 | ↓ -14% | Stable |
| VelocitySurvivalBonus | +16.8 | +0.1 | +10.4 | ↓ -38% | Stable |

**Exploration Efficiency (Final Phase):** 0.0235 score/step
- *Note: A higher rate indicates faster map traversal, independent of survival time.*

## Reward Balance Analysis

### Warnings

- **DeathPenalty consistently negative** - This component has been negative throughout training, averaging -138.7/episode. The intended behavior may not be incentivized strongly enough, or there may be a conflict with other rewards.

- **DistanceBasedKillReward dominates reward (68%)** - This single component accounts for most of all positive reward. Other behaviors may be under-incentivized.

### Confirmations

- **VelocitySurvivalBonus positive** - Agents are learning to stay alive
- **Penalty ratio healthy** - Negative rewards are not overwhelming positive

### Recommendations

- Consider increasing the magnitude of consistently negative reward components
- Check if there are conflicting incentives preventing the behavior
- Review if other behaviors need stronger incentives
- Consider reducing the dominant component or boosting others

## Population Health Dashboard

### Current Status: 🔴 Warning

| Metric | Value | Trend (Recent) | Status |
|--------|-------|----------------|--------|
| Diversity Index | 0.30 | ↑ Increasing | 🟢 Good |
| Elite Gap | 0.64 | → | 🟢 Good |
| Min Fitness Trend | +310.5 | ↑ | 🟢 Good |
| Max Fitness Trend | +488.0 | ↑ | 🟢 Good |
| IQR (p75-p25) | 323 | ↑ 69 | 🟢 |

### Warnings

- ⚠️ High stagnation (100 gens) - population stuck

## Stagnation Analysis

- **Current Stagnation:** 100 generations
- **Average Stagnation Period:** 18.7 generations
- **Longest Stagnation:** 100 generations
- **Number of Stagnation Periods:** 9

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Accuracy | Ratio | Grade | Cause of Death |
|-----|--------------|-----------|----------|-------|-------|----------------|
| 169 | 1684 | 1790 | 23.2% | 1.06 | A | asteroid_collision |
| 170 | 1422 | 589 | 16.7% | 0.41 | D | asteroid_collision |
| 171 | 1492 | 1356 | 22.5% | 0.91 | A | asteroid_collision |
| 172 | 1393 | 279 | 18.5% | 0.20 | F | asteroid_collision |
| 173 | 1073 | -106 | 6.2% | -0.10 | F | asteroid_collision |
| 174 | 1524 | -151 | 0.0% | -0.10 | F | asteroid_collision |
| 175 | 1273 | 922 | 19.0% | 0.72 | B | asteroid_collision |
| 176 | 1333 | 2173 | 24.5% | 1.63 | A | completed_episode |
| 177 | 1399 | 201 | 16.7% | 0.14 | F | asteroid_collision |
| 178 | 1231 | 1916 | 30.6% | 1.56 | A | asteroid_collision |

### Generalization Summary

- **Average Fitness Ratio:** 0.81
- **Best Ratio:** 2.36
- **Worst Ratio:** 0.00

**Grade Distribution:** A:61 B:14 C:17 D:24 F:62 

## Correlation Analysis

### Fitness Correlations

| Metric | Correlation | Strength |
|--------|-------------|----------|
| Kills | +1.00 | Strong |
| Steps Survived | +0.94 | Strong |
| Accuracy | +0.93 | Strong |

### Interpretation

Fitness is most strongly predicted by kills (r=1.00).

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 747 steps (49.8% of max)
- **Max Survival:** 1118 steps

### Survival Progression

| Phase | Mean Steps | Change |
|-------|------------|--------|
| Phase 1 | 721 |  |
| Phase 2 | 777 | +56 |
| Phase 3 | 804 | +28 |
| Phase 4 | 767 | -38 |
| Phase 5 | 752 | -15 |

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 9.88
- **Avg Steps Survived:** 754
- **Avg Accuracy:** 43.9%
- **Max Kills (Any Agent Ever):** 20.25
- **Max Steps (Any Agent Ever):** 1234.6666666666667

## Learning Progress

**Comparing First 17 vs Last 17 Generations:**

| Metric | Early | Late | Change |
|--------|-------|------|--------|
| Best Fitness | 934.1 | 1334.3 | +42.8% |
| Avg Fitness | 470.6 | 798.4 | +69.7% |

**Verdict:** Moderate learning - some improvement but room for more training.

## Neural & Behavioral Complexity

| Gen | Saturation | Entropy | Control Style |
|-----|------------|---------|---------------|
| 150 |  83.7% |  1.30 | Bang-Bang (Binary) |
| 151 |  82.9% |  1.33 | Bang-Bang (Binary) |
| 152 |  84.3% |  1.25 | Bang-Bang (Binary) |
| 153 |  81.1% |  1.36 | Bang-Bang (Binary) |
| 154 |  79.9% |  1.45 | Balanced |
| 155 |  86.7% |  1.15 | Bang-Bang (Binary) |
| 156 |  86.8% |  1.13 | Bang-Bang (Binary) |
| 157 |  87.1% |  0.99 | Bang-Bang (Binary) |
| 158 |  87.6% |  0.97 | Bang-Bang (Binary) |
| 159 |  85.8% |  1.10 | Bang-Bang (Binary) |
| 160 |  87.9% |  0.89 | Bang-Bang (Binary) |
| 161 |  86.1% |  1.07 | Bang-Bang (Binary) |
| 162 |  87.1% |  0.96 | Bang-Bang (Binary) |
| 163 |  88.0% |  0.88 | Bang-Bang (Binary) |
| 164 |  87.1% |  1.03 | Bang-Bang (Binary) |
| 165 |  87.3% |  1.06 | Bang-Bang (Binary) |
| 166 |  86.5% |  1.09 | Bang-Bang (Binary) |
| 167 |  86.6% |  1.09 | Bang-Bang (Binary) |
| 168 |  84.9% |  1.20 | Bang-Bang (Binary) |
| 169 |  85.5% |  1.26 | Bang-Bang (Binary) |
| 170 |  83.2% |  1.42 | Bang-Bang (Binary) |
| 171 |  84.1% |  1.53 | Bang-Bang (Binary) |
| 172 |  82.0% |  1.64 | Bang-Bang (Binary) |
| 173 |  82.1% |  1.58 | Bang-Bang (Binary) |
| 174 |  82.1% |  1.57 | Bang-Bang (Binary) |
| 175 |  83.1% |  1.58 | Bang-Bang (Binary) |
| 176 |  82.9% |  1.54 | Bang-Bang (Binary) |
| 177 |  83.8% |  1.45 | Bang-Bang (Binary) |
| 178 |  83.9% |  1.41 | Bang-Bang (Binary) |
| 179 |  79.7% |  1.59 | Balanced |

**Metrics Explanation:**
- **Saturation**: % of time neurons are stuck at hard limits (0 or 1). High (>80%) means binary control; Low means analog control.
- **Entropy**: Measure of input unpredictability. Low = simple loops; High = random/complex.

## Risk Profile Analysis

Analysis of how close agents let asteroids get before reacting or killing them.

| Gen | Avg Min Dist | Fitness | Kills | Archetype |
|-----|--------------|---------|-------|-----------|
| 150 |   15.6px |  900.7 | 10.8 | Daredevil |
| 151 |   15.4px |  899.3 | 10.7 | Daredevil |
| 152 |   15.4px |  895.9 | 10.7 | Daredevil |
| 153 |   14.8px |  887.4 | 10.7 | Daredevil |
| 154 |   15.1px |  813.9 |  9.8 | Daredevil |
| 155 |   14.8px |  860.4 | 10.3 | Daredevil |
| 156 |   15.1px |  938.6 | 11.1 | Daredevil |
| 157 |   14.9px |  792.4 |  9.6 | Daredevil |
| 158 |   15.0px |  772.4 |  9.6 | Daredevil |
| 159 |   15.1px |  779.3 |  9.5 | Daredevil |
| 160 |   15.2px |  848.3 | 10.3 | Daredevil |
| 161 |   15.1px |  760.0 |  9.2 | Daredevil |
| 162 |   14.9px |  802.8 |  9.8 | Daredevil |
| 163 |   15.2px |  800.7 |  9.9 | Daredevil |
| 164 |   15.1px |  774.1 |  9.5 | Daredevil |
| 165 |   14.8px |  755.8 |  9.3 | Daredevil |
| 166 |   15.1px |  762.8 |  9.6 | Daredevil |
| 167 |   15.1px |  749.6 |  9.4 | Daredevil |
| 168 |   15.2px |  722.7 |  9.0 | Daredevil |
| 169 |   15.0px |  828.1 | 10.2 | Daredevil |
| 170 |   15.1px |  824.9 | 10.1 | Daredevil |
| 171 |   15.2px |  849.4 | 10.2 | Daredevil |
| 172 |   14.7px |  846.1 | 10.2 | Daredevil |
| 173 |   14.3px |  784.2 |  9.5 | Daredevil |
| 174 |   15.3px |  817.0 |  9.9 | Daredevil |
| 175 |   14.6px |  746.3 |  9.1 | Daredevil |
| 176 |   15.2px |  843.3 | 10.2 | Daredevil |
| 177 |   15.2px |  857.0 | 10.3 | Daredevil |
| 178 |   15.8px |  844.2 | 10.1 | Daredevil |
| 179 |   15.2px |  766.6 |  9.3 | Daredevil |

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 242.36
- Average Range (Best-Min): 1013.49
- Diversity Change: +25.7%
- **Status:** Population is converging (low diversity)

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Safe Dist | Max Kills |
|--------|-----------|-----------|--------------|-----------|----------|
| Q1 | 8.29 | 736 | 39.2% | 161.4px | 16.75 |
| Q2 | 10.27 | 783 | 44.5% | 158.0px | 20.25 |
| Q3 | 10.50 | 784 | 46.1% | 158.1px | 18.5 |
| Q4 | 9.91 | 753 | 43.7% | 160.0px | 18.666666666666668 |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
|--------|----------|--------|---------|-------------------|
| Q1 | 4.5% | 51.1% | 93.4% | **Spinner** |
| Q2 | 0.1% | 36.5% | 97.4% | **Spinner** |
| Q3 | 0.8% | 39.8% | 96.4% | **Spinner** |
| Q4 | 3.6% | 33.9% | 96.5% | **Spinner** |

### Input Control Style

| Period | Thrust Dur | Turn Dur | Shoot Dur | Idle Rate | Wraps |
|--------|------------|----------|-----------|-----------|-------|
| Q1 | 0.0f | 0.0f | 0.0f | 3.3% | 0.2 |
| Q2 | 0.0f | 0.0f | 0.0f | 2.2% | 0.0 |
| Q3 | 0.0f | 0.0f | 0.0f | 2.0% | 0.0 |
| Q4 | 0.0f | 0.0f | 0.0f | 1.7% | 0.2 |

### Intra-Episode Score Breakdown

Analysis of when agents earn their reward during an episode (Early vs Late game).

| Quarter | Avg Score | Share of Total | Play Style |
|---------|-----------|----------------|------------|
| Start (0-25%) | 94.0 | 12.3% | Balanced |
| Mid-Game (25-50%) | 221.8 | 28.9% | Balanced |
| Late-Game (50-75%) | 260.5 | 34.0% | Balanced |
| End-Game (75-100%) | 190.3 | 24.8% | Balanced |

## Recent Generations (Last 30)

<details>
<summary>Click to expand Recent Generations table</summary>

| Gen   | Best   | Avg    | StdDev | Kills  | Steps  | Acc%   | Stag   |
|-------|--------|--------|--------|--------|--------|--------|--------|
| 150   | 1236   | 901    | 199    | 10.8   | 802    | 45     | 71     |
| 151   | 1572   | 899    | 300    | 10.7   | 810    | 44     | 72     |
| 152   | 1310   | 896    | 251    | 10.7   | 786    | 45     | 73     |
| 153   | 1338   | 887    | 208    | 10.7   | 771    | 46     | 74     |
| 154   | 1580   | 814    | 295    | 9.8    | 721    | 44     | 75     |
| 155   | 1386   | 860    | 249    | 10.3   | 760    | 45     | 76     |
| 156   | 1478   | 939    | 232    | 11.1   | 796    | 47     | 77     |
| 157   | 1402   | 792    | 195    | 9.6    | 730    | 44     | 78     |
| 158   | 1474   | 772    | 294    | 9.6    | 717    | 43     | 79     |
| 159   | 1390   | 779    | 232    | 9.5    | 759    | 42     | 80     |
| 160   | 1186   | 848    | 216    | 10.3   | 779    | 42     | 81     |
| 161   | 1351   | 760    | 231    | 9.2    | 725    | 43     | 82     |
| 162   | 1218   | 803    | 227    | 9.8    | 737    | 43     | 83     |
| 163   | 1445   | 801    | 275    | 9.9    | 755    | 42     | 84     |
| 164   | 1158   | 774    | 211    | 9.5    | 728    | 44     | 85     |
| 165   | 1227   | 756    | 246    | 9.3    | 728    | 43     | 86     |
| 166   | 1199   | 763    | 224    | 9.6    | 746    | 42     | 87     |
| 167   | 1352   | 750    | 192    | 9.4    | 734    | 40     | 88     |
| 168   | 1177   | 723    | 236    | 9.0    | 705    | 41     | 89     |
| 169   | 1684   | 828    | 294    | 10.2   | 764    | 43     | 90     |
| 170   | 1422   | 825    | 275    | 10.1   | 753    | 44     | 91     |
| 171   | 1492   | 849    | 295    | 10.2   | 767    | 44     | 92     |
| 172   | 1393   | 846    | 221    | 10.2   | 754    | 44     | 93     |
| 173   | 1073   | 784    | 190    | 9.5    | 716    | 43     | 94     |
| 174   | 1524   | 817    | 286    | 9.9    | 742    | 45     | 95     |
| 175   | 1273   | 746    | 286    | 9.1    | 714    | 45     | 96     |
| 176   | 1333   | 843    | 190    | 10.2   | 765    | 45     | 97     |
| 177   | 1399   | 857    | 271    | 10.3   | 763    | 46     | 98     |
| 178   | 1231   | 844    | 236    | 10.1   | 784    | 43     | 99     |
| 179   | 1300   | 767    | 244    | 9.3    | 781    | 41     | 100    |

</details>


## Top 10 Best Generations

<details>
<summary>Click to expand Top 10 Best Generations table</summary>

| Rank | Gen   | Best   | Avg    | Kills  | Steps  | Accuracy |
|------|-------|--------|--------|--------|--------|----------|
| 1    | 79    | 1819   | 977    | 20.2   | 1235   | 51.4     |
| 2    | 169   | 1684   | 828    | 18.7   | 1112   | 55.1     |
| 3    | 84    | 1679   | 968    | 18.2   | 1176   | 55.7     |
| 4    | 102   | 1651   | 960    | 18.4   | 1075   | 56.1     |
| 5    | 129   | 1649   | 795    | 18.5   | 1090   | 56.0     |
| 6    | 77    | 1629   | 1000   | 18.2   | 1022   | 59.7     |
| 7    | 73    | 1624   | 856    | 18.1   | 1070   | 58.4     |
| 8    | 116   | 1601   | 911    | 18.2   | 1002   | 60.4     |
| 9    | 146   | 1599   | 858    | 17.8   | 1127   | 48.2     |
| 10   | 142   | 1594   | 833    | 17.8   | 969    | 57.8     |

</details>


## Trend Analysis

| Period | Avg Best | Avg Mean | Avg Min | Improvement |
|--------|----------|----------|---------|-------------|
| Q1 | 1119.6 | 664.3 | 258.5 |  |
| Q2 | 1331.1 | 842.1 | 412.8 | +211.5 |
| Q3 | 1370.2 | 870.3 | 412.5 | +39.1 |
| Q4 | 1349.5 | 816.2 | 350.0 | -20.7 |


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

    1819 |                          *                                 
    1698 |                                                            
    1577 |                        *                      *   *    *   
    1455 |         *                   * **   *   *         *         
    1334 |      *    *    *      * *    *  *   *** * * *      * *  *  
    1213 |        *     *   *  **    **      *          *  *        **
    1091 |    *  *    *    *  *             *       * *   *    * *    
     970 |          *  * *   *      o   o                             
     849 |  ** *     o oo         o  ooo ooooooo o          o         
     728 | *    o o o o  ooooooooo o            o oo o ooooo ooooooooo
     606 |       o o                                o o               
     485 |* oooo                                                      
     364 |                                                            
     243 | o                                                          
     121 |                                                            
       0 |o                                                           
         ------------------------------------------------------------
         Gen 1                                             Gen 179
```


---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 0.00s
- **Evaluation (Simulation):** 54.54s (0.0%)
- **Evolution (GA Operators):** 0.0177s (0.0%)

| Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
|-----------|---------------|---------------|------------|
| 1-17 | 51.71s | 0.0136s | 0.00s |
| 18-34 | 56.83s | 0.0140s | 0.00s |
| 35-51 | 57.36s | 0.0147s | 0.00s |
| 52-68 | 59.51s | 0.0176s | 0.00s |
| 69-85 | 60.57s | 0.0137s | 0.00s |
| 86-102 | 61.51s | 0.0166s | 0.00s |
| 103-119 | 57.25s | 0.0163s | 0.00s |
| 120-136 | 54.59s | 0.0175s | 0.00s |
| 137-153 | 55.55s | 0.0174s | 0.00s |
| 154-170 | 53.67s | 0.0181s | 0.00s |
| 171-179 | 54.51s | 0.0182s | 0.00s |

## Genetic Operator Statistics

**Recent Averages (Population: 25)**
- **Crossovers:** 8.1 (32.4%)
- **Mutations:** 25.0 (100.0%)
- **Elites Preserved:** 2.0

