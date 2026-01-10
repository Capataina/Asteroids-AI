# Training Summary Report

**Generated:** 2026-01-10 16:24:45
**Schema Version:** 2.0

## Quick Trend Overview

```
Best Fitness: 325 → 448   [▁█] +38%
Avg Fitness:  66 → 109   [▁█] +65%
Avg Kills:    3.9 → 6.1   [▁█] +57%
Avg Accuracy: 51% → 59%   [▁█] +17%
Avg Steps:    276 → 322   [▁█] +17%
Diversity:    95 → 105   [▁█] +10%
```

## Training Configuration

```
population_size: 50
num_generations: 500
mutation_probability: 0.2
mutation_gaussian_sigma: 0.15
crossover_probability: 0.7
max_workers: 16
frame_delay: 0.016666666666666666
```

## Overall Summary

- **Total Generations:** 2
- **Training Duration:** 0:00:44.905773
- **All-Time Best Fitness:** 448.31
- **Best Generation:** 2
- **Final Best Fitness:** 448.31
- **Final Average Fitness:** 109.05
- **Avg Improvement (Early->Late):** 0.00
- **Stagnation:** 0 generations since improvement

**Generalization (Fresh Game Performance):**
- Avg Generalization Ratio: 0.64
- Best Fresh Fitness: 207.59 (Gen 1)
- Episode Completion Rate: 0.0%

## Generation Highlights

Not enough data for generation highlights.

## Training Progress by Decile

Not enough data for decile breakdown (need at least 5 generations).

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 1.91 (up from 1.42 in Phase 1)
- **Shots per Kill:** 2.57 (down from 2.82 in Phase 1)
- **Kill Conversion Rate:** 38.9% (up from 35.5% in Phase 1)
- **Average Kills per Episode:** 6.1

### Efficiency Trend

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 | 1.42 | 2.82 | 35.5% |
| Phase 2 | 1.91 | 2.57 | 38.9% |

**Assessment:** Agent shows slight efficiency improvement. Shots per kill dropped 9%.

## Learning Velocity

Not enough data for velocity analysis (need at least 10 generations).

## Reward Component Evolution

| Component | Phase 1 | Mid | Final | Trend | Status |
|-----------|---------|-----|-------|-------|--------|
| DeathPenalty | -75.0 | -75.0 | -75.0 | → +0% | Not learned |
| DistanceBasedKillReward | +44.6 | +69.3 | +69.3 | ↑↑ +55% | Learned |
| ConservingAmmoBonus | +38.5 | +63.8 | +63.8 | ↑↑ +66% | Learned |
| ExplorationBonus | +44.2 | +34.8 | +34.8 | ↓ -21% | Stable |
| SurvivalBonus | +13.8 | +16.1 | +16.1 | ↑ +17% | Learned |

## Reward Balance Analysis

### Warnings

- **DeathPenalty consistently negative** - This component has been negative throughout training, averaging -75.0/episode. The intended behavior may not be incentivized strongly enough, or there may be a conflict with other rewards.

### Confirmations

- **Reward reasonably balanced** - No single component >60%
- **SurvivalBonus positive** - Agents are learning to stay alive

### Recommendations

- Consider increasing the magnitude of consistently negative reward components
- Check if there are conflicting incentives preventing the behavior

## Population Health Dashboard

Not enough data for population health analysis.

## Stagnation Analysis

No stagnation periods detected - fitness improved every generation!

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Ratio | Grade | Cause of Death |
|-----|--------------|-----------|-------|-------|----------------|
| 1 | 325 | 208 | 0.64 | C | asteroid_collision |

### Generalization Summary

- **Average Fitness Ratio:** 0.64
- **Best Ratio:** 0.64
- **Worst Ratio:** 0.64

**Grade Distribution:** C:1 

## Correlation Analysis

Not enough data for correlation analysis.

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 322 steps (21.4% of max)
- **Max Survival:** 644 steps

### Survival Progression

| Phase | Mean Steps | Change |
|-------|------------|--------|
| Phase 1 | 276 |  |
| Phase 2 | 322 | +46 |

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 5.03
- **Avg Steps Survived:** 299
- **Avg Accuracy:** 55.1%
- **Max Kills (Any Agent Ever):** 21.166666666666668
- **Max Steps (Any Agent Ever):** 643.8333333333334

## Learning Progress

Not enough data for learning analysis.

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 100.43
- Average Range (Best-Min): 425.12
- Diversity Change: +0.0%
- **Status:** Population is converging (low diversity)

## Behavioral Trends

Not enough data for behavioral trend analysis.

## Recent Generations (Last 30)

| Gen | Best | Avg | StdDev | Kills | Steps | Acc% | Stag |
|-----|------|-----|--------|-------|-------|------|------|
| 1 | 325 | 66 | 95 | 3.9 | 276 | 51 | 0 |
| 2 | 448 | 109 | 105 | 6.1 | 322 | 59 | 0 |


## Top 10 Best Generations

| Rank | Gen | Best | Avg | Kills | Steps | Accuracy |
|------|-----|------|-----|-------|-------|----------|
| 1 | 2 | 448 | 109 | 21.166666666666668 | 643.8333333333334 | 84.6% |
| 2 | 1 | 325 | 66 | 15.5 | 520.1666666666666 | 74.6% |


## Trend Analysis

Not enough data for trend analysis.


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

     448 | *
     418 |  
     389 |  
     359 |  
     329 |  
     299 |* 
     269 |  
     239 |  
     209 |  
     179 |  
     149 |  
     120 |  
      90 | o
      60 |o 
      30 |  
       0 |  
         --
         Gen 1Gen 2
```

