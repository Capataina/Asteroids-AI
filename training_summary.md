# Training Summary Report

**Generated:** 2026-01-10 23:28:46
**Schema Version:** 2.0

## Quick Trend Overview

```
Best Fitness: 457 → 691   [▁▁▃▃▄█▅▄▇▆] +51%
Avg Fitness:  90 → 357   [▁▃▄▆▅▆▆▇▆█] +297%
Avg Kills:    5.5 → 19.6   [▁▃▄▆▆▇▆▇▆█] +256%
Avg Accuracy: 48% → 74%   [▁▅▆▇▇▇▇▇▇█] +54%
Avg Steps:    409 → 668   [▁▄▄▆▆▇▆▇▆█] +63%
Diversity:    130 → 116   [▅█▅▅▂▆▂▁▆▆] -10%
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

- **Total Generations:** 28
- **Training Duration:** 0:24:32.908009
- **All-Time Best Fitness:** 812.49
- **Best Generation:** 16
- **Final Best Fitness:** 690.83
- **Final Average Fitness:** 356.67
- **Avg Improvement (Early->Late):** 118.01
- **Stagnation:** 12 generations since improvement

**Generalization (Fresh Game Performance):**
- Avg Generalization Ratio: 0.24
- Best Fresh Fitness: 390.62 (Gen 7)
- Episode Completion Rate: 7.4%

## Best Agent Deep Profile

The most fit agent appeared in **Generation 16** with a fitness of **812.49**.

### Combat Efficiency

- **Total Kills:** 36.833333333333336
- **Survival Time:** 17.5 seconds (1047.4166666666667 steps)
- **Accuracy:** 87.2%
- **Shots per Kill:** 1.1
- **Time per Kill:** 0.47 seconds

### Behavioral Signature

**Classification:** `Aggressive`

| Action | Rate (per step) | Description |
|--------|-----------------|-------------|
| **Thrust** | 2.9% | Movement frequency |
| **Turn** | 27.6% | Rotation frequency |
| **Shoot** | 65.2% | Trigger discipline |

## Generation Highlights

### Best Improvement

**Generation 21**: Best fitness jumped +270.4 (+56.2%)
- New best fitness: 751.5

### Worst Regression

**Generation 22**: Best fitness dropped -213.6 (-28.4%)
- New best fitness: 538.0
- *Note: This may be normal variation after a lucky outlier*

### Most Accurate Generation

**Generation 21**: Population accuracy reached 78.0%

### Most Kills (Single Agent)

**Generation 16**: An agent achieved 37 kills

### First Viable Population

**Generation 1**: Average fitness first became positive

### Most Diverse Generation

**Generation 1**: Diversity index 1.45

### Most Converged Generation

**Generation 15**: Diversity index 0.21

## Milestone Timeline

| Generation | Category | Value | Description |
|------------|----------|-------|-------------|
| 1 | Fitness | 457 | Best fitness crossed 100 |
| 1 | Kills | 22.166666666666668 | First agent to achieve 1 kills |
| 1 | Kills | 22.166666666666668 | First agent to achieve 5 kills |
| 1 | Kills | 22.166666666666668 | First agent to achieve 10 kills |
| 1 | Kills | 22.166666666666668 | First agent to achieve 20 kills |
| 2 | Fitness | 523 | Best fitness crossed 500 |

## Training Progress by Decile

| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|------|----------|---------|-----------|---------|-----------|----------|
| 0-10% | 1-2 | 523 | 139 | 7.5 | 53% | 440 | 146 |
| 10-20% | 3-4 | 609 | 264 | 13.9 | 69% | 575 | 158 |
| 20-30% | 5-6 | 533 | 264 | 13.7 | 68% | 565 | 140 |
| 30-40% | 7-8 | 561 | 336 | 18.7 | 73% | 664 | 129 |
| 40-50% | 9-10 | 611 | 338 | 19.1 | 74% | 678 | 110 |
| 50-60% | 11-12 | 715 | 370 | 20.3 | 75% | 692 | 129 |
| 60-70% | 13-14 | 742 | 357 | 19.6 | 74% | 672 | 113 |
| 70-80% | 15-16 | 812 | 394 | 20.5 | 75% | 686 | 107 |
| 80-90% | 17-18 | 697 | 381 | 20.1 | 76% | 674 | 132 |
| 90-100% | 19-28 | 752 | 386 | 20.8 | 76% | 692 | 114 |

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 2.97 (up from 1.69 in Phase 1)
- **Shots per Kill:** 2.12 (down from 2.61 in Phase 1)
- **Kill Conversion Rate:** 47.1% (up from 38.4% in Phase 1)
- **Average Kills per Episode:** 20.3

### Efficiency Trend

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 | 2.17 | 2.38 | 42.0% |
| Phase 2 | 2.75 | 2.19 | 45.8% |
| Phase 3 | 2.94 | 2.13 | 46.9% |
| Phase 4 | 2.98 | 2.11 | 47.3% |
| Phase 5 | 3.01 | 2.10 | 47.7% |

**Assessment:** Agent shows slight efficiency improvement. Shots per kill dropped 18%.

## Learning Velocity

### Velocity by Phase

| Phase | Fitness Delta | Delta/Gen | Velocity | Trend |
|-------|---------------|-----------|----------|-------|
| Phase 1 | +77 | +15.3 | Moderate |  |
| Phase 2 | +110 | +21.9 | Fast | ↑ Accelerating |
| Phase 3 | -125 | -25.1 | Stalled | ↓ Slowing |
| Phase 4 | -331 | -66.3 | Stalled | ↓ Slowing |
| Phase 5 | -61 | -7.6 | Stalled | ↑ Accelerating |

### Current Velocity

- **Recent Improvement Rate:** -7.6 fitness/generation
- **Acceleration:** -51.6 (learning slowing down)
- **Projected Generations to +50% Fitness:** N/A (not improving)

### Velocity Assessment

Learning has stalled. Fitness is no longer improving. Consider:
- Stopping training (may have converged)
- Restarting with different hyperparameters
- Reviewing reward structure

## Reward Component Evolution

| Component | Phase 1 | Mid | Final | Trend | Status |
|-----------|---------|-----|-------|-------|--------|
| DistanceBasedKillReward | +94.0 | +256.8 | +256.3 | ↑↑↑ +173% | Learned |
| ConservingAmmoBonus | +77.0 | +224.9 | +225.2 | ↑↑↑ +192% | Learned |
| DeathPenalty | -148.2 | -144.5 | -144.5 | → +3% | Improving |
| ExplorationBonus | +59.6 | +29.4 | +24.9 | ↓↓ -58% | Stable |
| VelocitySurvivalBonus | +56.4 | +15.5 | +10.8 | ↓↓ -81% | Stable |

**Exploration Efficiency (Final Phase):** 0.0365 score/step
- *Note: A higher rate indicates faster map traversal, independent of survival time.*

## Reward Balance Analysis

### Warnings

- **DeathPenalty consistently negative** - This component has been negative throughout training, averaging -144.5/episode. The intended behavior may not be incentivized strongly enough, or there may be a conflict with other rewards.

- **DistanceBasedKillReward is dominant (51%)** - This component accounts for a large portion of positive reward. Consider if this is intentional.

- **ConservingAmmoBonus is dominant (45%)** - This component accounts for a large portion of positive reward. Consider if this is intentional.

- **VelocitySurvivalBonus declining** - This component dropped from 56.4 to 10.8. The agent may be trading off this behavior for others.

- **ExplorationBonus declining** - This component dropped from 59.6 to 24.9. The agent may be trading off this behavior for others.

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

| Metric | Value | Trend (Recent) | Status |
|--------|-------|----------------|--------|
| Diversity Index | 0.30 | ↓ Decreasing | 🟡 Watch |
| Elite Gap | 0.60 | → | 🟢 Good |
| Min Fitness Trend | +132.7 | ↑ | 🟢 Good |
| Max Fitness Trend | +75.8 | ↑ | 🟢 Good |
| IQR (p75-p25) | 148 | ↓ 64 | 🟢 |

## Stagnation Analysis

- **Current Stagnation:** 12 generations
- **Average Stagnation Period:** 4.2 generations
- **Longest Stagnation:** 12 generations
- **Number of Stagnation Periods:** 5

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Accuracy | Ratio | Grade | Cause of Death |
|-----|--------------|-----------|----------|-------|-------|----------------|
| 18 | 683 | 87 | 21.6% | 0.13 | F | asteroid_collision |
| 19 | 658 | 247 | 27.1% | 0.38 | D | asteroid_collision |
| 20 | 481 | -87 | 13.8% | -0.18 | F | asteroid_collision |
| 21 | 752 | -158 | 6.2% | -0.21 | F | asteroid_collision |
| 22 | 538 | -12 | 15.1% | -0.02 | F | asteroid_collision |
| 23 | 618 | 29 | 16.1% | 0.05 | F | asteroid_collision |
| 24 | 669 | -183 | 4.8% | -0.27 | F | asteroid_collision |
| 25 | 552 | 225 | 17.0% | 0.41 | D | completed_episode |
| 26 | 524 | -129 | 4.5% | -0.25 | F | asteroid_collision |
| 27 | 690 | -160 | 5.7% | -0.23 | F | asteroid_collision |

### Generalization Summary

- **Average Fitness Ratio:** 0.24
- **Best Ratio:** 0.70
- **Worst Ratio:** 0.04

**Grade Distribution:** C:1 D:3 F:23 

## Correlation Analysis

### Fitness Correlations

| Metric | Correlation | Strength |
|--------|-------------|----------|
| Kills | +0.98 | Strong |
| Steps Survived | +0.98 | Strong |
| Accuracy | +0.90 | Strong |

### Interpretation

Fitness is most strongly predicted by kills (r=0.98).

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 683 steps (45.6% of max)
- **Max Survival:** 994 steps

### Survival Progression

| Phase | Mean Steps | Change |
|-------|------------|--------|
| Phase 1 | 521 |  |
| Phase 2 | 649 | +128 |
| Phase 3 | 683 | +35 |
| Phase 4 | 679 | -4 |
| Phase 5 | 695 | +15 |

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 20.78
- **Avg Steps Survived:** 692
- **Avg Accuracy:** 75.8%
- **Max Kills (Any Agent Ever):** 36.833333333333336
- **Max Steps (Any Agent Ever):** 1047.4166666666667

## Learning Progress

**Comparing First 2 vs Last 2 Generations:**

| Metric | Early | Late | Change |
|--------|-------|------|--------|
| Best Fitness | 489.8 | 690.7 | +41.0% |
| Avg Fitness | 138.8 | 372.7 | +168.5% |

**Verdict:** Moderate learning - some improvement but room for more training.

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 116.12
- Average Range (Best-Min): 477.57
- Diversity Change: -16.6%
- **Status:** Population is converging (low diversity)

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Max Kills |
|--------|-----------|-----------|--------------|----------|
| Q1 | 12.72 | 547 | 64.6% | 28.25 |
| Q2 | 19.50 | 678 | 74.3% | 34.333333333333336 |
| Q3 | 20.61 | 687 | 75.5% | 36.833333333333336 |
| Q4 | 20.68 | 690 | 76.0% | 32.5 |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
|--------|----------|--------|---------|-------------------|
| Q1 | 9446.1% | 26297.3% | 42895.7% | **Dogfighter** |
| Q2 | 1808.1% | 35177.1% | 65351.1% | **Dogfighter** |
| Q3 | 2994.7% | 31191.7% | 68689.1% | **Dogfighter** |
| Q4 | 1787.0% | 26202.7% | 68993.2% | **Dogfighter** |

## Recent Generations (Last 30)

| Gen   | Best   | Avg    | StdDev | Kills  | Steps  | Acc%   | Stag   |
|-------|--------|--------|--------|--------|--------|--------|--------|
| 1     | 457    | 90     | 130    | 5.5    | 409    | 48     | 0      |
| 2     | 523    | 188    | 163    | 9.4    | 472    | 57     | 0      |
| 3     | 483    | 221    | 157    | 12.1   | 548    | 66     | 1      |
| 4     | 609    | 306    | 158    | 15.7   | 603    | 71     | 0      |
| 5     | 533    | 267    | 132    | 13.7   | 571    | 69     | 1      |
| 6     | 501    | 260    | 148    | 13.7   | 559    | 67     | 2      |
| 7     | 561    | 349    | 135    | 18.9   | 669    | 74     | 3      |
| 8     | 539    | 323    | 123    | 18.4   | 659    | 73     | 4      |
| 9     | 598    | 329    | 98     | 18.9   | 673    | 73     | 5      |
| 10    | 611    | 348    | 122    | 19.2   | 683    | 75     | 0      |
| 11    | 715    | 357    | 138    | 19.9   | 685    | 75     | 0      |
| 12    | 573    | 383    | 119    | 20.7   | 699    | 76     | 1      |
| 13    | 605    | 347    | 98     | 19.4   | 668    | 73     | 2      |
| 14    | 742    | 367    | 129    | 19.8   | 676    | 75     | 0      |
| 15    | 589    | 398    | 84     | 20.6   | 689    | 76     | 1      |
| 16    | 812    | 390    | 130    | 20.4   | 683    | 75     | 0      |
| 17    | 697    | 355    | 142    | 19.3   | 655    | 74     | 1      |
| 18    | 683    | 406    | 122    | 21.0   | 693    | 77     | 2      |
| 19    | 658    | 431    | 140    | 22.1   | 722    | 77     | 3      |
| 20    | 481    | 334    | 91     | 18.6   | 643    | 72     | 4      |
| 21    | 752    | 435    | 119    | 22.3   | 727    | 78     | 5      |
| 22    | 538    | 338    | 105    | 19.1   | 651    | 73     | 6      |
| 23    | 618    | 407    | 97     | 21.9   | 716    | 76     | 7      |
| 24    | 669    | 409    | 115    | 22.1   | 715    | 77     | 8      |
| 25    | 552    | 381    | 104    | 20.7   | 697    | 76     | 9      |
| 26    | 524    | 380    | 115    | 20.4   | 684    | 78     | 10     |
| 27    | 690    | 389    | 138    | 21.0   | 699    | 78     | 11     |
| 28    | 691    | 357    | 116    | 19.6   | 668    | 74     | 12     |


## Top 10 Best Generations

| Rank | Gen   | Best   | Avg    | Kills  | Steps  | Accuracy |
|------|-------|--------|--------|--------|--------|----------|
| 1    | 16    | 812    | 390    | 36.8   | 1047   | 87.2     |
| 2    | 21    | 752    | 435    | 33.8   | 1021   | 88.6     |
| 3    | 14    | 742    | 367    | 33.8   | 990    | 92.3     |
| 4    | 11    | 715    | 357    | 34.3   | 990    | 91.7     |
| 5    | 17    | 697    | 355    | 32.6   | 991    | 92.4     |
| 6    | 28    | 691    | 357    | 31.6   | 994    | 84.4     |
| 7    | 27    | 690    | 389    | 31.2   | 968    | 86.3     |
| 8    | 18    | 683    | 406    | 32.3   | 915    | 84.1     |
| 9    | 24    | 669    | 409    | 32.5   | 923    | 84.3     |
| 10   | 19    | 658    | 431    | 28.9   | 909    | 81.7     |


## Trend Analysis

| Period | Avg Best | Avg Mean | Avg Min | Improvement |
|--------|----------|----------|---------|-------------|
| Q1 | 523.9 | 240.3 | -5.1 |  |
| Q2 | 625.9 | 350.6 | 145.9 | +102.0 |
| Q3 | 667.4 | 392.7 | 191.3 | +41.5 |
| Q4 | 611.6 | 380.2 | 147.6 | -55.8 |


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

     812 |               *            
     758 |                            
     704 |          *  *      *       
     650 |                ***    *  **
     596 |   *    **  *         *     
     542 |      *    *  *         *   
     487 | *  ** *             *   *  
     433 |* *                *o       
     379 |           o  oo oo   ooooo 
     325 |      o ooo oo  o  o o     o
     271 |   o   o                    
     217 |  o oo                      
     162 | o                          
     108 |                            
      54 |o                           
       0 |                            
         ----------------------------
         Gen 1             Gen 28
```


---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 44.47s
- **Evaluation (Simulation):** 44.47s (100.0%)
- **Evolution (GA Operators):** 0.0079s (0.0%)

| Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
|-----------|---------------|---------------|------------|
| 1-2 | 23.69s | 0.0038s | 23.70s |
| 3-4 | 34.51s | 0.0084s | 34.52s |
| 5-6 | 34.29s | 0.0091s | 34.30s |
| 7-8 | 44.03s | 0.0150s | 44.05s |
| 9-10 | 42.62s | 0.0080s | 42.63s |
| 11-12 | 44.17s | 0.0071s | 44.18s |
| 13-14 | 42.82s | 0.0073s | 42.83s |
| 15-16 | 44.26s | 0.0078s | 44.27s |
| 17-18 | 44.67s | 0.0072s | 44.67s |
| 19-20 | 44.24s | 0.0065s | 44.25s |
| 21-22 | 44.00s | 0.0087s | 44.00s |
| 23-24 | 45.58s | 0.0083s | 45.58s |
| 25-26 | 44.93s | 0.0082s | 44.94s |
| 27-28 | 43.58s | 0.0077s | 43.59s |

## Genetic Operator Statistics

**Recent Averages (Population: 25)**
- **Crossovers:** 8.9 (35.6%)
- **Mutations:** 25.0 (100.0%)
- **Elites Preserved:** 2.0

