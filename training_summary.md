# Training Summary Report

**Generated:** 2026-01-13 16:21:35
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
Best Fitness: 590 → 745   [▁▇▆▅▂▂▄█▂▃] +26%
Avg Fitness:  160 → 535   [▁▆▇▇▆▇▇█▇▇] +234%
Avg Kills:    2.6 → 7.0   [▁▆▇▇▆▇▇█▇▇] +165%
Avg Accuracy: 27% → 35%   [▁▆▇▇▆█▇▆▆▆] +28%
Avg Steps:    464 → 708   [▁▆▇▇▆▇▆█▇▇] +53%
Diversity:    199 → 111   [█▆▄▄▂▁▄▆▂▃] -44%
```

## Training Configuration

```
population_size: 25
num_generations: 500
mutation_probability: 0.05
max_workers: 16
```

## Overall Summary

- **Total Generations:** 55
- **Training Duration:** 1:13:41.309163
- **All-Time Best Fitness:** 1017.01
- **Best Generation:** 28
- **Final Best Fitness:** 744.59
- **Final Average Fitness:** 535.01
- **Avg Improvement (Early->Late):** 119.03
- **Stagnation:** 27 generations since improvement

**Generalization (Fresh Game Performance):**
- Avg Generalization Ratio: 0.85
- Best Fresh Fitness: 1580.56 (Gen 38)
- Episode Completion Rate: 1.9%

## Best Agent Deep Profile

The most fit agent appeared in **Generation 28** with a fitness of **1017.01**.

### Combat Efficiency

- **Total Kills:** 11.4
- **Survival Time:** 15.0 seconds (900.3 steps)
- **Accuracy:** 40.5%
- **Shots per Kill:** 2.5
- **Time per Kill:** 1.32 seconds

### Behavioral Signature

**Classification:** `Spinner`

| Action | Rate (per step) | Description |
|--------|-----------------|-------------|
| **Thrust** | 4.3% | Movement frequency |
| **Turn** | 58.4% | Rotation frequency |
| **Shoot** | 94.2% | Trigger discipline |

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
|                                     .                                                                                  |
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

### Spatial Analytics (Population Average - Sample of 30)

**Position Heatmap (Where do they fly?)**
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

**Kill Zone Heatmap (Where do they kill?)**
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

**Generation 52**: Best fitness jumped +250.4 (+34.9%)
- New best fitness: 967.4

### Worst Regression

**Generation 29**: Best fitness dropped -283.2 (-27.9%)
- New best fitness: 733.8
- *Note: This may be normal variation after a lucky outlier*

### Most Accurate Generation

**Generation 43**: Population accuracy reached 35.7%

### Most Kills (Single Agent)

**Generation 36**: An agent achieved 12 kills

### First Viable Population

**Generation 1**: Average fitness first became positive

### Most Diverse Generation

**Generation 1**: Diversity index 1.24

### Most Converged Generation

**Generation 26**: Diversity index 0.16

## Milestone Timeline

| Generation | Category | Value | Description |
|------------|----------|-------|-------------|
| 1 | Fitness | 590 | Best fitness crossed 100 |
| 1 | Fitness | 590 | Best fitness crossed 500 |
| 1 | Kills | 7.35 | First agent to achieve 1 kills |
| 1 | Kills | 7.35 | First agent to achieve 5 kills |
| 6 | Kills | 10.9 | First agent to achieve 10 kills |
| 28 | Fitness | 1017 | Best fitness crossed 1000 |

## Training Progress by Decile

| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|------|----------|---------|-----------|---------|-----------|----------|
| 0-10% | 1-5 | 812 | 369 | 5.0 | 31% | 606 | 191 |
| 10-20% | 6-10 | 949 | 459 | 6.1 | 34% | 669 | 167 |
| 20-30% | 11-15 | 894 | 514 | 6.8 | 35% | 705 | 122 |
| 30-40% | 16-20 | 859 | 508 | 6.7 | 34% | 694 | 138 |
| 40-50% | 21-25 | 830 | 505 | 6.7 | 34% | 681 | 138 |
| 50-60% | 26-30 | 1017 | 513 | 6.8 | 35% | 698 | 124 |
| 60-70% | 31-35 | 868 | 502 | 6.7 | 34% | 680 | 135 |
| 70-80% | 36-40 | 993 | 534 | 7.1 | 34% | 705 | 139 |
| 80-90% | 41-45 | 872 | 531 | 7.0 | 35% | 705 | 129 |
| 90-100% | 46-55 | 967 | 533 | 7.0 | 35% | 709 | 127 |

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 0.97 (up from 0.83 in Phase 1)
- **Shots per Kill:** 6.38 (down from 6.70 in Phase 1)
- **Kill Conversion Rate:** 15.7% (up from 14.9% in Phase 1)
- **Average Kills per Episode:** 6.9

### Efficiency Trend

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 | 0.88 | 6.60 | 15.2% |
| Phase 2 | 0.97 | 6.39 | 15.6% |
| Phase 3 | 0.98 | 6.28 | 15.9% |
| Phase 4 | 1.01 | 6.23 | 16.0% |
| Phase 5 | 0.98 | 6.38 | 15.7% |

**Assessment:** Agent shows slight efficiency improvement. Shots per kill dropped 5%.

## Learning Velocity

### Velocity by Phase

| Phase | Fitness Delta | Delta/Gen | Velocity | Trend |
|-------|---------------|-----------|----------|-------|
| Phase 1 | +304 | +27.6 | Fast |  |
| Phase 2 | +119 | +10.8 | Moderate | ↓ Slowing |
| Phase 3 | +90 | +8.2 | Moderate | ↓ Slowing |
| Phase 4 | -32 | -2.9 | Stalled | ↓ Slowing |
| Phase 5 | -10 | -0.9 | Stalled | ↑ Accelerating |

### Current Velocity

- **Recent Improvement Rate:** -0.9 fitness/generation
- **Acceleration:** -17.8 (learning slowing down)
- **Projected Generations to +50% Fitness:** N/A (not improving)

### Velocity Assessment

Learning has stalled. Fitness is no longer improving. Consider:
- Stopping training (may have converged)
- Restarting with different hyperparameters
- Reviewing reward structure

## Reward Component Evolution

| Component | Phase 1 | Mid | Final | Trend | Status |
|-----------|---------|-----|-------|-------|--------|
| DistanceBasedKillReward | +319.5 | +428.1 | +434.5 | ↑ +36% | Learned |
| ConservingAmmoBonus | +149.5 | +201.6 | +208.8 | ↑ +40% | Learned |
| DeathPenalty | -142.6 | -140.1 | -138.3 | → +3% | Improving |
| ExplorationBonus | +23.3 | +13.4 | +13.9 | ↓ -41% | Stable |
| VelocitySurvivalBonus | +19.8 | +7.2 | +7.7 | ↓↓ -61% | Stable |

**Exploration Efficiency (Final Phase):** 0.0197 score/step
- *Note: A higher rate indicates faster map traversal, independent of survival time.*

## Reward Balance Analysis

### Warnings

- **DeathPenalty consistently negative** - This component has been negative throughout training, averaging -138.3/episode. The intended behavior may not be incentivized strongly enough, or there may be a conflict with other rewards.

- **DistanceBasedKillReward dominates reward (65%)** - This single component accounts for most of all positive reward. Other behaviors may be under-incentivized.

- **VelocitySurvivalBonus declining** - This component dropped from 19.8 to 7.7. The agent may be trading off this behavior for others.

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
| Diversity Index | 0.24 | ↓ Decreasing | 🟡 Watch |
| Elite Gap | 0.50 | → | 🟢 Good |
| Min Fitness Trend | +246.6 | ↑ | 🟢 Good |
| Max Fitness Trend | +48.0 | ↑ | 🟢 Good |
| IQR (p75-p25) | 167 | ↓ 90 | 🟢 |

### Warnings

- ⚠️ High stagnation (27 gens) - population stuck

## Stagnation Analysis

- **Current Stagnation:** 27 generations
- **Average Stagnation Period:** 16.7 generations
- **Longest Stagnation:** 27 generations
- **Number of Stagnation Periods:** 3

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Accuracy | Ratio | Grade | Cause of Death |
|-----|--------------|-----------|----------|-------|-------|----------------|
| 45 | 755 | 995 | 13.4% | 1.32 | A | asteroid_collision |
| 46 | 713 | 1161 | 18.2% | 1.63 | A | asteroid_collision |
| 47 | 890 | 185 | 10.7% | 0.21 | F | asteroid_collision |
| 48 | 747 | 193 | 11.1% | 0.26 | F | asteroid_collision |
| 49 | 733 | 319 | 9.3% | 0.44 | D | asteroid_collision |
| 50 | 869 | 888 | 12.3% | 1.02 | A | asteroid_collision |
| 51 | 717 | 236 | 12.0% | 0.33 | D | asteroid_collision |
| 52 | 967 | 49 | 8.7% | 0.05 | F | asteroid_collision |
| 53 | 807 | 84 | 5.7% | 0.10 | F | asteroid_collision |
| 54 | 821 | 967 | 22.4% | 1.18 | A | asteroid_collision |

### Generalization Summary

- **Average Fitness Ratio:** 0.85
- **Best Ratio:** 2.18
- **Worst Ratio:** 0.00

**Grade Distribution:** A:20 B:4 C:4 D:5 F:21 

## Correlation Analysis

### Fitness Correlations

| Metric | Correlation | Strength |
|--------|-------------|----------|
| Kills | +0.99 | Strong |
| Steps Survived | +0.97 | Strong |
| Accuracy | +0.93 | Strong |

### Interpretation

Fitness is most strongly predicted by kills (r=0.99).

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 705 steps (47.0% of max)
- **Max Survival:** 934 steps

### Survival Progression

| Phase | Mean Steps | Change |
|-------|------------|--------|
| Phase 1 | 644 |  |
| Phase 2 | 694 | +50 |
| Phase 3 | 687 | -7 |
| Phase 4 | 705 | +18 |
| Phase 5 | 707 | +2 |

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 6.95
- **Avg Steps Survived:** 709
- **Avg Accuracy:** 34.6%
- **Max Kills (Any Agent Ever):** 11.65
- **Max Steps (Any Agent Ever):** 1042.5

## Learning Progress

**Comparing First 5 vs Last 5 Generations:**

| Metric | Early | Late | Change |
|--------|-------|------|--------|
| Best Fitness | 739.7 | 811.6 | +9.7% |
| Avg Fitness | 369.4 | 526.6 | +42.5% |

**Verdict:** Moderate learning - some improvement but room for more training.

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 130.37
- Average Range (Best-Min): 519.80
- Diversity Change: -29.0%
- **Status:** Population is converging (low diversity)

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Safe Dist | Max Kills |
|--------|-----------|-----------|--------------|-----------|----------|
| Q1 | 5.80 | 652 | 33.0% | 169.2px | 10.9 |
| Q2 | 6.76 | 692 | 34.5% | 164.5px | 10.2 |
| Q3 | 6.84 | 693 | 34.0% | 165.4px | 11.65 |
| Q4 | 7.00 | 708 | 34.6% | 163.8px | 11.15 |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
|--------|----------|--------|---------|-------------------|
| Q1 | 8.2% | 78.5% | 87.8% | **Spinner** |
| Q2 | 3.6% | 70.7% | 95.4% | **Spinner** |
| Q3 | 3.4% | 49.8% | 96.5% | **Spinner** |
| Q4 | 2.8% | 65.7% | 98.9% | **Spinner** |

### Input Control Style

| Period | Thrust Dur | Turn Dur | Shoot Dur | Idle Rate | Wraps |
|--------|------------|----------|-----------|-----------|-------|
| Q1 | 0.0f | 0.0f | 0.0f | 2.8% | 0.5 |
| Q2 | 0.0f | 0.0f | 0.0f | 1.1% | 0.2 |
| Q3 | 0.0f | 0.0f | 0.0f | 0.7% | 0.1 |
| Q4 | 0.0f | 0.0f | 0.0f | 0.2% | 0.1 |

### Intra-Episode Score Breakdown

Analysis of when agents earn their reward during an episode (Early vs Late game).

| Quarter | Avg Score | Share of Total | Play Style |
|---------|-----------|----------------|------------|
| Start (0-25%) | 59.4 | 11.1% | Balanced |
| Mid-Game (25-50%) | 157.4 | 29.4% | Balanced |
| Late-Game (50-75%) | 211.1 | 39.4% | Balanced |
| End-Game (75-100%) | 107.1 | 20.0% | Balanced |

## Recent Generations (Last 30)

<details>
<summary>Click to expand Recent Generations table</summary>

| Gen   | Best   | Avg    | StdDev | Kills  | Steps  | Acc%   | Stag   |
|-------|--------|--------|--------|--------|--------|--------|--------|
| 26    | 688    | 517    | 81     | 6.9    | 692    | 36     | 20     |
| 27    | 855    | 526    | 141    | 6.9    | 712    | 35     | 21     |
| 28    | 1017   | 499    | 169    | 6.6    | 683    | 35     | 0      |
| 29    | 734    | 499    | 111    | 6.7    | 700    | 34     | 1      |
| 30    | 861    | 526    | 120    | 6.9    | 705    | 34     | 2      |
| 31    | 818    | 493    | 133    | 6.5    | 682    | 35     | 3      |
| 32    | 868    | 476    | 132    | 6.5    | 658    | 33     | 4      |
| 33    | 840    | 490    | 143    | 6.6    | 663    | 34     | 5      |
| 34    | 810    | 528    | 123    | 7.1    | 695    | 33     | 6      |
| 35    | 799    | 524    | 144    | 7.0    | 701    | 34     | 7      |
| 36    | 993    | 540    | 169    | 7.1    | 719    | 34     | 8      |
| 37    | 763    | 495    | 134    | 6.7    | 674    | 34     | 9      |
| 38    | 859    | 556    | 130    | 7.4    | 713    | 34     | 10     |
| 39    | 817    | 522    | 138    | 7.0    | 700    | 34     | 11     |
| 40    | 765    | 560    | 122    | 7.3    | 721    | 34     | 12     |
| 41    | 703    | 522    | 115    | 7.0    | 692    | 34     | 13     |
| 42    | 758    | 519    | 122    | 6.9    | 697    | 34     | 14     |
| 43    | 872    | 586    | 150    | 7.5    | 739    | 36     | 15     |
| 44    | 778    | 527    | 124    | 7.0    | 703    | 35     | 16     |
| 45    | 755    | 502    | 135    | 6.7    | 694    | 34     | 17     |
| 46    | 713    | 508    | 131    | 6.8    | 685    | 34     | 18     |
| 47    | 890    | 564    | 142    | 7.2    | 722    | 35     | 19     |
| 48    | 747    | 557    | 136    | 7.2    | 727    | 35     | 20     |
| 49    | 733    | 506    | 103    | 6.7    | 697    | 34     | 21     |
| 50    | 869    | 564    | 128    | 7.2    | 728    | 35     | 22     |
| 51    | 717    | 523    | 104    | 6.8    | 709    | 35     | 23     |
| 52    | 967    | 549    | 160    | 7.0    | 714    | 35     | 24     |
| 53    | 807    | 512    | 132    | 6.8    | 699    | 34     | 25     |
| 54    | 821    | 514    | 120    | 6.8    | 696    | 35     | 26     |
| 55    | 745    | 535    | 111    | 7.0    | 708    | 35     | 27     |

</details>


## Top 10 Best Generations

<details>
<summary>Click to expand Top 10 Best Generations table</summary>

| Rank | Gen   | Best   | Avg    | Kills  | Steps  | Accuracy |
|------|-------|--------|--------|--------|--------|----------|
| 1    | 28    | 1017   | 499    | 11.4   | 900    | 40.5     |
| 2    | 36    | 993    | 540    | 11.7   | 1018   | 41.1     |
| 3    | 52    | 967    | 549    | 11.2   | 887    | 41.7     |
| 4    | 6     | 949    | 455    | 10.9   | 1042   | 41.6     |
| 5    | 11    | 894    | 511    | 10.6   | 911    | 41.9     |
| 6    | 47    | 890    | 564    | 10.2   | 886    | 40.8     |
| 7    | 43    | 872    | 586    | 10.3   | 918    | 37.4     |
| 8    | 50    | 869    | 564    | 10.2   | 868    | 38.6     |
| 9    | 32    | 868    | 476    | 10.7   | 855    | 34.7     |
| 10   | 30    | 861    | 526    | 10.3   | 901    | 38.2     |

</details>


## Trend Analysis

| Period | Avg Best | Avg Mean | Avg Min | Improvement |
|--------|----------|----------|---------|-------------|
| Q1 | 761.9 | 433.9 | 94.1 |  |
| Q2 | 775.8 | 511.4 | 257.9 | +13.9 |
| Q3 | 848.8 | 513.4 | 266.2 | +73.0 |
| Q4 | 790.1 | 534.2 | 289.9 | -58.7 |


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

    1017 |                           *                           
     949 |                                   *               *   
     881 |     *    *                                   *        
     814 |               * *   * *  *  ****    **   *      *   * 
     746 | ***     *  * *   **  * *        ** *  * * **  *    *  
     678 |    * ***  * *  *   *    *  *           *    *  * *   *
     610 |                                                       
     542 |*                o                   o o  o   oo o o   
     475 |    o  o oo ooooo  o oooooooooooooooo o oo ooo  o o ooo
     407 |  oo o  o  o      o o                                  
     339 |      o                                                
     271 | o                                                     
     203 |                                                       
     136 |o                                                      
      68 |                                                       
       0 |                                                       
         -------------------------------------------------------
         Gen 1                                        Gen 55
```


---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 0.00s
- **Evaluation (Simulation):** 70.93s (0.0%)
- **Evolution (GA Operators):** 0.0150s (0.0%)

| Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
|-----------|---------------|---------------|------------|
| 1-5 | 57.46s | 0.0075s | 0.00s |
| 6-10 | 65.28s | 0.0114s | 0.00s |
| 11-15 | 70.10s | 0.0128s | 0.00s |
| 16-20 | 69.25s | 0.0156s | 0.00s |
| 21-25 | 67.16s | 0.0165s | 0.00s |
| 26-30 | 68.71s | 0.0119s | 0.00s |
| 31-35 | 68.58s | 0.0132s | 0.00s |
| 36-40 | 70.12s | 0.0128s | 0.00s |
| 41-45 | 70.09s | 0.0140s | 0.00s |
| 46-50 | 71.10s | 0.0140s | 0.00s |
| 51-55 | 70.76s | 0.0160s | 0.00s |

## Genetic Operator Statistics

**Recent Averages (Population: 25)**
- **Crossovers:** 9.1 (36.4%)
- **Mutations:** 25.0 (100.0%)
- **Elites Preserved:** 2.0

