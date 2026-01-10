# Training Summary Report

**Generated:** 2026-01-10 18:52:13
**Schema Version:** 2.0

## Quick Trend Overview

```
Best Fitness: 166 → 405   [▁▅▇▆▄▄▅▆█▅] +145%
Avg Fitness:  -7 → 109   [▁▆▆▆█▇▆▇▇▇] +1748%
Avg Kills:    3.1 → 10.3   [▁▆▆▇█▇▆▇▇▇] +231%
Avg Accuracy: 46% → 67%   [▁▆▆▆█▇▅▆▇▇] +44%
Avg Steps:    251 → 400   [▁▆▆▆█▇▇▇▆▆] +59%
Diversity:    62 → 114   [▁▇▇▆▆▃▇█▇▄] +83%
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

- **Total Generations:** 44
- **Training Duration:** 0:22:02.177761
- **All-Time Best Fitness:** 542.14
- **Best Generation:** 18
- **Final Best Fitness:** 405.18
- **Final Average Fitness:** 109.43
- **Avg Improvement (Early->Late):** 47.24
- **Stagnation:** 26 generations since improvement

**Generalization (Fresh Game Performance):**
- Avg Generalization Ratio: 0.38
- Best Fresh Fitness: 446.92 (Gen 1)
- Episode Completion Rate: 2.3%

## Best Agent Deep Profile

The most fit agent appeared in **Generation 18** with a fitness of **542.14**.

### Combat Efficiency

- **Total Kills:** 30.0
- **Survival Time:** 13.8 seconds (828.6666666666666 steps)
- **Accuracy:** 86.1%
- **Shots per Kill:** 1.1
- **Time per Kill:** 0.46 seconds

### Behavioral Signature

**Classification:** `Spinner`

| Action | Rate (per step) | Description |
|--------|-----------------|-------------|
| **Thrust** | 3.4% | Movement frequency |
| **Turn** | 33.2% | Rotation frequency |
| **Shoot** | 38.5% | Trigger discipline |

## Generation Highlights

### Best Improvement

**Generation 18**: Best fitness jumped +219.8 (+68.2%)
- New best fitness: 542.1

### Worst Regression

**Generation 19**: Best fitness dropped -209.0 (-38.5%)
- New best fitness: 333.2
- *Note: This may be normal variation after a lucky outlier*

### Most Accurate Generation

**Generation 15**: Population accuracy reached 73.3%

### Most Kills (Single Agent)

**Generation 18**: An agent achieved 30 kills

### First Viable Population

**Generation 2**: Average fitness first became positive

### Most Diverse Generation

**Generation 1**: Diversity index 9.36

### Most Converged Generation

**Generation 31**: Diversity index 0.58

## Milestone Timeline

| Generation | Category | Value | Description |
|------------|----------|-------|-------------|
| 1 | Fitness | 166 | Best fitness crossed 100 |
| 1 | Kills | 14.0 | First agent to achieve 1 kills |
| 1 | Kills | 14.0 | First agent to achieve 5 kills |
| 1 | Kills | 14.0 | First agent to achieve 10 kills |
| 5 | Kills | 23.5 | First agent to achieve 20 kills |
| 7 | Fitness | 503 | Best fitness crossed 500 |

## Training Progress by Decile

| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|------|----------|---------|-----------|---------|-----------|----------|
| 0-10% | 1-4 | 306 | 31 | 5.2 | 56% | 304 | 83 |
| 10-20% | 5-8 | 503 | 104 | 10.0 | 67% | 395 | 108 |
| 20-30% | 9-12 | 455 | 114 | 10.6 | 68% | 397 | 106 |
| 30-40% | 13-16 | 502 | 133 | 11.4 | 72% | 432 | 107 |
| 40-50% | 17-20 | 542 | 122 | 10.8 | 70% | 418 | 106 |
| 50-60% | 21-24 | 339 | 116 | 10.9 | 67% | 416 | 94 |
| 60-70% | 25-28 | 428 | 114 | 10.4 | 66% | 404 | 108 |
| 70-80% | 29-32 | 435 | 136 | 11.0 | 70% | 409 | 99 |
| 80-90% | 33-36 | 523 | 141 | 11.0 | 70% | 402 | 114 |
| 90-100% | 37-44 | 489 | 120 | 10.5 | 70% | 399 | 105 |

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 2.64 (up from 1.72 in Phase 1)
- **Shots per Kill:** 2.30 (down from 2.71 in Phase 1)
- **Kill Conversion Rate:** 43.6% (up from 36.9% in Phase 1)
- **Average Kills per Episode:** 10.7

### Efficiency Trend

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 | 2.18 | 2.43 | 41.1% |
| Phase 2 | 2.66 | 2.29 | 43.7% |
| Phase 3 | 2.59 | 2.27 | 44.1% |
| Phase 4 | 2.64 | 2.32 | 43.2% |
| Phase 5 | 2.67 | 2.30 | 43.4% |

**Assessment:** Agent shows slight efficiency improvement. Shots per kill dropped 15%.

## Learning Velocity

### Velocity by Phase

| Phase | Fitness Delta | Delta/Gen | Velocity | Trend |
|-------|---------------|-----------|----------|-------|
| Phase 1 | +130 | +16.3 | Moderate |  |
| Phase 2 | -54 | -6.8 | Stalled | ↓ Slowing |
| Phase 3 | -39 | -4.9 | Stalled | ↑ Accelerating |
| Phase 4 | +10 | +1.3 | Slow | ↑ Accelerating |
| Phase 5 | -85 | -7.1 | Stalled | ↓ Slowing |

### Current Velocity

- **Recent Improvement Rate:** -7.1 fitness/generation
- **Acceleration:** -8.3 (learning slowing down)
- **Projected Generations to +50% Fitness:** N/A (not improving)

### Velocity Assessment

Learning has stalled. Fitness is no longer improving. Consider:
- Stopping training (may have converged)
- Restarting with different hyperparameters
- Reviewing reward structure

## Reward Component Evolution

| Component | Phase 1 | Mid | Final | Trend | Status |
|-----------|---------|-----|-------|-------|--------|
| DeathPenalty | -150.0 | -150.0 | -149.8 | → +0% | Improving |
| DistanceBasedKillReward | +59.6 | +124.6 | +120.2 | ↑↑↑ +102% | Learned |
| ConservingAmmoBonus | +51.1 | +108.6 | +111.3 | ↑↑↑ +118% | Learned |
| ExplorationBonus | +41.2 | +22.7 | +24.8 | ↓ -40% | Stable |
| VelocitySurvivalBonus | +29.4 | +10.2 | +13.4 | ↓↓ -55% | Stable |

## Reward Balance Analysis

### Warnings

- **DeathPenalty consistently negative** - This component has been negative throughout training, averaging -149.8/episode. The intended behavior may not be incentivized strongly enough, or there may be a conflict with other rewards.

- **DistanceBasedKillReward is dominant (46%)** - This component accounts for a large portion of positive reward. Consider if this is intentional.

- **ConservingAmmoBonus is dominant (43%)** - This component accounts for a large portion of positive reward. Consider if this is intentional.

- **VelocitySurvivalBonus declining** - This component dropped from 29.4 to 13.4. The agent may be trading off this behavior for others.

- **High penalty ratio (57.7%)** - Negative rewards are 58% of positive rewards. Agents may be struggling to achieve net positive fitness.

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
| Diversity Index | 0.86 | ↑ Increasing | 🟡 Watch |
| Elite Gap | 2.32 | → | 🟡 Watch |
| Min Fitness Trend | +40.1 | ↑ | 🟢 Good |
| Max Fitness Trend | +87.5 | ↑ | 🟢 Good |
| IQR (p75-p25) | 146 | ↑ 7 | 🟢 |

## Stagnation Analysis

- **Current Stagnation:** 26 generations
- **Average Stagnation Period:** 9.5 generations
- **Longest Stagnation:** 26 generations
- **Number of Stagnation Periods:** 4

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Ratio | Grade | Cause of Death |
|-----|--------------|-----------|-------|-------|----------------|
| 34 | 523 | -87 | -0.17 | F | asteroid_collision |
| 35 | 467 | -18 | -0.04 | F | asteroid_collision |
| 36 | 483 | -119 | -0.25 | F | asteroid_collision |
| 37 | 382 | -42 | -0.11 | F | asteroid_collision |
| 38 | 489 | -92 | -0.19 | F | asteroid_collision |
| 39 | 405 | 56 | 0.14 | F | asteroid_collision |
| 40 | 345 | -89 | -0.26 | F | asteroid_collision |
| 41 | 385 | -58 | -0.15 | F | asteroid_collision |
| 42 | 337 | 9 | 0.03 | F | asteroid_collision |
| 43 | 437 | 323 | 0.74 | B | completed_episode |

### Generalization Summary

- **Average Fitness Ratio:** 0.38
- **Best Ratio:** 2.70
- **Worst Ratio:** 0.01

**Grade Distribution:** A:1 B:1 D:3 F:38 

## Correlation Analysis

### Fitness Correlations

| Metric | Correlation | Strength |
|--------|-------------|----------|
| Kills | +0.98 | Strong |
| Steps Survived | +0.98 | Strong |
| Accuracy | +0.92 | Strong |

### Interpretation

Fitness is most strongly predicted by kills (r=0.98).

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 404 steps (27.0% of max)
- **Max Survival:** 703 steps

### Survival Progression

| Phase | Mean Steps | Change |
|-------|------------|--------|
| Phase 1 | 349 |  |
| Phase 2 | 414 | +65 |
| Phase 3 | 417 | +3 |
| Phase 4 | 406 | -11 |
| Phase 5 | 400 | -6 |

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 10.64
- **Avg Steps Survived:** 401
- **Avg Accuracy:** 70.1%
- **Max Kills (Any Agent Ever):** 30.0
- **Max Steps (Any Agent Ever):** 828.6666666666666

## Learning Progress

**Comparing First 4 vs Last 4 Generations:**

| Metric | Early | Late | Change |
|--------|-------|------|--------|
| Best Fitness | 249.3 | 390.9 | +56.8% |
| Avg Fitness | 31.4 | 119.9 | +281.7% |

**Verdict:** Strong learning - both best and average fitness improved significantly.

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 106.26
- Average Range (Best-Min): 474.08
- Diversity Change: +9.9%
- **Status:** Population is converging (low diversity)

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Max Kills |
|--------|-----------|-----------|--------------|----------|
| Q1 | 8.34 | 361 | 62.7% | 27.0 |
| Q2 | 11.14 | 423 | 70.4% | 30.0 |
| Q3 | 10.68 | 406 | 67.6% | 25.5 |
| Q4 | 10.68 | 401 | 69.9% | 28.166666666666668 |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
|--------|----------|--------|---------|-------------------|
| Q1 | 5445.5% | 27083.2% | 29638.9% | **Dogfighter** |
| Q2 | 2357.6% | 30078.8% | 38168.5% | **Dogfighter** |
| Q3 | 3724.9% | 20128.1% | 37932.8% | **Dogfighter** |
| Q4 | 4236.2% | 31438.9% | 37894.0% | **Dogfighter** |

## Recent Generations (Last 30)

| Gen | Best | Avg | StdDev | Kills | Steps | Acc% | Stag |
|-----|------|-----|--------|-------|-------|------|------|
| 15 | 502 | 138 | 116 | 11.7 | 447 | 73 | 8 |
| 16 | 401 | 138 | 110 | 11.7 | 441 | 72 | 9 |
| 17 | 322 | 144 | 107 | 11.8 | 433 | 73 | 10 |
| 18 | 542 | 91 | 126 | 9.5 | 395 | 68 | 0 |
| 19 | 333 | 126 | 91 | 10.9 | 431 | 70 | 1 |
| 20 | 365 | 126 | 99 | 10.8 | 414 | 70 | 2 |
| 21 | 329 | 133 | 84 | 11.3 | 427 | 70 | 3 |
| 22 | 313 | 117 | 100 | 11.1 | 415 | 67 | 4 |
| 23 | 339 | 113 | 92 | 10.8 | 417 | 67 | 5 |
| 24 | 283 | 101 | 99 | 10.4 | 406 | 64 | 6 |
| 25 | 367 | 109 | 115 | 10.4 | 408 | 64 | 7 |
| 26 | 322 | 95 | 92 | 9.8 | 396 | 63 | 8 |
| 27 | 399 | 128 | 120 | 11.0 | 417 | 67 | 9 |
| 28 | 428 | 123 | 105 | 10.5 | 394 | 69 | 10 |
| 29 | 435 | 136 | 115 | 11.2 | 416 | 69 | 11 |
| 30 | 397 | 127 | 104 | 10.8 | 409 | 69 | 12 |
| 31 | 379 | 144 | 83 | 11.3 | 412 | 72 | 13 |
| 32 | 377 | 138 | 92 | 10.7 | 397 | 70 | 14 |
| 33 | 490 | 139 | 108 | 10.7 | 392 | 69 | 15 |
| 34 | 523 | 139 | 121 | 11.0 | 400 | 68 | 16 |
| 35 | 467 | 143 | 117 | 11.0 | 402 | 71 | 17 |
| 36 | 483 | 143 | 110 | 11.4 | 412 | 71 | 18 |
| 37 | 382 | 127 | 85 | 10.9 | 406 | 73 | 19 |
| 38 | 489 | 126 | 106 | 10.7 | 397 | 71 | 20 |
| 39 | 405 | 121 | 108 | 10.0 | 386 | 69 | 21 |
| 40 | 345 | 106 | 105 | 9.8 | 386 | 71 | 22 |
| 41 | 385 | 122 | 127 | 11.0 | 407 | 68 | 23 |
| 42 | 337 | 119 | 101 | 10.8 | 404 | 71 | 24 |
| 43 | 437 | 129 | 98 | 10.6 | 407 | 70 | 25 |
| 44 | 405 | 109 | 114 | 10.3 | 400 | 67 | 26 |


## Top 10 Best Generations

| Rank | Gen | Best | Avg | Kills | Steps | Accuracy |
|------|-----|------|-----|-------|-------|----------|
| 1 | 18 | 542 | 91 | 30.0 | 828.6666666666666 | 86.1% |
| 2 | 34 | 523 | 139 | 28.166666666666668 | 815.0 | 88.1% |
| 3 | 7 | 503 | 124 | 27.0 | 819.1666666666666 | 78.9% |
| 4 | 15 | 502 | 138 | 26.833333333333332 | 767.8333333333334 | 93.8% |
| 5 | 33 | 490 | 139 | 25.5 | 729.5 | 90.8% |
| 6 | 38 | 489 | 126 | 24.0 | 757.6666666666666 | 91.8% |
| 7 | 36 | 483 | 143 | 25.5 | 715.3333333333334 | 81.2% |
| 8 | 35 | 467 | 143 | 22.166666666666668 | 678.1666666666666 | 87.9% |
| 9 | 9 | 455 | 112 | 22.833333333333332 | 696.0 | 93.2% |
| 10 | 11 | 445 | 97 | 25.833333333333332 | 762.6666666666666 | 88.0% |


## Trend Analysis

| Period | Avg Best | Avg Mean | Avg Min | Improvement |
|--------|----------|----------|---------|-------------|
| Q1 | 336.7 | 79.2 | -105.1 |  |
| Q2 | 391.1 | 127.2 | -79.4 | +54.4 |
| Q3 | 383.3 | 123.0 | -67.1 | -7.8 |
| Q4 | 423.3 | 125.9 | -62.6 | +40.0 |


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

     542 |                 *                          
     506 |                                 *          
     469 |      *       *                 *  * *      
     432 |        * * *               *     *       * 
     396 |           *   *          ** *        *    *
     359 |    *              *    *     **    *   *   
     323 |     *       *    * * *                * *  
     286 |  *    * *      *    *   *                  
     249 | *                     *                    
     213 |   *                                        
     176 |                                            
     140 |*               o             o   oo        
     103 |    o o oo ooooo  ooooo o oooo ooo  oooooooo
      67 |     o o  o      o     o o                  
      30 |  oo                                        
      -7 |oo                                          
         --------------------------------------------
         Gen 1                             Gen 44
```


---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 19.80s
- **Evaluation (Simulation):** 19.78s (99.9%)
- **Evolution (GA Operators):** 0.0163s (0.1%)

| Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
|-----------|---------------|---------------|------------|
| 1-4 | 12.99s | 0.0088s | 13.00s |
| 5-8 | 18.76s | 0.0113s | 18.77s |
| 9-12 | 21.21s | 0.0118s | 21.22s |
| 13-16 | 22.38s | 0.0133s | 22.39s |
| 17-20 | 20.50s | 0.0121s | 20.51s |
| 21-24 | 20.90s | 0.0120s | 20.91s |
| 25-28 | 20.83s | 0.0122s | 20.85s |
| 29-32 | 20.36s | 0.0142s | 20.37s |
| 33-36 | 20.48s | 0.0146s | 20.49s |
| 37-40 | 19.34s | 0.0154s | 19.36s |
| 41-44 | 19.78s | 0.0176s | 19.80s |

## Genetic Operator Statistics

**Recent Averages (Population: 50)**
- **Crossovers:** 16.6 (33.2%)
- **Mutations:** 50.0 (100.0%)
- **Elites Preserved:** 5.0

