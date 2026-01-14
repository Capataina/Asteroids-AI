# Training Summary Report

**Generated:** 2026-01-13 23:03:28
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
Best Fitness: 300 → 879   [▂▁▅█] +193%
Avg Fitness:  21 → 333   [▁▂▄█] +1516%
Avg Kills:    1.2 → 4.5   [▁▂▄█] +281%
Avg Accuracy: 24% → 25%   [▂▁█▅] +5%
Avg Steps:    374 → 627   [▁▁▂█] +67%
Diversity:    119 → 280   [▂▁▄█] +135%
```

## Training Configuration

```
population_size: 10
num_generations: 500
mutation_probability: 0.05
max_workers: 16
```

## Overall Summary

- **Total Generations:** 4
- **Training Duration:** 0:00:34.492983
- **All-Time Best Fitness:** 878.57
- **Best Generation:** 4
- **Final Best Fitness:** 878.57
- **Final Average Fitness:** 333.19
- **Avg Improvement (Early->Late):** 0.00
- **Stagnation:** 0 generations since improvement

**Generalization (Fresh Game Performance):**
- Avg Generalization Ratio: 0.35
- Best Fresh Fitness: 127.01 (Gen 2)
- Episode Completion Rate: 0.0%

## Best Agent Deep Profile

The most fit agent appeared in **Generation 4** with a fitness of **878.57**.

### Combat Efficiency

- **Total Kills:** 10.2
- **Survival Time:** 14.9 seconds (896.8 steps)
- **Accuracy:** 31.3%
- **Shots per Kill:** 3.1
- **Time per Kill:** 1.47 seconds

### Behavioral Signature

**Classification:** `Dogfighter`

| Action | Rate (per step) | Description |
|--------|-----------------|-------------|
| **Thrust** | 13.6% | Movement frequency |
| **Turn** | 70.3% | Rotation frequency |
| **Shoot** | 72.9% | Trigger discipline |

### Spatial Analytics (Best Agent - Generations 1-4)

**Position Heatmap (Where does it fly?)**
```
|               .      .                  .                  .          .                                                |
|                                     .                 .                           ..                                 . |
|                                                                              .  . .:.                                  |
|          .                  .                    .                     .  .  .  :    .                    .            |
|                                                             .                                   .              .       |
|                                       .         .                    . .                                  .            |
|                                                      .  .                                             .    .           |
|   .                                              .   ..         .                                         -            |
|   .         .                                .        .     .    .                ...          .     .   . .           |
|  .                      .           .                  .-       .              .        .                   . .        |
|                .                            .           .    .                   ::                                    |
|             .    .                   .                   . . .     .    .                                              |
|              .       .                             . .      .                                                          |
|                  .     .          .                       :..   . .               .                                  . |
|                        .                                  .@- .                   .         .                          |
|                        .                    ..             .    .                           .                          |
|       .                        .    .                           .                      .          .       .            |
|  .            .                           .                        .                         ..                        |
|     .                   .                                                              .        .   .            .  .  |
|                        .     ..                                         .                     .    .      .   .      . |
|                       .                 .                                   .                                      .   |
|                                  .                                       :   .                    . .      .       ..  |
|                                                                                            .                   .       |
|                                   .                         . .   .                               .                    |
|                                 .                                ..                                                    |
|.                                                                                                                       |
|                  .         .                                                                                           |
|                                                                 .                                                      |
|           .                                .                                            .                          .   |
|          .                      .                                                                                      |
```

**Kill Zone Heatmap (Where does it kill?)**
```
|                                      -                                -           -                                    |
|                     -                                                            - -                                   |
|                                                                                   - -                   -          -   |
|                                                                          -  -- =-                                      |
|                                                                           -                                            |
|        -                                                              - -                                      --      |
|                                                                                                            =           |
|    -                                                - -                                                   *            |
|                            -                       =   -       -                                      -     -       -  |
|                                 -                      -*     -                                         -              |
|                                                         =         -                                                    |
|                  -                                                                                    -            -   |
|              --                                                     -           -                                      |
|                        -                                         -                  -  -                               |
|                        -                                   @*                              -                           |
|      -             -              -          -                                                - --                     |
|    -              -      -    ----  - -                                                                -  -            |
|-                                                                                                                      -|
|                                  -                                                                                     |
|                             -    -                                                 -           -   -              -  - |
|                                                                                                    -      -        =   |
|                                          -                                -      -                                  *  |
|                                                               -                          -                             |
|                                - -                                                            -   -                    |
|                                                                                                                        |
|                                                                                               -                        |
|                                                                  -                                                     |
|                                           -                                                                            |
|                                                                                                                        |
|-                                                                      -             -                                  |
```

### Spatial Analytics (Population Average - Generations 1-4)

**Position Heatmap (Where do they fly?)**
```
|  .        .  ...  .  ..              .  . ..   .   . .  :  ..         . .. .     .      .  . .      .                . |
|  .        . .  .        . .   .   . .  . .        . . ..     .  .   .   .  ..:.   ..        ..  .         .          ..|
|. . .         .                .  .  ..         .   . ...: .     .          . .  . ...       .  .          .            |
|          ..    . .       .  .            ....    ..    ..  -...  .   ...  .. .  :.   ..                   . .          |
|    .   .            ..   .          .   .   .       .  ..  .. ..  .  . .. .          . .       .. .            . .     |
|                     .    .   .  .   ...     ... .    . . .. .  .    .: .  . ...          .  .. .   . .    ..         . |
|            .     .     .  .  .   .. . . .  .     . : .  ...:....  ..: ...    ...  .  ..  .  .   .     . .  .           |
|  ...         .   . ..   .      .  . .  .  ...    ..  .... .:.  .:. ..  :   .. . .                         :          . |
|  ..     .   .         .               . ..  ...... :. . . .::.  ...     .... ...  ... .     .  .     .   . .  .        |
|. .      ..              .  .        ... .   .     ..  .::  : .... .    . ..    .. .     .             .     . ..       |
| .           .  .   ..       . ..     .. .  .. ... .. .. ...: ...:...     .     ..:.    .      .                      . |
|       .     .    .                  :..  .  .   ...:: :..::-:..  . ..   .  .  ..       .     .   .        .            |
|      .   .   .   .  ...       .           .    .   . .  :::::. .  . .  .   . .                   .                . .. |
|     .         .  .     ..    .   ...    .  ..       .  ..:-=:.  : .   .           .   ..  .        . . .      .   .  . |
|            .    .      .                    ..         . .=@:.:     .     .       ..    .   ....  .  .  ..   .       . |
|.     ..     .         ..   .. .             .. .          .:.   .                           .   .                .     |
|       .  .       .          . .. .  .            ..      .  ..  .           .  . .     ..   ..    .    .  .    .       |
|  ..   .. .    .   .  .      ...      .    .    .      .     .   .  .        .. ..     .   .. ..                    .   |
|     ..   .  .           .       .    .     ..      . .  .  .                       .   . .     ..   .            .  . .|
|     . ..  .      .  .  . ... ..   .           ...           .     .     .           . ..      .... ..  .  .   ..     . |
|   .         ..        ....              . .   . ..    . .          .   .    .            . .        .. . . .       . . |
|  .  .            . ...           .      .     .   ...        .      ..   .   . .     . . ..    .  . .      .     ..... |
| .      .  .       .  . .         .  . .     .         .    .                           .   .        . .        .  .    |
|        .  .       .     .         ..                        . .   .    .                 ..       .         .      .   |
|   .  .  .   .        .        . .  .         .  .  .      .   .  .. .  .                        ..    . ..     .       |
|..    .     . .      .....           .       .  .      .      .                                .  . .   ..        .     |
|.            .    .   .    ..             .     .  .   .  .  ..                         ..           .   .     . .    . |
|    .    .    .             . . .       .   . .       ..         .. .   .  .    .           ....                  .     |
|        .  .  .     .         .           . . .      .   .             .    .  .       ... .    .     . .         . .   |
|..  .   . ...         .          .      . .     ..  .    .   . . .        .   ..          .         .                   |
```

**Kill Zone Heatmap (Where do they kill?)**
```
|.              .   ..                 .  .        .      -    .        .  . :.     . .                                  |
|                     .     .    . .        .    .       :         .            .  . .                  .                |
|                                             .     . .:.             ..  .     ..  . .       .           .          ..  |
|   .       .                       ..     .  .  .  :-     .     .    ..   .  :. :.    .                            . :  |
|   .                    :.  .                .               .     . . .   :                 .           .  . .         |
|      . .   .                         .    .                         . . .   ..  .       ..          ..         ..      |
|         .              .                    .        .       .  .            .                             :       .   |
|    .                              . :    . ..     . . .  ....       .        .                            -        . . |
|         .                  .           ..  : .  . .:   .  ..   .           -                          . .   .       .  |
|         .                       .    .   :        .   ..-     .        .                                .              |
|.   ..                    :  .  .         .  :        .  : :.      .                              .   .                 |
|                  ...         .       .      .. .  . :.. . :..  :                                  ..  .            :   |
|   .          ..     .     .         .                  ..-.. :      .  .  ..    .                      .      .        |
|                        .      .                          .-    ...      .          ..  .                               |
|     .      .   .       .   .          .   . .           . -@-                    .  .      ..                          |
|      ..            .              .        . .. .          : .            .                 . ....                     |
|.   .    .     .   . .    .    ....  . ..     .               : .                      .    ..          .  .            |
|.            .                                          .       .               .                                      .|
|                   .       .      .                         ..                              .                           |
|                             .    .                :                               ...          .   .      .       .  . |
| .                                               .                                                  .      .        :   |
|    .   :          . .     .              .  .    :                 .:     .      .             .               .    -  |
|                 .    .     .                .  .              ..          .           .: .                             |
|         .     .                . .     .        .                          .      .  ..  .    .   .       .            |
|                                                  .                  .                          .       . .             |
|..                          .       .        .  .                         .                    .           .            |
|   .        .           .               .            .            .                           .          :             .|
|    .     .      .                         . .              .                 .                                         |
|        . .                    .        .             .             .          .            .         .      .          |
|.      :       .       .         .        .      .                     . .     :     .    ..     .     .                |
```

## Generation Highlights

Not enough data for generation highlights.

## Milestone Timeline

| Generation | Category | Value | Description |
|------------|----------|-------|-------------|
| 1 | Fitness | 300 | Best fitness crossed 100 |
| 1 | Kills | 3.6 | First agent to achieve 1 kills |
| 3 | Fitness | 632 | Best fitness crossed 500 |
| 3 | Kills | 8.2 | First agent to achieve 5 kills |
| 4 | Kills | 10.2 | First agent to achieve 10 kills |

## Training Progress by Decile

Not enough data for decile breakdown (need at least 5 generations).

### Metric Distributions (Last 4 Generations)

Visualizing population consistency: `|---O---|` represents Mean ± 1 StdDev.
- **Narrow bar**: Consistent population (Convergence)
- **Wide bar**: Chaotic/Diverse population

**Accuracy Distribution**
```
Gen   1:  |-----------------------O-----------------------|  24.1% ± 11.2%
Gen   2: |-----------------------O-----------------------|   23.6% ± 11.2%
Gen   3:              |----------------O---------------|     26.2% ±  7.5%
Gen   4:            |----------------O----------------|      25.3% ±  7.8%
```

**Survival Steps Distribution**
```
Gen   1:             |-------O------|                        374.1 ± 139.7
Gen   2:              |-----O-----|                          361.1 ± 103.2
Gen   3:               |--------O-------|                    428.7 ± 156.0
Gen   4:                       |----------O-----------|      626.6 ± 211.2
```

**Kills Distribution**
```
Gen   1: |------O------|                                       1.2 ±   1.1
Gen   2:      |----O----|                                      1.7 ±   0.8
Gen   3:     |------------O------------|                       2.8 ±   2.1
Gen   4:          |-----------------O-----------------|        4.5 ±   2.9
```

**Fitness Distribution**
```
Gen   1: |------O-------|                                     20.6 ± 119.3
Gen   2:      |----O----|                                     69.6 ±  77.5
Gen   3:      |-----------O-----------|                      169.4 ± 188.8
Gen   4:          |-----------------O------------------|     333.2 ± 279.7
```

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 0.72 (up from 0.32 in Phase 1)
- **Shots per Kill:** 7.24 (down from 9.75 in Phase 1)
- **Kill Conversion Rate:** 13.8% (up from 10.3% in Phase 1)
- **Average Kills per Episode:** 4.5

### Efficiency Trend

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 | 0.32 | 9.75 | 10.3% |
| Phase 2 | 0.48 | 10.62 | 9.4% |
| Phase 3 | 0.65 | 8.26 | 12.1% |
| Phase 4 | 0.72 | 7.24 | 13.8% |

**Assessment:** Agent has improved efficiency moderately. Shots per kill dropped 26%.

## Learning Velocity

Not enough data for velocity analysis (need at least 10 generations).

## Reward Component Evolution

| Component | Phase 1 | Mid | Final | Trend | Status |
|-----------|---------|-----|-------|-------|--------|
| DistanceBasedKillReward | +71.4 | +179.9 | +299.3 | ↑↑↑ +319% | Learned |
| DeathPenalty | -147.0 | -150.0 | -141.0 | → +4% | Improving |
| ConservingAmmoBonus | +27.1 | +66.6 | +116.3 | ↑↑↑ +329% | Learned |
| ExplorationBonus | +35.0 | +39.6 | +30.4 | ↓ -13% | Stable |
| VelocitySurvivalBonus | +34.0 | +33.3 | +28.2 | ↓ -17% | Stable |

**Exploration Efficiency (Final Phase):** 0.0485 score/step
- *Note: A higher rate indicates faster map traversal, independent of survival time.*

## Reward Balance Analysis

### Warnings

- **DeathPenalty consistently negative** - This component has been negative throughout training, averaging -141.0/episode. The intended behavior may not be incentivized strongly enough, or there may be a conflict with other rewards.

- **DistanceBasedKillReward dominates reward (63%)** - This single component accounts for most of all positive reward. Other behaviors may be under-incentivized.

### Confirmations

- **VelocitySurvivalBonus positive** - Agents are learning to stay alive
- **Penalty ratio healthy** - Negative rewards are not overwhelming positive

### Recommendations

- Consider increasing the magnitude of consistently negative reward components
- Check if there are conflicting incentives preventing the behavior
- Review if other behaviors need stronger incentives
- Consider reducing the dominant component or boosting others

## Population Health Dashboard

Not enough data for population health analysis.

## Stagnation Analysis

- **Current Stagnation:** 0 generations
- **Average Stagnation Period:** 1.0 generations
- **Longest Stagnation:** 1 generations
- **Number of Stagnation Periods:** 1

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Accuracy | Ratio | Grade | Cause of Death |
|-----|--------------|-----------|----------|-------|-------|----------------|
| 1 | 300 | -136 | 0.0% | -0.45 | F | asteroid_collision |
| 2 | 197 | 127 | 3.2% | 0.65 | C | asteroid_collision |
| 3 | 632 | 32 | 11.1% | 0.05 | F | asteroid_collision |

### Generalization Summary

- **Average Fitness Ratio:** 0.35
- **Best Ratio:** 0.65
- **Worst Ratio:** 0.05

**Grade Distribution:** C:1 F:2 

## Correlation Analysis

Not enough data for correlation analysis.

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 627 steps (41.8% of max)
- **Max Survival:** 897 steps

### Survival Progression

| Phase | Mean Steps | Change |
|-------|------------|--------|
| Phase 1 | 374 |  |
| Phase 2 | 361 | -13 |
| Phase 3 | 429 | +68 |
| Phase 4 | 627 | +198 |

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 2.55
- **Avg Steps Survived:** 448
- **Avg Accuracy:** 24.8%
- **Max Kills (Any Agent Ever):** 10.2
- **Max Steps (Any Agent Ever):** 896.8

## Learning Progress

Not enough data for learning analysis.

## Neural & Behavioral Complexity

| Gen | Saturation | Entropy | Control Style |
|-----|------------|---------|---------------|
| 1 |  34.0% |  1.71 | Balanced |
| 2 |  28.9% |  1.94 | Balanced |
| 3 |  22.5% |  2.05 | Balanced / Chaotic |
| 4 |  32.4% |  1.86 | Balanced |

**Metrics Explanation:**
- **Saturation**: % of time neurons are stuck at hard limits (0 or 1). High (>80%) means binary control; Low means analog control.
- **Entropy**: Measure of input unpredictability. Low = simple loops; High = random/complex.

## Risk Profile Analysis

Analysis of how close agents let asteroids get before reacting or killing them.

| Gen | Avg Min Dist | Fitness | Kills | Archetype |
|-----|--------------|---------|-------|-----------|
| 1 |   15.7px |   20.6 |  1.2 | Victim |
| 2 |   15.4px |   69.6 |  1.7 | Victim |
| 3 |   15.2px |  169.4 |  2.8 | Victim |
| 4 |   15.2px |  333.2 |  4.5 | Victim |

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 166.30
- Average Range (Best-Min): 535.58
- Diversity Change: +0.0%
- **Status:** Population is converging (low diversity)

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Safe Dist | Max Kills |
|--------|-----------|-----------|--------------|-----------|----------|
| Q1 | 1.18 | 374 | 24.1% | 193.5px | 3.6 |
| Q2 | 1.72 | 361 | 23.6% | 199.3px | 3.0 |
| Q3 | 2.80 | 429 | 26.2% | 182.2px | 8.2 |
| Q4 | 4.50 | 627 | 25.3% | 166.6px | 10.2 |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
|--------|----------|--------|---------|-------------------|
| Q1 | 45.1% | 91.3% | 36.1% | **Dogfighter** |
| Q2 | 36.7% | 84.3% | 66.8% | **Dogfighter** |
| Q3 | 29.9% | 83.2% | 72.1% | **Dogfighter** |
| Q4 | 13.6% | 70.3% | 72.9% | **Dogfighter** |

### Input Control Style

| Period | Thrust Dur | Turn Dur | Shoot Dur | Idle Rate | Wraps |
|--------|------------|----------|-----------|-----------|-------|
| Q1 | 0.0f | 0.0f | 0.0f | 1.6% | 1.6 |
| Q2 | 0.0f | 0.0f | 0.0f | 0.3% | 1.7 |
| Q3 | 0.0f | 0.0f | 0.0f | 0.5% | 1.6 |
| Q4 | 0.0f | 0.0f | 0.0f | 0.7% | 1.4 |

### Intra-Episode Score Breakdown

Analysis of when agents earn their reward during an episode (Early vs Late game).

| Quarter | Avg Score | Share of Total | Play Style |
|---------|-----------|----------------|------------|
| Start (0-25%) | 33.2 | 10.0% | Balanced |
| Mid-Game (25-50%) | 123.0 | 36.9% | Balanced |
| Late-Game (50-75%) | 128.5 | 38.6% | Balanced |
| End-Game (75-100%) | 48.5 | 14.6% | Balanced |

## Recent Generations (Last 30)

<details>
<summary>Click to expand Recent Generations table</summary>

| Gen   | Best   | Avg    | StdDev | Kills  | Steps  | Acc%   | Stag   |
|-------|--------|--------|--------|--------|--------|--------|--------|
| 1     | 300    | 21     | 119    | 1.2    | 374    | 24     | 0      |
| 2     | 197    | 70     | 78     | 1.7    | 361    | 24     | 1      |
| 3     | 632    | 169    | 189    | 2.8    | 429    | 26     | 0      |
| 4     | 879    | 333    | 280    | 4.5    | 627    | 25     | 0      |

</details>


## Top 10 Best Generations

<details>
<summary>Click to expand Top 10 Best Generations table</summary>

| Rank | Gen   | Best   | Avg    | Kills  | Steps  | Accuracy |
|------|-------|--------|--------|--------|--------|----------|
| 1    | 4     | 879    | 333    | 10.2   | 897    | 31.3     |
| 2    | 3     | 632    | 169    | 8.2    | 676    | 33.8     |
| 3    | 1     | 300    | 21     | 3.6    | 537    | 30.5     |
| 4    | 2     | 197    | 70     | 3.0    | 485    | 21.0     |

</details>


## Trend Analysis

Not enough data for trend analysis.


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

     879 |   *
     820 |    
     761 |    
     703 |    
     644 |    
     586 |  * 
     527 |    
     469 |    
     410 |    
     351 |    
     293 |*  o
     234 |    
     176 | *  
     117 |  o 
      59 | o  
       0 |o   
         ----
         Gen 1Gen 4
```


---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 0.00s
- **Evaluation (Simulation):** 4.66s (0.0%)
- **Evolution (GA Operators):** 0.0022s (0.0%)

| Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
|-----------|---------------|---------------|------------|
| 1-1 | 3.49s | 0.0000s | 0.00s |
| 2-2 | 3.82s | 0.0020s | 0.00s |
| 3-3 | 4.47s | 0.0035s | 0.00s |
| 4-4 | 6.88s | 0.0035s | 0.00s |

## Genetic Operator Statistics

**Recent Averages (Population: 10)**
- **Crossovers:** 1.8 (17.5%)
- **Mutations:** 7.5 (75.0%)
- **Elites Preserved:** 1.5

