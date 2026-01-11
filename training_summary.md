# Training Summary Report

**Generated:** 2026-01-11 01:18:52
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
Best Fitness: 549 → 690   [▁▂█▃▅] +26%
Avg Fitness:  136 → 370   [▁▁▄▆█] +172%
Avg Kills:    7.1 → 20.4   [▁▁▄▆█] +187%
Avg Accuracy: 63% → 62%   [▄▁█▅▃] -2%
Avg Steps:    468 → 685   [▁▁▅▅█] +46%
Diversity:    139 → 138   [▁▁█▆▁] -1%
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

- **Total Generations:** 5
- **Training Duration:** 0:03:50.247048
- **All-Time Best Fitness:** 760.24
- **Best Generation:** 3
- **Final Best Fitness:** 690.22
- **Final Average Fitness:** 370.37
- **Avg Improvement (Early->Late):** 0.00
- **Stagnation:** 2 generations since improvement

**Generalization (Fresh Game Performance):**
- Avg Generalization Ratio: 0.06
- Best Fresh Fitness: 38.17 (Gen 4)
- Episode Completion Rate: 0.0%

## Best Agent Deep Profile

The most fit agent appeared in **Generation 3** with a fitness of **760.24**.

### Combat Efficiency

- **Total Kills:** 34.833333333333336
- **Survival Time:** 16.8 seconds (1006.0833333333334 steps)
- **Accuracy:** 81.4%
- **Shots per Kill:** 1.2
- **Time per Kill:** 0.48 seconds

### Behavioral Signature

**Classification:** `Dogfighter`

| Action | Rate (per step) | Description |
|--------|-----------------|-------------|
| **Thrust** | 12.4% | Movement frequency |
| **Turn** | 52.7% | Rotation frequency |
| **Shoot** | 39.3% | Trigger discipline |

### Spatial Analytics (Best Agent)

**Position Heatmap (Where does it fly?)**
```
|          |
|          |
|     .    |
|     .    |
|     @    |
|          |
|          |
|          |
|     .    |
|          |
```

**Kill Zone Heatmap (Where does it kill?)**
```
|     :.   |
|     :    |
|     -    |
|     +    |
|     @.   |
|.    .    |
|     .    |
|     ..   |
|     %    |
|     ..:  |
```

## Generation Highlights

### Best Improvement

**Generation 3**: Best fitness jumped +168.8 (+28.5%)
- New best fitness: 760.2

### Worst Regression

**Generation 4**: Best fitness dropped -140.1 (-18.4%)
- New best fitness: 620.1
- *Note: This may be normal variation after a lucky outlier*

### Most Accurate Generation

**Generation 3**: Population accuracy reached 67.2%

### Most Kills (Single Agent)

**Generation 3**: An agent achieved 35 kills

### First Viable Population

**Generation 1**: Average fitness first became positive

### Most Diverse Generation

**Generation 2**: Diversity index 1.08

### Most Converged Generation

**Generation 5**: Diversity index 0.37

## Milestone Timeline

| Generation | Category | Value | Description |
|------------|----------|-------|-------------|
| 1 | Fitness | 549 | Best fitness crossed 100 |
| 1 | Fitness | 549 | Best fitness crossed 500 |
| 1 | Kills | 26.75 | First agent to achieve 1 kills |
| 1 | Kills | 26.75 | First agent to achieve 5 kills |
| 1 | Kills | 26.75 | First agent to achieve 10 kills |
| 1 | Kills | 26.75 | First agent to achieve 20 kills |

## Training Progress by Decile

| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|------|----------|---------|-----------|---------|-----------|----------|
| 0-20% | 1-1 | 549 | 136 | 7.1 | 63% | 468 | 139 |
| 20-40% | 2-2 | 591 | 130 | 7.8 | 59% | 452 | 141 |
| 40-60% | 3-3 | 760 | 264 | 13.6 | 67% | 591 | 199 |
| 60-80% | 4-4 | 620 | 310 | 16.9 | 65% | 613 | 184 |
| 80-100% | 5-5 | 690 | 370 | 20.4 | 62% | 685 | 138 |

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 2.98 (up from 1.52 in Phase 1)
- **Shots per Kill:** 2.08 (down from 2.71 in Phase 1)
- **Kill Conversion Rate:** 48.0% (up from 36.9% in Phase 1)
- **Average Kills per Episode:** 20.4

### Efficiency Trend

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 | 1.52 | 2.71 | 36.9% |
| Phase 2 | 1.73 | 2.79 | 35.9% |
| Phase 3 | 2.31 | 2.28 | 43.9% |
| Phase 4 | 2.75 | 2.12 | 47.3% |
| Phase 5 | 2.98 | 2.08 | 48.0% |

**Assessment:** Agent has improved efficiency moderately. Shots per kill dropped 23%.

## Learning Velocity

Not enough data for velocity analysis (need at least 10 generations).

## Reward Component Evolution

| Component | Phase 1 | Mid | Final | Trend | Status |
|-----------|---------|-----|-------|-------|--------|
| DistanceBasedKillReward | +88.8 | +172.1 | +264.6 | ↑↑↑ +198% | Learned |
| ConservingAmmoBonus | +82.3 | +142.1 | +181.3 | ↑↑↑ +120% | Learned |
| DeathPenalty | -149.5 | -145.5 | -142.0 | → +5% | Improving |
| ExplorationBonus | +61.4 | +51.8 | +35.0 | ↓ -43% | Stable |
| VelocitySurvivalBonus | +53.4 | +43.6 | +31.4 | ↓ -41% | Stable |

**Exploration Efficiency (Final Phase):** 0.0512 score/step
- *Note: A higher rate indicates faster map traversal, independent of survival time.*

## Reward Balance Analysis

### Warnings

- **DeathPenalty consistently negative** - This component has been negative throughout training, averaging -142.0/episode. The intended behavior may not be incentivized strongly enough, or there may be a conflict with other rewards.

- **DistanceBasedKillReward is dominant (52%)** - This component accounts for a large portion of positive reward. Consider if this is intentional.

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
| Diversity Index | 0.66 | → Stable | 🟢 Good |
| Elite Gap | 1.65 | → | 🟢 Good |
| Min Fitness Trend | +0.0 | ↓ | 🟢 Good |
| Max Fitness Trend | +0.0 | ↓ | 🟡 Watch |
| IQR (p75-p25) | 209 | ↑ 0 | 🟢 |

## Stagnation Analysis

- **Current Stagnation:** 2 generations
- **Average Stagnation Period:** 2.0 generations
- **Longest Stagnation:** 2 generations
- **Number of Stagnation Periods:** 1

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Accuracy | Ratio | Grade | Cause of Death |
|-----|--------------|-----------|----------|-------|-------|----------------|
| 1 | 549 | -154 | 14.3% | -0.28 | F | asteroid_collision |
| 2 | 591 | -102 | 12.2% | -0.17 | F | asteroid_collision |
| 3 | 760 | -15 | 13.8% | -0.02 | F | asteroid_collision |
| 4 | 620 | 38 | 23.7% | 0.06 | F | asteroid_collision |

### Generalization Summary

- **Average Fitness Ratio:** 0.06
- **Best Ratio:** 0.06
- **Worst Ratio:** 0.06

**Grade Distribution:** F:4 

## Correlation Analysis

Not enough data for correlation analysis.

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 685 steps (45.7% of max)
- **Max Survival:** 930 steps

### Survival Progression

| Phase | Mean Steps | Change |
|-------|------------|--------|
| Phase 1 | 468 |  |
| Phase 2 | 452 | -16 |
| Phase 3 | 591 | +139 |
| Phase 4 | 613 | +22 |
| Phase 5 | 685 | +71 |

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 13.17
- **Avg Steps Survived:** 562
- **Avg Accuracy:** 63.2%
- **Max Kills (Any Agent Ever):** 34.833333333333336
- **Max Steps (Any Agent Ever):** 1006.0833333333334

## Learning Progress

**Comparing First 1 vs Last 1 Generations:**

| Metric | Early | Late | Change |
|--------|-------|------|--------|
| Best Fitness | 548.8 | 690.2 | +25.8% |
| Avg Fitness | 136.4 | 370.4 | +171.5% |

**Verdict:** Moderate learning - some improvement but room for more training.

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 160.34
- Average Range (Best-Min): 651.21
- Diversity Change: +0.0%
- **Status:** Population is converging (low diversity)

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Safe Dist | Max Kills |
|--------|-----------|-----------|--------------|-----------|----------|
| Q1 | 7.11 | 468 | 63.2% | 0.0px | 26.75 |
| Q2 | 7.81 | 452 | 58.9% | 0.0px | 27.916666666666668 |
| Q3 | 13.64 | 591 | 67.2% | 0.0px | 34.833333333333336 |
| Q4 | 18.65 | 649 | 63.4% | 0.0px | 31.25 |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
|--------|----------|--------|---------|-------------------|
| Q1 | 15222.7% | 34494.7% | 23709.7% | **Dogfighter** |
| Q2 | 12771.0% | 38291.7% | 27673.7% | **Dogfighter** |
| Q3 | 12435.0% | 53009.0% | 39560.0% | **Dogfighter** |
| Q4 | 6142.0% | 64240.7% | 52375.0% | **Dogfighter** |

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
| Start (0-25%) | -5.2 | -1.4% | Balanced |
| Mid-Game (25-50%) | 113.0 | 30.5% | Balanced |
| Late-Game (50-75%) | 187.4 | 50.6% | Balanced |
| End-Game (75-100%) | 75.2 | 20.3% | Balanced |

## Recent Generations (Last 30)

<details>
<summary>Click to expand Recent Generations table</summary>

| Gen   | Best   | Avg    | StdDev | Kills  | Steps  | Acc%   | Stag   |
|-------|--------|--------|--------|--------|--------|--------|--------|
| 1     | 549    | 136    | 139    | 7.1    | 468    | 63     | 0      |
| 2     | 591    | 130    | 141    | 7.8    | 452    | 59     | 0      |
| 3     | 760    | 264    | 199    | 13.6   | 591    | 67     | 0      |
| 4     | 620    | 310    | 184    | 16.9   | 613    | 65     | 1      |
| 5     | 690    | 370    | 138    | 20.4   | 685    | 62     | 2      |

</details>


## Top 10 Best Generations

<details>
<summary>Click to expand Top 10 Best Generations table</summary>

| Rank | Gen   | Best   | Avg    | Kills  | Steps  | Accuracy |
|------|-------|--------|--------|--------|--------|----------|
| 1    | 3     | 760    | 264    | 34.8   | 1006   | 81.4     |
| 2    | 5     | 690    | 370    | 31.2   | 892    | 71.6     |
| 3    | 4     | 620    | 310    | 29.8   | 887    | 79.8     |
| 4    | 2     | 591    | 130    | 27.9   | 833    | 84.4     |
| 5    | 1     | 549    | 136    | 26.8   | 810    | 79.3     |

</details>


## Trend Analysis

Not enough data for trend analysis.


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

     760 |  *  
     710 |     
     659 |    *
     608 |   * 
     558 | *   
     507 |*    
     456 |     
     405 |     
     355 |    o
     304 |   o 
     253 |  o  
     203 |     
     152 |     
     101 |oo   
      51 |     
       0 |     
         -----
         Gen 1Gen 5
```


---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 36.89s
- **Evaluation (Simulation):** 36.88s (100.0%)
- **Evolution (GA Operators):** 0.0073s (0.0%)

| Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
|-----------|---------------|---------------|------------|
| 1-1 | 25.93s | 0.0000s | 25.93s |
| 2-2 | 26.31s | 0.0070s | 26.32s |
| 3-3 | 38.22s | 0.0125s | 38.23s |
| 4-4 | 42.64s | 0.0089s | 42.65s |
| 5-5 | 51.31s | 0.0079s | 51.32s |

## Genetic Operator Statistics

**Recent Averages (Population: 25)**
- **Crossovers:** 7.6 (30.4%)
- **Mutations:** 20.0 (80.0%)
- **Elites Preserved:** 1.6

