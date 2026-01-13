# Training Summary Report

**Generated:** 2026-01-13 00:45:25
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

Not enough data for sparklines.

## Training Configuration

```
population_size: 25
num_generations: 500
mutation_probability: 0.05
max_workers: 16
```

## Overall Summary

- **Total Generations:** 1
- **Training Duration:** 0:00:50.165373
- **All-Time Best Fitness:** 397.35
- **Best Generation:** 1
- **Final Best Fitness:** 397.35
- **Final Average Fitness:** 96.99
- **Avg Improvement (Early->Late):** 0.00
- **Stagnation:** 0 generations since improvement

## Best Agent Deep Profile

The most fit agent appeared in **Generation 1** with a fitness of **397.35**.

### Combat Efficiency

- **Total Kills:** 17.6
- **Survival Time:** 10.4 seconds (621.75 steps)
- **Accuracy:** 73.4%
- **Shots per Kill:** 1.3
- **Time per Kill:** 0.59 seconds

### Behavioral Signature

**Classification:** `Dogfighter`

| Action | Rate (per step) | Description |
|--------|-----------------|-------------|
| **Thrust** | 23.9% | Movement frequency |
| **Turn** | 48.8% | Rotation frequency |
| **Shoot** | 30.9% | Trigger discipline |

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
|                                                           .@                                                           |
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
|                                                  .                                                                     |
|                                                                                                                        |
|                                                                                                                        |
|                                                            .                                                           |
|                                                                         .                                              |
|                                                                                                                        |
|                                                        .                                                               |
|                                                                                                                        |
|                                                                          .                                             |
|                                           .                                                                            |
|                                    .                                                                                   |
|                                                                                                                        |
|                     .                                                               :                                  |
|                                                                  .   .              ::                                 |
|                                                           .@                         ..                                |
|                                                                                                                        |
|                                                                   .                            .                       |
|                          .    .                                                                                        |
|                                           .  .                        .                        .   .   .               |
|                                                                                                                        |
|                        .                                                                               .               |
|                                                                                                                        |
|                         .                                                                                              |
|                                  .                                                                                     |
|                                                                         :                                              |
|                                                                         .                                              |
|                                                                                                                        |
|                               .                                         .                                              |
|                                                                                                                        |
|                                                                         .      .                                       |
```

## Generation Highlights

Not enough data for generation highlights.

## Milestone Timeline

| Generation | Category | Value | Description |
|------------|----------|-------|-------------|
| 1 | Fitness | 397 | Best fitness crossed 100 |
| 1 | Kills | 17.6 | First agent to achieve 1 kills |
| 1 | Kills | 17.6 | First agent to achieve 5 kills |
| 1 | Kills | 17.6 | First agent to achieve 10 kills |

## Training Progress by Decile

Not enough data for decile breakdown (need at least 5 generations).

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 1.18 (up from 1.18 in Phase 1)
- **Shots per Kill:** 2.80 (down from 2.80 in Phase 1)
- **Kill Conversion Rate:** 35.8% (up from 35.8% in Phase 1)
- **Average Kills per Episode:** 5.7

### Efficiency Trend

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 | 1.18 | 2.80 | 35.8% |

**Assessment:** Agent efficiency has not improved significantly.

## Learning Velocity

Not enough data for velocity analysis (need at least 10 generations).

## Reward Component Evolution

| Component | Phase 1 | Mid | Final | Trend | Status |
|-----------|---------|-----|-------|-------|--------|
| DeathPenalty | -147.6 | -147.6 | -147.6 | → +0% | Not learned |
| DistanceBasedKillReward | +71.0 | +71.0 | +71.0 | → +0% | Stable |
| ConservingAmmoBonus | +63.1 | +63.1 | +63.1 | → +0% | Stable |
| ExplorationBonus | +59.3 | +59.3 | +59.3 | → +0% | Stable |
| VelocitySurvivalBonus | +51.1 | +51.1 | +51.1 | → +0% | Stable |

**Exploration Efficiency (Final Phase):** 0.1216 score/step
- *Note: A higher rate indicates faster map traversal, independent of survival time.*

## Reward Balance Analysis

### Warnings

- **DeathPenalty consistently negative** - This component has been negative throughout training, averaging -147.6/episode. The intended behavior may not be incentivized strongly enough, or there may be a conflict with other rewards.

- **High penalty ratio (60.3%)** - Negative rewards are 60% of positive rewards. Agents may be struggling to achieve net positive fitness.

### Confirmations

- **Reward reasonably balanced** - No single component >60%
- **VelocitySurvivalBonus positive** - Agents are learning to stay alive

### Recommendations

- Consider increasing the magnitude of consistently negative reward components
- Check if there are conflicting incentives preventing the behavior

## Population Health Dashboard

Not enough data for population health analysis.

## Stagnation Analysis

No stagnation periods detected - fitness improved every generation!

## Correlation Analysis

Not enough data for correlation analysis.

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 488 steps (32.5% of max)
- **Max Survival:** 750 steps

### Survival Progression

| Phase | Mean Steps | Change |
|-------|------------|--------|
| Phase 1 | 488 |  |

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 5.74
- **Avg Steps Survived:** 488
- **Avg Accuracy:** 58.4%
- **Max Kills (Any Agent Ever):** 17.6
- **Max Steps (Any Agent Ever):** 750.4

## Learning Progress

Not enough data for learning analysis.

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 119.47
- Average Range (Best-Min): 468.00
- Diversity Change: +0.0%
- **Status:** Population is converging (low diversity)

## Behavioral Trends

Not enough data for behavioral trend analysis.

### Intra-Episode Score Breakdown

Analysis of when agents earn their reward during an episode (Early vs Late game).

| Quarter | Avg Score | Share of Total | Play Style |
|---------|-----------|----------------|------------|
| Start (0-25%) | 21.1 | 21.7% | Balanced |
| Mid-Game (25-50%) | 55.8 | 57.6% | Balanced |
| Late-Game (50-75%) | 76.0 | 78.3% | Balanced |
| End-Game (75-100%) | -55.9 | -57.6% | Balanced |

## Recent Generations (Last 30)

<details>
<summary>Click to expand Recent Generations table</summary>

| Gen   | Best   | Avg    | StdDev | Kills  | Steps  | Acc%   | Stag   |
|-------|--------|--------|--------|--------|--------|--------|--------|
| 1     | 397    | 97     | 119    | 5.7    | 488    | 58     | 0      |

</details>


## Top 10 Best Generations

<details>
<summary>Click to expand Top 10 Best Generations table</summary>

| Rank | Gen   | Best   | Avg    | Kills  | Steps  | Accuracy |
|------|-------|--------|--------|--------|--------|----------|
| 1    | 1     | 397    | 97     | 17.6   | 622    | 73.4     |

</details>


## Trend Analysis

Not enough data for trend analysis.


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

     397 |*
     371 | 
     344 | 
     318 | 
     291 | 
     265 | 
     238 | 
     212 | 
     185 | 
     159 | 
     132 | 
     106 | 
      79 |o
      53 | 
      26 | 
       0 | 
         -
         Gen 1Gen 1
```


---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 0.00s
