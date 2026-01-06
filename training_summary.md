# Training Summary Report

**Generated:** 2026-01-06 01:07:21

## Training Configuration

```
population_size: 100
num_generations: 500
mutation_probability: 0.2
mutation_gaussian_sigma: 0.15
crossover_probability: 0.7
max_workers: 16
frame_delay: 0.016666666666666666
```

## Overall Summary

- **Total Generations:** 25
- **Training Duration:** 0:12:45.659999
- **All-Time Best Fitness:** 1910.24
- **Best Generation:** 25
- **Final Best Fitness:** 1910.24
- **Final Average Fitness:** 641.55
- **Avg Improvement (Early->Late):** 345.01
- **Stagnation:** 0 generations since improvement

## Reward Component Analysis

Based on the average scores from the final generation:

| Reward Component         | Avg. Score per Episode | Pct of Positive Rewards |
| ------------------------ | ---------------------- | ----------------------- |
| KillAsteroid             | 325.92                 | +47.9%                  |
| ConservingAmmoBonus      | 316.33                 | +46.5%                  |
| MaintainingMomentumBonus | -38.40                 | -5.6%                   |
| NearMiss                 | 29.95                  | +4.4%                   |
| SurvivalBonus            | 7.74                   | +1.1%                   |
| MovingTowardDangerBonus  | 0.06                   | +0.0%                   |
| SpacingFromWallsBonus    | -0.04                  | -0.0%                   |

_Note: Percentages are relative to the sum of all positive rewards in the final generation._

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 12.31
- **Avg Steps Survived:** 447
- **Avg Accuracy:** 77.6%
- **Max Kills (Any Agent Ever):** 38.333333333333336
- **Max Steps (Any Agent Ever):** 992.0

## Learning Progress

**Comparing First 2 vs Last 2 Generations:**

| Metric       | Early | Late   | Change   |
| ------------ | ----- | ------ | -------- |
| Best Fitness | 607.6 | 1797.8 | +195.9%  |
| Avg Fitness  | 33.3  | 648.1  | +1847.4% |

**Verdict:** Strong learning - both best and average fitness improved significantly.
