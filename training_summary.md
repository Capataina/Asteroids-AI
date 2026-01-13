# Training Summary Report

**Generated:** 2026-01-13 02:02:06
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
Best Fitness: 292 → 482   [▁▃▄▅▅█▅▅▇▄] +65%
Avg Fitness:  81 → 305   [▁▃▅▄▆▆▆▇█▇] +277%
Avg Kills:    4.9 → 16.4   [▁▃▄▄▅▆▅▇█▇] +234%
Avg Accuracy: 49% → 72%   [▁▃▆▆▆▆▆▇█▇] +49%
Avg Steps:    362 → 619   [▁▂▅▄▅▅▅▇█▇] +71%
Diversity:    105 → 116   [▂▅▁█▅▇▅▇▄▃] +11%
```

## Training Configuration

```
population_size: 25
num_generations: 500
mutation_probability: 0.05
max_workers: 16
```

## Overall Summary

- **Total Generations:** 10
- **Training Duration:** 0:11:59.254070
- **All-Time Best Fitness:** 656.47
- **Best Generation:** 6
- **Final Best Fitness:** 482.45
- **Final Average Fitness:** 304.98
- **Avg Improvement (Early->Late):** 0.00
- **Stagnation:** 4 generations since improvement

**Generalization (Fresh Game Performance):**
- Avg Generalization Ratio: 0.40
- Best Fresh Fitness: 456.25 (Gen 2)
- Episode Completion Rate: 22.2%

## Best Agent Deep Profile

The most fit agent appeared in **Generation 6** with a fitness of **656.47**.

### Combat Efficiency

- **Total Kills:** 28.05
- **Survival Time:** 14.4 seconds (862.4 steps)
- **Accuracy:** 84.9%
- **Shots per Kill:** 1.2
- **Time per Kill:** 0.51 seconds

### Behavioral Signature

**Classification:** `Dogfighter`

| Action | Rate (per step) | Description |
|--------|-----------------|-------------|
| **Thrust** | 22.1% | Movement frequency |
| **Turn** | 63.5% | Rotation frequency |
| **Shoot** | 93.4% | Trigger discipline |

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

**Generation 6**: Best fitness jumped +149.1 (+29.4%)
- New best fitness: 656.5

### Worst Regression

**Generation 10**: Best fitness dropped -148.4 (-23.5%)
- New best fitness: 482.4
- *Note: This may be normal variation after a lucky outlier*

### Most Accurate Generation

**Generation 9**: Population accuracy reached 72.8%

### Most Kills (Single Agent)

**Generation 6**: An agent achieved 28 kills

### First Viable Population

**Generation 1**: Average fitness first became positive

### Most Diverse Generation

**Generation 1**: Diversity index 1.29

### Most Converged Generation

**Generation 9**: Diversity index 0.37

## Milestone Timeline

| Generation | Category | Value | Description |
|------------|----------|-------|-------------|
| 1 | Fitness | 292 | Best fitness crossed 100 |
| 1 | Kills | 15.75 | First agent to achieve 1 kills |
| 1 | Kills | 15.75 | First agent to achieve 5 kills |
| 1 | Kills | 15.75 | First agent to achieve 10 kills |
| 4 | Fitness | 530 | Best fitness crossed 500 |
| 4 | Kills | 24.9 | First agent to achieve 20 kills |

## Training Progress by Decile

| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|------|----------|---------|-----------|---------|-----------|----------|
| 0-10% | 1-1 | 292 | 81 | 4.9 | 49% | 362 | 105 |
| 10-20% | 2-2 | 434 | 182 | 8.7 | 58% | 443 | 130 |
| 20-30% | 3-3 | 449 | 248 | 11.9 | 68% | 535 | 97 |
| 30-40% | 4-4 | 530 | 205 | 10.4 | 66% | 507 | 146 |
| 40-50% | 5-5 | 507 | 269 | 13.1 | 69% | 550 | 130 |
| 50-60% | 6-6 | 656 | 285 | 14.2 | 69% | 551 | 140 |
| 60-70% | 7-7 | 522 | 275 | 13.4 | 68% | 539 | 127 |
| 70-80% | 8-8 | 526 | 300 | 16.4 | 72% | 622 | 140 |
| 80-90% | 9-9 | 631 | 337 | 17.3 | 73% | 647 | 125 |
| 90-100% | 10-10 | 482 | 305 | 16.4 | 72% | 619 | 116 |

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 2.66 (up from 1.36 in Phase 1)
- **Shots per Kill:** 2.25 (down from 3.09 in Phase 1)
- **Kill Conversion Rate:** 44.5% (up from 32.4% in Phase 1)
- **Average Kills per Episode:** 16.4

### Efficiency Trend

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 | 1.69 | 2.78 | 36.0% |
| Phase 2 | 2.14 | 2.50 | 40.1% |
| Phase 3 | 2.47 | 2.40 | 41.7% |
| Phase 4 | 2.56 | 2.30 | 43.6% |
| Phase 5 | 2.66 | 2.22 | 45.0% |

**Assessment:** Agent has improved efficiency moderately. Shots per kill dropped 27%.

## Learning Velocity

### Velocity by Phase

| Phase | Fitness Delta | Delta/Gen | Velocity | Trend |
|-------|---------------|-----------|----------|-------|
| Phase 1 | +142 | +70.8 | Fast |  |
| Phase 2 | +81 | +40.7 | Fast | ↓ Slowing |
| Phase 3 | +149 | +74.5 | Fast | ↑ Accelerating |
| Phase 4 | +5 | +2.4 | Slow | ↓ Slowing |
| Phase 5 | -148 | -74.2 | Stalled | ↓ Slowing |

### Current Velocity

- **Recent Improvement Rate:** -74.2 fitness/generation
- **Acceleration:** -54.8 (learning slowing down)
- **Projected Generations to +50% Fitness:** N/A (not improving)

### Velocity Assessment

Learning has stalled. Fitness is no longer improving. Consider:
- Stopping training (may have converged)
- Restarting with different hyperparameters
- Reviewing reward structure

## Reward Component Evolution

| Component | Phase 1 | Mid | Final | Trend | Status |
|-----------|---------|-----|-------|-------|--------|
| DistanceBasedKillReward | +62.9 | +179.9 | +208.4 | ↑↑↑ +231% | Learned |
| ConservingAmmoBonus | +48.3 | +155.3 | +184.2 | ↑↑↑ +281% | Learned |
| DeathPenalty | -149.7 | -146.7 | -146.1 | → +2% | Improving |
| ExplorationBonus | +62.6 | +53.1 | +34.8 | ↓ -44% | Stable |
| VelocitySurvivalBonus | +56.7 | +43.4 | +23.6 | ↓↓ -58% | Stable |

**Exploration Efficiency (Final Phase):** 0.0563 score/step
- *Note: A higher rate indicates faster map traversal, independent of survival time.*

## Reward Balance Analysis

### Warnings

- **DeathPenalty consistently negative** - This component has been negative throughout training, averaging -146.1/episode. The intended behavior may not be incentivized strongly enough, or there may be a conflict with other rewards.

- **DistanceBasedKillReward is dominant (46%)** - This component accounts for a large portion of positive reward. Consider if this is intentional.

- **ConservingAmmoBonus is dominant (41%)** - This component accounts for a large portion of positive reward. Consider if this is intentional.

- **VelocitySurvivalBonus declining** - This component dropped from 56.7 to 23.6. The agent may be trading off this behavior for others.

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
| Diversity Index | 0.50 | → Stable | 🟢 Good |
| Elite Gap | 1.02 | → | 🟢 Good |
| Min Fitness Trend | +0.0 | ↓ | 🟢 Good |
| Max Fitness Trend | +0.0 | ↓ | 🟡 Watch |
| IQR (p75-p25) | 188 | ↑ 0 | 🟢 |

## Stagnation Analysis

- **Current Stagnation:** 4 generations
- **Average Stagnation Period:** 2.5 generations
- **Longest Stagnation:** 4 generations
- **Number of Stagnation Periods:** 2

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Accuracy | Ratio | Grade | Cause of Death |
|-----|--------------|-----------|----------|-------|-------|----------------|
| 1 | 292 | 101 | 16.1% | 0.35 | D | asteroid_collision |
| 2 | 434 | 456 | 24.0% | 1.05 | A | completed_episode |
| 3 | 449 | -42 | 9.5% | -0.09 | F | asteroid_collision |
| 4 | 530 | 62 | 12.8% | 0.12 | F | asteroid_collision |
| 5 | 507 | 75 | 16.0% | 0.15 | F | asteroid_collision |
| 6 | 656 | 94 | 18.7% | 0.14 | F | asteroid_collision |
| 7 | 522 | -45 | 9.7% | -0.09 | F | asteroid_collision |
| 8 | 526 | 320 | 17.0% | 0.61 | C | completed_episode |
| 9 | 631 | -199 | 5.9% | -0.32 | F | asteroid_collision |

### Generalization Summary

- **Average Fitness Ratio:** 0.40
- **Best Ratio:** 1.05
- **Worst Ratio:** 0.12

**Grade Distribution:** A:1 C:1 D:1 F:6 

## Correlation Analysis

### Fitness Correlations

| Metric | Correlation | Strength |
|--------|-------------|----------|
| Kills | +0.98 | Strong |
| Steps Survived | +0.97 | Strong |
| Accuracy | +0.89 | Strong |

### Interpretation

Fitness is most strongly predicted by kills (r=0.98).

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 619 steps (41.3% of max)
- **Max Survival:** 814 steps

### Survival Progression

| Phase | Mean Steps | Change |
|-------|------------|--------|
| Phase 1 | 402 |  |
| Phase 2 | 521 | +118 |
| Phase 3 | 551 | +30 |
| Phase 4 | 581 | +30 |
| Phase 5 | 633 | +52 |

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 12.66
- **Avg Steps Survived:** 537
- **Avg Accuracy:** 66.2%
- **Max Kills (Any Agent Ever):** 28.05
- **Max Steps (Any Agent Ever):** 873.7

## Learning Progress

**Comparing First 1 vs Last 1 Generations:**

| Metric | Early | Late | Change |
|--------|-------|------|--------|
| Best Fitness | 292.4 | 482.4 | +65.0% |
| Avg Fitness | 80.8 | 305.0 | +277.3% |

**Verdict:** Strong learning - both best and average fitness improved significantly.

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 125.58
- Average Range (Best-Min): 472.70
- Diversity Change: +0.0%
- **Status:** Population is converging (low diversity)

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Safe Dist | Max Kills |
|--------|-----------|-----------|--------------|-----------|----------|
| Q1 | 6.79 | 402 | 53.2% | 0.0px | 18.95 |
| Q2 | 11.14 | 521 | 67.1% | 0.0px | 24.9 |
| Q3 | 13.63 | 551 | 68.6% | 0.0px | 28.05 |
| Q4 | 15.87 | 607 | 71.1% | 0.0px | 27.9 |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
|--------|----------|--------|---------|-------------------|
| Q1 | 40.4% | 72.4% | 61.0% | **Dogfighter** |
| Q2 | 23.9% | 76.4% | 73.8% | **Dogfighter** |
| Q3 | 22.9% | 69.0% | 89.5% | **Dogfighter** |
| Q4 | 12.7% | 57.0% | 88.6% | **Dogfighter** |

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
| Start (0-25%) | 19.0 | 6.2% | Balanced |
| Mid-Game (25-50%) | 111.6 | 36.6% | Balanced |
| Late-Game (50-75%) | 152.2 | 49.9% | Balanced |
| End-Game (75-100%) | 22.2 | 7.3% | Balanced |

## Recent Generations (Last 30)

<details>
<summary>Click to expand Recent Generations table</summary>

| Gen   | Best   | Avg    | StdDev | Kills  | Steps  | Acc%   | Stag   |
|-------|--------|--------|--------|--------|--------|--------|--------|
| 1     | 292    | 81     | 105    | 4.9    | 362    | 49     | 0      |
| 2     | 434    | 182    | 130    | 8.7    | 443    | 58     | 0      |
| 3     | 449    | 248    | 97     | 11.9   | 535    | 68     | 0      |
| 4     | 530    | 205    | 146    | 10.4   | 507    | 66     | 0      |
| 5     | 507    | 269    | 130    | 13.1   | 550    | 69     | 1      |
| 6     | 656    | 285    | 140    | 14.2   | 551    | 69     | 0      |
| 7     | 522    | 275    | 127    | 13.4   | 539    | 68     | 1      |
| 8     | 526    | 300    | 140    | 16.4   | 622    | 72     | 2      |
| 9     | 631    | 337    | 125    | 17.3   | 647    | 73     | 3      |
| 10    | 482    | 305    | 116    | 16.4   | 619    | 72     | 4      |

</details>


## Top 10 Best Generations

<details>
<summary>Click to expand Top 10 Best Generations table</summary>

| Rank | Gen   | Best   | Avg    | Kills  | Steps  | Accuracy |
|------|-------|--------|--------|--------|--------|----------|
| 1    | 6     | 656    | 285    | 28.1   | 862    | 84.9     |
| 2    | 9     | 631    | 337    | 27.9   | 874    | 81.4     |
| 3    | 4     | 530    | 205    | 22.3   | 749    | 80.1     |
| 4    | 8     | 526    | 300    | 26.0   | 812    | 81.2     |
| 5    | 7     | 522    | 275    | 22.2   | 715    | 80.3     |
| 6    | 5     | 507    | 269    | 20.6   | 768    | 85.5     |
| 7    | 10    | 482    | 305    | 25.8   | 814    | 79.6     |
| 8    | 3     | 449    | 248    | 19.1   | 772    | 82.2     |
| 9    | 2     | 434    | 182    | 18.9   | 758    | 75.6     |
| 10   | 1     | 292    | 81     | 13.1   | 528    | 74.2     |

</details>


## Trend Analysis

| Period | Avg Best | Avg Mean | Avg Min | Improvement |
|--------|----------|----------|---------|-------------|
| Q1 | 363.2 | 131.5 | -47.2 |  |
| Q2 | 489.3 | 226.5 | 38.9 | +126.1 |
| Q3 | 581.9 | 276.9 | 44.2 | +92.6 |
| Q4 | 540.3 | 304.2 | 57.9 | -41.6 |


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

     656 |     *    
     613 |        * 
     569 |          
     525 |   *   *  
     481 |    * *  *
     438 |  *       
     394 | *        
     350 |          
     306 |        o 
     263 |*   oooo o
     219 |  o       
     175 | o o      
     131 |          
      88 |          
      44 |o         
       0 |          
         ----------
         Gen 1Gen 10
```


---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 0.00s
- **Evaluation (Simulation):** 58.41s (0.0%)
- **Evolution (GA Operators):** 0.0089s (0.0%)

| Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
|-----------|---------------|---------------|------------|
| 1-1 | 32.75s | 0.0000s | 0.00s |
| 2-2 | 44.59s | 0.0071s | 0.00s |
| 3-3 | 56.88s | 0.0069s | 0.00s |
| 4-4 | 56.18s | 0.0111s | 0.00s |
| 5-5 | 62.59s | 0.0090s | 0.00s |
| 6-6 | 61.11s | 0.0163s | 0.00s |
| 7-7 | 58.73s | 0.0107s | 0.00s |
| 8-8 | 68.58s | 0.0105s | 0.00s |
| 9-9 | 73.91s | 0.0085s | 0.00s |
| 10-10 | 68.81s | 0.0090s | 0.00s |

## Genetic Operator Statistics

**Recent Averages (Population: 25)**
- **Crossovers:** 8.7 (34.8%)
- **Mutations:** 22.5 (90.0%)
- **Elites Preserved:** 1.8

