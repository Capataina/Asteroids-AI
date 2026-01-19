# Training Summary Report

**Generated:** 2026-01-16 18:29:50
**Schema Version:** 2.1

## Table of Contents

- [Quick Trend Overview](#quick-trend-overview)
- [Report Takeaways (All Sections)](#report-takeaways-all-sections)
- [Training Configuration](#training-configuration)
- [Overall Summary](#overall-summary)
- [Best Agent Deep Profile](#best-agent-deep-profile)
- [Generation Highlights](#generation-highlights)
- [Milestone Timeline](#milestone-timeline)
- [Training Progress by Phase](#training-progress-by-phase)
- [Distribution Analysis](#distribution-analysis)
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
- [Neural & Behavioral Complexity](#neural--behavioral-complexity)
- [Risk Profile Analysis](#risk-profile-analysis)
- [Control Diagnostics](#control-diagnostics)
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
Best Fitness     175 -> 164  [ :*@=# --- .%.%+ ++ ]  stagnation (low confidence)
Avg Fitness      -97 -> -97  [ -#***-=+*:-+ @%-=+-]  volatile (low confidence (noisy))
Min Fitness      -246 -> -246  [.+@=*+:=*% :+.*+-*+=]  volatile (low confidence (noisy))
Fitness Spread   89 -> 88  [. +**@-=-:.:#:## -* ]  stagnation (low confidence)
Avg Kills        6.8 -> 7.2  [ =####=+*#=+#-%@++*=]  volatile (low confidence (noisy))
Avg Accuracy     35% -> 35%  [ -#+**-=*#:=+=@#.=*-]  stagnation (low confidence)
Avg Steps        717 -> 702  [ =@**+:=+*:-+ %%:-+-]  stagnation (low confidence)
Action Entropy   1.11 -> 0.87  [@+-:::-.-..:..:    .]  stagnation (low confidence)
Output Saturation 5% -> 12%  [  .-#+-+=@==+++*%**=]  stagnation (low confidence (noisy))
Frontness Avg    50% -> 51%  [-. -=%##%%#*+#+=+@#*]  stagnation (low confidence)
Danger Exposure  16% -> 16%  [.-**+@::+- **.#=-* =]  volatile (low confidence (noisy))
Seed Fitness Std 119.7 -> 126.3  [ ++*@*-+=#=++-+%*+%=]  volatile (low confidence (noisy))
```

### Quick Trend Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Average kills:** Mean kills per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Average steps:** Mean steps survived per episode across the population.
- **Action entropy:** Entropy of action combinations (higher = more varied control).
- **Output saturation:** Share of NN outputs near 0 or 1 (binary control tendency).
- **Frontness average:** Alignment of nearest asteroid with ship heading (1 ahead, 0 behind).
- **Danger exposure rate:** Fraction of frames with a nearby asteroid inside danger radius.
- **Soft-min TTC:** Weighted time-to-collision proxy that emphasizes the nearest threats (seconds).
- **Seed fitness std:** Average per-agent fitness std dev across seeds (evaluation noise proxy).

## Report Takeaways (All Sections)

- Quick Trend Overview: sparklines summarize phase-based metric direction and confidence.
- Training Configuration: report includes a full hyperparameter snapshot for reproducibility.
- Overall Summary: best fitness 364.01 at Gen 167.
- Best Agent Deep Profile: Gen 167 with 21.333333333333332 kills.
- Heatmaps: spatial patterns available for best agent and population.
- Generation Highlights: top improvements/regressions and record runs flagged.
- Milestone Timeline: milestones are run-relative (percent-of-peak thresholds).
- Training Progress by Phase: 4 equal phases used for normalized comparisons.
- Distribution Analysis: fitness spread trend is stagnation.
- Kill Efficiency: phase-level kill rates and shot efficiency tracked.
- Learning Velocity: phase-based fitness deltas and acceleration reported.
- Reward Component Evolution: per-component shifts tracked across 4 phases.
- Reward Balance Analysis: dominance, entropy, and penalty skew checked.
- Population Health Dashboard: diversity, elite gap, and floor trends summarized.
- Stagnation Analysis: plateau lengths compared to run history.
- Generalization Analysis: fresh-game ratios and reward transfer gaps reported.
- Correlation Analysis: fitness vs kills/survival/accuracy correlations reported.
- Survival Distribution: phase-level survival averages and max survival summarized.
- Behavioral Summary: recent kills, steps, and accuracy summarized.
- Learning Progress: phase comparisons for best/avg/min fitness.
- Neural & Behavioral Complexity: saturation and entropy trends reported.
- Risk Profile Analysis: proximity trends and archetypes reported.
- Control Diagnostics: turn bias, frontness, danger, and movement diagnostics reported.
- Convergence Analysis: recent diversity and range trends summarized.
- Behavioral Trends: action mix and intra-episode scoring patterns reported.
- Recent Generations: last 30 gens tabulated.
- Top Generations: best run is Gen 167.
- Trend Analysis: phase-based fitness trend table provided.
- ASCII Chart: best vs avg fitness progression visualized.
- Technical Appendix: runtime costs, operator stats, and ES optimizer diagnostics reported when available.

## Training Configuration

```
method: Evolution Strategies
optimizer: cmaes
population_size: 100
num_generations: 500
cmaes_sigma: 0.15
cmaes_mu: auto
cmaes_cov_min: 1e-06
cmaes_cov_target_rate: 0.001
cmaes_cov_max_scale: 10000.0
sigma_min: 0.02
use_antithetic: True
seeds_per_agent: 3
use_common_seeds: True
noise_handling_enabled: True
noise_handling_top_k: 5
noise_handling_extra_seeds: 1
noise_handling_seed_offset: 100000
restart_enabled: True
restart_patience: 12
restart_min_generations: 5
restart_cooldown: 5
restart_sigma_multiplier: 1.0
restart_use_best_candidate: True
max_workers: 16
temporal_stack_enabled: True
temporal_stack_size: 4
temporal_stack_include_deltas: True
pareto_enabled: True
pareto_objectives: ['hits', 'time_alive', 'softmin_ttc']
pareto_accuracy_min_shots: 5
pareto_accuracy_zero_below_min_shots: True
pareto_frame_delay: 0.016666666666666666
pareto_risk_ttc_max: 5.0
pareto_risk_tau: 1.0
pareto_fitness_tiebreaker: True
```

### Config Takeaways

- Configuration snapshot captures the exact training parameters for reproducibility.

### Config Glossary

- **Config value:** Literal hyperparameter or run setting recorded at training start.

## Overall Summary

- **Total Generations:** 190
- **Training Duration:** 15:06:31.674648
- **All-Time Best Fitness:** 364.01
- **Best Generation:** 167
- **Final Best Fitness:** 113.46
- **Final Average Fitness:** -114.97
- **Avg Improvement (Phase 1->Phase 4):** -0.30
- **Stagnation:** 23 generations since improvement

**Generalization (Fresh Game Performance):**
- Avg Generalization Ratio: 2.37
- Best Fresh Fitness: 498.70 (Gen 114)
- Episode Completion Rate: 8.5%

### Takeaways

- Best fitness achieved: 364.01 (Gen 167).
- Final avg fitness: -114.97.
- Current stagnation: 23 generations without improvement.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Avg improvement (Phase 1->Phase 4):** Difference between average fitness in the first and last 25% of training.
- **Generalization ratio:** Fresh-game fitness divided by training fitness (averaged across fresh runs).
- **Episode completion rate:** Share of fresh-game episodes that completed the full max-step window.

## Best Agent Deep Profile

The most fit agent appeared in **Generation 167** with a fitness of **364.01**.

### Combat Efficiency

- **Total Kills:** 21.333333333333332
- **Survival Time:** 25.0 seconds (1500.0 steps)
- **Accuracy:** 48.6%
- **Shots per Kill:** 2.0
- **Time per Kill:** 1.17 seconds

### Behavioral Signature

**Classification:** `Sniper`

| Action | Rate (per step) | Description |
|--------|-----------------|-------------|
| **Thrust** | 2.0% | Movement frequency |
| **Turn** | 100.0% | Rotation frequency |
| **Shoot** | 97.2% | Trigger discipline |

### Takeaways

- Best agent achieved 21.333333333333332 kills with 48.6% accuracy.
- Behavioral classification: Sniper.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Average steps:** Mean steps survived per episode across the population.
- **Shots per kill:** Shots fired divided by kills (lower is more efficient).

### Spatial Analytics (Best Agent - Generations 181-190)

**Position Heatmap (Where does it fly?)**
```
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                             .                                          |
|                                                               . .   .    .                                             |
|                                                                     .    . ..                                          |
|                                                                           .                                            |
|                                                       .    .: ..  .  .  .                                              |
|                                                   . . .  ..  . ..                                                      |
|                                                    :. .     .  .                                                       |
|                                                .-:... -:=-+@-...-.                                                     |
|                                               . .   :-.=---::.....         .                                           |
|                                               ..  .   :::..                          .                                 |
|                                                       :..:. . .  . .                      .                            |
|                                                   . ....   .  .  .                                                     |
|                                                      :      ...     .                                                  |
|                                                           :...           .                                             |
|                                                            .                                                           |
|                                                                            .                                           |
|                                                                   .                                                    |
|                                                                                                                        |
|                                                                                                                        |
|                                                                      .                                                 |
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
|                                                                          .                                             |
|                                                                            .                                           |
|                                                                :   ..     .                                            |
|                                                                    . .    ...                                          |
|                                                                         .                                              |
|                                                      .  .   .   .  ...                                                 |
|                                                   .. .  ..: .  ..                                                      |
|                                                    :.      .                                                           |
|                                                .- :.:.:-=-+@. .:=.                                                     |
|                                                     :-:-:--.:..::                                                      |
|                                                . . .  :::..                                                            |
|                                                       .. .   .                             .                           |
|                                                   .. ...     .  . .                                                    |
|                                                     .:       .                                                         |
|                                                           :....        . .                                             |
|                                                            .             .                                             |
|                                                                            .                                           |
|                                                                  ..                                                    |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
|                                                                                                                        |
```

### Spatial Analytics (Population Average - Generations 181-190)

**Position Heatmap (Where do they fly?)**
```
|                                      .            .     .                                                              |
|                                        .        .                     .      .                                         |
|                                      .                                    .                                            |
|                          .                                                                                             |
|                                                          ..   .      . .                 .                             |
|                                              .     .        .    .       .       .        .                            |
|                                                    ..  .. .  ..              .  .   .                                  |
|                                        .    . .     . . .  .  ..   .             .       .                             |
|          .                  .            .            .  .   ..   . .         .                                        |
|                                        .        . ..    .   ...... .   .     .                 .                       |
|                                    .  .     .  ...... . .  ....  .   . .  . .                                          |
|                                             .  . ... .........   ...     . .     .    .                 .              |
|                .          ...       .  .  .    .:..:....::.......:.... ..   ..  ..                                     |
| .                                . .    . . . ... ..:::::------:.........       .      .                               |
|        .                    .    ..   .   :    ....::::-==+@+--::::. ... .. ..                                         |
|        .              . .        .  . ..  . .  :....::--=+=+=--::::.   ...  . ..                                       |
|                                     . . ...   ...:.::::--:.-::..:...  .                                                |
|                         .   ..  .       ... ........ .:...:...:. ... ...   .                                           |
|                         .            .... .       . .:.  ...  ...      ..        .                          .          |
|                                                . ... .. .  ..  ..                .                                     |
|                                      .   .       .    ..   .   .    .     .  .                                         |
|                                                   . . .. .           .  ..                                             |
|                                          .    .     .          .                        .                              |
|                                                 .        ..  .     .                          .                        |
|                                                   .  .     .                                                           |
|                                    .                          .   ..                                                   |
|                                                               .                                                        |
|                                                                                                       .                |
|                                  .     .                         .  .                                                  |
|                                                         . .                                                            |
```

**Kill Zone Heatmap (Where do they kill?)**
```
|                                                                                                                        |
|                                                 .      .             .                                                 |
|                                    .                   . .                .                                            |
|                                         .                               .                                              |
|                                          .               .                               .                             |
|                                                 .  .             .         .  ..         .                             |
|                                              .     .   . .   .                                                         |
|                                                  ..   :..   . .        .     .   .                                     |
|                                                    ...   ..   .                  .             .                       |
|                                                      .  .   ...  .      ..  .                                    .     |
|                                               ...  .. .. .. ...     .                                                  |
|                       .               .            .  . :...:  .  . .  .           .                   .               |
|                        .  .  .  .      .       ..:...:...:...:. :: ....:.   . .                                        |
|                                   .      .     ......::::--:---:..::.....   ..                                         |
|                                       .   : .   . .::::-===@+-=:::...    : .                                           |
|   .                   ..            . .. .. .  ::.::::--=+=+=--- :  ... .. .                                           |
|               .          .     .      . ..:   ..:...::::-::-:-::.....                                                  |
|               .              .  .     .   : .  . ... .:::. ......    . .                                               |
|                                          .           : . :.   ..     . .         .                                     |
|                                                .    .   .   . .    .        .         .                                |
|                                         .      .         ..:            .    .   .                                     |
|                                           .   .    .     . .         .   :                                             |
|                                   .             .   ..                                                                 |
|                                                        .                                     .                         |
|                                         .                  .                                                           |
|                                                                                                                        |
|                                                               .                                                        |
|                                                                .                                                       |
|                                                           .                                                            |
|                                                               .                                                        |
```

### Heatmap Takeaways

- Heatmaps aggregate spatial samples over the last 10 generations.
- Best-agent and population heatmaps highlight spatial biases and kill zones.

### Heatmap Glossary

- **Position heatmap:** Density of sampled player positions during evaluation.
- **Kill heatmap:** Density of player positions at kill events (proxy for engagement zones).

## Generation Highlights

### Best Improvement

**Generation 84**: Best fitness jumped +286.0 (+412.4%)
- New best fitness: 355.3

### Worst Regression

**Generation 69**: Best fitness dropped -285.2 (-83.6%)
- New best fitness: 55.9
- Note: this can be normal variation after a lucky outlier

### Most Accurate Generation

**Generation 107**: Population accuracy reached 43.4%

### Most Kills (Single Agent)

**Generation 119**: An agent achieved 25 kills

### First Viable Population

**Generation 36**: Average fitness first became positive

### Most Diverse Generation

**Generation 107**: Diversity index 199.48

### Most Converged Generation

**Generation 189**: Diversity index 0.25

### Takeaways

- Best improvement at Gen 84 (+286.0).
- Worst regression at Gen 69 (-285.2).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Max kills:** Highest kills achieved by any agent in the generation.
- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).

## Milestone Timeline

| Generation | Category | Value | Description |
|------------|----------|-------|-------------|
| 1 | Fitness | 149 | Best fitness reached 25% of run peak |
| 1 | Kills | 14 | Max kills reached 25% of run peak |
| 1 | Kills | 14 | Max kills reached 50% of run peak |
| 6 | Fitness | 190 | Best fitness reached 50% of run peak |
| 17 | Fitness | 311 | Best fitness reached 75% of run peak |
| 17 | Kills | 20 | Max kills reached 75% of run peak |
| 36 | Avg Fitness | 35 | Avg fitness reached 25% of run peak |
| 36 | Avg Fitness | 35 | Avg fitness reached 50% of run peak |
| 36 | Avg Fitness | 35 | Avg fitness reached 75% of run peak |
| 36 | Viability | 35 | Average fitness turned positive |
| 49 | Kills | 23 | Max kills reached 90% of run peak |
| 58 | Avg Fitness | 40 | Avg fitness reached 90% of run peak |
| 68 | Fitness | 341 | Best fitness reached 90% of run peak |
| 84 | Fitness | 355 | Best fitness reached 95% of run peak |
| 167 | Fitness | 364 | Best fitness reached 98% of run peak |

### Takeaways

- Total milestones reached: 15.
- Latest milestone at Gen 167 (Fitness).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Max kills:** Highest kills achieved by any agent in the generation.

## Training Progress by Phase

| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|------|----------|---------|-----------|---------|-----------|----------|
| Phase 1 (0-25%) | 1-48 | 318 | -97 | 6.8 | 35% | 717 | 89 |
| Phase 2 (25-51%) | 49-96 | 355 | -96 | 7.2 | 36% | 710 | 90 |
| Phase 3 (51-75%) | 97-143 | 326 | -102 | 6.9 | 35% | 686 | 90 |
| Phase 4 (75-100%) | 144-190 | 364 | -97 | 7.2 | 35% | 702 | 88 |

### Takeaways

- Phase breakdown uses equal 25% blocks for run-normalized comparisons.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Average kills:** Mean kills per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Average steps:** Mean steps survived per episode across the population.
- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).

## Distribution Analysis

### Metric Distributions (Last 10 Generations)

Visualizing population consistency: `|---O---|` represents Mean +/- 1 StdDev.
- **Narrow bar**: Consistent population (convergence)
- **Wide bar**: Diverse or noisy population

**Accuracy Distribution**
```
Gen 181:  |--------------O---------------|                   28.4% +/-  8.1%
Gen 182:         |------------O------------|                 31.1% +/-  6.8%
Gen 183:                     |-----------O-----------|       36.7% +/-  6.3%
Gen 184:                    |-----------O-----------|        36.0% +/-  6.2%
Gen 185:               |----------O----------|               32.9% +/-  5.9%
Gen 186:                           |---------O--------|      38.7% +/-  5.1%
Gen 187:             |------------O-------------|            33.1% +/-  7.1%
Gen 188:                           |--------O---------|      38.6% +/-  5.0%
Gen 189: |-----------O------------|                          26.3% +/-  6.7%
Gen 190:                              |---------O---------|  40.6% +/-  5.3%
```

**Survival Steps Distribution**
```
Gen 181:           |-----O------|                            404.5 +/- 161.6
Gen 182:                   |--------O-------|                652.9 +/- 204.2
Gen 183:                       |-------O--------|            737.3 +/- 200.6
Gen 184:                    |---------O---------|            712.1 +/- 233.0
Gen 185:                       |-------O-------|             734.6 +/- 187.6
Gen 186:                          |------O-------|           784.3 +/- 177.3
Gen 187:                   |------O------|                   615.1 +/- 167.4
Gen 188:                             |-------O--------|      884.2 +/- 208.1
Gen 189:            |----O----|                              389.9 +/- 120.8
Gen 190:                       |-----O-----|                 684.2 +/- 139.4
```

**Kills Distribution**
```
Gen 181:  |--------O--------|                                  2.8 +/-   2.5
Gen 182:              |----------O-----------|                 6.7 +/-   3.2
Gen 183:                 |-----------O----------|              7.7 +/-   3.1
Gen 184:               |------------O------------|             7.5 +/-   3.5
Gen 185:                   |---------O---------|               7.7 +/-   2.8
Gen 186:                   |-----------O-----------|           8.3 +/-   3.2
Gen 187:          |----------O---------|                       5.5 +/-   2.9
Gen 188:                       |-----------O----------|        9.4 +/-   3.1
Gen 189:     |-------O------|                                  3.4 +/-   2.0
Gen 190:              |---------O--------|                     6.4 +/-   2.6
```

**Fitness Distribution**
```
Gen 181: |---------O----------|                             -207.3 +/-  74.2
Gen 182:            |------------O-------------|            -108.3 +/-  92.6
Gen 183:                |------------O------------|          -82.7 +/-  89.8
Gen 184:              |--------------O-------------|         -86.4 +/- 100.7
Gen 185:                 |-----------O-----------|           -86.2 +/-  83.6
Gen 186:                   |------------O------------|       -62.4 +/-  90.8
Gen 187:        |-----------O-----------|                   -144.1 +/-  82.4
Gen 188:                      |-------------O-------------|  -34.2 +/-  94.4
Gen 189:   |-------O------|                                 -211.5 +/-  53.5
Gen 190:              |---------O----------|                -115.0 +/-  75.7
```

**Aim Frontness Distribution**
```
Gen 181:  |-----------------------O-----------------------|  51.6% +/-  7.8%
Gen 182:        |-------------------O-------------------|    52.2% +/-  6.4%
Gen 183:   |--------------------O-------------------|        50.8% +/-  6.6%
Gen 184:      |-----------------O-----------------|          50.9% +/-  5.7%
Gen 185:         |---------------O---------------|           51.1% +/-  5.1%
Gen 186:     |-----------------O------------------|          50.6% +/-  5.9%
Gen 187:  |-------------------O------------------|           50.2% +/-  6.3%
Gen 188:       |------------------O-----------------|        51.4% +/-  6.1%
Gen 189: |---------------------O---------------------|       50.4% +/-  7.1%
Gen 190:         |---------------O---------------|           51.3% +/-  5.1%
```

**Danger Exposure Distribution**
```
Gen 181:     |---------O---------|                           13.8% +/-  3.0%
Gen 182:     |------------O------------|                     14.7% +/-  3.7%
Gen 183:                |----------------O----------------|  19.2% +/-  5.0%
Gen 184:                    |-------------O-------------|    19.3% +/-  4.2%
Gen 185:          |------------O-------------|               16.2% +/-  3.8%
Gen 186:                |-------------O--------------|       18.3% +/-  4.3%
Gen 187: |---------------O---------------|                   14.4% +/-  4.8%
Gen 188:                 |-----------O-----------|           17.9% +/-  3.5%
Gen 189:   |---------O----------|                            13.3% +/-  3.1%
Gen 190:     |----------------O---------------|              15.7% +/-  4.7%
```

**Turn Deadzone Distribution**
```
Gen 181: O                                                    0.0% +/-  0.0%
Gen 182: O                                                    0.0% +/-  0.0%
Gen 183: O                                                    0.0% +/-  0.0%
Gen 184: O                                                    0.0% +/-  0.0%
Gen 185: O                                                    0.0% +/-  0.0%
Gen 186: O                                                    0.0% +/-  0.0%
Gen 187: O                                                    0.0% +/-  0.0%
Gen 188: O                                                    0.0% +/-  0.0%
Gen 189: O                                                    0.0% +/-  0.0%
Gen 190: O                                                    0.0% +/-  0.0%
```

**Coverage Ratio Distribution**
```
Gen 181: |---------------------O----------------------|      15.1% +/- 12.0%
Gen 182:    |--------------------O--------------------|      16.1% +/- 10.9%
Gen 183:         |-----------------O-----------------|       17.1% +/-  9.3%
Gen 184:   |-----------------------O----------------------|  16.9% +/- 12.4%
Gen 185:    |------------------O-------------------|         15.2% +/- 10.4%
Gen 186:     |--------------O---------------|                13.4% +/-  8.1%
Gen 187: |-------------------O-------------------|           13.7% +/- 10.4%
Gen 188:     |---------------O----------------|              14.0% +/-  8.7%
Gen 189:  |------------O------------|                        10.9% +/-  6.8%
Gen 190:     |-----------O-----------|                       11.9% +/-  6.4%
```

**Seed Fitness Std Distribution**
```
Gen 181:  |-------------O-------------|                       73.0 +/-  67.0
Gen 182:             |---------------O----------------|      137.7 +/-  78.2
Gen 183:        |---------------O---------------|            112.1 +/-  77.4
Gen 184:            |---------------O---------------|        130.9 +/-  78.2
Gen 185:             |---------------O---------------|       136.2 +/-  75.8
Gen 186:              |---------------O---------------|      140.7 +/-  77.0
Gen 187:       |---------------O--------------|              105.9 +/-  72.8
Gen 188:             |--------------O-------------|          130.3 +/-  70.5
Gen 189:    |----------O---------|                            67.4 +/-  52.0
Gen 190:      |----------------O----------------|            109.1 +/-  80.7
```

### Takeaways

- Fitness spread trend: stagnation (low confidence).
- Seed variance trend: volatile (low confidence (noisy)).

### Glossary

- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Seed fitness std:** Average per-agent fitness std dev across seeds (evaluation noise proxy).
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Accuracy std dev:** Standard deviation of accuracy across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Steps std dev:** Standard deviation of survival steps across the population.
- **Average kills:** Mean kills per episode across the population.
- **Kills std dev:** Standard deviation of kills across the population.
- **Frontness average:** Alignment of nearest asteroid with ship heading (1 ahead, 0 behind).
- **Frontness std dev:** Standard deviation of frontness across the population.
- **Danger exposure rate:** Fraction of frames with a nearby asteroid inside danger radius.
- **Danger exposure std dev:** Standard deviation of danger exposure across the population.
- **Soft-min TTC:** Weighted time-to-collision proxy that emphasizes the nearest threats (seconds).
- **Soft-min TTC std dev:** Standard deviation of soft-min TTC across the population.
- **Turn deadzone rate:** Fraction of frames where signed turn input is exactly zero (deadzone currently disabled).
- **Deadzone std dev:** Standard deviation of the per-agent zero-turn rate across the population (deadzone currently disabled).
- **Coverage ratio:** Fraction of spatial grid cells visited (0 to 1).
- **Coverage std dev:** Standard deviation of coverage ratio across the population.

## Kill Efficiency Analysis

### Current Performance (Final Phase)

- **Kills per 100 Steps:** 1.03 (Phase 1: 0.95)
- **Shots per Kill:** 6.05 (Phase 1: 6.09)
- **Kill Conversion Rate:** 16.5% (Phase 1: 16.4%)
- **Average Kills per Episode:** 7.2

### Efficiency Trend (Phase Averages)

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 (0-25%) | 0.95 | 6.09 | 16.4% |
| Phase 2 (25-51%) | 1.01 | 6.14 | 16.3% |
| Phase 3 (51-75%) | 1.01 | 6.19 | 16.1% |
| Phase 4 (75-100%) | 1.03 | 6.05 | 16.5% |

### Takeaways

- Kill rate changed from 0.95 to 1.03 kills/100 steps.
- Shots per kill moved from 6.09 to 6.05.

### Glossary

- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Average shots:** Mean shots fired per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Shots per kill:** Shots fired divided by kills (lower is more efficient).

## Learning Velocity

### Velocity by Phase

| Phase | Fitness Delta | Delta/Gen | Velocity Band |
|-------|---------------|-----------|---------------|
| Phase 1 (0-25%) | +52 | +1.1 | Slow |
| Phase 2 (25-51%) | +65 | +1.4 | Fast |
| Phase 3 (51-75%) | +142 | +3.0 | Fast |
| Phase 4 (75-100%) | -100 | -2.1 | Slow |

### Current Velocity

- **Recent Improvement Rate:** -2.1 fitness/generation
- **Acceleration:** -0.8 (positive = speeding up)

### Takeaways

- Velocity mean +0.8 with std 1.9 across phases.

### Warnings

- Recent learning velocity is in the slowest quartile of the run.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).

## Reward Component Evolution

| Component | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Trend | Status |
|-----------|---------|---------|---------|---------|-------|--------|
| DeathPenalty | -216.0 | -218.8 | -221.6 | -218.5 | ~ -1% | Worsening penalty |
| DistanceBasedKillReward | +122.0 | +128.9 | +124.3 | +130.4 | ~ +7% | Stable |
| ConservingAmmoBonus | -17.3 | -17.4 | -17.6 | -18.0 | ~ -4% | Worsening penalty |
| ExplorationBonus | +10.9 | +9.4 | +10.2 | +8.2 | - -24% | Neutral |
| VelocitySurvivalBonus | +5.8 | +3.6 | +4.3 | +2.6 | - -55% | Neutral |

**Exploration Efficiency (Final Phase):** 0.0124 score/step
- *A higher rate indicates faster map traversal, independent of survival time.*

### Takeaways

- Reward component shifts are modest or mixed across phases.

### Warnings

- DeathPenalty penalty deepened (more negative over time).
- ConservingAmmoBonus penalty deepened (more negative over time).

### Glossary

- **Reward breakdown:** Per-component average reward contribution per episode.

## Reward Balance Analysis

### Balance Metrics (Latest Generation)

- Reward dominance index (HHI): 0.87
- Reward entropy (normalized): 0.27
- Max component share: 92.9%
- Positive component count: 3

### Takeaways

- Reward mix is broadly stable with no major dominance spikes.

### Warnings

- Max component share is high (92.9%).
- VelocitySurvivalBonus is volatile across the run (high variance vs mean).
- ConservingAmmoBonus remains negative on average (behavior may be over-penalized).
- DeathPenalty remains negative on average (behavior may be over-penalized).
- Penalty ratio is high (1.91), negative rewards dominate.

### Glossary

- **Reward breakdown:** Per-component average reward contribution per episode.
- **Reward dominance index:** HHI-style dominance of positive rewards (higher = more concentrated).
- **Reward entropy:** Normalized entropy of positive reward components (balance proxy).
- **Reward max share:** Share of total positive reward from the largest component.
- **Positive component count:** Number of reward components with positive contribution.

## Population Health Dashboard

### Current Status: Watch

| Metric | Value | Trend (Recent) |
|--------|-------|----------------|
| Diversity Index | 0.91 | Decreasing |
| Elite Gap | 2.69 | Stable |
| Min Fitness Trend | -0.3 | Down |
| Max Fitness Trend | -11.5 | Down |
| IQR (p75-p25) | 122 | Narrowing |

### Takeaways

- Health status is Watch.
- Diversity index at 0.91 with decreasing spread.
- Fitness floor trend -0.3, ceiling trend -11.5.

### Warnings

- Fitness floor trending down (weakest agents worsening)

### Glossary

- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Average fitness:** Mean fitness across the population for a generation.
- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Fitness p25:** 25th percentile of population fitness.
- **Fitness p75:** 75th percentile of population fitness.

## Stagnation Analysis

- **Current Stagnation:** 23 generations
- **Average Stagnation Period:** 20.0 generations
- **Longest Stagnation:** 82 generations
- **Number of Stagnation Periods:** 9

### Takeaways

- Stagnation periods average 20.0 generations.
- Longest plateau reached 82 generations.

### Warnings

- Current stagnation is above typical plateaus.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).

## Generalization Analysis (Fresh Game)

### Recent Fresh Game Performance

| Gen | Training Fit | Fresh Fit | Accuracy | Ratio | Grade | Cause of Death |
|-----|--------------|-----------|----------|-------|-------|----------------|
| 180 | 302 | -233 | 25.6% | -2.20 | F | asteroid_collision |
| 181 | 90 | -153 | 36.7% | 0.00 | F | asteroid_collision |
| 182 | 113 | -191 | 29.3% | 0.00 | F | asteroid_collision |
| 183 | 183 | 27 | 42.2% | 0.20 | F | asteroid_collision |
| 184 | 165 | 338 | 51.1% | 3.28 | A | completed_episode |
| 185 | 138 | -236 | 34.1% | -3.44 | F | asteroid_collision |
| 186 | 167 | -293 | 13.3% | 0.00 | F | asteroid_collision |
| 187 | 162 | -92 | 37.1% | -0.73 | F | asteroid_collision |
| 188 | 247 | -27 | 31.0% | -0.17 | F | asteroid_collision |
| 189 | 6 | -170 | 38.7% | 0.00 | F | asteroid_collision |

### Generalization Summary

- **Average Fitness Ratio:** 2.37
- **Best Ratio:** 9.27
- **Worst Ratio:** 0.00

**Grade Distribution:** A:17 B:1 D:2 F:169 

### Reward Transfer Gap (Fresh vs Training)

| Gen | Share Shift | Largest Share Deltas |
|-----|-------------|----------------------|
| 180 |    4.6% | ExplorationBonus +5%, VelocitySurvivalBonus -3%, DistanceBasedKillReward -2% |
| 181 |   15.5% | DistanceBasedKillReward +15%, ExplorationBonus -10%, VelocitySurvivalBonus -6% |
| 182 |    4.3% | DistanceBasedKillReward +4%, VelocitySurvivalBonus -3%, ExplorationBonus -1% |
| 183 |    5.5% | DistanceBasedKillReward +6%, VelocitySurvivalBonus -3%, ExplorationBonus -3% |
| 184 |    7.0% | DistanceBasedKillReward +6%, ExplorationBonus -4%, VelocitySurvivalBonus -3% |
| 185 |   15.6% | ExplorationBonus +16%, DistanceBasedKillReward -13%, VelocitySurvivalBonus -2% |
| 186 |   94.9% | ExplorationBonus +95%, DistanceBasedKillReward -94%, VelocitySurvivalBonus -1% |
| 187 |    5.8% | DistanceBasedKillReward +6%, ExplorationBonus -5%, VelocitySurvivalBonus -1% |
| 188 |    3.7% | DistanceBasedKillReward +4%, ExplorationBonus -2%, VelocitySurvivalBonus -1% |
| 189 |    6.1% | DistanceBasedKillReward +6%, ExplorationBonus -4%, VelocitySurvivalBonus -2% |

### Takeaways

- Average fitness ratio 2.37 (range 0.00 to 9.27).

### Warnings

- Generalization ratios are low relative to peak training performance.
- Some generations show severe generalization drop-off.

### Glossary

- **Fitness ratio:** Fresh-game fitness divided by training fitness for the same generation.
- **Generalization grade:** Letter grade derived from generalization ratios.
- **Reward breakdown:** Per-component average reward contribution per episode.

## Correlation Analysis

### Fitness Correlations

| Metric | Correlation | Strength |
|--------|-------------|----------|
| Kills | +0.99 | Strong |
| Steps Survived | +0.97 | Strong |
| Accuracy | +0.90 | Strong |

### Interpretation

Fitness is most strongly predicted by kills (r=0.99).

### Takeaways

- Strongest fitness driver: kills (r=0.99).

### Glossary

- **Average fitness:** Mean fitness across the population for a generation.
- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).

## Survival Distribution - Still in Early Phases

### Survival Statistics (Final Phase)

- **Mean Survival:** 702 steps (46.8% of max)
- **Max Survival:** 1500 steps

### Survival Progression (Phase Averages)

| Phase | Mean Steps | Change vs Prior |
|-------|------------|-----------------|
| Phase 1 (0-25%) | 717 |  |
| Phase 2 (25-51%) | 710 | -8 |
| Phase 3 (51-75%) | 686 | -24 |
| Phase 4 (75-100%) | 702 | +16 |

### Takeaways

- Final-phase survival averages 702 steps.
- Best survival reached 1500 steps.

### Warnings

- Average survival remains below half of max steps; survivability is still limited.

### Glossary

- **Average steps:** Mean steps survived per episode across the population.
- **Max steps:** Highest steps survived by any agent in the generation.

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 6.55
- **Avg Steps Survived:** 660
- **Avg Accuracy:** 34.2%
- **Max Kills (Any Agent Ever):** 24.666666666666668
- **Max Steps (Any Agent Ever):** 1500.0

### Takeaways

- Recent average kills: 6.55.
- Recent average accuracy: 34.2%.

### Glossary

- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).

## Learning Progress

| Phase | Gens | Avg Best | Avg Mean | Avg Min |
|-------|------|----------|----------|---------|
| Phase 1 (0-25%) | 1-48 | 175.2 | -96.5 | -245.6 |
| Phase 2 (25-51%) | 49-96 | 167.9 | -95.9 | -245.5 |
| Phase 3 (51-75%) | 97-143 | 166.2 | -102.3 | -252.3 |
| Phase 4 (75-100%) | 144-190 | 163.7 | -96.8 | -246.0 |

### Takeaways

- Best fitness trend: stagnation (low confidence).
- Average fitness trend: volatile (low confidence (noisy)).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.

## Neural & Behavioral Complexity

| Gen | Saturation | Entropy | Control Style |
|-----|------------|---------|---------------|
| 161 |   8.4% |  0.75 | Balanced / Repetitive |
| 162 |   6.1% |  0.96 | Balanced |
| 163 |   5.5% |  1.10 | Analog-leaning / Exploratory |
| 164 |   8.2% |  0.95 | Balanced |
| 165 |  10.5% |  0.85 | Balanced / Repetitive |
| 166 |  12.2% |  0.79 | Balanced / Repetitive |
| 167 |  13.0% |  0.88 | Binary-leaning |
| 168 |  15.4% |  0.85 | Binary-leaning / Repetitive |
| 169 |  21.1% |  0.75 | Binary-leaning / Repetitive |
| 170 |  18.3% |  0.73 | Binary-leaning / Repetitive |
| 171 |  13.9% |  0.84 | Binary-leaning / Repetitive |
| 172 |  15.4% |  0.84 | Binary-leaning / Repetitive |
| 173 |  14.2% |  0.83 | Binary-leaning / Repetitive |
| 174 |  15.8% |  0.77 | Binary-leaning / Repetitive |
| 175 |  10.7% |  0.94 | Balanced |
| 176 |  12.6% |  0.82 | Binary-leaning / Repetitive |
| 177 |  11.2% |  0.78 | Balanced / Repetitive |
| 178 |  12.5% |  0.70 | Binary-leaning / Repetitive |
| 179 |  14.6% |  0.76 | Binary-leaning / Repetitive |
| 180 |   4.5% |  1.16 | Analog-leaning / Exploratory |
| 181 |   6.9% |  0.93 | Balanced |
| 182 |   6.9% |  0.94 | Balanced |
| 183 |   7.9% |  0.93 | Balanced |
| 184 |   7.2% |  0.87 | Balanced |
| 185 |   7.8% |  0.87 | Balanced |
| 186 |   7.4% |  0.96 | Balanced |
| 187 |   9.1% |  0.91 | Balanced |
| 188 |   7.3% |  0.97 | Balanced |
| 189 |  11.1% |  0.83 | Balanced / Repetitive |
| 190 |   8.1% |  0.82 | Balanced / Repetitive |

### Takeaways

- Output saturation trend: stagnation (low confidence (noisy)).
- Action entropy trend: stagnation (low confidence).

### Glossary

- **Output saturation:** Share of NN outputs near 0 or 1 (binary control tendency).
- **Action entropy:** Entropy of action combinations (higher = more varied control).

## Risk Profile Analysis

Analysis of how close agents let asteroids get before reacting or killing them.

| Gen | Avg Min Dist | Fitness | Kills | Archetype |
|-----|--------------|---------|-------|-----------|
| 161 |   13.9px | -178.8 |  4.3 | Overexposed |
| 162 |   14.7px |  -73.2 |  8.4 | Balanced |
| 163 |   15.6px |  -88.5 |  7.0 | Balanced |
| 164 |   14.7px | -127.6 |  6.3 | Overexposed |
| 165 |   15.0px |  -31.5 | 10.0 | Balanced |
| 166 |   17.0px | -109.2 |  6.9 | Balanced |
| 167 |   14.3px |  -63.0 |  8.6 | Daredevil |
| 168 |   18.7px |  -62.7 |  8.5 | Sniper |
| 169 |   15.1px | -186.6 |  4.4 | Balanced |
| 170 |   14.5px | -233.5 |  2.3 | Overexposed |
| 171 |   17.3px |  -68.8 |  8.3 | Balanced |
| 172 |   14.1px | -111.7 |  6.6 | Balanced |
| 173 |   14.6px | -170.9 |  4.6 | Overexposed |
| 174 |   14.9px | -126.9 |  6.2 | Balanced |
| 175 |   18.0px |  -14.2 | 10.1 | Sniper |
| 176 |   15.3px |  -66.3 |  8.2 | Balanced |
| 177 |   17.9px |  -56.8 |  8.8 | Sniper |
| 178 |   15.2px | -109.1 |  6.7 | Balanced |
| 179 |   15.9px | -115.8 |  6.6 | Balanced |
| 180 |   16.1px |  -34.0 |  8.8 | Balanced |
| 181 |   15.8px | -207.3 |  2.8 | Balanced |
| 182 |   14.9px | -108.3 |  6.7 | Balanced |
| 183 |   15.9px |  -82.7 |  7.7 | Balanced |
| 184 |   15.0px |  -86.4 |  7.5 | Balanced |
| 185 |   14.4px |  -86.2 |  7.7 | Balanced |
| 186 |   16.1px |  -62.4 |  8.3 | Balanced |
| 187 |   17.0px | -144.1 |  5.5 | Cautious Underperformer |
| 188 |   16.1px |  -34.2 |  9.4 | Sniper |
| 189 |   16.5px | -211.5 |  3.4 | Cautious Underperformer |
| 190 |   15.3px | -115.0 |  6.4 | Balanced |

### Takeaways

- Min-distance trend: stagnation (low confidence).
- Danger exposure trend: volatile (low confidence (noisy)).

### Glossary

- **Min asteroid distance:** Closest distance to an asteroid during an episode (pixels).
- **Average asteroid distance:** Mean distance to nearest asteroid over time (pixels).
- **Danger exposure rate:** Fraction of frames with a nearby asteroid inside danger radius.
- **Soft-min TTC:** Weighted time-to-collision proxy that emphasizes the nearest threats (seconds).

## Control Diagnostics

### Control Snapshot (Latest Generation)

| Category | Metric | Value |
|----------|--------|-------|
| Turn | Deadzone Rate | 0.0% |
| Turn | Turn Balance (R-L) | -0.05 |
| Turn | Switch Rate | 26.0% |
| Turn | Avg Streak | 30.5f |
| Turn | Max Streak | 158f |
| Aim | Frontness Avg | 51.3% |
| Aim | Frontness at Shot | 51.2% |
| Aim | Frontness at Hit | 56.5% |
| Aim | Shot Distance | 166.7px |
| Aim | Hit Distance | 125.8px |
| Danger | Exposure Rate | 15.7% |
| Danger | Entries | 2.8 |
| Danger | Reaction Time | 0.0f |
| Danger | Wraps in Danger | 0.0 |
| Movement | Distance Traveled | 64.6px |
| Movement | Avg Speed | 0.08 |
| Movement | Speed Std | 0.08 |
| Movement | Coverage Ratio | 11.9% |
| Shooting | Shots per Kill | 7.40 |
| Shooting | Shots per Hit | 2.39 |
| Shooting | Cooldown Usage | 89.0% |
| Shooting | Cooldown Ready | 1.5% |
| Stability | Fitness Std (Seeds) | 109.1 |

### Recent Control Trends (Last 10)

| Gen | Deadzone | Turn Bias | Switch | Frontness | Danger | Coverage |
|-----|----------|-----------|--------|-----------|--------|----------|
| 181 |    0.0% |  -0.22 |   28.4% |   51.6% |   13.8% |   15.1% |
| 182 |    0.0% |  -0.08 |   30.7% |   52.2% |   14.7% |   16.1% |
| 183 |    0.0% |  -0.18 |   28.5% |   50.8% |   19.2% |   17.1% |
| 184 |    0.0% |  -0.26 |   26.4% |   50.9% |   19.3% |   16.9% |
| 185 |    0.0% |  -0.04 |   28.2% |   51.1% |   16.2% |   15.2% |
| 186 |    0.0% |  +0.02 |   28.8% |   50.6% |   18.3% |   13.4% |
| 187 |    0.0% |  -0.02 |   29.1% |   50.2% |   14.4% |   13.7% |
| 188 |    0.0% |  +0.15 |   32.2% |   51.4% |   17.9% |   14.0% |
| 189 |    0.0% |  +0.02 |   32.3% |   50.4% |   13.3% |   10.9% |
| 190 |    0.0% |  -0.05 |   26.0% |   51.3% |   15.7% |   11.9% |





### Takeaways

- Turn balance trend: stagnation (low confidence).
- Aim alignment trend: stagnation (low confidence).
- Danger exposure trend: volatile (low confidence (noisy)).

### Glossary

- **Turn deadzone rate:** Fraction of frames where signed turn input is exactly zero (deadzone currently disabled).
- **Turn balance:** Right-turn frames minus left-turn frames divided by total turning.
- **Turn switch rate:** Rate of turn direction switches per signed turn.
- **Average turn streak:** Average consecutive frames turning in the same direction.
- **Max turn streak:** Longest consecutive turn streak per episode (averaged).
- **Frontness average:** Alignment of nearest asteroid with ship heading (1 ahead, 0 behind).
- **Frontness at shot:** Frontness measured at shot times (aim alignment during firing).
- **Frontness at hit:** Frontness measured at hit times (aim alignment on hits).
- **Shot distance:** Distance to nearest asteroid when firing (pixels).
- **Hit distance:** Distance to nearest asteroid when hits occur (pixels).
- **Danger exposure rate:** Fraction of frames with a nearby asteroid inside danger radius.
- **Danger entries:** Average number of entries into the danger zone per episode.
- **Danger reaction time:** Average frames to react after entering danger.
- **Danger wraps:** Screen-wrap count while in danger zones (mobility under threat).
- **Distance traveled:** Total distance traveled per episode (pixels).
- **Average speed:** Mean movement speed per episode.
- **Speed std dev:** Standard deviation of movement speed per episode.
- **Coverage ratio:** Fraction of spatial grid cells visited (0 to 1).
- **Shots per kill:** Shots fired divided by kills (lower is more efficient).
- **Shots per hit:** Shots fired divided by hits (lower is more efficient).
- **Seed fitness std:** Average per-agent fitness std dev across seeds (evaluation noise proxy).

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 88.51
- Average Range (Best-Min): 412.66
- Diversity Change: -1.4%
- **Status:** Population has balanced diversity

### Takeaways

- Convergence status: balanced.
- Diversity change: -1.4%.

### Glossary

- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Minimum fitness:** Lowest fitness in the population for a generation.

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Safe Dist | Max Kills |
|--------|-----------|-----------|--------------|-----------|----------|
| Q1 | 6.74 | 715 | 34.8% | 158.1px | 21.666666666666668 |
| Q2 | 7.13 | 708 | 35.7% | 163.1px | 24.333333333333332 |
| Q3 | 6.86 | 683 | 35.3% | 164.6px | 24.666666666666668 |
| Q4 | 7.34 | 709 | 35.1% | 162.4px | 23.333333333333332 |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
|--------|----------|--------|---------|-------------------|
| Q1 | 6.1% | 100.0% | 78.6% | **Skirmisher** |
| Q2 | 3.2% | 100.0% | 90.4% | **Balanced** |
| Q3 | 3.9% | 100.0% | 94.5% | **Balanced** |
| Q4 | 2.2% | 100.0% | 94.5% | **Balanced** |

### Input Control Style

| Period | Thrust Dur | Turn Dur | Shoot Dur | Idle Rate | Wraps |
|--------|------------|----------|-----------|-----------|-------|
| Q1 | 3.4f | 715.0f | 140.7f | 0.0% | 0.2 |
| Q2 | 0.8f | 707.9f | 185.7f | 0.0% | 0.1 |
| Q3 | 1.0f | 682.9f | 275.0f | 0.0% | 0.2 |
| Q4 | 0.6f | 709.0f | 271.7f | 0.0% | 0.1 |

### Takeaways

- Kills trend: volatile.
- Accuracy trend: stagnation.
- Idle rate trend: stagnation.

### Glossary

- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Average asteroid distance:** Mean distance to nearest asteroid over time (pixels).
- **Thrust frames:** Average frames with thrust active per episode.
- **Turn frames:** Average frames with turn input active per episode.
- **Shoot frames:** Average frames with shooting active per episode.
- **Thrust duration:** Average consecutive frames per thrust burst.
- **Turn duration:** Average consecutive frames per turning burst.
- **Shoot duration:** Average consecutive frames per shooting burst.
- **Idle rate:** Fraction of frames with no action input.
- **Screen wraps:** Average number of screen-edge wraps per episode.

### Intra-Episode Score Breakdown

Analysis of when agents earn their reward during an episode (Early vs Late game).

| Quarter | Avg Score | Share of Total | Play Style |
|---------|-----------|----------------|------------|
| Start (0-25%) | 5.2 | -4.6% | Balanced |
| Mid-Game (25-50%) | 19.3 | -17.1% | Balanced |
| Late-Game (50-75%) | 35.9 | -31.9% | Balanced |
| End-Game (75-100%) | -173.3 | 153.6% | Back-loaded |

### Intra-Episode Takeaways

- Highest scoring quarter: Late-Game (50-75%) (-31.9% of episode reward).

### Intra-Episode Glossary

- **Quarterly scores:** Average reward earned in each episode quarter (0-25%, 25-50%, 50-75%, 75-100%).

## Recent Generations (Last 30)

<details>
<summary>Click to expand Recent Generations table</summary>

| Gen   | Best   | Avg    | StdDev | Kills  | Steps  | Acc%   | Stag   |
|-------|--------|--------|--------|--------|--------|--------|--------|
| 161   | 16     | -179   | 79     | 4.3    | 496    | 27     | 77     |
| 162   | 201    | -73    | 94     | 8.4    | 748    | 35     | 78     |
| 163   | 175    | -88    | 100    | 7.0    | 701    | 38     | 79     |
| 164   | 140    | -128   | 89     | 6.3    | 577    | 33     | 80     |
| 165   | 333    | -32    | 94     | 10.0   | 890    | 37     | 81     |
| 166   | 85     | -109   | 78     | 6.9    | 665    | 33     | 82     |
| 167   | 364    | -63    | 102    | 8.6    | 776    | 36     | 0      |
| 168   | 122    | -63    | 80     | 8.5    | 792    | 41     | 1      |
| 169   | 98     | -187   | 67     | 4.4    | 466    | 31     | 2      |
| 170   | 8      | -233   | 72     | 2.3    | 322    | 20     | 3      |
| 171   | 271    | -69    | 97     | 8.3    | 803    | 40     | 4      |
| 172   | 223    | -112   | 117    | 6.6    | 652    | 35     | 5      |
| 173   | 5      | -171   | 61     | 4.6    | 497    | 32     | 6      |
| 174   | 226    | -127   | 90     | 6.2    | 589    | 34     | 7      |
| 175   | 200    | -14    | 86     | 10.1   | 937    | 43     | 8      |
| 176   | 165    | -66    | 99     | 8.2    | 791    | 37     | 9      |
| 177   | 214    | -57    | 88     | 8.8    | 817    | 39     | 10     |
| 178   | 132    | -109   | 91     | 6.7    | 657    | 36     | 11     |
| 179   | 188    | -116   | 84     | 6.6    | 637    | 32     | 12     |
| 180   | 302    | -34    | 118    | 8.8    | 840    | 41     | 13     |
| 181   | 90     | -207   | 74     | 2.8    | 405    | 28     | 14     |
| 182   | 113    | -108   | 93     | 6.7    | 653    | 31     | 15     |
| 183   | 183    | -83    | 90     | 7.7    | 737    | 37     | 16     |
| 184   | 165    | -86    | 101    | 7.5    | 712    | 36     | 17     |
| 185   | 138    | -86    | 84     | 7.7    | 735    | 33     | 18     |
| 186   | 167    | -62    | 91     | 8.3    | 784    | 39     | 19     |
| 187   | 162    | -144   | 82     | 5.5    | 615    | 33     | 20     |
| 188   | 247    | -34    | 94     | 9.4    | 884    | 39     | 21     |
| 189   | 6      | -212   | 54     | 3.4    | 390    | 26     | 22     |
| 190   | 113    | -115   | 76     | 6.4    | 684    | 41     | 23     |

</details>

### Recent Table Takeaways

- Recent table covers 30 generations ending at Gen 190.
- Latest best fitness: 113.5.

### Recent Table Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Median fitness:** Median population fitness (robust central tendency).
- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Best improvement:** Change in best fitness compared to the previous generation.
- **Average improvement:** Change in average fitness compared to the previous generation.
- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).


## Top 10 Best Generations

<details>
<summary>Click to expand Top 10 Best Generations table</summary>

| Rank | Gen   | Best   | Avg    | Kills  | Steps  | Accuracy |
|------|-------|--------|--------|--------|--------|----------|
| 1    | 167   | 364    | -63    | 21.3   | 1500   | 48.6     |
| 2    | 84    | 355    | -49    | 24.3   | 1500   | 53.2     |
| 3    | 68    | 341    | -87    | 22.0   | 1279   | 55.4     |
| 4    | 165   | 333    | -32    | 23.3   | 1352   | 54.0     |
| 5    | 107   | 326    | -1     | 21.0   | 1390   | 51.4     |
| 6    | 34    | 318    | -58    | 20.3   | 1218   | 49.8     |
| 7    | 142   | 313    | 17     | 17.7   | 1500   | 46.1     |
| 8    | 17    | 311    | -23    | 20.0   | 1311   | 52.2     |
| 9    | 119   | 305    | -42    | 24.7   | 1485   | 55.2     |
| 10   | 180   | 302    | -34    | 18.3   | 1187   | 50.8     |

</details>

### Top Generations Takeaways

- Top generation is Gen 167 with best fitness 364.0.

### Top Generations Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Accuracy:** Hits divided by shots fired (0 to 1).


## Trend Analysis

| Phase | Avg Best | Avg Mean | Avg Min | Improvement |
|-------|----------|----------|---------|-------------|
| Phase 1 (0-25%) | 175.2 | -96.5 | -245.6 |  |
| Phase 2 (25-51%) | 167.9 | -95.9 | -245.5 | -7.3 |
| Phase 3 (51-75%) | 166.2 | -102.3 | -252.3 | -1.7 |
| Phase 4 (75-100%) | 163.7 | -96.8 | -246.0 | -2.5 |

### Takeaways

- Best fitness: stagnation (low confidence).
- Average fitness: volatile (low confidence (noisy)).
- Minimum fitness: volatile (low confidence (noisy)).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

     318 |           *                                                    
     283 |                                               *                
     248 |                   *                      *  *  *  *            
     213 |        **  *   *          *          * *                *      
     178 |     **          *       *       *                        *     
     143 |* *    *  *    *        *                     *  **  **      ** 
     108 |             *    * * **  *  *     * * * *  *              *   *
      73 | * **         *             *  *    *      *        *  **   *   
      38 |                   o *        * * *                             
       3 |                                               o                
     -32 |                                             o    oo      o     
     -67 |         o oo  ooo     o o o                    oo              
    -102 |     o  o     o       o     o    o    ooo     o       o      o  
    -137 |o o   oo          o  o    o  o     ooo    o o       o  o o o   o
    -172 | o oo     o  o      o   o     ooo        o                    o 
    -207 |                                  o        o         o  o   o   
         ----------------------------------------------------------------
         Gen 1                                                 Gen 190
```

### Takeaways

- Best fitness trend: stagnation (low confidence).
- Average fitness trend: volatile (low confidence (noisy)).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.


---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 0.00s
- **Evaluation (Simulation):** 3275.37s (0.0%)
- **Evolution (GA Operators):** 0.0000s (0.0%)

| Phase | Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
|-------|-----------|---------------|---------------|------------|
| Phase 1 (0-25%) | 1-48 | 111.86s | 0.0000s | 0.00s |
| Phase 2 (25-51%) | 49-96 | 106.95s | 0.0000s | 0.00s |
| Phase 3 (51-75%) | 97-143 | 102.58s | 0.0000s | 0.00s |
| Phase 4 (75-100%) | 144-190 | 780.37s | 0.0000s | 0.00s |

### Takeaways

- Evaluation accounts for 0.0% of generation time.
- Evolution accounts for 0.0% of generation time.

### Glossary

- **Evaluation duration:** Wall time spent evaluating a generation.
- **Evolution duration:** Wall time spent evolving a generation.
- **Total generation duration:** Combined evaluation and evolution wall time.

## ES Optimizer Diagnostics

**Recent Averages (Last 10 Generations):**
- **Sigma:** 0.14635
- **Cov diag mean:** 0.99980
- **Cov diag std:** 0.000571
- **Cov diag mean abs dev:** 0.000481
- **Cov diag max abs dev:** 0.002407
- **Cov lr scale:** 541.95
- **Cov lr effective rate:** 0.001000

### Optimizer Takeaways

- CMA-ES step-size and diagonal covariance movement are tracked across recent generations.

### Optimizer Glossary

- **Sigma:** CMA-ES global step size controlling exploration radius.
- **Cov diag mean:** Mean diagonal covariance value (per-parameter variance).
- **Cov diag std:** Standard deviation of diagonal covariance values.
- **Cov diag mean abs dev:** Mean absolute deviation of diagonal covariance from 1.0.
- **Cov diag max abs dev:** Largest absolute deviation of diagonal covariance from 1.0.
- **Cov lr scale:** Scaling factor applied to CMA-ES covariance learning rates (c1/cmu).
- **Cov lr effective rate:** Effective c1 + cmu rate used for diagonal covariance update.

