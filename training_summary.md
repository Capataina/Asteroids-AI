# Training Summary Report

**Generated:** 2026-01-09 19:09:52
**Schema Version:** 2.0

## Quick Trend Overview

```
Best Fitness: 359 → 749   [▁▃▂▃▃▆▅▆█▆] +109%
Avg Fitness:  35 → 424   [▁▄▃▄▅▆▆▆▇█] +1097%
Avg Kills:    2.8 → 20.0   [▁▄▄▄▅▆▆▇▇█] +616%
Avg Accuracy: 50% → 88%   [▁▄▄▅▆▆▆▇▇█] +77%
Avg Steps:    278 → 589   [▁▃▃▄▅▅▆▆▇█] +112%
Diversity:    76 → 139   [▁▄▄▄▄▆▇▆█▆] +82%
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

- **Total Generations:** 301
- **Training Duration:** 2:59:33.370314
- **All-Time Best Fitness:** 855.77
- **Best Generation:** 195
- **Final Best Fitness:** 748.61
- **Final Average Fitness:** 423.61
- **Avg Improvement (Early->Late):** 277.78
- **Stagnation:** 106 generations since improvement

**Generalization (Fresh Game Performance):**
- Avg Generalization Ratio: 0.39
- Best Fresh Fitness: 801.14 (Gen 234)
- Episode Completion Rate: 9.7%

## Training Progress by Decile

| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|------|----------|---------|-----------|---------|-----------|----------|
| 0-10% | 1-30 | 631 | 193 | 10.2 | 69% | 401 | 106 |
| 10-20% | 31-60 | 587 | 202 | 10.6 | 69% | 403 | 101 |
| 20-30% | 61-90 | 615 | 204 | 10.6 | 71% | 403 | 106 |
| 30-40% | 91-120 | 627 | 230 | 11.9 | 74% | 433 | 97 |
| 40-50% | 121-150 | 712 | 284 | 14.3 | 78% | 476 | 116 |
| 50-60% | 151-180 | 845 | 335 | 16.5 | 81% | 518 | 123 |
| 60-70% | 181-210 | 856 | 342 | 16.9 | 81% | 526 | 123 |
| 70-80% | 211-240 | 781 | 341 | 16.8 | 80% | 524 | 123 |
| 80-90% | 241-270 | 826 | 378 | 18.2 | 84% | 555 | 125 |
| 90-100% | 271-301 | 834 | 419 | 19.8 | 87% | 590 | 130 |

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 3.35 (up from 2.55 in Phase 1)
- **Shots per Kill:** 1.88 (down from 2.29 in Phase 1)
- **Kill Conversion Rate:** 53.2% (up from 43.7% in Phase 1)
- **Average Kills per Episode:** 19.7

### Efficiency Trend

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 | 2.59 | 2.31 | 43.4% |
| Phase 2 | 2.69 | 2.27 | 44.1% |
| Phase 3 | 3.09 | 2.02 | 49.5% |
| Phase 4 | 3.21 | 1.96 | 50.9% |
| Phase 5 | 3.32 | 1.90 | 52.6% |

**Assessment:** Agent shows slight efficiency improvement. Shots per kill dropped 18%.

## Reward Component Evolution

| Component | Phase 1 | Mid | Final | Trend | Status |
|-----------|---------|-----|-------|-------|--------|
| ConservingAmmoBonus | +107.6 | +173.9 | +223.7 | ↑↑↑ +108% | Learned |
| DistanceBasedKillReward | +116.5 | +176.8 | +222.1 | ↑↑ +91% | Learned |
| DeathPenalty | -75.0 | -74.8 | -74.4 | → +1% | Improving |
| SurvivalBonus | +20.1 | +25.1 | +29.5 | ↑ +47% | Learned |
| ExplorationBonus | +23.8 | +15.4 | +17.6 | ↓ -26% | Stable |

## Population Health Dashboard

### Current Status: 🟢 Healthy

| Metric | Value | Trend (Recent) | Status |
|--------|-------|----------------|--------|
| Diversity Index | 0.32 | ↑ Increasing | 🟢 Good |
| Elite Gap | 0.77 | → | 🟢 Good |
| Min Fitness Trend | +177.9 | ↑ | 🟢 Good |
| Max Fitness Trend | +314.5 | ↑ | 🟢 Good |
| IQR (p75-p25) | 181 | ↑ 52 | 🟢 |

## Stagnation Analysis

- **Current Stagnation:** 106 generations
- **Average Stagnation Period:** 29.1 generations
- **Longest Stagnation:** 117 generations
- **Number of Stagnation Periods:** 10

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Ratio | Grade | Cause of Death |
|-----|--------------|-----------|-------|-------|----------------|
| 291 | 631 | 328 | 0.52 | C | asteroid_collision |
| 292 | 636 | 769 | 1.21 | A | completed_episode |
| 293 | 738 | 665 | 0.90 | A | completed_episode |
| 294 | 701 | 171 | 0.24 | F | asteroid_collision |
| 295 | 674 | 232 | 0.34 | D | asteroid_collision |
| 296 | 735 | 14 | 0.02 | F | asteroid_collision |
| 297 | 748 | 252 | 0.34 | D | asteroid_collision |
| 298 | 736 | -16 | -0.02 | F | asteroid_collision |
| 299 | 756 | -13 | -0.02 | F | asteroid_collision |
| 300 | 706 | 93 | 0.13 | F | asteroid_collision |

### Generalization Summary

- **Average Fitness Ratio:** 0.39
- **Best Ratio:** 1.82
- **Worst Ratio:** 0.00

**Grade Distribution:** A:19 B:16 C:27 D:43 F:195 

## Correlation Analysis

### Fitness Correlations

| Metric | Correlation | Strength |
|--------|-------------|----------|
| Kills | +1.00 | Strong |
| Steps Survived | +0.99 | Strong |
| Accuracy | +0.92 | Strong |

### Interpretation

Fitness is most strongly predicted by kills (r=1.00).

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 590 steps (39.3% of max)
- **Max Survival:** 975 steps

### Survival Progression

| Phase | Mean Steps | Change |
|-------|------------|--------|
| Phase 1 | 402 |  |
| Phase 2 | 418 | +16 |
| Phase 3 | 497 | +79 |
| Phase 4 | 525 | +28 |
| Phase 5 | 573 | +48 |

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 19.17
- **Avg Steps Survived:** 576
- **Avg Accuracy:** 86.6%
- **Max Kills (Any Agent Ever):** 39.0
- **Max Steps (Any Agent Ever):** 1015.1666666666666

## Learning Progress

**Comparing First 30 vs Last 30 Generations:**

| Metric | Early | Late | Change |
|--------|-------|------|--------|
| Best Fitness | 466.2 | 733.7 | +57.4% |
| Avg Fitness | 193.1 | 418.5 | +116.7% |

**Verdict:** Strong learning - both best and average fitness improved significantly.

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 130.09
- Average Range (Best-Min): 567.03
- Diversity Change: +30.7%
- **Status:** Population is converging (low diversity)

## Behavioral Trends

| Period | Avg Kills | Avg Steps | Avg Accuracy | Max Kills |
|--------|-----------|-----------|--------------|----------|
| Q1 | 10.35 | 400 | 68.9% | 29.5 |
| Q2 | 12.69 | 447 | 75.0% | 32.666666666666664 |
| Q3 | 16.71 | 522 | 80.6% | 39.0 |
| Q4 | 18.59 | 563 | 84.6% | 38.0 |

## Recent Generations (Last 30)

| Gen | Best | Avg | StdDev | Kills | Steps | Acc% | Stag |
|-----|------|-----|--------|-------|-------|------|------|
| 272 | 692 | 402 | 115 | 19.0 | 570 | 86 | 77 |
| 273 | 756 | 431 | 153 | 20.2 | 597 | 86 | 78 |
| 274 | 816 | 424 | 143 | 20.1 | 595 | 87 | 79 |
| 275 | 756 | 433 | 127 | 20.4 | 606 | 88 | 80 |
| 276 | 736 | 424 | 129 | 19.9 | 597 | 87 | 81 |
| 277 | 783 | 432 | 124 | 20.3 | 608 | 88 | 82 |
| 278 | 759 | 453 | 128 | 21.2 | 624 | 87 | 83 |
| 279 | 792 | 421 | 125 | 19.8 | 590 | 88 | 84 |
| 280 | 700 | 422 | 144 | 20.1 | 596 | 87 | 85 |
| 281 | 722 | 439 | 120 | 20.6 | 610 | 87 | 86 |
| 282 | 834 | 426 | 142 | 20.1 | 596 | 88 | 87 |
| 283 | 708 | 435 | 136 | 20.4 | 610 | 88 | 88 |
| 284 | 760 | 471 | 127 | 22.2 | 644 | 89 | 89 |
| 285 | 668 | 442 | 128 | 20.8 | 619 | 87 | 90 |
| 286 | 780 | 404 | 127 | 19.3 | 577 | 86 | 91 |
| 287 | 700 | 416 | 133 | 19.9 | 588 | 87 | 92 |
| 288 | 774 | 440 | 134 | 20.5 | 611 | 87 | 93 |
| 289 | 738 | 438 | 148 | 20.4 | 608 | 87 | 94 |
| 290 | 728 | 363 | 134 | 17.4 | 534 | 84 | 95 |
| 291 | 631 | 374 | 105 | 17.8 | 548 | 85 | 96 |
| 292 | 636 | 423 | 106 | 19.7 | 588 | 87 | 97 |
| 293 | 738 | 368 | 125 | 17.6 | 545 | 85 | 98 |
| 294 | 701 | 402 | 122 | 19.0 | 575 | 87 | 99 |
| 295 | 674 | 396 | 136 | 18.9 | 567 | 86 | 100 |
| 296 | 735 | 402 | 110 | 18.9 | 568 | 87 | 101 |
| 297 | 748 | 377 | 137 | 17.8 | 549 | 85 | 102 |
| 298 | 736 | 410 | 128 | 19.4 | 580 | 86 | 103 |
| 299 | 756 | 433 | 147 | 20.3 | 601 | 88 | 104 |
| 300 | 706 | 429 | 136 | 20.2 | 600 | 87 | 105 |
| 301 | 749 | 424 | 139 | 20.0 | 589 | 88 | 106 |


## Top 10 Best Generations

| Rank | Gen | Best | Avg | Kills | Steps | Accuracy |
|------|-----|------|-----|-------|-------|----------|
| 1 | 195 | 856 | 356 | 38.5 | 1015.1666666666666 | 96.7% |
| 2 | 155 | 845 | 348 | 38.666666666666664 | 1010.0 | 87.5% |
| 3 | 191 | 843 | 344 | 37.5 | 993.3333333333334 | 96.5% |
| 4 | 282 | 834 | 426 | 37.166666666666664 | 975.1666666666666 | 96.6% |
| 5 | 170 | 832 | 349 | 39.0 | 977.1666666666666 | 95.3% |
| 6 | 210 | 828 | 362 | 37.666666666666664 | 968.1666666666666 | 95.0% |
| 7 | 193 | 827 | 338 | 36.5 | 936.8333333333334 | 93.1% |
| 8 | 265 | 826 | 400 | 36.0 | 986.0 | 95.5% |
| 9 | 241 | 818 | 406 | 38.0 | 974.6666666666666 | 95.2% |
| 10 | 274 | 816 | 424 | 36.0 | 941.3333333333334 | 96.9% |


## Trend Analysis

| Period | Avg Best | Avg Mean | Avg Min | Improvement |
|--------|----------|----------|---------|-------------|
| Q1 | 461.6 | 196.5 | -0.0 |  |
| Q2 | 520.1 | 249.0 | 42.3 | +58.5 |
| Q3 | 654.0 | 338.6 | 89.6 | +134.0 |
| Q4 | 704.3 | 387.8 | 129.9 | +50.2 |


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

     827 |                                *                  
     772 |                                        *   * *    
     717 |                                   *         *  * *
     662 |                         *        *   ** *     * * 
     607 |                 *        * * **    **    **       
     552 |    *  *              ***  *     *                 
     496 |     *         *    *        *                     
     441 |  **  *  ****   * ** *                             
     386 |        *    **                         o   ooooooo
     331 |**                        o o ooooooooo  ooo       
     276 |                    o   oo o o         o           
     221 |   oo  o o    ooo o  ooo                           
     165 |  o  oo o oooo   o o                               
     110 | o                                                 
      55 |                                                   
       0 |o                                                  
         ---------------------------------------------------
         Gen 1                                    Gen 301
```

