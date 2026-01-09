# Analytics Enhancement Proposal: Comprehensive Training Analysis System

## Document Information

| Field | Value |
|-------|-------|
| **Author** | AI Research Team |
| **Date** | 2026-01-08 |
| **Status** | Proposal / Design Document |
| **Related Files** | `training/analytics.py`, `training_summary.md`, `training_data.json` |
| **Dependencies** | `TRAINING_DATA_SCHEMA_EXPANSION.md` (must be implemented first) |
| **Stakeholders** | ML Engineers, Researchers, Training Pipeline Maintainers |

---

## Critical Dependency Notice

> **This document depends on the Training Data Schema Expansion being implemented first.**
>
> Several enhancements in this proposal require data that is not currently tracked. The companion document `TRAINING_DATA_SCHEMA_EXPANSION.md` defines the necessary data collection changes, including:
>
> - **Fresh game performance tracking** (critical for generalization analysis)
> - **Per-agent distribution arrays** (required for correlation and survival analysis)
> - **Action frequency metrics** (required for behavioral classification)
> - **Operator statistics** (optional, for GA tuning insights)
>
> Implement the schema expansion first, then proceed with these analytics enhancements.

---

## Executive Summary

This document proposes 15 enhancements to the training analytics system for the AsteroidsAI genetic algorithm pipeline. The current analytics implementation provides basic per-generation statistics and a summary report, but lacks the depth required for meaningful behavioral analysis, debugging training issues, and understanding emergent agent strategies.

The proposed enhancements are organized into three tiers based on implementation priority and expected value. Each enhancement is designed to answer specific questions about training dynamics, agent behavior, and population health that are currently difficult or impossible to answer from the existing output.

**Core Philosophy**: A researcher should be able to understand everything important about a training run from a single summary file, without needing to parse raw JSON data or re-run analysis scripts.

---

## Table of Contents

1. [Background and Motivation](#1-background-and-motivation)
2. [Current System Limitations](#2-current-system-limitations)
3. [Proposed Enhancements Overview](#3-proposed-enhancements-overview)
4. [Tier 1: Essential Enhancements](#4-tier-1-essential-enhancements)
5. [Tier 2: High-Value Enhancements](#5-tier-2-high-value-enhancements)
6. [Tier 3: Quality-of-Life Enhancements](#6-tier-3-quality-of-life-enhancements)
7. [Implementation Considerations](#7-implementation-considerations)
8. [Data Requirements and Prerequisites](#8-data-requirements-and-prerequisites)
9. [Future Extensions](#9-future-extensions)

---

## 1. Background and Motivation

### 1.1 The Problem of Training Opacity

Genetic algorithm training runs can span hundreds of generations and produce tens of thousands of data points. Without proper analytics, researchers face several challenges:

- **Information Overload**: Raw generation data is too granular to interpret manually
- **Hidden Patterns**: Trends and anomalies are buried in noise
- **Behavioral Blindness**: Fitness scores don't reveal *how* agents are achieving those scores
- **Debugging Difficulty**: When training fails or stagnates, root cause analysis is guesswork
- **Comparison Impossibility**: Different runs cannot be meaningfully compared

### 1.2 What Good Analytics Should Provide

A well-designed analytics system should answer these questions at a glance:

1. **Is learning happening?** - Clear trend indicators showing improvement over time
2. **What did the agent learn?** - Behavioral characterization beyond just fitness
3. **Is the population healthy?** - Diversity metrics, convergence indicators
4. **Where are the problems?** - Stagnation detection, reward imbalance warnings
5. **What's the best agent like?** - Detailed profile of the champion
6. **How does this compare?** - Benchmarks against baselines or previous runs

### 1.3 Design Principles

The enhanced analytics system should adhere to these principles:

- **Glanceability**: The most important information should be visible in the first 20 lines
- **Progressive Disclosure**: Summary first, details available for those who want them
- **Actionability**: Every metric should inform a potential decision or insight
- **Robustness**: Handle edge cases (short runs, degenerate populations, interrupted training)
- **Self-Documenting**: Include explanations of what each metric means

---

## 2. Current System Limitations

### 2.1 Existing Analytics Output

The current `training_summary.md` includes:

- Training configuration
- Overall summary (total generations, duration, best fitness)
- Reward component analysis (final generation only)
- Behavioral summary (last 10 generations)
- Learning progress (first 2 vs last 2 generations)

### 2.2 What's Missing

| Gap | Impact |
|-----|--------|
| No temporal breakdown | Cannot see learning trajectory across training |
| Single-point behavioral data | Cannot see how behavior evolved |
| No population health metrics | Cannot detect premature convergence |
| No stagnation analysis | Cannot identify learning plateaus |
| No efficiency metrics | Cannot distinguish lucky kills from skilled play |
| No agent classification | Cannot characterize emergent strategy |
| No correlation analysis | Cannot understand what drives fitness |
| No milestone tracking | Cannot identify breakthrough moments |

### 2.3 The JSON Problem

The `training_data.json` file contains all the raw data needed for deep analysis, but:

- It's hundreds or thousands of lines long
- Requires custom scripts to extract insights
- Not human-readable for quick inspection
- Forces researchers to write ad-hoc analysis code

The goal of these enhancements is to **pre-compute** all useful analyses and present them in the summary file.

---

## 3. Proposed Enhancements Overview

### 3.1 Enhancement Tiers

| Tier | Focus | Enhancements | Implementation Effort |
|------|-------|--------------|----------------------|
| **Tier 1** | Essential | 5 enhancements | Medium |
| **Tier 2** | High-Value | 5 enhancements | Medium-High |
| **Tier 3** | Quality-of-Life | 5 enhancements | Low-Medium |

### 3.2 Complete Enhancement List

| # | Enhancement | Tier | Primary Question Answered |
|---|-------------|------|---------------------------|
| 1 | Decile Breakdown Table | 1 | How did training progress over time? |
| 2 | Reward Component Evolution | 1 | What did the agent learn to optimize? |
| 3 | Kill Efficiency Metrics | 1 | How skilled (vs lucky) is the agent? |
| 4 | Behavioral Classification | 1 | What strategy emerged? |
| 5 | Population Health Dashboard | 1 | Is the GA working correctly? |
| 6 | Stagnation Analysis | 2 | Where did learning get stuck? |
| 7 | Best Agent Deep Profile | 2 | What does the champion look like? |
| 8 | Learning Velocity Chart | 2 | Is learning accelerating or slowing? |
| 9 | Milestone Timeline | 2 | When did breakthroughs happen? |
| 10 | Survival Distribution | 2 | How and when do agents die? |
| 11 | Correlation Matrix | 3 | What metrics predict fitness? |
| 12 | Generation Highlights | 3 | What were the notable moments? |
| 13 | Reward Balance Warnings | 3 | Is the reward structure working? |
| 14 | Action Distribution Estimates | 3 | How is the agent behaving? |
| 15 | ASCII Trend Sparklines | 3 | Quick visual trend indicators? |

---

## 4. Tier 1: Essential Enhancements

These enhancements address the most critical gaps in the current analytics system. They should be implemented first and will provide the highest return on investment.

---

### 4.1 Enhancement #1: Decile Breakdown Table

#### 4.1.1 Purpose and Rationale

The single most valuable addition to the analytics system is a temporal breakdown of training into equal phases. By dividing training into 10 equal parts (deciles), we can observe:

- **Learning trajectory**: Is fitness improving linearly, exponentially, or plateauing?
- **Behavioral evolution**: How did kills, accuracy, and survival change over time?
- **Phase transitions**: Were there distinct learning phases (exploration → exploitation)?
- **Regression detection**: Did any metrics get worse over time?

Currently, the summary only compares "first 2 vs last 2 generations," which misses everything in between. A 500-generation run has 496 generations of invisible data.

#### 4.1.2 What It Answers

- "How did training progress over time?"
- "When did the agent learn each skill?"
- "Was there a breakthrough moment or gradual improvement?"
- "Did any metrics regress during training?"

#### 4.1.3 Proposed Format

```
## Training Progress by Decile

| Phase | Gens   | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |
|-------|--------|----------|---------|-----------|---------|-----------|-----------|
| 0-10% | 1-50   | 612      | 89      | 3.2       | 35%     | 263       | 0.85      |
| 10-20%| 51-100 | 1,137    | 312     | 8.1       | 63%     | 366       | 0.72      |
| 20-30%| 101-150| 1,577    | 498     | 10.8      | 72%     | 416       | 0.58      |
| ...   | ...    | ...      | ...     | ...       | ...     | ...       | ...       |
| 90-100%| 451-500| 1,910   | 641     | 12.3      | 78%     | 447       | 0.48      |
```

#### 4.1.4 Implementation Approach

1. Calculate decile boundaries based on total generations completed
2. For each decile, aggregate all generation data within that range
3. Compute mean, max, and key percentiles for each metric
4. Handle edge cases: runs shorter than 10 generations should use fewer phases
5. Include per-decile reward component breakdown in a secondary table

#### 4.1.5 Prerequisites

- Access to full `generations_data` list
- Minimum of 1 generation completed (graceful degradation for short runs)

#### 4.1.6 Design Considerations

**Why 10 phases (deciles)?**
- Provides sufficient granularity to see trends
- Maps naturally to percentages (0-10%, 10-20%, etc.)
- Not so granular that the table becomes unwieldy
- Alternative: 5 phases (quintiles) for shorter runs

**Adaptive phase count:**
For very short runs (<20 generations), consider using fewer phases to avoid phases with only 1-2 generations each. Suggested thresholds:
- <10 generations: No phase breakdown, just show all generations
- 10-19 generations: 5 phases
- 20+ generations: 10 phases

---

### 4.2 Enhancement #2: Reward Component Evolution

#### 4.2.1 Purpose and Rationale

Understanding *what* the agent learned to optimize is often more important than knowing the final fitness score. The reward system has multiple components, and agents may learn to exploit some while ignoring others.

Current limitation: The summary shows reward breakdown for the final generation only, hiding the evolution of reward acquisition over time.

By tracking reward component evolution, we can:

- **Identify learned behaviors**: Which rewards did the agent learn to maximize?
- **Detect reward hacking**: Is the agent exploiting unintended reward shortcuts?
- **Diagnose stuck behaviors**: Which rewards remain negative throughout training?
- **Validate reward design**: Is the reward structure incentivizing intended behaviors?

#### 4.2.2 What It Answers

- "What did the agent learn to optimize?"
- "Which rewards are still negative (unlearned behaviors)?"
- "Did the agent discover the intended strategy or an exploit?"
- "Is my reward structure working as designed?"

#### 4.2.3 Proposed Format

```
## Reward Component Evolution

| Component              | Phase 1 | Phase 5 | Phase 10 | Trend     | Status       |
|------------------------|---------|---------|----------|-----------|--------------|
| KillAsteroid           | +80.2   | +275.1  | +325.9   | ↑↑↑ +307% | ✅ Learned    |
| ConservingAmmoBonus    | -83.1   | +147.8  | +316.3   | ↑↑↑↑+480% | ✅ Learned    |
| NearMiss               | +23.0   | +27.8   | +29.9    | ↑ +30%    | ✅ Stable     |
| SurvivalBonus          | +4.4    | +6.9    | +7.7     | ↑ +77%    | ✅ Improving  |
| MaintainingMomentumBonus| -9.1   | -31.9   | -38.4    | ↓↓ -322%  | ⚠️ Not learned|
| MovingTowardDangerBonus| +1.1    | +0.4    | +0.06    | ↓ -95%    | ⚠️ Declining  |
| SpacingFromWallsBonus  | -0.6    | -0.3    | -0.04    | → ~0      | ➖ Negligible |
```

#### 4.2.4 Implementation Approach

1. For each decile phase, compute mean reward breakdown across all generations
2. Calculate percentage change from first to last phase
3. Assign trend indicators based on direction and magnitude
4. Assign status labels based on final value and trend:
   - **Learned**: Positive and improving
   - **Stable**: Positive, minimal change
   - **Improving**: Was negative, now positive or less negative
   - **Not learned**: Still negative after training
   - **Declining**: Was positive, now less positive or negative
   - **Negligible**: Near zero throughout

#### 4.2.5 Prerequisites

- `avg_reward_breakdown` tracked per generation
- Reward component names must be consistent across training

#### 4.2.6 Design Considerations

**Handling new/removed components:**
If reward components are added or removed mid-training (not recommended but possible), the evolution table should:
- Show "N/A" for phases where a component didn't exist
- Include a note about configuration changes

**Normalization:**
Consider showing reward components as percentage of total positive reward, not just absolute values. This shows relative importance even as overall fitness scales.

---

### 4.3 Enhancement #3: Kill Efficiency Metrics

#### 4.3.1 Purpose and Rationale

Raw kill counts can be misleading. An agent with 20 kills from 200 shots is fundamentally different from one with 20 kills from 25 shots. Efficiency metrics reveal the *quality* of performance, not just quantity.

Kill efficiency is particularly important for distinguishing:

- **Lucky agents**: High kills due to favorable asteroid positions, not skill
- **Spray-and-pray agents**: Many kills but terrible accuracy
- **Skilled agents**: High kills with proportionally few shots
- **Efficient hunters**: High kills per time survived

#### 4.3.2 What It Answers

- "Is the agent skilled or just lucky?"
- "How efficient is the agent's killing strategy?"
- "Is accuracy translating into actual kills?"
- "What's the agent's kill rate over time?"

#### 4.3.3 Proposed Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Kills per 100 Steps** | (kills / steps) × 100 | Killing rate normalized by survival time |
| **Shots per Kill** | shots / kills | Lower is better; measures efficiency |
| **Kill Conversion Rate** | kills / shots | What fraction of shots result in kills |
| **Kills per Episode** | Direct count | Absolute productivity |
| **Kill Acceleration** | (late kills/step) / (early kills/step) | Is killing rate improving? |

#### 4.3.4 Proposed Format

```
## Kill Efficiency Analysis

### Current Performance (Final Decile)
- **Kills per 100 Steps**: 2.75 (up from 1.22 in Phase 1)
- **Shots per Kill**: 2.38 (down from 7.14 in Phase 1)
- **Kill Conversion Rate**: 42.0% (up from 14.0% in Phase 1)
- **Average Kills per Episode**: 12.3

### Efficiency Trend
| Phase   | Kills/100 Steps | Shots/Kill | Conversion Rate |
|---------|-----------------|------------|-----------------|
| Phase 1 | 1.22            | 7.14       | 14.0%           |
| Phase 5 | 2.44            | 3.28       | 30.5%           |
| Phase 10| 2.75            | 2.38       | 42.0%           |

**Assessment**: Agent has learned efficient killing. Shots per kill dropped 67%.
```

#### 4.3.5 Implementation Approach

1. Calculate raw efficiency metrics from existing tracked data:
   - `avg_kills`, `avg_shots`, `avg_steps` are already tracked
2. Compute derived metrics using simple division
3. Track these metrics per decile to show evolution
4. Generate assessment text based on trends

#### 4.3.6 Prerequisites

- `avg_kills`, `avg_shots_fired`, `avg_steps_survived` tracked per generation
- Division by zero handling for agents with 0 kills or 0 shots

#### 4.3.7 Design Considerations

**Edge cases:**
- Agents with 0 kills: Show "N/A" for efficiency metrics
- Agents with 0 shots: Unusual but possible; show "No shots fired"
- Perfect accuracy agents: Shots per kill approaches 1.0; this is the theoretical minimum (each asteroid takes 1 shot)

**Interpreting Shots per Kill:**
In Asteroids, destroying an asteroid may spawn smaller asteroids. A "kill" might mean the asteroid is fully destroyed, or just hit. The metric's interpretation depends on how `total_kills` is defined. Document this clearly.

---

### 4.4 Enhancement #4: Behavioral Classification

#### 4.4.1 Purpose and Rationale

Different agents can achieve similar fitness scores through completely different strategies. Classifying the emergent behavior type provides immediate insight into *how* the agent plays, not just how well.

Behavioral classification is valuable for:

- **Strategy identification**: What approach did evolution discover?
- **Comparative analysis**: Do different hyperparameters produce different strategies?
- **Debugging**: A "Camper" classification explains why movement rewards are negative
- **Research**: Understanding which strategies emerge under which conditions

#### 4.4.2 What It Answers

- "What kind of agent emerged?"
- "Is the agent playing the way I intended?"
- "Why might this agent struggle in certain scenarios?"
- "How does this strategy compare to other runs?"

#### 4.4.3 Proposed Classifications

| Archetype | Characteristics | Typical Metrics |
|-----------|-----------------|-----------------|
| **Camper** | Stays stationary, waits for asteroids to approach, high accuracy | Low momentum, high accuracy, medium kills |
| **Hunter** | Actively pursues asteroids, high movement | High momentum, high danger approach, high kills |
| **Sniper** | Few shots, very high accuracy, patient | Low shots, >90% accuracy, medium kills |
| **Sprayer** | Many shots, low accuracy, volume strategy | High shots, <50% accuracy, variable kills |
| **Survivor** | Prioritizes staying alive over killing | High steps, low kills, low shots |
| **Balanced** | No dominant characteristic | Moderate all metrics |
| **Erratic** | Inconsistent behavior | High variance in metrics |

#### 4.4.4 Classification Algorithm (Conceptual)

```
1. Normalize all behavioral metrics to 0-1 scale based on observed ranges
2. Calculate characteristic scores:
   - Camping Score = accuracy × (1 - momentum_normalized)
   - Hunting Score = momentum_normalized × danger_approach_normalized
   - Sniping Score = accuracy × (1 - shots_normalized)
   - Spraying Score = shots_normalized × (1 - accuracy)
   - Surviving Score = steps_normalized × (1 - kills_normalized)
3. Assign classification based on highest score
4. If no score is dominant (all within 20% of each other), classify as "Balanced"
5. If variance across episodes is very high, classify as "Erratic"
```

#### 4.4.5 Proposed Format

```
## Behavioral Classification

**Primary Archetype**: 🎯 Sniper

**Classification Confidence**: 78%

**Reasoning**:
- Very high accuracy (77.6%) indicates patient, aimed shots
- Low momentum penalty suggests minimal movement
- Moderate kill count (12.3/episode) achieved efficiently
- Shots per kill (2.38) is well below population average

**Secondary Traits**:
- Slight Camper tendency (prefers stationary positions)
- No Hunter characteristics (low danger approach bonus)

**Strategy Summary**: This agent has evolved a stationary sniping strategy.
It waits for asteroids to enter its field of fire rather than actively pursuing them.
This is effective for the current reward structure but may struggle with
aggressive asteroid spawns that require repositioning.
```

#### 4.4.6 Implementation Approach

1. Define thresholds for each archetype based on metric combinations
2. Calculate archetype scores using weighted metric combinations
3. Select primary archetype as highest-scoring
4. Calculate confidence as (highest score - second highest) / highest
5. Generate natural language reasoning based on which metrics drove the classification
6. Identify secondary traits from other above-threshold scores

#### 4.4.7 Prerequisites

- All behavioral metrics (kills, accuracy, steps, shots) tracked
- Reward component data (momentum bonus, danger approach bonus)
- Reasonable population size to establish baseline ranges

#### 4.4.8 Design Considerations

**Rule-based vs. Learned Classification:**
The proposal uses rule-based thresholds, which are:
- Transparent and debuggable
- Don't require training data
- May need tuning for different game configurations

An alternative would be clustering-based classification (k-means on behavioral metrics), but this:
- Requires multiple runs to establish clusters
- Produces arbitrary cluster labels
- Is harder to interpret

**Recommendation**: Start with rule-based, refine thresholds empirically.

**Handling Edge Cases:**
- Very short runs: Classification may be unreliable; show confidence warning
- Degenerate runs (all agents fail): Skip classification or show "Undetermined"
- Multi-modal populations: Consider per-agent classification, not just best agent

---

### 4.5 Enhancement #5: Population Health Dashboard

#### 4.5.1 Purpose and Rationale

A genetic algorithm's effectiveness depends on maintaining a healthy population that balances exploration and exploitation. Unhealthy populations exhibit:

- **Premature convergence**: Population becomes too similar too quickly
- **Diversity collapse**: All agents converge to local optimum
- **Elite domination**: Only top agents contribute to next generation
- **Stagnation**: No improvement despite continued training

The population health dashboard provides early warning signs of these issues.

#### 4.5.2 What It Answers

- "Is the genetic algorithm working correctly?"
- "Is the population converging too quickly?"
- "Is genetic diversity being maintained?"
- "Are improvements spreading through the population or isolated to elites?"

#### 4.5.3 Proposed Metrics

| Metric | Formula | Healthy Range | Warning Signs |
|--------|---------|---------------|---------------|
| **Diversity Index** | std_dev / mean | 0.3-0.7 | <0.2 (converged) or >1.0 (chaotic) |
| **Elite Gap** | (best - avg) / avg | 0.5-2.0 | >3.0 (knowledge not spreading) |
| **Floor Trend** | Δ(min fitness) | Positive | Negative (worst getting worse) |
| **Ceiling Trend** | Δ(max fitness) | Positive | Flat for >10 gens (stuck) |
| **IQR Trend** | Δ(p75 - p25) | Stable/Shrinking | Rapidly shrinking (premature convergence) |
| **Coefficient of Variation** | std_dev / mean | 0.3-0.6 | <0.1 (homogeneous) |

#### 4.5.4 Proposed Format

```
## Population Health Dashboard

### Current Status: 🟢 Healthy

| Metric              | Value   | Trend (last 10 gens) | Status |
|---------------------|---------|----------------------|--------|
| Diversity Index     | 0.48    | ↓ Decreasing         | 🟡 Watch |
| Elite Gap           | 1.98    | → Stable             | 🟢 Good  |
| Min Fitness Trend   | +12.3   | ↑ Improving          | 🟢 Good  |
| Max Fitness Trend   | +45.2   | ↑ Improving          | 🟢 Good  |
| IQR (p75-p25)       | 435.8   | ↓ Narrowing          | 🟢 Good  |

### Diversity Over Time
| Phase   | Diversity Index | Elite Gap | Min Fitness |
|---------|-----------------|-----------|-------------|
| Phase 1 | 0.85            | 6.43      | -180        |
| Phase 5 | 0.62            | 2.34      | -84         |
| Phase 10| 0.48            | 1.98      | +50         |

### Warnings
- ⚠️ Diversity Index declining - population may be converging prematurely
- ✅ Elite Gap has normalized - knowledge is spreading to population
- ✅ Floor improving - even worst agents are getting better

### Recommendations
- Consider increasing mutation rate if diversity drops below 0.3
- Current elitism rate (20%) appears appropriate
```

#### 4.5.5 Implementation Approach

1. Calculate diversity metrics per generation (most already tracked as std_dev)
2. Compute trends by comparing recent generations to earlier ones
3. Apply threshold-based rules to assign status indicators
4. Generate recommendations based on detected issues
5. Create phase-by-phase diversity table

#### 4.5.6 Prerequisites

- Standard deviation tracked per generation (already exists)
- Percentile data (p25, p75, p90) tracked per generation (already exists)
- Min and max fitness tracked per generation (already exists)

#### 4.5.7 Design Considerations

**Status Thresholds:**
These should be tunable and documented. Initial suggestions:
- 🟢 Green: Metric in healthy range
- 🟡 Yellow: Metric approaching concerning range
- 🔴 Red: Metric indicates problem

**Adaptive Thresholds:**
What's "healthy" may depend on training phase:
- Early training: Higher diversity expected and desired
- Late training: Lower diversity is natural as population converges
Consider phase-adjusted thresholds.

**Actionable Recommendations:**
Each warning should include a potential remedy:
- Low diversity → Increase mutation rate
- High elite gap → Increase tournament size or reduce elitism
- Flat ceiling → Consider restart or architecture change

---

## 5. Tier 2: High-Value Enhancements

These enhancements provide significant additional insight but are less critical than Tier 1. They should be implemented after the essential enhancements are stable.

---

### 5.1 Enhancement #6: Stagnation Analysis

#### 5.1.1 Purpose and Rationale

Learning plateaus are common in evolutionary algorithms. Understanding when, where, and why stagnation occurs helps diagnose training issues and set appropriate hyperparameters.

Stagnation analysis reveals:

- **Plateau patterns**: How long does the algorithm typically get stuck?
- **Recovery ability**: Can the algorithm escape local optima?
- **Training duration**: How long should we run before giving up?
- **Hyperparameter feedback**: Do certain settings cause more stagnation?

#### 5.1.2 What It Answers

- "How often did learning get stuck?"
- "How long were the plateaus?"
- "Did the algorithm recover or stay stuck?"
- "When should I stop a run that isn't improving?"

#### 5.1.3 Proposed Format

```
## Stagnation Analysis

### Summary
- **Total Stagnation Periods**: 4 (periods of 3+ gens without improvement)
- **Longest Plateau**: 6 generations (gens 8-14)
- **Total Generations in Stagnation**: 17 (34% of training)
- **Average Recovery Time**: 4.2 generations

### Stagnation Periods
| Period | Generations | Duration | Best Fitness | Escaped? |
|--------|-------------|----------|--------------|----------|
| 1      | 8-14        | 6 gens   | 1,678        | ✅ Yes    |
| 2      | 16          | 1 gen    | 1,720        | ✅ Yes    |
| 3      | 18-21       | 4 gens   | 1,724        | ✅ Yes    |
| 4      | 23          | 1 gen    | 1,746        | ✅ Yes    |

### Current Momentum
- **Generations Since Last Improvement**: 0
- **Current Trend**: 🟢 Actively improving
- **Projected Plateau Risk**: Low (based on recent improvement rate)
```

#### 5.1.4 Implementation Approach

1. Define stagnation as N consecutive generations without best fitness improvement
2. Scan generation history to identify stagnation periods
3. Calculate period statistics (duration, fitness at plateau, recovery)
4. Assess current momentum based on recent improvement pattern
5. Optionally predict plateau risk based on historical patterns

#### 5.1.5 Prerequisites

- `all_time_best` and `generations_since_improvement` tracked per generation
- Sufficient generations to identify patterns (minimum ~20)

---

### 5.2 Enhancement #7: Best Agent Deep Profile

#### 5.2.1 Purpose and Rationale

The best agent represents the pinnacle of the evolutionary process. A detailed profile helps understand what made this agent successful and whether its success is robust or lucky.

#### 5.2.2 What It Answers

- "What does the champion agent look like?"
- "How much better is it than the population?"
- "When did this agent emerge?"
- "Is this agent's success reproducible?"

#### 5.2.3 Proposed Format

```
## Best Agent Profile

### Identity
- **Generation Discovered**: 25
- **Fitness Score**: 1,910.24
- **Rank**: #1 of 2,500 total agents evaluated

### Performance Metrics
| Metric          | Best Agent | Population Avg | Percentile |
|-----------------|------------|----------------|------------|
| Kills           | 38.3       | 12.3           | 99.8%      |
| Steps Survived  | 946        | 447            | 99.2%      |
| Accuracy        | 95.5%      | 77.6%          | 98.5%      |
| Shots Fired     | 40.1       | 29.3           | 87.3%      |

### Reward Breakdown
| Component              | Score   | % of Total |
|------------------------|---------|------------|
| KillAsteroid           | +958.3  | 50.2%      |
| ConservingAmmoBonus    | +760.7  | 39.8%      |
| NearMiss               | +180.0  | 9.4%       |
| SurvivalBonus          | +15.8   | 0.8%       |
| MaintainingMomentumBonus| -4.2   | -0.2%      |
| Other                  | -0.4    | 0.0%       |

### Dominance Analysis
- **Gap to #2 Agent**: 164.0 points (9.4% better)
- **Gap to Average**: 1,268.7 points (198% better)
- **Gap to Median**: 1,222.7 points (178% better)

### Consistency (across 3 evaluation seeds)
- **Fitness Variance**: ±47.2 (2.5% of mean)
- **Kill Variance**: ±3.1 kills
- **Assessment**: High consistency - performance is skill, not luck

### Generalization Analysis (NEW - requires fresh_game data)
| Metric          | Training | Fresh Game | Ratio  | Assessment |
|-----------------|----------|------------|--------|------------|
| Fitness         | 1,910.2  | 1,652.4    | 86.5%  | ✅ Good     |
| Kills           | 38.3     | 31         | 80.9%  | ✅ Good     |
| Steps Survived  | 946      | 1,127      | 119.1% | ✅ Better!  |
| Accuracy        | 95.5%    | 88.2%      | 92.4%  | ✅ Good     |

**Generalization Grade**: B (86.5% fitness transfer)

**Interpretation**: This agent generalizes well to unseen asteroid configurations.
The slightly lower accuracy in fresh games suggests some overfitting to evaluation
seed patterns, but overall performance transfers robustly.

### Fresh Game Reward Breakdown
| Component              | Training | Fresh Game | Delta    |
|------------------------|----------|------------|----------|
| KillAsteroid           | +958.3   | +775.0     | -183.3   |
| ConservingAmmoBonus    | +760.7   | +612.4     | -148.3   |
| NearMiss               | +180.0   | +225.0     | +45.0    |
| SurvivalBonus          | +15.8    | +18.8      | +3.0     |
| MaintainingMomentumBonus| -4.2    | -8.6       | -4.4     |
```

#### 5.2.4 Implementation Approach

1. Store detailed metrics for the best individual when discovered
2. Compare best agent to population statistics
3. Calculate percentiles for each metric
4. Assess consistency using variance across multi-seed evaluation
5. Compute dominance gaps
6. **(NEW)** Compare training metrics to fresh game metrics
7. **(NEW)** Calculate generalization ratios and grade
8. **(NEW)** Generate interpretation based on ratio patterns

#### 5.2.5 Prerequisites

- Detailed per-agent metrics (not just population averages)
- Multi-seed evaluation data for consistency analysis
- **(NEW)** `fresh_game.*` data from Schema Expansion Priority 1
- **(NEW)** `generalization_metrics.*` derived data

---

### 5.3 Enhancement #8: Learning Velocity Chart

#### 5.3.1 Purpose and Rationale

Knowing *how fast* learning is happening is as important as knowing *that* learning is happening. Learning velocity helps:

- **Predict completion time**: When will training reach target fitness?
- **Detect slowdowns**: Is learning decelerating?
- **Compare runs**: Which hyperparameters learn faster?

#### 5.3.2 What It Answers

- "How fast is the agent improving?"
- "Is learning accelerating or decelerating?"
- "How long until we reach target fitness?"

#### 5.3.3 Proposed Format

```
## Learning Velocity

### Velocity by Phase
| Phase   | Fitness Δ | Δ per Gen | Velocity | Trend      |
|---------|-----------|-----------|----------|------------|
| Phase 1 | +525      | +21.0     | Fast     | --         |
| Phase 2 | +394      | +15.8     | Fast     | ↓ Slowing  |
| Phase 3 | +286      | +11.4     | Moderate | ↓ Slowing  |
| Phase 4 | +156      | +6.2      | Slow     | ↓ Slowing  |
| Phase 5 | +113      | +4.5      | Slow     | → Stable   |

### Current Velocity
- **Recent Improvement Rate**: +4.5 fitness/generation
- **Acceleration**: -0.8 fitness/gen² (decelerating)
- **Projected Generations to +3000 Fitness**: ~290 generations

### Velocity Assessment
Learning is decelerating, which is typical as the population converges.
The deceleration rate is within normal bounds. Consider:
- Increasing mutation if velocity drops below +1.0/gen
- This may indicate approaching local optimum
```

#### 5.3.4 Implementation Approach

1. Calculate fitness delta between consecutive phases
2. Compute per-generation improvement rate
3. Calculate acceleration (change in velocity)
4. Project future fitness using linear extrapolation
5. Generate assessment based on velocity patterns

---

### 5.4 Enhancement #9: Milestone Timeline

#### 5.4.1 Purpose and Rationale

Identifying when specific achievements were first reached provides insight into the learning progression and helps set expectations for future runs.

#### 5.4.2 What It Answers

- "When did agents first achieve X kills?"
- "How long did it take to reach 50% accuracy?"
- "What was the progression of breakthroughs?"

#### 5.4.3 Proposed Format

```
## Milestone Timeline

### Kill Milestones
| Milestone    | First Achieved | Generation | Agent Fitness |
|--------------|----------------|------------|---------------|
| 5 kills      | 0:01:23        | Gen 3      | 156.2         |
| 10 kills     | 0:03:45        | Gen 7      | 412.8         |
| 20 kills     | 0:06:12        | Gen 12     | 892.4         |
| 30 kills     | 0:08:34        | Gen 17     | 1,324.1       |
| 38 kills     | 0:12:45        | Gen 25     | 1,910.2       |

### Accuracy Milestones
| Milestone    | First Achieved | Generation |
|--------------|----------------|------------|
| 50% accuracy | 0:02:34        | Gen 5      |
| 70% accuracy | 0:04:56        | Gen 9      |
| 80% accuracy | 0:07:23        | Gen 14     |
| 90% accuracy | 0:09:12        | Gen 19     |

### Survival Milestones
| Milestone     | First Achieved | Generation |
|---------------|----------------|------------|
| 500 steps     | 0:02:01        | Gen 4      |
| 750 steps     | 0:05:43        | Gen 11     |
| 900 steps     | 0:08:56        | Gen 17     |

### Population Milestones
| Milestone              | First Achieved | Generation |
|------------------------|----------------|------------|
| Positive avg fitness   | 0:00:32        | Gen 1      |
| All agents positive    | 0:11:23        | Gen 22     |
| Avg fitness > 500      | 0:07:45        | Gen 15     |
```

#### 5.4.4 Implementation Approach

1. Define milestone thresholds for each metric category
2. Scan generation history for first occurrence of each threshold
3. Record generation number and timestamp
4. Handle missing milestones (not yet achieved)

---

### 5.5 Enhancement #10: Survival Distribution

#### 5.5.1 Purpose and Rationale

Understanding when and how agents die reveals whether agents are learning survival skills or just getting lucky with early kills before dying.

#### 5.5.2 What It Answers

- "When do agents typically die?"
- "Are agents surviving longer over training?"
- "What percentage complete full episodes?"

#### 5.5.3 Proposed Format

```
## Survival Analysis

### Survival Distribution (Final Phase)
- **Mean Survival**: 447 steps (29.8% of max)
- **Median Survival**: 412 steps
- **Full Episode Completion**: 8.3% of agents
- **Early Death (<25% of max)**: 12.4% of agents

### Survival Progression
| Phase   | Mean Steps | Completion % | Early Death % |
|---------|------------|--------------|---------------|
| Phase 1 | 263        | 1.2%         | 34.5%         |
| Phase 5 | 412        | 4.8%         | 18.2%         |
| Phase 10| 447        | 8.3%         | 12.4%         |

### Death Time Distribution (Final Phase)
| Survival Range  | % of Agents |
|-----------------|-------------|
| 0-150 steps     | 5.2%        |
| 150-375 steps   | 22.4%       |
| 375-750 steps   | 48.1%       |
| 750-1125 steps  | 18.6%       |
| 1125-1500 steps | 5.7%        |
```

#### 5.5.4 Implementation Approach

1. Track step distribution per generation (requires per-agent data, not just averages)
2. Calculate survival percentiles and completion rates
3. Compare across phases to show progression

---

## 6. Tier 3: Quality-of-Life Enhancements

These enhancements provide polish and additional insight but are lowest priority. They improve the user experience without being essential.

---

### 6.1 Enhancement #11: Correlation Matrix

#### 6.1.1 Purpose and Rationale

Understanding which metrics correlate with fitness helps identify what truly matters for performance and can guide reward design.

#### 6.1.2 Proposed Format

```
## Correlation Analysis

### Fitness Correlations
| Metric       | Correlation | Strength   |
|--------------|-------------|------------|
| Kills        | +0.89       | Strong     |
| Accuracy     | +0.76       | Strong     |
| Steps        | +0.52       | Moderate   |
| Shots        | +0.34       | Weak       |

### Interpretation
Fitness is most strongly predicted by kills (r=0.89), followed by accuracy (r=0.76).
Survival time has moderate correlation, suggesting that surviving longer helps
but isn't sufficient without killing asteroids.
```

#### 6.1.3 Implementation Approach

Calculate Pearson correlation coefficient between fitness and each behavioral metric across all agents in the final generation (or across all generations for trend analysis).

---

### 6.2 Enhancement #12: Generation Highlights

#### 6.2.1 Purpose and Rationale

Notable generations (best improvements, worst regressions, unusual events) deserve special attention. Highlighting them saves the reader from scanning all data.

#### 6.2.2 Proposed Format

```
## Generation Highlights

### 🏆 Best Improvement
**Generation 6**: Best fitness jumped +305.5 (+24.0%)
- Best fitness: 1,577.0 (from 1,271.5)
- Key change: ConservingAmmoBonus flipped positive for first time

### 📉 Worst Regression
**Generation 16**: Best fitness dropped -487.3 (-28.3%)
- Best fitness: 1,233.3 (from 1,720.5)
- Note: New all-time best had emerged previous generation; this is reversion to mean

### 🎯 Most Accurate Generation
**Generation 25**: Population accuracy reached 79.7% (highest ever)

### 🔥 Most Kills Generation
**Generation 25**: Population averaged 13.0 kills (highest ever)

### 🎲 Most Diverse Generation
**Generation 1**: Diversity index 0.85 (expected for initial random population)

### 🎯 Most Converged Generation
**Generation 25**: Diversity index 0.48 (population converging)
```

---

### 6.3 Enhancement #13: Reward Balance Warnings

#### 6.3.1 Purpose and Rationale

Automatically detect potential issues with reward configuration and surface them as warnings. This is "linting" for reward design.

#### 6.3.2 Proposed Format

```
## Reward Balance Analysis

### Warnings
⚠️ **MaintainingMomentumBonus consistently negative**
   This component has been negative for 100% of training, averaging -28.4/episode.
   Agents have not learned to move. Consider:
   - Increasing the bonus magnitude
   - Reducing penalties that discourage movement
   - Verifying the component is detecting movement correctly

⚠️ **KillAsteroid dominates reward (47.9%)**
   This single component accounts for nearly half of all positive reward.
   While this may be intentional, consider whether other behaviors are
   being adequately incentivized.

### Confirmations
✅ **ConservingAmmoBonus learned** - Started negative, now strongly positive
✅ **No single component >60%** - Reward is reasonably balanced
✅ **Survival component positive** - Agents are learning to stay alive
```

---

### 6.4 Enhancement #14: Action Distribution Estimates

#### 6.4.1 Purpose and Rationale

While we don't directly track action frequency, we can estimate action patterns from behavioral metrics. This gives insight into how the agent is actually playing.

#### 6.4.2 Proposed Format

```
## Estimated Action Distribution

Based on behavioral metrics, the agent's action patterns are approximately:

| Action   | Estimated Usage | Inference Source              |
|----------|-----------------|-------------------------------|
| Thrust   | Low (~15%)      | MaintainingMomentumBonus < 0  |
| Turn     | Medium (~40%)   | High accuracy implies aiming  |
| Shoot    | High (~65%)     | 29.3 shots per episode        |
| Idle     | Medium (~30%)   | Low momentum, waiting periods |

**Note**: These are estimates based on reward outcomes, not direct action tracking.
```

---

### 6.5 Enhancement #15: ASCII Trend Sparklines

#### 6.5.1 Purpose and Rationale

Compact visual representations of trends allow readers to see patterns at a glance without reading tables. Sparklines are particularly effective for showing direction and magnitude of change.

#### 6.5.2 Proposed Format

```
## Quick Trend Overview

Best Fitness: 612 → 1,910   [▁▂▃▄▅▆▆▇▇█] +212%
Avg Fitness:  16 → 642      [▁▁▂▃▄▅▆▇▇█] +3912%
Avg Kills:    3.2 → 12.3    [▁▂▃▅▆▆▇▇▇█] +284%
Avg Accuracy: 35% → 78%     [▁▃▅▆▇▇▇███] +119%
Avg Steps:    263 → 447     [▁▂▃▄▅▆▆▇▇█] +70%
Diversity:    0.85 → 0.48   [█▇▇▆▅▅▄▃▃▂] -44%
```

#### 6.5.3 Implementation Approach

1. Sample metric values at 10 evenly-spaced points
2. Normalize to 0-7 scale (8 sparkline characters: ▁▂▃▄▅▆▇█)
3. Map normalized values to sparkline characters
4. Calculate percentage change

---

## 7. Implementation Considerations

### 7.1 File Structure

The enhanced `training_summary.md` should follow this structure:

```
# Training Summary Report

## Quick Overview (Sparklines + Key Stats)  ← NEW
## Training Configuration
## Overall Summary
## Quick Trend Overview (Sparklines)        ← NEW
## Training Progress by Decile              ← NEW (Enhancement #1)
## Behavioral Classification                ← NEW (Enhancement #4)
## Kill Efficiency Analysis                 ← NEW (Enhancement #3)
## Reward Component Evolution               ← NEW (Enhancement #2)
## Population Health Dashboard              ← NEW (Enhancement #5)
## Stagnation Analysis                      ← NEW (Enhancement #6)
## Best Agent Profile                       ← NEW (Enhancement #7)
## Learning Velocity                        ← NEW (Enhancement #8)
## Milestone Timeline                       ← NEW (Enhancement #9)
## Survival Analysis                        ← NEW (Enhancement #10)
## Correlation Analysis                     ← NEW (Enhancement #11)
## Generation Highlights                    ← NEW (Enhancement #12)
## Reward Balance Warnings                  ← NEW (Enhancement #13)
## Action Distribution Estimates            ← NEW (Enhancement #14)
```

### 7.2 Performance Considerations

Most enhancements require only post-hoc analysis of existing data. However:

- **Memory**: Storing per-agent data (not just averages) increases memory usage
- **Computation**: Correlation analysis and classification add post-training computation
- **File size**: Enhanced summary will be significantly longer

Recommendations:
- Keep raw generation data in memory/JSON as-is
- Compute enhanced analytics only at report generation time
- Consider optional "detailed" vs "summary" report modes

### 7.3 Backward Compatibility

The `training_data.json` format should remain unchanged to maintain compatibility with existing analysis scripts. New data required for enhanced analytics should be added as additional fields, not replacing existing ones.

### 7.4 Testing Strategy

Each enhancement should be tested with:
- Normal run (50+ generations)
- Short run (<10 generations)
- Interrupted run
- Degenerate run (all agents fail)
- Perfect run (all agents succeed)

### 7.5 Configuration

Consider adding analytics configuration options:
- Enable/disable individual enhancements
- Adjust thresholds for warnings
- Set decile count (5, 10, 20)
- Choose sparkline style

---

## 8. Data Requirements and Prerequisites

> **See also**: `TRAINING_DATA_SCHEMA_EXPANSION.md` for complete schema documentation.

### 8.1 Data Availability After Schema Expansion

The companion document `TRAINING_DATA_SCHEMA_EXPANSION.md` defines all data collection changes. After implementation, the following data will be available:

#### 8.1.1 Existing Data (Already Tracked)

| Data Point | Source | Used By |
|------------|--------|---------|
| `best_fitness` | Per generation | All enhancements |
| `avg_fitness` | Per generation | Decile breakdown, velocity |
| `min_fitness` | Per generation | Health dashboard |
| `std_dev` | Per generation | Health dashboard, diversity |
| `p25_fitness`, `p75_fitness`, `p90_fitness` | Per generation | Health dashboard |
| `avg_kills`, `avg_steps`, `avg_accuracy` | Per generation | Efficiency, survival |
| `avg_reward_breakdown` | Per generation | Reward evolution |
| `best_agent_kills`, `best_agent_steps`, `best_agent_accuracy` | Per generation | Best agent profile |
| `all_time_best`, `generations_since_improvement` | Per generation | Stagnation analysis |

#### 8.1.2 New Data (From Schema Expansion - Priority 1)

| Data Point | Source | Used By |
|------------|--------|---------|
| `fresh_game.fitness` | Fresh game test | Generalization analysis, best agent profile |
| `fresh_game.kills` | Fresh game test | Generalization analysis |
| `fresh_game.steps_survived` | Fresh game test | Generalization analysis |
| `fresh_game.accuracy` | Fresh game test | Generalization analysis |
| `fresh_game.reward_breakdown` | Fresh game test | Best agent profile |
| `generalization_metrics.fitness_ratio` | Derived | Generalization grade, warnings |
| `generalization_metrics.generalization_grade` | Derived | Quick assessment |

#### 8.1.3 New Data (From Schema Expansion - Priority 2)

| Data Point | Source | Used By |
|------------|--------|---------|
| `distributions.fitness_values` | All agents | Correlation matrix, distribution analysis |
| `distributions.kills_values` | All agents | Survival distribution, correlation |
| `distributions.steps_values` | All agents | Survival distribution |
| `distributions.accuracy_values` | All agents | Correlation matrix |
| `distribution_stats.viable_agent_count` | Derived | Health dashboard |
| `distribution_stats.fitness_skewness` | Derived | Population health |

#### 8.1.4 New Data (From Schema Expansion - Priority 3)

| Data Point | Source | Used By |
|------------|--------|---------|
| `action_metrics.avg_thrust_frequency` | Episode tracking | Behavioral classification |
| `action_metrics.avg_turn_frequency` | Episode tracking | Behavioral classification |
| `action_metrics.avg_shoot_frequency` | Episode tracking | Action estimates |
| `action_metrics.avg_idle_frequency` | Episode tracking | Behavioral classification |
| `action_metrics.best_agent_action_counts` | Episode tracking | Best agent profile |

#### 8.1.5 New Data (From Schema Expansion - Priority 4-5)

| Data Point | Source | Used By |
|------------|--------|---------|
| `operator_stats.crossovers_performed` | Evolution step | GA tuning insights |
| `operator_stats.mutations_performed` | Evolution step | GA tuning insights |
| `timing.generation_duration_seconds` | Timestamps | Performance profiling |
| `timing.evaluation_duration_seconds` | Timestamps | Performance profiling |

### 8.2 Enhancement-to-Data Mapping

This table shows which data each enhancement requires:

| Enhancement | Required Data | Data Status |
|-------------|---------------|-------------|
| #1 Decile Breakdown | Existing aggregates + fresh_game | ✅ Available after P1 |
| #2 Reward Evolution | avg_reward_breakdown | ✅ Already available |
| #3 Kill Efficiency | avg_kills, avg_shots, avg_steps | ✅ Already available |
| #4 Behavioral Classification | action_metrics | ✅ Available after P3 |
| #5 Population Health | std_dev, percentiles, distributions | ✅ Available after P2 |
| #6 Stagnation Analysis | all_time_best, generations_since_improvement | ✅ Already available |
| #7 Best Agent Profile | best_agent_*, fresh_game, distributions | ✅ Available after P2 |
| #8 Learning Velocity | avg_fitness, best_fitness | ✅ Already available |
| #9 Milestone Timeline | Aggregates + timestamps | ✅ Available after P5 |
| #10 Survival Distribution | distributions.steps_values | ✅ Available after P2 |
| #11 Correlation Matrix | distributions.* arrays | ✅ Available after P2 |
| #12 Generation Highlights | All aggregates | ✅ Already available |
| #13 Reward Warnings | avg_reward_breakdown | ✅ Already available |
| #14 Action Estimates | action_metrics | ✅ Available after P3 |
| #15 Sparklines | All aggregates | ✅ Already available |

### 8.3 Implementation Phasing

Given the data dependencies, implement analytics enhancements in this order:

**Phase A** (No new data needed):
- #2 Reward Evolution
- #3 Kill Efficiency
- #6 Stagnation Analysis
- #8 Learning Velocity
- #12 Generation Highlights
- #13 Reward Warnings
- #15 Sparklines

**Phase B** (After Schema P1 - Fresh Game):
- #1 Decile Breakdown (enhanced with generalization)
- #7 Best Agent Profile (with fresh game comparison)

**Phase C** (After Schema P2 - Distributions):
- #5 Population Health Dashboard
- #10 Survival Distribution
- #11 Correlation Matrix

**Phase D** (After Schema P3 - Actions):
- #4 Behavioral Classification
- #14 Action Distribution Estimates

**Phase E** (After Schema P5 - Timing):
- #9 Milestone Timeline (with precise timestamps)

---

## 9. Future Extensions

### 9.1 Cross-Run Comparison

Once baseline runs are saved, add:
- Comparison to previous best run
- Comparison to baseline configuration
- Statistical significance testing

### 9.2 Real-Time Analytics

Stream analytics during training:
- Live dashboard in terminal
- Early stopping based on stagnation
- Automatic hyperparameter adjustment

### 9.3 Visualization Export

Generate visual reports:
- PNG charts of learning curves
- HTML interactive dashboard
- Jupyter notebook for custom analysis

### 9.4 Agent Replay Integration

Link best agents to replay files:
- Save best agent parameters
- Provide command to replay agent
- Include replay link in summary

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Decile** | One of 10 equal parts of the training run |
| **Diversity Index** | Standard deviation divided by mean; measures population spread |
| **Elite Gap** | Difference between best and average fitness |
| **Stagnation** | Period without improvement in best fitness |
| **Sparkline** | Compact inline visualization of trend data |
| **Archetype** | Classification of agent behavioral strategy |

---

## Appendix B: References

- Stanley, K. O., & Miikkulainen, R. (2002). Evolving Neural Networks through Augmenting Topologies. *Evolutionary Computation*.
- Eiben, A. E., & Smith, J. E. (2015). *Introduction to Evolutionary Computing*. Springer.
- De Jong, K. A. (2006). *Evolutionary Computation: A Unified Approach*. MIT Press.

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-08 | AI Research Team | Initial proposal |
| 1.1 | 2026-01-08 | AI Research Team | Added dependency notice for Schema Expansion; Updated Section 8 with full data mapping; Added generalization analysis to Best Agent Profile; Added implementation phasing based on data availability |

---

*End of Document*
