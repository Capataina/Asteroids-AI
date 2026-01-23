# Training Summary Report

**Generated:** 2026-01-23 22:56:35
**Schema Version:** 2.3

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
- [Correlation Analysis](#correlation-analysis)
- [Survival Distribution](#survival-distribution)
- [Behavioral Summary](#behavioral-summary-last-10-generations)
- [Learning Progress](#learning-progress)
- [Neural & Behavioral Complexity](#neural--behavioral-complexity)
- [Risk Profile Analysis](#risk-profile-analysis)
- [Control Diagnostics](#control-diagnostics)
- [Graph Neural Network and Soft Actor-Critic Diagnosis](#graph-neural-network-and-soft-actor-critic-diagnosis)
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
Best Fitness     -3 -> 8  [ .:- :..-==-==--@=+*]  breakout improvement (low confidence (noisy))
Avg Fitness      -9 -> -2  [...: ...:=--=-::@---]  great improvement (low confidence (noisy))
Min Fitness      -15 -> -10  [...:  ..:-:-=-.:@:::]  steady improvement (moderate confidence)
Fitness Spread   5 -> 8  [ :.- =. ==+:--=:**%@]  regression (moderate confidence)
Avg Kills        1.9 -> 3.0  [::.: . .:--:-:..@---]  steady improvement (moderate confidence)
Avg Accuracy     31% -> 47%  [  +-:-==+*%+@##+##+#]  stagnation (low confidence)
Avg Steps        315 -> 353  [+- -    ::::....@-- ]  slight improvement (low confidence)
Seed Fitness Std 4.7 -> 7.5  [ :.- =. ==+:--=:**%@]  regression (moderate confidence)
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
- Overall Summary: best fitness 56.00 at Gen 166.
- Best Agent Deep Profile: Gen 166 with 0 kills.
- Heatmaps: spatial patterns available for best agent and population.
- Generation Highlights: top improvements/regressions and record runs flagged.
- Milestone Timeline: milestones are run-relative (percent-of-peak thresholds).
- Training Progress by Phase: 4 equal phases used for normalized comparisons.
- Distribution Analysis: fitness spread trend is regression.
- Kill Efficiency: phase-level kill rates and shot efficiency tracked.
- Learning Velocity: phase-based fitness deltas and acceleration reported.
- Reward Component Evolution: per-component shifts tracked across 4 phases.
- Reward Balance Analysis: dominance, entropy, and penalty skew checked.
- Population Health Dashboard: diversity, elite gap, and floor trends summarized.
- Stagnation Analysis: plateau lengths compared to run history.
- Generalization Analysis: no fresh-game data recorded.
- Correlation Analysis: fitness vs kills/survival/accuracy correlations reported.
- Survival Distribution: phase-level survival averages and max survival summarized.
- Behavioral Summary: recent kills, steps, and accuracy summarized.
- Learning Progress: phase comparisons for best/avg/min fitness.
- Neural & Behavioral Complexity: saturation and entropy trends reported.
- Risk Profile Analysis: proximity trends and archetypes reported.
- Control Diagnostics: turn bias, frontness, danger, and movement diagnostics reported.
- GNN-SAC Diagnosis: learner health, replay quality, action saturation, and eval trends reported.
- Convergence Analysis: recent diversity and range trends summarized.
- Behavioral Trends: action mix and intra-episode scoring patterns reported.
- Recent Generations: last 30 gens tabulated.
- Top Generations: best run is Gen 166.
- Trend Analysis: phase-based fitness trend table provided.
- ASCII Chart: best vs avg fitness progression visualized.
- Technical Appendix: runtime costs, operator stats, and ES optimizer diagnostics reported when available.

## Training Configuration

```
method: GNN + SAC
total_steps: 500000
max_episode_steps: 1500
frame_delay: 0.016666666666666666
gamma: 0.99
tau: 0.005
batch_size: 256
replay_size: 100000
learn_start_steps: 5000
updates_per_step: 1
reward_scale: 0.2
obs_norm_enabled: True
obs_norm_eps: 1e-08
obs_norm_clip: None
action_smoothing_enabled: False
action_smoothing_alpha: 0.6
num_collectors: 1
collector_seed_offset: 10000
actor_lr: 0.0003
critic_lr: 0.0001
alpha_lr: 0.0003
critic_loss: huber
huber_delta: 1.0
auto_entropy: True
init_alpha: 0.2
target_entropy: -3.0
agc_enabled: True
agc_clip_factor: 0.01
agc_eps: 0.001
gnn_hidden_dim: 64
gnn_num_layers: 2
gnn_heads: 4
gnn_dropout: 0.0
actor_hidden_dim: 256
critic_hidden_dim: 256
max_asteroids: None
device: cuda
eval_seeds: [1001, 1002, 1003, 1004, 1005]
holdout_eval_seeds: []
eval_every_episodes: 5
best_checkpoint_path: training/sac_checkpoints/best_sac.pt
```

### Config Takeaways

- Configuration snapshot captures the exact training parameters for reproducibility.

### Config Glossary

- **Config value:** Literal hyperparameter or run setting recorded at training start.

## Overall Summary

- **Total Generations:** 171
- **Training Duration:** 2 days, 22:08:35.620284
- **All-Time Best Fitness:** 56.00
- **Best Generation:** 166
- **Final Best Fitness:** -2.76
- **Final Average Fitness:** -10.74
- **Avg Improvement (Phase 1->Phase 4):** 7.52
- **Stagnation:** 5 generations since improvement

### Takeaways

- Best fitness achieved: 56.00 (Gen 166).
- Final avg fitness: -10.74.
- Current stagnation: 5 generations without improvement.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Avg improvement (Phase 1->Phase 4):** Difference between average fitness in the first and last 25% of training.

## Best Agent Deep Profile

The most fit agent appeared in **Generation 166** with a fitness of **56.00**.

### Combat Efficiency

- **Total Kills:** 0
- **Survival Time:** 0.0 seconds (0 steps)
- **Accuracy:** 0.0%
- **Shots per Kill:** 0.0
- **Time per Kill:** 0.00 seconds

### Behavioral Signature

**Classification:** `Drifter`

| Action | Rate (per step) | Description |
|--------|-----------------|-------------|
| **Thrust** | 0.0% | Movement frequency |
| **Turn** | 0.0% | Rotation frequency |
| **Shoot** | 0.0% | Trigger discipline |

### Takeaways

- Best agent achieved 0 kills with 0.0% accuracy.
- Behavioral classification: Drifter.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Average steps:** Mean steps survived per episode across the population.
- **Shots per kill:** Shots fired divided by kills (lower is more efficient).

## Generation Highlights

### Best Improvement

**Generation 166**: Best fitness jumped +60.3 (+1415.8%)
- New best fitness: 56.0

### Worst Regression

**Generation 167**: Best fitness dropped -52.0 (-92.8%)
- New best fitness: 4.0
- Note: this can be normal variation after a lucky outlier

### Most Accurate Generation

**Generation 168**: Population accuracy reached 85.7%

### Most Kills (Single Agent)

**Generation 166**: An agent achieved 16 kills

### First Viable Population

**Generation 27**: Average fitness first became positive

### Most Diverse Generation

**Generation 27**: Diversity index 97.52

### Most Converged Generation

**Generation 33**: Diversity index 0.02

### Takeaways

- Best improvement at Gen 166 (+60.3).
- Worst regression at Gen 167 (-52.0).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Accuracy:** Hits divided by shots fired (0 to 1).
- **Max kills:** Highest kills achieved by any agent in the generation.
- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).

## Milestone Timeline

| Generation | Category | Value | Description |
|------------|----------|-------|-------------|
| 4 | Kills | 5 | Max kills reached 25% of run peak |
| 14 | Fitness | 15 | Best fitness reached 25% of run peak |
| 14 | Kills | 8 | Max kills reached 50% of run peak |
| 27 | Viability | 0 | Average fitness turned positive |
| 46 | Fitness | 29 | Best fitness reached 50% of run peak |
| 83 | Avg Fitness | 9 | Avg fitness reached 25% of run peak |
| 108 | Avg Fitness | 20 | Avg fitness reached 50% of run peak |
| 140 | Avg Fitness | 32 | Avg fitness reached 75% of run peak |
| 140 | Avg Fitness | 32 | Avg fitness reached 90% of run peak |
| 141 | Kills | 12 | Max kills reached 75% of run peak |
| 166 | Fitness | 56 | Best fitness reached 75% of run peak |
| 166 | Fitness | 56 | Best fitness reached 90% of run peak |
| 166 | Fitness | 56 | Best fitness reached 95% of run peak |
| 166 | Fitness | 56 | Best fitness reached 98% of run peak |
| 166 | Kills | 16 | Max kills reached 90% of run peak |

### Takeaways

- Total milestones reached: 15.
- Latest milestone at Gen 166 (Kills).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Max kills:** Highest kills achieved by any agent in the generation.

## Training Progress by Phase

| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|------|----------|---------|-----------|---------|-----------|----------|
| Phase 1 (0-25%) | 1-43 | 18 | -9 | 1.9 | 31% | 315 | 5 |
| Phase 2 (25-50%) | 44-86 | 29 | -7 | 2.1 | 40% | 294 | 5 |
| Phase 3 (50-75%) | 87-129 | 28 | -5 | 2.2 | 50% | 283 | 6 |
| Phase 4 (75-100%) | 130-171 | 56 | -2 | 3.0 | 47% | 353 | 8 |

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

**Fitness Distribution**
```
Gen 162:                       |O|                             5.8 +/-   1.4
Gen 163:         |-----O-----|                                -5.4 +/-   7.1
Gen 164:       |---------O--------|                           -3.3 +/-  11.6
Gen 165:        |---O--|                                      -9.7 +/-   4.3
Gen 166: |----------------------O-----------------------|      5.6 +/-  29.1
Gen 167:           |---O----|                                 -5.3 +/-   5.4
Gen 168:                       O                               4.2 +/-   0.0
Gen 169:       |----------O---------|                         -2.3 +/-  13.0
Gen 170:       |--O---|                                      -11.3 +/-   4.0
Gen 171:      |----O----|                                    -10.7 +/-   5.8
```

### Takeaways

- Fitness spread trend: regression (moderate confidence).
- Seed variance trend: regression (moderate confidence).

### Warnings

- Fitness spread is widening or volatile; convergence is weak.
- Seed-to-seed variance is rising; evaluation noise may mask true improvements.

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

- **Kills per 100 Steps:** 0.86 (Phase 1: 0.61)
- **Shots per Kill:** 5.72 (Phase 1: 9.31)
- **Kill Conversion Rate:** 17.5% (Phase 1: 10.7%)
- **Average Kills per Episode:** 3.0

### Efficiency Trend (Phase Averages)

| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |
|-------|-----------------|------------|----------------|
| Phase 1 (0-25%) | 0.61 | 9.31 | 10.7% |
| Phase 2 (25-50%) | 0.73 | 6.83 | 14.6% |
| Phase 3 (50-75%) | 0.78 | 5.78 | 17.3% |
| Phase 4 (75-100%) | 0.86 | 5.72 | 17.5% |

### Takeaways

- Kill rate changed from 0.61 to 0.86 kills/100 steps.
- Shots per kill moved from 9.31 to 5.72.

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
| Phase 1 (0-25%) | +7 | +0.2 | Slow |
| Phase 2 (25-50%) | +18 | +0.4 | Fast |
| Phase 3 (50-75%) | +12 | +0.3 | Fast |
| Phase 4 (75-100%) | -6 | -0.2 | Slow |

### Current Velocity

- **Recent Improvement Rate:** -0.2 fitness/generation
- **Acceleration:** -0.2 (positive = speeding up)

### Takeaways

- Velocity mean +0.2 with std 0.2 across phases.

### Warnings

- Recent learning velocity is in the slowest quartile of the run.
- Learning is decelerating faster than typical phase-to-phase variation.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).

## Reward Component Evolution

No reward breakdown data available.

## Reward Balance Analysis

### Glossary

- **Reward breakdown:** Per-component average reward contribution per episode.
- **Reward dominance index:** HHI-style dominance of positive rewards (higher = more concentrated).
- **Reward entropy:** Normalized entropy of positive reward components (balance proxy).
- **Reward max share:** Share of total positive reward from the largest component.
- **Positive component count:** Number of reward components with positive contribution.

## Population Health Dashboard

### Current Status: Warning

| Metric | Value | Trend (Recent) |
|--------|-------|----------------|
| Diversity Index | 3.92 | Increasing |
| Elite Gap | 4.95 | Stable |
| Min Fitness Trend | +4.8 | Up |
| Max Fitness Trend | +10.9 | Up |
| IQR (p75-p25) | 16 | Widening |

### Takeaways

- Health status is Warning.
- Diversity index at 3.92 with increasing spread.
- Fitness floor trend +4.8, ceiling trend +10.9.

### Warnings

- Diversity inflated vs run baseline (population may be too chaotic)
- Elite gap unusually high vs run baseline (knowledge not spreading)

### Glossary

- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Average fitness:** Mean fitness across the population for a generation.
- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Fitness p25:** 25th percentile of population fitness.
- **Fitness p75:** 75th percentile of population fitness.

## Stagnation Analysis

- **Current Stagnation:** 5 generations
- **Average Stagnation Period:** 17.7 generations
- **Longest Stagnation:** 93 generations
- **Number of Stagnation Periods:** 9

### Takeaways

- Stagnation periods average 17.7 generations.
- Longest plateau reached 93 generations.

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).

## Correlation Analysis

### Fitness Correlations

| Metric | Correlation | Strength |
|--------|-------------|----------|
| Kills | +0.96 | Strong |
| Steps Survived | +0.72 | Strong |
| Accuracy | +0.30 | Weak |

### Interpretation

Fitness is most strongly predicted by kills (r=0.96).

### Takeaways

- Strongest fitness driver: kills (r=0.96).

### Glossary

- **Average fitness:** Mean fitness across the population for a generation.
- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).

## Survival Distribution

### Survival Statistics (Final Phase)

- **Mean Survival:** 353 steps (23.5% of max)
- **Max Survival:** 0 steps

### Survival Progression (Phase Averages)

| Phase | Mean Steps | Change vs Prior |
|-------|------------|-----------------|
| Phase 1 (0-25%) | 315 |  |
| Phase 2 (25-50%) | 294 | -22 |
| Phase 3 (50-75%) | 283 | -11 |
| Phase 4 (75-100%) | 353 | +70 |

### Takeaways

- Final-phase survival averages 353 steps.
- Best survival reached 0 steps.

### Warnings

- Average survival remains below half of max steps; survivability is still limited.

### Glossary

- **Average steps:** Mean steps survived per episode across the population.
- **Max steps:** Highest steps survived by any agent in the generation.

## Behavioral Summary (Last 10 Generations)

- **Avg Kills per Agent:** 2.84
- **Avg Steps Survived:** 282
- **Avg Accuracy:** 47.5%
- **Max Kills (Any Agent Ever):** 16.0
- **Max Steps (Any Agent Ever):** 0

### Takeaways

- Recent average kills: 2.84.
- Recent average accuracy: 47.5%.

### Glossary

- **Average kills:** Mean kills per episode across the population.
- **Average steps:** Mean steps survived per episode across the population.
- **Accuracy:** Hits divided by shots fired (0 to 1).

## Learning Progress

| Phase | Gens | Avg Best | Avg Mean | Avg Min |
|-------|------|----------|----------|---------|
| Phase 1 (0-25%) | 1-43 | -3.3 | -9.4 | -14.6 |
| Phase 2 (25-50%) | 44-86 | 0.1 | -7.1 | -13.2 |
| Phase 3 (50-75%) | 87-129 | 3.7 | -4.8 | -11.8 |
| Phase 4 (75-100%) | 130-171 | 7.6 | -1.9 | -9.7 |

### Takeaways

- Best fitness trend: breakout improvement (low confidence (noisy)).
- Average fitness trend: great improvement (low confidence (noisy)).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.

## Neural & Behavioral Complexity

| Gen | Saturation | Entropy | Control Style |
|-----|------------|---------|---------------|
| 142 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 143 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 144 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 145 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 146 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 147 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 148 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 149 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 150 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 151 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 152 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 153 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 154 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 155 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 156 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 157 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 158 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 159 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 160 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 161 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 162 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 163 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 164 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 165 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 166 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 167 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 168 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 169 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 170 |   0.0% |  0.00 | Binary-leaning / Repetitive |
| 171 |   0.0% |  0.00 | Binary-leaning / Repetitive |

### Takeaways

- Output saturation trend: stagnation (low confidence).
- Action entropy trend: stagnation (low confidence).

### Glossary

- **Output saturation:** Share of NN outputs near 0 or 1 (binary control tendency).
- **Action entropy:** Entropy of action combinations (higher = more varied control).

## Risk Profile Analysis

Analysis of how close agents let asteroids get before reacting or killing them.

| Gen | Avg Min Dist | Fitness | Kills | Archetype |
|-----|--------------|---------|-------|-----------|
| 142 |    0.0px |    4.6 |  4.0 | Daredevil |
| 143 |    0.0px |   16.8 |  7.0 | Daredevil |
| 144 |    0.0px |   14.5 |  6.0 | Daredevil |
| 145 |    0.0px |   -0.8 |  3.5 | Balanced |
| 146 |    0.0px |   -9.2 |  1.7 | Overexposed |
| 147 |    0.0px |    1.4 |  3.7 | Balanced |
| 148 |    0.0px |   -7.8 |  1.7 | Balanced |
| 149 |    0.0px |   -7.2 |  1.5 | Balanced |
| 150 |    0.0px |    4.6 |  4.5 | Daredevil |
| 151 |    0.0px |   -5.8 |  3.0 | Balanced |
| 152 |    0.0px |   -1.0 |  3.3 | Balanced |
| 153 |    0.0px |   -5.6 |  2.5 | Balanced |
| 154 |    0.0px |   -0.9 |  3.5 | Balanced |
| 155 |    0.0px |    3.8 |  4.5 | Daredevil |
| 156 |    0.0px |   -1.1 |  2.0 | Balanced |
| 157 |    0.0px |  -12.0 |  0.7 | Overexposed |
| 158 |    0.0px |  -13.6 |  0.4 | Overexposed |
| 159 |    0.0px |   -8.5 |  1.3 | Overexposed |
| 160 |    0.0px |    0.5 |  4.7 | Balanced |
| 161 |    0.0px |  -13.0 |  0.7 | Overexposed |
| 162 |    0.0px |    5.8 |  5.5 | Daredevil |
| 163 |    0.0px |   -5.4 |  2.0 | Balanced |
| 164 |    0.0px |   -3.3 |  3.0 | Balanced |
| 165 |    0.0px |   -9.7 |  1.0 | Overexposed |
| 166 |    0.0px |    5.6 |  5.0 | Daredevil |
| 167 |    0.0px |   -5.3 |  2.6 | Balanced |
| 168 |    0.0px |    4.2 |  4.0 | Daredevil |
| 169 |    0.0px |   -2.3 |  3.0 | Balanced |
| 170 |    0.0px |  -11.3 |  1.0 | Overexposed |
| 171 |    0.0px |  -10.7 |  1.3 | Overexposed |

### Takeaways

- Min-distance trend: stagnation (low confidence).
- Danger exposure trend: stagnation (low confidence).

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
| Turn | Turn Balance (R-L) | +0.00 |
| Turn | Switch Rate | 0.0% |
| Turn | Avg Streak | 0.0f |
| Turn | Max Streak | 0f |
| Aim | Frontness Avg | 0.0% |
| Aim | Frontness at Shot | 0.0% |
| Aim | Frontness at Hit | 0.0% |
| Aim | Shot Distance | 0.0px |
| Aim | Hit Distance | 0.0px |
| Danger | Exposure Rate | 0.0% |
| Danger | Entries | 0.0 |
| Danger | Reaction Time | 0.0f |
| Danger | Wraps in Danger | 0.0 |
| Movement | Distance Traveled | 0.0px |
| Movement | Avg Speed | 0.00 |
| Movement | Speed Std | 0.00 |
| Movement | Coverage Ratio | 0.0% |
| Shooting | Shots per Kill | 4.50 |
| Shooting | Shots per Hit | 3.66 |
| Shooting | Cooldown Usage | 0.0% |
| Shooting | Cooldown Ready | 0.0% |
| Stability | Fitness Std (Seeds) | 5.8 |

### Recent Control Trends (Last 10)

| Gen | Deadzone | Turn Bias | Switch | Frontness | Danger | Coverage |
|-----|----------|-----------|--------|-----------|--------|----------|
| 162 |    0.0% |  +0.00 |    0.0% |    0.0% |    0.0% |    0.0% |
| 163 |    0.0% |  +0.00 |    0.0% |    0.0% |    0.0% |    0.0% |
| 164 |    0.0% |  +0.00 |    0.0% |    0.0% |    0.0% |    0.0% |
| 165 |    0.0% |  +0.00 |    0.0% |    0.0% |    0.0% |    0.0% |
| 166 |    0.0% |  +0.00 |    0.0% |    0.0% |    0.0% |    0.0% |
| 167 |    0.0% |  +0.00 |    0.0% |    0.0% |    0.0% |    0.0% |
| 168 |    0.0% |  +0.00 |    0.0% |    0.0% |    0.0% |    0.0% |
| 169 |    0.0% |  +0.00 |    0.0% |    0.0% |    0.0% |    0.0% |
| 170 |    0.0% |  +0.00 |    0.0% |    0.0% |    0.0% |    0.0% |
| 171 |    0.0% |  +0.00 |    0.0% |    0.0% |    0.0% |    0.0% |

### Takeaways

- Turn balance trend: stagnation (low confidence).
- Aim alignment trend: stagnation (low confidence).
- Danger exposure trend: stagnation (low confidence).

### Warnings

- Frontness at shot lags overall frontness (aiming during shots is weak).

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

## Graph Neural Network and Soft Actor-Critic Diagnosis

This section is generated only for GNN-SAC runs and summarizes learner health, replay quality,
representation stability, and evaluation behavior over time.

Note: SAC 'fitness' in the main report refers to training episode returns; evaluation is tracked separately.

### Run Timebase & Evaluation

| Metric | Latest | Notes |
|--------|--------|-------|
| Env Steps | 171,000 | total environment steps |
| Updates | 166,001 | total optimizer steps |
| Update/Data Ratio | 0.971 | updates per env step |
| Latest Eval Return | -15.00 ± 3.81 | fixed seeds |
| Best Eval Return | 0.11 @ step 26,658 | best so far |
| Eval Since Improve | 106 | eval cycles |

Per-seed eval returns (latest):

`[-9.522882226990008, -19.633333333333336, -15.288296417969669, -12.031615463729516, -18.514593515263368]`

```
Eval Return Trend  [--+@ :. .=*.. -= . .+:-=]
```

### Learner Stability by Phase

| Phase | Critic Loss | TD Abs p99 | Q Mean | Target Q Mean | Alpha | Critic Grad | Clip Rate |
|-------|-------------|------------|--------|----------------|-------|-------------|-----------|
| Phase 1 (0-25%) | 0.15 | 1.85 | 1.76 | 1.78 | 0.02 | 0.30 | 0.000 |
| Phase 2 (25-50%) | 0.19 | 2.59 | 1.60 | 1.60 | 0.00 | 0.42 | 0.000 |
| Phase 3 (50-75%) | 0.19 | 2.78 | 0.77 | 0.77 | 0.00 | 0.44 | 0.000 |
| Phase 4 (75-100%) | 0.20 | 2.92 | 1.01 | 1.00 | 0.00 | 0.46 | 0.000 |

### Action Health by Phase

| Phase | Turn μ | Turn σ | Turn Sat | Thrust μ | Thrust σ | Thrust Sat | Shoot Rate | Shoot Sat |
|-------|--------|--------|----------|----------|----------|------------|-----------|-----------|
| Phase 1 (0-25%) | 0.04 | 0.59 | 0.072 | 0.53 | 0.32 | 0.190 | 0.506 | 0.215 |
| Phase 2 (25-50%) | 0.02 | 0.54 | 0.055 | 0.46 | 0.32 | 0.206 | 0.440 | 0.268 |
| Phase 3 (50-75%) | 0.06 | 0.53 | 0.052 | 0.39 | 0.31 | 0.187 | 0.391 | 0.263 |
| Phase 4 (75-100%) | 0.05 | 0.52 | 0.043 | 0.35 | 0.30 | 0.217 | 0.476 | 0.241 |

### Replay & Data Health by Phase

| Phase | Replay Size | Ep Steps μ | Ep Steps p90 | Step Reward μ | Step Reward σ | Terminal μ | Terminal % |
|-------|-------------|------------|--------------|----------------|--------------|-------------|------------|
| Phase 1 (0-25%) | 22000.00 | 315.41 | 421.53 | -0.03 | 1.08 | 0.00 | 0.003 |
| Phase 2 (25-50%) | 65000.00 | 293.74 | 421.97 | -0.03 | 1.15 | 0.00 | 0.004 |
| Phase 3 (50-75%) | 97883.72 | 282.93 | 408.19 | -0.02 | 1.18 | 0.00 | 0.004 |
| Phase 4 (75-100%) | 100000.00 | 353.21 | 486.68 | -0.02 | 1.07 | 0.00 | 0.003 |

### Representation Health by Phase

| Phase | Embedding Norm | Dim Std | Cos Sim |
|-------|----------------|---------|---------|
| Phase 1 (0-25%) | 7.62 | 0.81 | 0.17 |
| Phase 2 (25-50%) | 8.55 | 0.89 | 0.25 |
| Phase 3 (50-75%) | 8.57 | 0.85 | 0.30 |
| Phase 4 (75-100%) | 8.61 | 0.81 | 0.37 |

### Policy & Critic Drift (Latest)

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Policy L1 Drift | 0.10 | change on fixed probe set |
| Critic/Target Gap | 0.08 | |Q - Q_target| on probe set |

### Weight Distribution Snapshot (Latest)

| Module | Mean | Std | Norm | Zero % |
|--------|------|-----|------|--------|
| GNN | 0.0031 | 0.1304 | 34.92 | 0.00% |
| Actor | -0.0281 | 0.1825 | 53.52 | 0.00% |
| Critic | -0.0046 | 0.0846 | 34.62 | 0.00% |

### Takeaways

- Evaluation metrics are reported on fixed seeds and tracked separately from training returns.
- Critic stability is summarized via TD error tails and gradient/clip rates.
- Action saturation rates expose control collapse or oscillation.

### Warnings

- Evaluation has not improved for several eval cycles (possible stagnation).

### Glossary

- **Eval return (mean):** Average deterministic evaluation return on fixed seeds.
- **Eval return (std):** Standard deviation of evaluation returns across fixed seeds.
- **Holdout eval return (mean):** Average deterministic evaluation return on held-out seeds.
- **Holdout eval return (std):** Standard deviation of held-out evaluation returns across seeds.
- **Critic loss:** Mean critic loss across update steps in the reporting window.
- **TD error p99:** 99th percentile absolute TD error (outlier magnitude proxy).
- **Entropy temperature (alpha):** Mean entropy temperature value used in SAC updates.
- **Policy entropy:** Mean policy entropy estimate from log-probabilities.
- **Turn saturation rate:** Share of turn actions near full magnitude (|turn| > 0.95).
- **Thrust saturation rate:** Share of thrust actions near extremes (<0.05 or >0.95).
- **Shoot saturation rate:** Share of shoot actions near extremes (<0.05 or >0.95).
- **Terminal fraction:** Fraction of steps that ended an episode (done/timeout).
- **Embedding cosine similarity:** Mean cosine similarity between state embeddings (high = collapse risk).
- **Policy drift:** Mean absolute change in actions on a fixed probe set vs previous log window.
- **Critic/target gap:** Mean |Q - Q_target| on a fixed probe set (stability proxy).

## Convergence Analysis

**Recent 20 Generations Analysis:**

- Average Standard Deviation: 8.19
- Average Range (Best-Min): 19.13
- Diversity Change: +61.2%
- **Status:** High diversity - population is still exploring

### Takeaways

- Convergence status: exploring.
- Diversity change: +61.2%.

### Warnings

- Diversity is rising late in training; convergence has not begun.

### Glossary

- **Fitness std dev:** Standard deviation of fitness across the population (diversity proxy).
- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Minimum fitness:** Lowest fitness in the population for a generation.

## Behavioral Trends

### Performance Metrics by Quarter

| Period | Avg Kills | Avg Steps | Avg Accuracy | Safe Dist | Max Kills |
|--------|-----------|-----------|--------------|-----------|----------|
| Q1 | 1.96 | 316 | 30.7% | 0.0px | 8.0 |
| Q2 | 1.99 | 276 | 40.1% | 0.0px | 11.0 |
| Q3 | 2.29 | 300 | 49.3% | 0.0px | 10.0 |
| Q4 | 3.01 | 349 | 46.2% | 0.0px | 16.0 |

### Action Distribution & Strategy Evolution

Analysis of how the population's physical behavior has changed over time.

| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |
|--------|----------|--------|---------|-------------------|
| Q1 | 0.0% | 0.0% | 0.0% | **Drifter** |
| Q2 | 0.0% | 0.0% | 0.0% | **Drifter** |
| Q3 | 0.0% | 0.0% | 0.0% | **Drifter** |
| Q4 | 0.0% | 0.0% | 0.0% | **Drifter** |

### Input Control Style

| Period | Thrust Dur | Turn Dur | Shoot Dur | Idle Rate | Wraps |
|--------|------------|----------|-----------|-----------|-------|
| Q1 | 0.0f | 0.0f | 0.0f | 0.0% | 0.0 |
| Q2 | 0.0f | 0.0f | 0.0f | 0.0% | 0.0 |
| Q3 | 0.0f | 0.0f | 0.0f | 0.0% | 0.0 |
| Q4 | 0.0f | 0.0f | 0.0f | 0.0% | 0.0 |

### Takeaways

- Kills trend: steady improvement.
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

## Recent Generations (Last 30)

<details>
<summary>Click to expand Recent Generations table</summary>

| Gen   | Best   | Avg    | StdDev | Kills  | Steps  | Acc%   | Stag   |
|-------|--------|--------|--------|--------|--------|--------|--------|
| 142   | 9      | 5      | 4      | 4.0    | 543    | 46     | 1      |
| 143   | 17     | 17     | 0      | 7.0    | 550    | 53     | 2      |
| 144   | 38     | 14     | 23     | 6.0    | 732    | 49     | 0      |
| 145   | 12     | -1     | 13     | 3.5    | 338    | 48     | 1      |
| 146   | -5     | -9     | 3      | 1.7    | 268    | 35     | 2      |
| 147   | 19     | 1      | 15     | 3.7    | 425    | 44     | 3      |
| 148   | -3     | -8     | 6      | 1.7    | 328    | 47     | 4      |
| 149   | -2     | -7     | 4      | 1.5    | 219    | 56     | 5      |
| 150   | 17     | 5      | 12     | 4.5    | 498    | 45     | 6      |
| 151   | 10     | -6     | 11     | 3.0    | 355    | 35     | 7      |
| 152   | 3      | -1     | 4      | 3.3    | 348    | 57     | 8      |
| 153   | -2     | -6     | 3      | 2.5    | 229    | 68     | 9      |
| 154   | 10     | -1     | 11     | 3.5    | 538    | 34     | 10     |
| 155   | 15     | 4      | 11     | 4.5    | 408    | 56     | 11     |
| 156   | 10     | -1     | 8      | 2.0    | 392    | 60     | 12     |
| 157   | -8     | -12    | 4      | 0.7    | 164    | 53     | 13     |
| 158   | -8     | -14    | 3      | 0.4    | 147    | 47     | 14     |
| 159   | 4      | -8     | 9      | 1.3    | 298    | 36     | 15     |
| 160   | 33     | 0      | 24     | 4.7    | 393    | 24     | 16     |
| 161   | -8     | -13    | 5      | 0.7    | 429    | 20     | 17     |
| 162   | 7      | 6      | 1      | 5.5    | 396    | 38     | 18     |
| 163   | 5      | -5     | 7      | 2.0    | 275    | 49     | 19     |
| 164   | 9      | -3     | 12     | 3.0    | 368    | 31     | 20     |
| 165   | -4     | -10    | 4      | 1.0    | 155    | 58     | 21     |
| 166   | 56     | 6      | 29     | 5.0    | 374    | 35     | 0      |
| 167   | 4      | -5     | 5      | 2.6    | 179    | 51     | 1      |
| 168   | 4      | 4      | 0      | 4.0    | 250    | 86     | 2      |
| 169   | 14     | -2     | 13     | 3.0    | 359    | 54     | 3      |
| 170   | -7     | -11    | 4      | 1.0    | 220    | 35     | 4      |
| 171   | -3     | -11    | 6      | 1.3    | 242    | 38     | 5      |

</details>

### Recent Table Takeaways

- Recent table covers 30 generations ending at Gen 171.
- Latest best fitness: -2.8.

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
| 1    | 166   | 56     | 6      | 0.0    | 0      | 0.0      |
| 2    | 144   | 38     | 14     | 0.0    | 0      | 0.0      |
| 3    | 141   | 37     | 14     | 0.0    | 0      | 0.0      |
| 4    | 160   | 33     | 0      | 0.0    | 0      | 0.0      |
| 5    | 140   | 32     | 32     | 0.0    | 0      | 0.0      |
| 6    | 46    | 29     | 3      | 0.0    | 0      | 0.0      |
| 7    | 92    | 28     | 7      | 0.0    | 0      | 0.0      |
| 8    | 128   | 26     | 13     | 0.0    | 0      | 0.0      |
| 9    | 108   | 25     | 20     | 0.0    | 0      | 0.0      |
| 10   | 79    | 22     | 2      | 0.0    | 0      | 0.0      |

</details>

### Top Generations Takeaways

- Top generation is Gen 166 with best fitness 56.0.

### Top Generations Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.
- **Accuracy:** Hits divided by shots fired (0 to 1).


## Trend Analysis

| Phase | Avg Best | Avg Mean | Avg Min | Improvement |
|-------|----------|----------|---------|-------------|
| Phase 1 (0-25%) | -3.3 | -9.4 | -14.6 |  |
| Phase 2 (25-50%) | 0.1 | -7.1 | -13.2 | +3.4 |
| Phase 3 (50-75%) | 3.7 | -4.8 | -11.8 | +3.7 |
| Phase 4 (75-100%) | 7.6 | -1.9 | -9.7 | +3.9 |

### Takeaways

- Best fitness: breakout improvement (low confidence (noisy)).
- Average fitness: great improvement (low confidence (noisy)).
- Minimum fitness: steady improvement (moderate confidence).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.
- **Minimum fitness:** Lowest fitness in the population for a generation.


## Fitness Progression (ASCII Chart)

```
Best Fitness (*) vs Avg Fitness (o) Over Generations

      56 |                                                       * 
      51 |                                                         
      47 |                                                         
      42 |                                                         
      37 |                                                         
      33 |                                                     *   
      28 |               *                                         
      24 |                                                         
      19 |                          *                              
      14 |                       *                                 
      10 |                           *            *       * **    *
       5 |      *                       * * *            *       o 
       0 | *  *    *     o          o *        **    *   o     o*  
      -4 | o *   ** *   *     *   **  o     o**   o** *   o* o    o
      -9 |  *oo*oo oo  *  * ** **ooo o *o*o  ooo     o *   oo * o  
     -14 |*    o  o  **oo o* oo o      o o *    o* oo oo*     o    
         ---------------------------------------------------------
         Gen 1                                          Gen 171
```

### Takeaways

- Best fitness trend: breakout improvement (low confidence (noisy)).
- Average fitness trend: great improvement (low confidence (noisy)).

### Glossary

- **Best fitness:** Highest per-generation fitness across the population (max average reward).
- **Average fitness:** Mean fitness across the population for a generation.


---

# Technical Appendix

## System Performance

**Average Duration (Last 10 Generations):** 0.00s
- **Evaluation (Simulation):** 22701.08s (0.0%)
- **Evolution (Operators):** 0.0000s (0.0%)

| Phase | Gen Range | Avg Eval Time | Avg Evol Time | Total Time |
|-------|-----------|---------------|---------------|------------|
| Phase 1 (0-25%) | 1-43 | 92.54s | 0.0000s | 0.00s |
| Phase 2 (25-50%) | 44-86 | 105.30s | 0.0000s | 0.00s |
| Phase 3 (50-75%) | 87-129 | 106.42s | 0.0000s | 0.00s |
| Phase 4 (75-100%) | 130-171 | 5700.32s | 0.0000s | 0.00s |

### Takeaways

- Evaluation accounts for 0.0% of generation time.
- Evolution accounts for 0.0% of generation time.

### Glossary

- **Evaluation duration:** Wall time spent evaluating a generation.
- **Evolution duration:** Wall time spent evolving a generation.
- **Total generation duration:** Combined evaluation and evolution wall time.

