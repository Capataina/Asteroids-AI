# Training Summary Report

**Generated:** 2026-01-09 01:53:04
**Schema Version:** 2.0

## Quick Trend Overview

```
Best Fitness: 47 → 82   [▁▂▅▆▇▅▆▄█▅] +73%
Avg Fitness:  -2 → 42   [▁▄▆▆▇▆▇▇█▆] +2827%
Avg Kills:    3.9 → 3.5   [▄▃▃▂▅▁█▅▇▃] -10%
Avg Accuracy: 41% → 55%   [▁▄▄▅▅▄█▆▆▅] +36%
Avg Steps:    294 → 236   [█▁▂▂▂▁▆▄▅▁] -20%
Diversity:    27 → 19   [█▁▆▃▁▁▁▂▁▄] -30%
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

- **Total Generations:** 42
- **Training Duration:** 0:11:17.201011
- **All-Time Best Fitness:** 130.94
- **Best Generation:** 4
- **Final Best Fitness:** 82.05
- **Final Average Fitness:** 41.63
- **Avg Improvement (Early->Late):** 18.19
- **Stagnation:** 38 generations since improvement

**Generalization (Fresh Game Performance):**
- Avg Generalization Ratio: 1.10
- Best Fresh Fitness: 325.59 (Gen 22)
- Episode Completion Rate: 0.0%

## Training Progress by Decile

| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|------|----------|---------|-----------|---------|-----------|----------|
| 0-10% | 1-4 | 131 | 17 | 4.0 | 49% | 278 | 25 |
| 10-20% | 5-8 | 76 | 31 | 3.7 | 51% | 253 | 21 |
| 20-30% | 9-12 | 88 | 36 | 3.5 | 53% | 254 | 20 |
| 30-40% | 13-16 | 100 | 38 | 3.3 | 52% | 245 | 19 |
| 40-50% | 17-20 | 99 | 37 | 3.9 | 54% | 253 | 21 |
| 50-60% | 21-24 | 92 | 40 | 3.6 | 54% | 254 | 19 |
| 60-70% | 25-28 | 109 | 45 | 4.2 | 59% | 267 | 20 |
| 70-80% | 29-32 | 89 | 45 | 4.3 | 59% | 267 | 20 |
| 80-90% | 33-36 | 106 | 48 | 4.4 | 60% | 271 | 18 |
| 90-100% | 37-42 | 119 | 42 | 3.8 | 57% | 254 | 21 |

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 1.45 (up from 1.43 in Phase 1)
- **Shots per Kill:** 3.46 (down from 2.96 in Phase 1)
- **Kill Conversion Rate:** 28.9% (up from 33.7% in Phase 1)
- **Average Kills per Episode:** 3.6

### Efficiency Trend

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 | 1.44 | 3.14 | 31.9% |
| Phase 2 | 1.36 | 3.46 | 28.9% |
| Phase 3 | 1.47 | 3.41 | 29.4% |
| Phase 4 | 1.60 | 3.24 | 30.9% |
| Phase 5 | 1.54 | 3.30 | 30.3% |

**Assessment:** Agent efficiency has not improved significantly.

## Reward Component Evolution

| Component | Phase 1 | Mid | Final | Trend | Status |
|-----------|---------|-----|-------|-------|--------|
| DeathPenalty | -50.0 | -50.0 | -50.0 | → +0% | Not learned |
| MaintainingMomentumBonus | +14.0 | +35.3 | +39.0 | ↑↑↑ +179% | Learned |
| NearMiss | +33.5 | +33.3 | +32.4 | → -4% | Stable |
| SurvivalBonus | +13.9 | +12.6 | +12.5 | → -10% | Stable |
| MovingTowardDangerBonus | +6.3 | +8.7 | +8.6 | ↑ +37% | Learned |
| ProximityPenalty | -0.4 | -0.3 | -0.4 | ↑ +13% | Improving |

## Population Health Dashboard

### Current Status: 🟢 Healthy

| Metric | Value | Trend (Recent) | Status |
|--------|-------|----------------|--------|
| Diversity Index | 0.45 | ↓ Decreasing | 🟢 Good |
| Elite Gap | 1.17 | → | 🟢 Good |
| Min Fitness Trend | +27.3 | ↑ | 🟢 Good |
| Max Fitness Trend | +19.6 | ↑ | 🟢 Good |
| IQR (p75-p25) | 26 | ↓ 6 | 🟢 |

## Stagnation Analysis

- **Current Stagnation:** 38 generations
- **Average Stagnation Period:** 38.0 generations
- **Longest Stagnation:** 38 generations
- **Number of Stagnation Periods:** 1

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Ratio | Grade | Cause of Death |
|-----|--------------|-----------|-------|-------|----------------|
| 32 | 87 | 158 | 1.81 | A | asteroid_collision |
| 33 | 105 | 118 | 1.12 | A | asteroid_collision |
| 34 | 106 | 226 | 2.12 | A | asteroid_collision |
| 35 | 90 | 65 | 0.73 | B | asteroid_collision |
| 36 | 95 | -2 | -0.02 | F | asteroid_collision |
| 37 | 86 | 99 | 1.15 | A | asteroid_collision |
| 38 | 119 | 62 | 0.53 | C | asteroid_collision |
| 39 | 91 | 23 | 0.25 | F | asteroid_collision |
| 40 | 90 | 134 | 1.49 | A | asteroid_collision |
| 41 | 96 | 167 | 1.74 | A | asteroid_collision |

### Generalization Summary

- **Average Fitness Ratio:** 1.10
- **Best Ratio:** 3.54
- **Worst Ratio:** 0.08

**Grade Distribution:** A:17 B:4 C:3 D:8 F:9 

## Correlation Analysis

### Fitness Correlations

| Metric | Correlation | Strength |
|--------|-------------|----------|
| Kills | +0.84 | Strong |
| Steps Survived | +0.84 | Strong |
| Accuracy | +0.91 | Strong |

### Interpretation

Fitness is most strongly predicted by accuracy (r=0.91).

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 250 steps (16.7% of max)
- **Max Survival:** 450 steps

### Survival Progression

| Phase | Mean Steps | Change |
|-------|------------|--------|
| Phase 1 | 266 |  |
| Phase 2 | 250 | -16 |
| Phase 3 | 253 | +3 |
| Phase 4 | 267 | +14 |
| Phase 5 | 260 | -6 |

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 4.00
- **Avg Steps Survived:** 260
- **Avg Accuracy:** 57.9%
- **Max Kills (Any Agent Ever):** 19.166666666666668
- **Max Steps (Any Agent Ever):** 651.6666666666666

## Learning Progress

**Comparing First 4 vs Last 4 Generations:**

| Metric | Early | Late | Change |
|--------|-------|------|--------|
| Best Fitness | 80.9 | 89.8 | +11.0% |
| Avg Fitness | 17.3 | 42.1 | +143.0% |

**Verdict:** Moderate learning - some improvement but room for more training.

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 19.72
- Average Range (Best-Min): 93.35
- Diversity Change: -12.6%
- **Status:** Population is converging (low diversity)

## Behavioral Trends

| Period | Avg Kills | Avg Steps | Avg Accuracy | Max Kills |
|--------|-----------|-----------|--------------|----------|
| Q1 | 3.71 | 262 | 49.9% | 19.166666666666668 |
| Q2 | 3.61 | 252 | 53.2% | 16.0 |
| Q3 | 3.91 | 260 | 56.8% | 15.833333333333334 |
| Q4 | 4.11 | 263 | 58.2% | 17.5 |

## Recent Generations (Last 30)

| Gen | Best | Avg | StdDev | Kills | Steps | Acc% | Stag |
|-----|------|-----|--------|-------|-------|------|------|
| 13 | 92 | 40 | 21 | 3.6 | 252 | 53 | 9 |
| 14 | 83 | 39 | 17 | 3.7 | 254 | 53 | 10 |
| 15 | 72 | 34 | 17 | 2.7 | 237 | 49 | 11 |
| 16 | 100 | 40 | 21 | 3.2 | 239 | 51 | 12 |
| 17 | 99 | 41 | 18 | 4.0 | 253 | 55 | 13 |
| 18 | 86 | 31 | 25 | 4.6 | 266 | 54 | 14 |
| 19 | 98 | 35 | 21 | 3.6 | 245 | 54 | 15 |
| 20 | 91 | 39 | 20 | 3.3 | 246 | 53 | 16 |
| 21 | 83 | 37 | 19 | 3.4 | 242 | 50 | 17 |
| 22 | 92 | 39 | 21 | 3.6 | 247 | 52 | 18 |
| 23 | 77 | 43 | 17 | 4.1 | 271 | 58 | 19 |
| 24 | 76 | 40 | 19 | 3.3 | 255 | 54 | 20 |
| 25 | 91 | 44 | 19 | 4.3 | 282 | 61 | 21 |
| 26 | 103 | 46 | 19 | 4.5 | 274 | 62 | 22 |
| 27 | 109 | 44 | 24 | 4.0 | 261 | 58 | 23 |
| 28 | 95 | 43 | 18 | 3.9 | 249 | 56 | 24 |
| 29 | 80 | 42 | 19 | 3.9 | 265 | 58 | 25 |
| 30 | 89 | 44 | 21 | 4.1 | 254 | 58 | 26 |
| 31 | 83 | 46 | 21 | 4.6 | 276 | 60 | 27 |
| 32 | 87 | 48 | 20 | 4.7 | 273 | 59 | 28 |
| 33 | 105 | 47 | 19 | 4.3 | 277 | 58 | 29 |
| 34 | 106 | 48 | 19 | 4.2 | 260 | 58 | 30 |
| 35 | 90 | 47 | 16 | 4.7 | 274 | 61 | 31 |
| 36 | 95 | 49 | 19 | 4.3 | 272 | 62 | 32 |
| 37 | 86 | 39 | 23 | 3.7 | 247 | 53 | 33 |
| 38 | 119 | 44 | 24 | 4.4 | 273 | 59 | 34 |
| 39 | 91 | 41 | 20 | 3.6 | 258 | 57 | 35 |
| 40 | 90 | 43 | 17 | 3.5 | 254 | 59 | 36 |
| 41 | 96 | 43 | 22 | 3.9 | 253 | 58 | 37 |
| 42 | 82 | 42 | 19 | 3.5 | 236 | 55 | 38 |


## Top 10 Best Generations

| Rank | Gen | Best | Avg | Kills | Steps | Accuracy |
|------|-----|------|-----|-------|-------|----------|
| 1 | 4 | 131 | 29 | 10.0 | 467.8333333333333 | 42.6% |
| 2 | 38 | 119 | 44 | 17.166666666666668 | 589.6666666666666 | 85.2% |
| 3 | 27 | 109 | 44 | 5.333333333333333 | 441.3333333333333 | 70.9% |
| 4 | 34 | 106 | 48 | 11.0 | 382.8333333333333 | 72.7% |
| 5 | 33 | 105 | 47 | 13.0 | 420.5 | 71.9% |
| 6 | 26 | 103 | 46 | 9.333333333333334 | 418.0 | 72.6% |
| 7 | 16 | 100 | 40 | 3.5 | 313.1666666666667 | 65.4% |
| 8 | 17 | 99 | 41 | 9.833333333333334 | 395.0 | 66.0% |
| 9 | 19 | 98 | 35 | 11.5 | 455.6666666666667 | 83.6% |
| 10 | 41 | 96 | 43 | 6.0 | 348.0 | 78.3% |


## Trend Analysis

| Period | Avg Best | Avg Mean | Avg Min | Improvement |
|--------|----------|----------|---------|-------------|
| Q1 | 76.4 | 26.1 | -25.6 |  |
| Q2 | 88.9 | 37.5 | -11.9 | +12.4 |
| Q3 | 89.3 | 42.4 | -1.4 | +0.5 |
| Q4 | 94.2 | 44.7 | -1.0 | +4.8 |


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

     131 |   *                                      
     122 |                                          
     113 |                                     *    
     104 |                          *     **        
      96 |               ** *      *              * 
      87 |           **      * *  *  * * *  **  **  
      78 |        ***  *   *  *       * *     *    *
      69 | **  ***      *       **                  
      60 |                                          
      51 |    *                                     
      43 |*                     o oooo ooooooo o o  
      34 |      o o ooooooo oooo o    o       o o oo
      25 |   o o o o       o                        
      16 | oo o                                     
       7 |                                          
      -2 |o                                         
         ------------------------------------------
         Gen 1                           Gen 42
```

