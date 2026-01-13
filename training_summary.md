# Training Summary Report

**Generated:** 2026-01-12 23:46:35
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
Best Fitness: 426 → 490   [▁▄▂▂▇▆▆█▅▃] +15%
Avg Fitness:  105 → 341   [▁▆▅▆▇▇▇█▆▆] +225%
Avg Kills:    5.8 → 19.2   [▁▆▆▇▇▇▇█▇▇] +233%
Avg Accuracy: 53% → 77%   [▁▆▆▆▇▇▇█▇▇] +44%
Avg Steps:    380 → 666   [▁▆▆▆▇▇▆█▇▇] +75%
Diversity:    114 → 81   [▅█▃▁▄▂▃▄▃▂] -29%
```

## Training Configuration

```
population_size: 25
num_generations: 500
mutation_probability: 0.05
mutation_gaussian_sigma: 0.1
crossover_probability: 0.7
max_workers: 16
frame_delay: 0.016666666666666666
```

## Overall Summary

- **Total Generations:** 35
- **Training Duration:** 0:52:52.679361
- **All-Time Best Fitness:** 618.80
- **Best Generation:** 29
- **Final Best Fitness:** 489.75
- **Final Average Fitness:** 341.50
- **Avg Improvement (Early->Late):** 66.45
- **Stagnation:** 6 generations since improvement

**Generalization (Fresh Game Performance):**
- Avg Generalization Ratio: 0.31
- Best Fresh Fitness: 257.14 (Gen 19)
- Episode Completion Rate: 2.9%

## Best Agent Deep Profile

The most fit agent appeared in **Generation 29** with a fitness of **618.80**.

### Combat Efficiency

- **Total Kills:** 29.8
- **Survival Time:** 16.2 seconds (972.9 steps)
- **Accuracy:** 85.8%
- **Shots per Kill:** 1.1
- **Time per Kill:** 0.54 seconds

### Behavioral Signature

**Classification:** `Spinner`

| Action | Rate (per step) | Description |
|--------|-----------------|-------------|
| **Thrust** | 0.5% | Movement frequency |
| **Turn** | 66.4% | Rotation frequency |
| **Shoot** | 69.7% | Trigger discipline |

### Spatial Analytics (Best Agent)

**Position Heatmap (Where does it fly?)**
```
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                            @                                                           |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
```

**Kill Zone Heatmap (Where does it kill?)**
```
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                            @                                                           |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
```

## Generation Highlights

### Best Improvement

**Generation 29**: Best fitness jumped +140.5 (+29.4%)
- New best fitness: 618.8

### Worst Regression

**Generation 30**: Best fitness dropped -129.3 (-20.9%)
- New best fitness: 489.5
- *Note: This may be normal variation after a lucky outlier*

### Most Accurate Generation

**Generation 22**: Population accuracy reached 79.7%

### Most Kills (Single Agent)

**Generation 22**: An agent achieved 30 kills

### First Viable Population

**Generation 1**: Average fitness first became positive

### Most Diverse Generation

**Generation 1**: Diversity index 1.08

### Most Converged Generation

**Generation 33**: Diversity index 0.14

## Milestone Timeline

| Generation | Category | Value | Description |
|------------|----------|-------|-------------|
| 1 | Fitness | 426 | Best fitness crossed 100 |
| 1 | Kills | 23.1 | First agent to achieve 1 kills |
| 1 | Kills | 23.1 | First agent to achieve 5 kills |
| 1 | Kills | 23.1 | First agent to achieve 10 kills |
| 1 | Kills | 23.1 | First agent to achieve 20 kills |
| 4 | Fitness | 526 | Best fitness crossed 500 |

## Training Progress by Decile

| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|------|----------|---------|-----------|---------|-----------|----------|
| 0-10% | 1-3 | 492 | 193 | 10.5 | 63% | 495 | 125 |
| 10-20% | 4-6 | 582 | 332 | 19.1 | 74% | 672 | 109 |
| 20-30% | 7-9 | 536 | 347 | 19.7 | 75% | 685 | 90 |
| 30-40% | 10-12 | 560 | 342 | 19.0 | 75% | 668 | 85 |
| 40-50% | 13-15 | 603 | 362 | 19.4 | 75% | 676 | 98 |
| 50-60% | 16-18 | 560 | 365 | 20.0 | 78% | 695 | 83 |
| 60-70% | 19-21 | 587 | 358 | 19.5 | 78% | 684 | 95 |
| 70-80% | 22-24 | 602 | 375 | 20.6 | 78% | 710 | 80 |
| 80-90% | 25-27 | 544 | 349 | 19.6 | 78% | 686 | 83 |
| 90-100% | 28-35 | 619 | 365 | 20.2 | 77% | 700 | 76 |

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 2.91 (up from 2.12 in Phase 1)
- **Shots per Kill:** 2.13 (down from 2.47 in Phase 1)
- **Kill Conversion Rate:** 47.0% (up from 40.5% in Phase 1)
- **Average Kills per Episode:** 20.2

### Efficiency Trend

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 | 2.57 | 2.24 | 44.7% |
| Phase 2 | 2.87 | 2.15 | 46.6% |
| Phase 3 | 2.87 | 2.16 | 46.3% |
| Phase 4 | 2.86 | 2.16 | 46.3% |
| Phase 5 | 2.91 | 2.12 | 47.1% |

**Assessment:** Agent shows slight efficiency improvement. Shots per kill dropped 14%.

## Learning Velocity

### Velocity by Phase

| Phase | Fitness Delta | Delta/Gen | Velocity | Trend |
|-------|---------------|-----------|----------|-------|
| Phase 1 | +43 | +6.1 | Moderate |  |
| Phase 2 | -5 | -0.7 | Stalled | ↓ Slowing |
| Phase 3 | -16 | -2.3 | Stalled | ↓ Slowing |
| Phase 4 | -124 | -17.7 | Stalled | ↓ Slowing |
| Phase 5 | -129 | -18.4 | Stalled | ↑ Accelerating |

### Current Velocity

- **Recent Improvement Rate:** -18.4 fitness/generation
- **Acceleration:** -15.6 (learning slowing down)
- **Projected Generations to +50% Fitness:** N/A (not improving)

### Velocity Assessment

Learning has stalled. Fitness is no longer improving. Consider:
- Stopping training (may have converged)
- Restarting with different hyperparameters
- Reviewing reward structure

## Reward Component Evolution

| Component | Phase 1 | Mid | Final | Trend | Status |
|-----------|---------|-----|-------|-------|--------|
| DistanceBasedKillReward | +132.6 | +249.4 | +256.3 | ↑↑ +93% | Learned |
| ConservingAmmoBonus | +113.6 | +225.9 | +227.3 | ↑↑↑ +100% | Learned |
| DeathPenalty | -147.7 | -145.2 | -144.4 | → +2% | Improving |
| ExplorationBonus | +51.1 | +20.2 | +20.3 | ↓↓ -60% | Stable |
| VelocitySurvivalBonus | +43.8 | +8.6 | +8.3 | ↓↓ -81% | Stable |

**Exploration Efficiency (Final Phase):** 0.0292 score/step
- *Note: A higher rate indicates faster map traversal, independent of survival time.*

## Reward Balance Analysis

### Warnings

- **DeathPenalty consistently negative** - This component has been negative throughout training, averaging -144.4/episode. The intended behavior may not be incentivized strongly enough, or there may be a conflict with other rewards.

- **DistanceBasedKillReward is dominant (53%)** - This component accounts for a large portion of positive reward. Consider if this is intentional.

- **ConservingAmmoBonus is dominant (47%)** - This component accounts for a large portion of positive reward. Consider if this is intentional.

- **VelocitySurvivalBonus declining** - This component dropped from 43.8 to 8.3. The agent may be trading off this behavior for others.

- **ExplorationBonus declining** - This component dropped from 51.1 to 20.3. The agent may be trading off this behavior for others.

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
| Diversity Index | 0.21 | ↓ Decreasing | 🟡 Watch |
| Elite Gap | 0.41 | → | 🟡 Watch |
| Min Fitness Trend | +123.2 | ↑ | 🟢 Good |
| Max Fitness Trend | +17.2 | ↑ | 🟢 Good |
| IQR (p75-p25) | 94 | ↓ 47 | 🟢 |

## Stagnation Analysis

- **Current Stagnation:** 6 generations
- **Average Stagnation Period:** 7.0 generations
- **Longest Stagnation:** 13 generations
- **Number of Stagnation Periods:** 4

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Accuracy | Ratio | Grade | Cause of Death |
|-----|--------------|-----------|----------|-------|-------|----------------|
| 25 | 538 | -177 | 0.0% | -0.33 | F | asteroid_collision |
| 26 | 544 | -153 | 4.5% | -0.28 | F | asteroid_collision |
| 27 | 487 | -102 | 13.0% | -0.21 | F | asteroid_collision |
| 28 | 478 | -141 | 11.1% | -0.29 | F | asteroid_collision |
| 29 | 619 | -117 | 7.4% | -0.19 | F | asteroid_collision |
| 30 | 489 | -64 | 20.4% | -0.13 | F | asteroid_collision |
| 31 | 499 | -169 | 7.7% | -0.34 | F | asteroid_collision |
| 32 | 465 | -53 | 11.9% | -0.11 | F | asteroid_collision |
| 33 | 518 | -169 | 0.0% | -0.33 | F | asteroid_collision |
| 34 | 522 | -11 | 19.6% | -0.02 | F | asteroid_collision |

### Generalization Summary

- **Average Fitness Ratio:** 0.31
- **Best Ratio:** 0.45
- **Worst Ratio:** 0.05

**Grade Distribution:** D:3 F:31 

## Correlation Analysis

### Fitness Correlations

| Metric | Correlation | Strength |
|--------|-------------|----------|
| Kills | +0.98 | Strong |
| Steps Survived | +0.96 | Strong |
| Accuracy | +0.90 | Strong |

### Interpretation

Fitness is most strongly predicted by kills (r=0.98).

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 696 steps (46.4% of max)
- **Max Survival:** 836 steps

### Survival Progression

| Phase | Mean Steps | Change |
|-------|------------|--------|
| Phase 1 | 596 |  |
| Phase 2 | 676 | +80 |
| Phase 3 | 689 | +13 |
| Phase 4 | 699 | +10 |
| Phase 5 | 699 | -1 |

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 20.12
- **Avg Steps Survived:** 697
- **Avg Accuracy:** 77.4%
- **Max Kills (Any Agent Ever):** 30.35
- **Max Steps (Any Agent Ever):** 972.9

## Learning Progress

**Comparing First 3 vs Last 3 Generations:**

| Metric | Early | Late | Change |
|--------|-------|------|--------|
| Best Fitness | 463.8 | 510.0 | +9.9% |
| Avg Fitness | 193.3 | 367.8 | +90.3% |

**Verdict:** Moderate learning - some improvement but room for more training.

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 81.67
- Average Range (Best-Min): 339.20
- Diversity Change: -26.5%
- **Status:** Population is converging (low diversity)

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Safe Dist | Max Kills |
|--------|-----------|-----------|--------------|-----------|----------|
| Q1 | 15.96 | 608 | 70.1% | 0.0px | 29.2 |
| Q2 | 19.52 | 680 | 75.6% | 0.0px | 28.9 |
| Q3 | 19.95 | 695 | 77.8% | 0.0px | 30.35 |
| Q4 | 20.07 | 696 | 77.3% | 0.0px | 29.8 |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
|--------|----------|--------|---------|-------------------|
| Q1 | 4826.9% | 42567.3% | 53802.8% | **Dogfighter** |
| Q2 | 2603.0% | 47257.0% | 65805.1% | **Dogfighter** |
| Q3 | 1737.7% | 53477.9% | 67857.6% | **Dogfighter** |
| Q4 | 907.3% | 63956.4% | 67570.2% | **Dogfighter** |

### Input Control Style

| Period | Thrust Dur | Turn Dur | Shoot Dur | Idle Rate | Wraps |
|--------|------------|----------|-----------|-----------|-------|
| Q1 | 0.0f | 0.0f | 0.0f | 0.0% | 0.0 |
| Q2 | 0.0f | 0.0f | 0.0f | 0.0% | 0.0 |
| Q3 | 0.0f | 0.0f | 0.0f | 0.0% | 0.0 |
| Q4 | 0.0f | 0.0f | 0.0f | 0.0% | 0.0 |

### Intra-Episode Score Breakdown

Analysis of when agents earn their reward during an episode (Early vs Late game).

| Quarter | Avg Score | Share of Total | Play Style |
|---------|-----------|----------------|------------|
| Start (0-25%) | 17.5 | 5.1% | Balanced |
| Mid-Game (25-50%) | 124.4 | 36.4% | Balanced |
| Late-Game (50-75%) | 165.6 | 48.5% | Balanced |
| End-Game (75-100%) | 34.1 | 10.0% | Balanced |

## Recent Generations (Last 30)

<details>
<summary>Click to expand Recent Generations table</summary>

| Gen   | Best   | Avg    | StdDev | Kills  | Steps  | Acc%   | Stag   |
|-------|--------|--------|--------|--------|--------|--------|--------|
| 6     | 582    | 340    | 110    | 19.8   | 676    | 74     | 0      |
| 7     | 469    | 309    | 94     | 18.3   | 672    | 74     | 1      |
| 8     | 519    | 368    | 93     | 20.5   | 694    | 76     | 2      |
| 9     | 536    | 364    | 81     | 20.3   | 691    | 75     | 3      |
| 10    | 454    | 336    | 74     | 19.3   | 674    | 75     | 4      |
| 11    | 521    | 352    | 84     | 19.4   | 670    | 76     | 5      |
| 12    | 560    | 336    | 98     | 18.4   | 661    | 75     | 6      |
| 13    | 578    | 367    | 104    | 19.8   | 696    | 76     | 7      |
| 14    | 514    | 339    | 84     | 18.1   | 648    | 74     | 8      |
| 15    | 603    | 381    | 108    | 20.1   | 686    | 76     | 0      |
| 16    | 560    | 379    | 83     | 20.7   | 712    | 78     | 1      |
| 17    | 514    | 363    | 78     | 20.0   | 692    | 77     | 2      |
| 18    | 552    | 355    | 89     | 19.3   | 682    | 78     | 3      |
| 19    | 569    | 359    | 96     | 19.4   | 681    | 78     | 4      |
| 20    | 572    | 353    | 105    | 19.1   | 672    | 77     | 5      |
| 21    | 587    | 362    | 84     | 20.1   | 699    | 78     | 6      |
| 22    | 602    | 397    | 99     | 21.5   | 734    | 80     | 7      |
| 23    | 575    | 370    | 75     | 20.3   | 697    | 78     | 8      |
| 24    | 455    | 360    | 67     | 20.0   | 699    | 77     | 9      |
| 25    | 538    | 347    | 92     | 19.6   | 683    | 77     | 10     |
| 26    | 544    | 362    | 90     | 20.1   | 695    | 78     | 11     |
| 27    | 487    | 338    | 67     | 19.1   | 679    | 78     | 12     |
| 28    | 478    | 350    | 83     | 19.5   | 708    | 78     | 13     |
| 29    | 619    | 358    | 101    | 20.1   | 695    | 78     | 0      |
| 30    | 489    | 353    | 53     | 19.8   | 688    | 77     | 1      |
| 31    | 499    | 395    | 68     | 21.5   | 722    | 79     | 2      |
| 32    | 465    | 356    | 62     | 20.3   | 697    | 76     | 3      |
| 33    | 518    | 392    | 56     | 21.4   | 720    | 76     | 4      |
| 34    | 522    | 370    | 107    | 20.1   | 702    | 77     | 5      |
| 35    | 490    | 341    | 81     | 19.2   | 666    | 77     | 6      |

</details>


## Top 10 Best Generations

<details>
<summary>Click to expand Top 10 Best Generations table</summary>

| Rank | Gen   | Best   | Avg    | Kills  | Steps  | Accuracy |
|------|-------|--------|--------|--------|--------|----------|
| 1    | 29    | 619    | 358    | 29.8   | 973    | 85.8     |
| 2    | 15    | 603    | 381    | 28.9   | 904    | 79.5     |
| 3    | 22    | 602    | 397    | 30.4   | 938    | 89.0     |
| 4    | 21    | 587    | 362    | 28.4   | 857    | 83.8     |
| 5    | 6     | 582    | 340    | 29.2   | 899    | 86.3     |
| 6    | 13    | 578    | 367    | 26.9   | 860    | 85.3     |
| 7    | 23    | 575    | 370    | 26.9   | 852    | 87.7     |
| 8    | 20    | 572    | 353    | 27.4   | 889    | 87.8     |
| 9    | 19    | 569    | 359    | 27.4   | 853    | 81.9     |
| 10   | 16    | 560    | 379    | 26.9   | 900    | 87.3     |

</details>


## Trend Analysis

| Period | Avg Best | Avg Mean | Avg Min | Improvement |
|--------|----------|----------|---------|-------------|
| Q1 | 493.7 | 281.5 | 60.7 |  |
| Q2 | 540.7 | 356.8 | 175.5 | +47.1 |
| Q3 | 553.3 | 364.7 | 187.7 | +12.6 |
| Q4 | 513.6 | 360.3 | 197.1 | -39.7 |


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

     619 |                            *      
     578 |     *      * *     **             
     536 |        *  *   * ***  * **         
     495 |   *   *  *  *  *             * ** 
     454 | ** * *  *             *  ** * *  *
     413 |*                                  
     371 |              oo     o        o o  
     330 |    oo ooooooo  ooooo oooooooo o oo
     289 |   o  o                            
     248 |  o                                
     206 | o                                 
     165 |                                   
     124 |                                   
      83 |o                                  
      41 |                                   
       0 |                                   
         -----------------------------------
         Gen 1                    Gen 35
```


---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 81.84s
- **Evaluation (Simulation):** 81.83s (100.0%)
- **Evolution (GA Operators):** 0.0097s (0.0%)

| Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
|-----------|---------------|---------------|------------|
| 1-3 | 51.17s | 0.0062s | 51.17s |
| 4-6 | 79.17s | 0.0079s | 79.17s |
| 7-9 | 83.50s | 0.0113s | 83.51s |
| 10-12 | 79.99s | 0.0127s | 80.00s |
| 13-15 | 83.04s | 0.0120s | 83.06s |
| 16-18 | 81.31s | 0.0077s | 81.32s |
| 19-21 | 80.74s | 0.0086s | 80.75s |
| 22-24 | 84.20s | 0.0071s | 84.21s |
| 25-27 | 81.78s | 0.0136s | 81.80s |
| 28-30 | 80.81s | 0.0075s | 80.82s |
| 31-33 | 84.59s | 0.0083s | 84.60s |
| 34-35 | 79.48s | 0.0158s | 79.50s |

## Genetic Operator Statistics

**Recent Averages (Population: 25)**
- **Crossovers:** 8.3 (33.2%)
- **Mutations:** 25.0 (100.0%)
- **Elites Preserved:** 2.0

