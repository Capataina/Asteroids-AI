# Training Data Schema Expansion Proposal

## Document Information

| Field | Value |
|-------|-------|
| **Author** | AI Research Team |
| **Date** | 2026-01-08 |
| **Status** | Proposal / Design Document |
| **Related Files** | `training/analytics.py`, `training/train_ga_parallel.py`, `training/parallel_evaluator.py` |
| **Dependencies** | Should be implemented BEFORE `ANALYTICS_ENHANCEMENT_PROPOSAL.md` |
| **Stakeholders** | ML Engineers, Researchers, Training Pipeline Maintainers |

---

## Executive Summary

This document proposes expansions to the training data collection schema (`training_data.json`) to enable richer analytics, better debugging, and deeper understanding of agent behavior. The current schema captures population-level aggregates but misses critical data about individual agent performance, generalization ability, and behavioral patterns.

The most significant gap is the **complete absence of fresh game performance tracking**. Currently, after each generation, the best agent is tested in a fresh (unseeded) game environment, but this critical generalization data is only logged to the console and immediately lost. This represents a fundamental blind spot in our understanding of whether agents are truly learning generalizable skills or merely memorizing specific seed configurations.

**Core Principle**: If we observe it during training, we should be able to analyze it later. Console logs are ephemeral; structured data is permanent.

---

## Table of Contents

1. [Background and Motivation](#1-background-and-motivation)
2. [Current Schema Analysis](#2-current-schema-analysis)
3. [Proposed Schema Expansions](#3-proposed-schema-expansions)
4. [Priority 1: Fresh Game Performance Tracking](#4-priority-1-fresh-game-performance-tracking)
5. [Priority 2: Distribution Data](#5-priority-2-distribution-data)
6. [Priority 3: Action-Level Metrics](#6-priority-3-action-level-metrics)
7. [Priority 4: Genetic Operator Statistics](#7-priority-4-genetic-operator-statistics)
8. [Priority 5: Computational Metadata](#8-priority-5-computational-metadata)
9. [Priority 6: Advanced Tracking](#9-priority-6-advanced-tracking)
10. [Schema Migration Strategy](#10-schema-migration-strategy)
11. [Storage Impact Analysis](#11-storage-impact-analysis)
12. [Implementation Roadmap](#12-implementation-roadmap)

---

## 1. Background and Motivation

### 1.1 The Data Collection Philosophy

Effective machine learning research requires comprehensive data collection. The principle is simple:

> **If you might want to analyze it later, track it now.**

Retroactively adding metrics requires re-running experiments, which is:
- Time-consuming (hours or days of training)
- Potentially impossible (if hyperparameters or code changed)
- Wasteful of computational resources

The cost of storing extra data is negligible compared to the cost of re-running experiments.

### 1.2 Current Pain Points

**Pain Point 1: The Fresh Game Black Hole**

Every generation, we test the best agent in a fresh game. We watch it play. We see kills, steps, accuracy displayed on screen. Then... it's gone. The only record is a console log line that scrolls away.

```
Testing best agent in fresh game (training fitness=1910.24, all-time best=1910.24)...
  Step 100: Score=156.2, Kills=4, Shots=8, Time=1.67s
  Step 200: Score=312.8, Kills=8, Shots=15, Time=3.33s
  ...
Best agent died after 847 steps
```

This data is incredibly valuable:
- Does training fitness predict fresh game performance?
- Are agents overfitting to evaluation seeds?
- How large is the generalization gap?

But we can't analyze any of this because we don't save it.

**Pain Point 2: Population Opacity**

We know the average fitness is 641, but what does the distribution look like?
- Is it normal? Bimodal? Heavily skewed?
- Are there outlier agents far above or below?
- What percentage of agents are "viable" vs "failed"?

We can't answer these questions because we only store aggregates.

**Pain Point 3: Behavioral Blindness**

We know agents average 12 kills, but:
- Do high-fitness agents kill more, or survive longer, or both?
- What's the correlation between accuracy and fitness?
- Do the top 10% of agents behave differently from the bottom 10%?

Without per-agent behavioral data, these questions are unanswerable.

**Pain Point 4: Action Inference**

We infer action patterns from outcomes:
- Negative momentum bonus → "agent probably isn't thrusting"
- High accuracy → "agent probably aims before shooting"

But these are guesses. Direct action frequency counts would give us certainty.

### 1.3 Design Goals for Schema Expansion

1. **Comprehensiveness**: Capture everything observable
2. **Efficiency**: Minimize storage and computation overhead
3. **Backward Compatibility**: Don't break existing analysis scripts
4. **Progressive Detail**: Summary data always present, detail data optional
5. **Self-Documenting**: Schema should be understandable without external docs

---

## 2. Current Schema Analysis

### 2.1 Existing Schema Structure

```json
{
  "config": {
    "population_size": 100,
    "num_generations": 500,
    "mutation_probability": 0.2,
    "mutation_gaussian_sigma": 0.15,
    "crossover_probability": 0.7,
    "max_workers": 16,
    "frame_delay": 0.016666666666666666
  },
  "start_time": "2026-01-06T00:54:36.126852",
  "end_time": "2026-01-06T01:07:21.788360",
  "summary": {
    "total_generations": 25,
    "training_duration": "0:12:45.661508",
    "final_best_fitness": 1910.24,
    "all_time_best_fitness": 1910.24,
    "final_avg_fitness": 641.55,
    "final_min_fitness": 50.27,
    "avg_improvement_early_to_late": 345.01,
    "best_generation": 25,
    "worst_generation": 2,
    "final_stagnation": 0,
    "final_avg_kills": 12.31,
    "final_avg_steps": 447,
    "final_avg_accuracy": 0.776,
    "max_kills_ever": 38.33,
    "max_steps_ever": 992
  },
  "generations": [
    {
      "generation": 1,
      "best_fitness": 612.06,
      "avg_fitness": 15.95,
      "min_fitness": -180.44,
      "median_fitness": 2.58,
      "std_dev": 102.96,
      "population_size": 100,
      "p25_fitness": -37.61,
      "p75_fitness": 37.40,
      "p90_fitness": 170.09,
      "best_improvement": 0.0,
      "avg_improvement": 0.0,
      "all_time_best": 612.06,
      "generations_since_improvement": 0,
      "avg_kills": 3.21,
      "avg_steps": 263.14,
      "avg_accuracy": 0.355,
      "avg_shots": 9.44,
      "total_kills": 321.0,
      "max_kills": 23.67,
      "max_steps": 768.67,
      "best_agent_kills": 19.33,
      "best_agent_steps": 639.67,
      "best_agent_accuracy": 0.959,
      "avg_reward_breakdown": {
        "KillAsteroid": 80.25,
        "SurvivalBonus": 4.39,
        "ConservingAmmoBonus": -83.13,
        "MaintainingMomentumBonus": -9.10,
        "NearMiss": 23.05,
        "SpacingFromWallsBonus": -0.64,
        "MovingTowardDangerBonus": 1.15
      }
    }
  ]
}
```

### 2.2 What's Present

| Category | Data Points | Completeness |
|----------|-------------|--------------|
| Configuration | All hyperparameters | ✅ Complete |
| Timing | Start, end, duration | ✅ Complete |
| Fitness Aggregates | Best, avg, min, median, std, percentiles | ✅ Complete |
| Behavioral Aggregates | Avg kills, steps, accuracy, shots | ✅ Complete |
| Best Agent (Training) | Kills, steps, accuracy | ⚠️ Partial |
| Reward Breakdown | Per-component averages | ✅ Complete |
| Fresh Game | **NOTHING** | ❌ Missing |
| Per-Agent Data | **NOTHING** | ❌ Missing |
| Action Data | **NOTHING** | ❌ Missing |
| Operator Stats | **NOTHING** | ❌ Missing |

### 2.3 Critical Gaps Summary

| Gap | Impact | Priority |
|-----|--------|----------|
| No fresh game data | Can't assess generalization | **Critical** |
| No per-agent arrays | Can't analyze distributions | **High** |
| No action frequencies | Can't verify behavioral claims | **Medium** |
| No operator stats | Can't tune GA effectively | **Medium** |
| No timing per generation | Can't profile performance | **Low** |

---

## 3. Proposed Schema Expansions

### 3.1 Expansion Categories

| Priority | Category | New Fields | Storage Impact |
|----------|----------|------------|----------------|
| P1 | Fresh Game Performance | ~15 fields per gen | ~1.5 KB/gen |
| P2 | Distribution Data | ~400 values per gen | ~4 KB/gen |
| P3 | Action Metrics | ~8 fields per gen | ~0.5 KB/gen |
| P4 | Operator Statistics | ~10 fields per gen | ~0.5 KB/gen |
| P5 | Computational Metadata | ~5 fields per gen | ~0.2 KB/gen |
| P6 | Advanced Tracking | Variable | Variable |

**Total Impact**: ~7 KB per generation → ~3.5 MB for 500 generations (negligible)

### 3.2 Naming Conventions

To maintain clarity and enable easy querying:

- **Training metrics**: No prefix (existing convention)
- **Fresh game metrics**: Prefix with `fresh_`
- **Per-agent arrays**: Suffix with `_distribution`
- **Action metrics**: Prefix with `action_`
- **Operator stats**: Prefix with `operator_`
- **Timing data**: Prefix with `timing_`

---

## 4. Priority 1: Fresh Game Performance Tracking

### 4.1 Rationale

This is the single most important addition to the schema. The fresh game test exists specifically to evaluate generalization—whether the agent learned real skills or just memorized the evaluation seeds. Currently, this critical data vanishes into console logs.

**The Generalization Question**: If an agent scores 1,910 fitness on training seeds but only 400 on a fresh game, that's a massive red flag. We need to track this systematically.

### 4.2 What Happens Currently

```python
def _start_best_agent_display(self):
    """Start displaying the current generation's best agent in a FRESH game."""
    # ... reset game with fresh random asteroids ...
    print(f"Testing best agent in fresh game (training fitness={self.display_fitness:.2f})...")

def _update_best_agent_display(self, delta_time):
    # ... agent plays ...
    if self.best_agent_steps % 100 == 0:
        print(f"  Step {self.best_agent_steps}: Score={current_score:.1f}, Kills={kills}...")

    # When agent dies or max steps reached:
    print(f"Best agent died after {self.best_agent_steps} steps")
    # DATA IS LOST HERE - never stored anywhere
```

### 4.3 Proposed Fresh Game Schema

```json
{
  "generation": 25,

  "// EXISTING TRAINING DATA": "...",

  "fresh_game": {
    "fitness": 1245.67,
    "kills": 28,
    "steps_survived": 847,
    "shots_fired": 34,
    "accuracy": 0.824,
    "time_alive_seconds": 14.12,
    "cause_of_death": "asteroid_collision",
    "completed_full_episode": false,
    "reward_breakdown": {
      "KillAsteroid": 700.0,
      "ConservingAmmoBonus": 480.0,
      "SurvivalBonus": 14.12,
      "MaintainingMomentumBonus": -25.3,
      "NearMiss": 75.0,
      "SpacingFromWallsBonus": -0.15,
      "MovingTowardDangerBonus": 2.0
    }
  },

  "generalization_metrics": {
    "fitness_ratio": 0.652,
    "kills_ratio": 0.730,
    "steps_ratio": 0.896,
    "accuracy_delta": -0.131,
    "generalization_grade": "B"
  }
}
```

### 4.4 Field Definitions

#### 4.4.1 Core Fresh Game Metrics

| Field | Type | Description |
|-------|------|-------------|
| `fresh_game.fitness` | float | Total fitness achieved in fresh game |
| `fresh_game.kills` | int | Asteroids destroyed |
| `fresh_game.steps_survived` | int | Steps before death or episode end |
| `fresh_game.shots_fired` | int | Total shots taken |
| `fresh_game.accuracy` | float | Hits / shots (0.0-1.0) |
| `fresh_game.time_alive_seconds` | float | Real time survived |
| `fresh_game.cause_of_death` | string | "asteroid_collision", "completed_episode", or "timeout" |
| `fresh_game.completed_full_episode` | bool | Did agent survive all max_steps? |
| `fresh_game.reward_breakdown` | object | Per-component reward scores |

#### 4.4.2 Generalization Metrics (Derived)

| Field | Type | Formula | Interpretation |
|-------|------|---------|----------------|
| `fitness_ratio` | float | fresh_fitness / training_fitness | 1.0 = perfect generalization |
| `kills_ratio` | float | fresh_kills / training_kills | How well killing skill transfers |
| `steps_ratio` | float | fresh_steps / training_steps | How well survival transfers |
| `accuracy_delta` | float | fresh_accuracy - training_accuracy | Positive = better in fresh |
| `generalization_grade` | string | A/B/C/D/F based on fitness_ratio | Quick assessment |

#### 4.4.3 Generalization Grade Thresholds

| Grade | Fitness Ratio | Interpretation |
|-------|---------------|----------------|
| A | ≥ 0.90 | Excellent generalization |
| B | 0.70 - 0.89 | Good generalization |
| C | 0.50 - 0.69 | Moderate generalization |
| D | 0.30 - 0.49 | Poor generalization |
| F | < 0.30 | Failed to generalize |

### 4.5 Implementation Approach

#### 4.5.1 Data Collection Point

The fresh game data should be collected in `_update_best_agent_display()` in `train_ga_parallel.py`. When the display phase ends (agent dies or max steps), capture all metrics before transitioning to the evolution phase.

```
Location: ParallelGATrainingDriver._update_best_agent_display()
Trigger: When self.showing_best_agent becomes False
Action: Package metrics into fresh_game dict, attach to current generation data
```

#### 4.5.2 Required Tracking During Fresh Game

Currently tracked (available via `game.metrics_tracker`):
- kills, shots_fired, time_alive, accuracy

Need to add tracking for:
- Per-component reward breakdown (use episode_runner.reward_calculator)
- Cause of death detection

#### 4.5.3 Cause of Death Detection

```
Logic:
- If steps >= max_steps AND player alive → "completed_episode"
- If player not in player_list → "asteroid_collision"
- If external termination → "timeout" (edge case)
```

### 4.6 Why This Matters

**Scenario 1: High Training, Low Fresh**
```
Training fitness: 1,910
Fresh fitness: 380
Ratio: 0.20 (Grade F)
```
This agent has massively overfit to the evaluation seeds. The "skill" it learned is actually memorization. This is a critical signal that:
- Multi-seed evaluation may not be diverse enough
- Agent strategy is brittle
- Fitness scores are misleading

**Scenario 2: Consistent Performance**
```
Training fitness: 1,910
Fresh fitness: 1,650
Ratio: 0.86 (Grade B)
```
This agent has learned generalizable skills. The training fitness is meaningful.

**Scenario 3: Better in Fresh Game**
```
Training fitness: 800
Fresh fitness: 1,200
Ratio: 1.50 (Grade A+)
```
Unusual but possible if evaluation seeds happened to be harder than average. Indicates robust learning.

### 4.7 Summary-Level Aggregations

Add to the top-level `summary` object:

```json
{
  "summary": {
    "// existing fields...": "...",

    "avg_generalization_ratio": 0.72,
    "best_fresh_fitness": 1650.0,
    "best_fresh_generation": 22,
    "worst_generalization_ratio": 0.35,
    "worst_generalization_generation": 8,
    "avg_fresh_kills": 18.4,
    "fresh_episode_completion_rate": 0.12
  }
}
```

---

## 5. Priority 2: Distribution Data

### 5.1 Rationale

Population-level aggregates hide important information about the distribution shape. Knowing "average fitness is 641" doesn't tell you if:
- Most agents are around 641 (tight normal distribution)
- Half are at 300, half at 1000 (bimodal)
- One agent is at 5000, rest are at 500 (extreme outlier)
- 80% are negative, 20% are very positive (skewed)

Distribution data enables:
- Identifying population health issues
- Detecting premature convergence
- Finding outlier strategies
- Correlation analysis between metrics

### 5.2 Proposed Distribution Schema

```json
{
  "generation": 25,

  "// EXISTING DATA": "...",

  "distributions": {
    "fitness_values": [50.3, 123.4, 156.7, ..., 1910.2],
    "kills_values": [2, 5, 8, 12, ..., 38],
    "steps_values": [120, 234, 456, ..., 946],
    "accuracy_values": [0.45, 0.62, 0.78, ..., 0.96],
    "shots_values": [15, 22, 28, ..., 45]
  },

  "distribution_stats": {
    "fitness_skewness": 0.85,
    "fitness_kurtosis": 2.34,
    "fitness_bimodality_coefficient": 0.42,
    "viable_agent_count": 92,
    "failed_agent_count": 8
  }
}
```

### 5.3 Field Definitions

#### 5.3.1 Raw Distribution Arrays

| Field | Type | Description |
|-------|------|-------------|
| `fitness_values` | float[] | All 100 fitness scores, sorted ascending |
| `kills_values` | float[] | All 100 kill counts (may be averaged across seeds) |
| `steps_values` | float[] | All 100 step counts |
| `accuracy_values` | float[] | All 100 accuracy values |
| `shots_values` | float[] | All 100 shot counts |

**Note**: Values should be sorted ascending to enable easy percentile queries.

#### 5.3.2 Distribution Statistics

| Field | Type | Description |
|-------|------|-------------|
| `fitness_skewness` | float | Measure of asymmetry (0 = symmetric, + = right tail, - = left tail) |
| `fitness_kurtosis` | float | Measure of tail heaviness (3 = normal, >3 = heavy tails) |
| `fitness_bimodality_coefficient` | float | Sarle's bimodality coefficient (>0.555 suggests bimodal) |
| `viable_agent_count` | int | Agents with fitness > 0 |
| `failed_agent_count` | int | Agents with fitness ≤ 0 |

### 5.4 Implementation Approach

#### 5.4.1 Data Collection Point

The `evaluate_population_parallel()` function already computes all per-agent fitnesses. Currently it returns only the fitness list; we need to also capture behavioral metrics per agent.

```
Location: parallel_evaluator.py:evaluate_population_parallel()
Current: Returns fitnesses (list), seed, aggregated_metrics
Change: Also return per-agent behavioral metrics
```

#### 5.4.2 Storage Considerations

For a population of 100 agents:
- 5 arrays × 100 values × 8 bytes = 4 KB per generation
- 500 generations = 2 MB total

This is negligible. Store full arrays.

#### 5.4.3 Alternative: Histogram Bins

If storage becomes a concern (unlikely), an alternative is to store histogram bins instead of raw values:

```json
{
  "fitness_histogram": {
    "bins": [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000],
    "counts": [8, 12, 25, 22, 15, 10, 5, 2, 0, 1]
  }
}
```

This reduces storage but loses individual agent data. **Recommendation**: Store full arrays.

### 5.5 Correlation Enablement

With per-agent arrays, we can compute correlations:

```
correlation(fitness, kills) = ?
correlation(fitness, accuracy) = ?
correlation(kills, steps) = ?
```

These correlations answer: "What metrics actually predict fitness?"

---

## 6. Priority 3: Action-Level Metrics

### 6.1 Rationale

Currently, we infer agent behavior from outcomes:
- Negative momentum bonus → "probably not thrusting much"
- High accuracy → "probably aiming before shooting"

These are educated guesses. Direct action tracking provides certainty.

### 6.2 Proposed Action Schema

```json
{
  "generation": 25,

  "action_metrics": {
    "avg_thrust_frequency": 0.23,
    "avg_turn_frequency": 0.45,
    "avg_shoot_frequency": 0.18,
    "avg_idle_frequency": 0.14,

    "best_agent_action_counts": {
      "thrust": 218,
      "turn_left": 312,
      "turn_right": 287,
      "shoot": 40,
      "idle": 89
    },

    "population_action_variance": {
      "thrust": 0.08,
      "turn": 0.12,
      "shoot": 0.05,
      "idle": 0.15
    }
  }
}
```

### 6.3 Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `avg_thrust_frequency` | float | Fraction of steps where thrust was active (0.0-1.0) |
| `avg_turn_frequency` | float | Fraction of steps with any turning |
| `avg_shoot_frequency` | float | Fraction of steps where shoot was active |
| `avg_idle_frequency` | float | Fraction of steps with no action |
| `best_agent_action_counts` | object | Raw action counts for best agent |
| `population_action_variance` | object | How much action patterns vary across population |

### 6.4 Implementation Approach

#### 6.4.1 Tracking During Episode

Add counters to the episode evaluation loop:

```
For each step:
  action = agent.get_action(state)
  action_counts['thrust'] += action[2] > 0.5
  action_counts['turn_left'] += action[0] > 0.5
  action_counts['turn_right'] += action[1] > 0.5
  action_counts['shoot'] += action[3] > 0.5
  action_counts['idle'] += all(a <= 0.5 for a in action)
```

#### 6.4.2 Aggregation

After all agents evaluated:
- Compute frequencies: count / total_steps
- Average across population
- Compute variance

### 6.5 Behavioral Insights Enabled

| Pattern | Interpretation |
|---------|----------------|
| High thrust, low turn | "Straight-line rusher" |
| Low thrust, high turn | "Stationary spinner" |
| Low thrust, low turn, high shoot | "Camper sniper" |
| High all actions | "Hyperactive" |
| High idle | "Passive/cautious" |

---

## 7. Priority 4: Genetic Operator Statistics

### 7.1 Rationale

Understanding how genetic operators are affecting the population helps tune hyperparameters. Are crossovers producing better offspring? Are mutations helping or hurting?

### 7.2 Proposed Operator Schema

```json
{
  "generation": 25,

  "operator_stats": {
    "crossovers_performed": 45,
    "mutations_performed": 90,
    "elites_preserved": 20,

    "offspring_fitness_avg": 598.4,
    "offspring_fitness_vs_parents": -42.3,

    "mutation_impact": {
      "improved_count": 34,
      "degraded_count": 41,
      "neutral_count": 15,
      "avg_fitness_delta": -8.2
    },

    "crossover_impact": {
      "better_than_both_parents": 12,
      "between_parents": 28,
      "worse_than_both_parents": 5,
      "avg_fitness_vs_better_parent": -15.4
    }
  }
}
```

### 7.3 Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `crossovers_performed` | int | Number of crossover operations |
| `mutations_performed` | int | Number of mutation operations |
| `elites_preserved` | int | Number of elite individuals copied unchanged |
| `offspring_fitness_avg` | float | Average fitness of newly created individuals |
| `offspring_fitness_vs_parents` | float | Offspring avg - parent avg |
| `mutation_impact.*` | various | How mutations affected fitness |
| `crossover_impact.*` | various | How crossovers affected fitness |

### 7.4 Implementation Complexity

This requires tracking parent-offspring relationships during evolution, which adds complexity.

**Simplified Alternative**: Track only counts (crossovers, mutations, elites) without fitness impact analysis. This is much simpler and still useful.

```json
{
  "operator_stats": {
    "crossovers_performed": 45,
    "mutations_performed": 90,
    "elites_preserved": 20,
    "new_individuals": 80
  }
}
```

### 7.5 Recommendation

Start with simplified tracking. Add impact analysis later if needed.

---

## 8. Priority 5: Computational Metadata

### 8.1 Rationale

Understanding computational performance helps:
- Identify bottlenecks
- Plan training schedules
- Compare hardware configurations

### 8.2 Proposed Metadata Schema

```json
{
  "generation": 25,

  "timing": {
    "generation_start": "2026-01-06T01:05:12.123456",
    "generation_end": "2026-01-06T01:05:43.789012",
    "generation_duration_seconds": 31.67,
    "evaluation_duration_seconds": 28.45,
    "evolution_duration_seconds": 0.12,
    "display_duration_seconds": 3.10
  },

  "computation": {
    "parallel_workers_used": 16,
    "evaluations_performed": 300,
    "evaluations_per_second": 10.54
  }
}
```

### 8.3 Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `generation_start` | ISO datetime | When generation started |
| `generation_end` | ISO datetime | When generation ended |
| `generation_duration_seconds` | float | Total wall-clock time |
| `evaluation_duration_seconds` | float | Time spent in parallel evaluation |
| `evolution_duration_seconds` | float | Time spent in selection/crossover/mutation |
| `display_duration_seconds` | float | Time spent displaying best agent |
| `parallel_workers_used` | int | Number of threads used |
| `evaluations_performed` | int | Total evaluations (pop_size × seeds_per_agent) |
| `evaluations_per_second` | float | Throughput metric |

### 8.4 Implementation Approach

Add timestamp captures at phase transitions in `ParallelGATrainingDriver.update()`.

---

## 9. Priority 6: Advanced Tracking

These are lower-priority additions that provide specialized insights.

### 9.1 Seed Information

```json
{
  "seeds": {
    "generation_base_seed": 1234567890,
    "seeds_per_agent": 3,
    "fresh_game_seed": null
  }
}
```

**Purpose**: Enables reproducibility and seed difficulty analysis.

### 9.2 Kill Timing Bins

```json
{
  "kill_timing": {
    "early_kills_pct": 0.25,
    "mid_kills_pct": 0.45,
    "late_kills_pct": 0.30
  }
}
```

**Purpose**: Reveals whether agents kill early then die, or build up over time.

**Implementation**: Requires tracking kill timestamps during episodes, moderate complexity.

### 9.3 Best Agent Lineage

```json
{
  "best_agent_lineage": {
    "parent1_fitness": 1456.2,
    "parent2_fitness": 1289.7,
    "was_elite": false,
    "mutation_applied": true,
    "generations_in_lineage": 12
  }
}
```

**Purpose**: Understand how the best agent was created.

**Implementation**: Requires tracking genealogy through evolution, high complexity.

### 9.4 Position Heatmap Data

```json
{
  "position_data": {
    "center_time_pct": 0.65,
    "edge_time_pct": 0.20,
    "corner_time_pct": 0.15,
    "avg_distance_from_center": 142.5
  }
}
```

**Purpose**: Detect camping vs roaming behavior.

**Implementation**: Requires position sampling during episodes, moderate complexity.

### 9.5 Recommendation

Defer P6 items until P1-P5 are implemented and proven useful.

---

## 10. Schema Migration Strategy

### 10.1 Backward Compatibility

New fields should be **additive only**. Never remove or rename existing fields. This ensures:
- Old analysis scripts continue to work
- Historical data remains valid
- No migration scripts needed

### 10.2 Optional Fields

New fields should be treated as optional by analysis code:
```python
fresh_fitness = gen_data.get('fresh_game', {}).get('fitness', None)
if fresh_fitness is not None:
    # analyze fresh game data
```

### 10.3 Version Tracking

Add schema version to enable future migrations:

```json
{
  "schema_version": "2.0",
  "config": { ... }
}
```

Version history:
- 1.0: Original schema
- 2.0: Added fresh_game, distributions, action_metrics, operator_stats, timing

---

## 11. Storage Impact Analysis

### 11.1 Current Storage

Per generation (current): ~2 KB
500 generations: ~1 MB

### 11.2 Projected Storage with Expansions

| Addition | Per Generation | 500 Generations |
|----------|---------------|-----------------|
| Fresh game data | ~1 KB | ~0.5 MB |
| Distribution arrays | ~4 KB | ~2 MB |
| Action metrics | ~0.5 KB | ~0.25 MB |
| Operator stats | ~0.5 KB | ~0.25 MB |
| Timing metadata | ~0.3 KB | ~0.15 MB |
| **Total New** | ~6.3 KB | ~3.15 MB |
| **Total (Old + New)** | ~8.3 KB | ~4.15 MB |

### 11.3 Assessment

A 4x increase in file size (1 MB → 4 MB) is completely acceptable. Modern systems handle this trivially. **Storage is not a concern.**

---

## 12. Implementation Roadmap

### 12.1 Phase 1: Fresh Game Tracking (Critical)

**Effort**: Low-Medium
**Files Modified**:
- `training/train_ga_parallel.py` - Capture fresh game metrics
- `training/analytics.py` - Store and report fresh game data

**Steps**:
1. Add fresh game metrics collection after display phase
2. Compute generalization metrics
3. Add to generation data structure
4. Add to summary aggregations
5. Update markdown report generation

### 12.2 Phase 2: Distribution Data

**Effort**: Low
**Files Modified**:
- `training/parallel_evaluator.py` - Return per-agent metrics
- `training/analytics.py` - Store distribution arrays

**Steps**:
1. Modify `evaluate_population_parallel()` to return per-agent data
2. Store arrays in generation data
3. Compute distribution statistics
4. Update report generation

### 12.3 Phase 3: Action Metrics

**Effort**: Medium
**Files Modified**:
- `training/parallel_evaluator.py` - Track actions during evaluation
- `training/analytics.py` - Store and aggregate action data

**Steps**:
1. Add action counters to `evaluate_single_agent()`
2. Return action data with other metrics
3. Aggregate across population
4. Update report generation

### 12.4 Phase 4: Operator Stats & Timing

**Effort**: Low
**Files Modified**:
- `training/train_ga_parallel.py` - Track timing and operator counts

**Steps**:
1. Add timestamps at phase transitions
2. Count operator applications in `_evolve_generation()`
3. Store in generation data

### 12.5 Testing Strategy

For each phase:
1. Run short training (10 generations)
2. Verify JSON schema is correct
3. Verify no performance regression
4. Verify markdown report includes new data
5. Test with interrupted training (Ctrl+C)

---

## Appendix A: Complete Proposed Schema

```json
{
  "schema_version": "2.0",

  "config": {
    "population_size": 100,
    "num_generations": 500,
    "mutation_probability": 0.2,
    "mutation_gaussian_sigma": 0.15,
    "crossover_probability": 0.7,
    "max_workers": 16,
    "frame_delay": 0.016666666666666666,
    "seeds_per_agent": 3,
    "max_steps": 1500,
    "hidden_size": 24
  },

  "start_time": "2026-01-06T00:54:36.126852",
  "end_time": "2026-01-06T01:07:21.788360",

  "summary": {
    "total_generations": 500,
    "training_duration": "2:45:33",
    "final_best_fitness": 2450.67,
    "all_time_best_fitness": 2450.67,
    "final_avg_fitness": 892.34,
    "final_min_fitness": 125.67,
    "avg_improvement_early_to_late": 567.89,
    "best_generation": 487,
    "worst_generation": 2,
    "final_stagnation": 3,
    "final_avg_kills": 18.45,
    "final_avg_steps": 623,
    "final_avg_accuracy": 0.823,
    "max_kills_ever": 52,
    "max_steps_ever": 1500,

    "avg_generalization_ratio": 0.78,
    "best_fresh_fitness": 2180.45,
    "best_fresh_generation": 487,
    "worst_generalization_ratio": 0.42,
    "avg_fresh_kills": 15.67,
    "fresh_episode_completion_rate": 0.18
  },

  "generations": [
    {
      "generation": 1,

      "best_fitness": 612.06,
      "avg_fitness": 15.95,
      "min_fitness": -180.44,
      "median_fitness": 2.58,
      "std_dev": 102.96,
      "population_size": 100,
      "p25_fitness": -37.61,
      "p75_fitness": 37.40,
      "p90_fitness": 170.09,
      "best_improvement": 0.0,
      "avg_improvement": 0.0,
      "all_time_best": 612.06,
      "generations_since_improvement": 0,

      "avg_kills": 3.21,
      "avg_steps": 263.14,
      "avg_accuracy": 0.355,
      "avg_shots": 9.44,
      "total_kills": 321.0,
      "max_kills": 23.67,
      "max_steps": 768.67,

      "best_agent_kills": 19.33,
      "best_agent_steps": 639.67,
      "best_agent_accuracy": 0.959,
      "best_agent_shots": 20.17,

      "avg_reward_breakdown": {
        "KillAsteroid": 80.25,
        "SurvivalBonus": 4.39,
        "ConservingAmmoBonus": -83.13,
        "MaintainingMomentumBonus": -9.10,
        "NearMiss": 23.05,
        "SpacingFromWallsBonus": -0.64,
        "MovingTowardDangerBonus": 1.15
      },

      "fresh_game": {
        "fitness": 425.67,
        "kills": 12,
        "steps_survived": 534,
        "shots_fired": 18,
        "accuracy": 0.667,
        "time_alive_seconds": 8.9,
        "cause_of_death": "asteroid_collision",
        "completed_full_episode": false,
        "reward_breakdown": {
          "KillAsteroid": 300.0,
          "ConservingAmmoBonus": 120.0,
          "SurvivalBonus": 8.9,
          "MaintainingMomentumBonus": -12.5,
          "NearMiss": 45.0,
          "SpacingFromWallsBonus": -0.23,
          "MovingTowardDangerBonus": 0.5
        }
      },

      "generalization_metrics": {
        "fitness_ratio": 0.695,
        "kills_ratio": 0.621,
        "steps_ratio": 0.835,
        "accuracy_delta": -0.292,
        "generalization_grade": "C"
      },

      "distributions": {
        "fitness_values": [-180.44, -150.23, ..., 612.06],
        "kills_values": [0, 1, 2, ..., 23.67],
        "steps_values": [45, 89, 123, ..., 768.67],
        "accuracy_values": [0.0, 0.12, 0.23, ..., 0.96],
        "shots_values": [2, 5, 8, ..., 34]
      },

      "distribution_stats": {
        "fitness_skewness": 1.23,
        "fitness_kurtosis": 4.56,
        "viable_agent_count": 58,
        "failed_agent_count": 42
      },

      "action_metrics": {
        "avg_thrust_frequency": 0.15,
        "avg_turn_frequency": 0.38,
        "avg_shoot_frequency": 0.12,
        "avg_idle_frequency": 0.35,
        "best_agent_action_counts": {
          "thrust": 156,
          "turn_left": 234,
          "turn_right": 212,
          "shoot": 20,
          "idle": 178
        }
      },

      "operator_stats": {
        "crossovers_performed": 45,
        "mutations_performed": 80,
        "elites_preserved": 20
      },

      "timing": {
        "generation_duration_seconds": 32.45,
        "evaluation_duration_seconds": 28.12,
        "evolution_duration_seconds": 0.08,
        "display_duration_seconds": 4.25
      },

      "seeds": {
        "generation_base_seed": 1234567890
      }
    }
  ]
}
```

---

## Appendix B: Summary-Level Fresh Game Additions

The `summary` object should include these fresh game aggregations:

| Field | Description |
|-------|-------------|
| `avg_generalization_ratio` | Mean fitness_ratio across all generations |
| `best_fresh_fitness` | Highest fresh game fitness achieved |
| `best_fresh_generation` | Generation that achieved best fresh fitness |
| `worst_generalization_ratio` | Lowest fitness_ratio (worst generalization) |
| `worst_generalization_generation` | Generation with worst generalization |
| `avg_fresh_kills` | Mean kills in fresh games |
| `avg_fresh_steps` | Mean survival in fresh games |
| `fresh_episode_completion_rate` | Fraction of fresh games where agent survived full episode |
| `generalization_trend` | "improving", "stable", or "declining" |

---

## Appendix C: Relationship to Analytics Enhancement Proposal

This document (Training Data Schema Expansion) should be implemented **before** the Analytics Enhancement Proposal. The analytics enhancements depend on the data tracked here:

| Analytics Enhancement | Required Data |
|-----------------------|---------------|
| Decile Breakdown | All existing + fresh_game |
| Reward Evolution | avg_reward_breakdown (exists) |
| Kill Efficiency | avg_kills, avg_shots, avg_steps (exists) |
| Behavioral Classification | action_metrics (new) |
| Population Health | distributions (new) |
| Stagnation Analysis | Existing data sufficient |
| Best Agent Profile | fresh_game (new), distributions (new) |
| Learning Velocity | Existing data sufficient |
| Milestone Timeline | Existing data sufficient |
| Survival Distribution | distributions.steps_values (new) |
| Correlation Matrix | distributions (new) |
| Generation Highlights | Existing data sufficient |
| Reward Warnings | avg_reward_breakdown (exists) |
| Action Estimates | action_metrics (new) |
| Sparklines | Existing data sufficient |

---

*End of Document*
