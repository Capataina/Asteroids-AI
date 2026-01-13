# Training Architecture Refactor: Current State & Planned Restructure

## 1. Introduction

This document outlines a refactoring plan for the AsteroidsAI training infrastructure. The goal is to transform the current monolithic, tightly-coupled code into a **modular, well-organized structure** with clear separation of concerns.

**This plan covers refactoring only.** No new training methods (ES, NEAT, RL) will be added as part of this effort. The refactored structure will make adding those methods easier in the future, but that is a separate effort.

### 1.1. Guiding Philosophy

The architecture follows a clear separation of concerns:

| Folder           | Responsibility                                                  | Contains                                            |
| :--------------- | :-------------------------------------------------------------- | :-------------------------------------------------- |
| **`ai_agents/`** | **What the agent IS** - the brain, decision-making logic        | Network architectures, agent wrappers               |
| **`training/`**  | **How we train** - population management, evaluation, evolution | Genetic operators, selection, evaluation, analytics |

This distinction matters because:

- **The agent is a static neural network.** It doesn't know it's being evolved.
- **Mutation, crossover, and selection are training mechanisms.** They are external pressures applied at the population level - they belong in `training/`, not `ai_agents/`.

### 1.2. Refactoring Goals

1. **Eliminate duplication** - Reward configuration should exist in exactly one place
2. **Correct misplaced code** - Move genetic operators from `ai_agents/` to `training/`
3. **Break up monolithic files** - `train_ga_parallel.py` (777 lines) should be split into focused modules
4. **Remove dead code** - Delete broken/unused files
5. **Establish clear boundaries** - Each folder has a single, well-defined purpose

---

## 2. Current System Analysis

### 2.1. Training Folder Structure

| File                    | Lines | Purpose                               | Status      | Issues                                             |
| :---------------------- | :---- | :------------------------------------ | :---------- | :------------------------------------------------- |
| `train_ga.py`           | 593   | Visual GA training (single-threaded)  | Active      | Different reward config than parallel version      |
| `train_ga_parallel.py`  | 777   | Parallel GA training (multi-threaded) | **Primary** | Monolithic - contains everything in one file       |
| `parallel_evaluator.py` | 478   | Parallel agent evaluation             | Active      | Duplicates reward config from train_ga_parallel.py |
| `base/BaseAgent.py`     | 32    | Abstract agent interface              | Active      | Well-designed                                      |
| `base/EpisodeRunner.py` | 131   | Episode execution harness             | Active      | Well-designed                                      |
| `base/EpisodeResult.py` | 19    | Episode result data class             | Active      | Well-designed                                      |

### 2.2. AI Agents Folder Structure

| File                               | Lines | Purpose                    | Status            | Issues                                               |
| :--------------------------------- | :---- | :------------------------- | :---------------- | :--------------------------------------------------- |
| `genetic_algorithm/ga_agent.py`    | 81    | Linear policy agent        | Superseded        | Works, but linear policies are too limited           |
| `genetic_algorithm/nn_ga_agent.py` | 158   | Neural network agent       | **Primary**       | Well-designed, but mixes network + agent logic       |
| `genetic_algorithm/operators.py`   | 108   | Crossover & mutation       | Active            | **Wrong location** - training logic, not agent logic |
| `genetic_algorithm/ga_trainer.py`  | 119   | GA trainer orchestrator    | **Broken**        | Has bugs, logic duplicated in train_ga_parallel.py   |
| `genetic_algorithm/ga_fitness.py`  | 27    | Fitness evaluation wrapper | **Broken**        | References undefined attributes                      |
| `reinforcement_learning/*.py`      | 0-203 | RL stubs                   | **Empty/Partial** | Placeholder files with no implementation             |

### 2.3. Critical Issues

#### Issue 1: Misplaced Responsibilities

Genetic operators (`operators.py`) currently live in `ai_agents/`. But these are **training mechanisms**, not part of the agent's brain. An agent doesn't mutate itself - evolution is applied externally by the training loop.

**Current (wrong):**

```
ai_agents/neuroevolution/genetic_algorithm/
├── nn_ga_agent.py    # The agent (correct)
└── operators.py      # Training logic (WRONG LOCATION)
```

**Should be:**

```
ai_agents/neuroevolution/
└── nn_agent.py       # The agent

training/methods/genetic_algorithm/
└── operators.py      # Training logic (CORRECT)
```

#### Issue 2: Reward Configuration Duplication

The reward calculator is configured **twice** with identical components:

- `train_ga_parallel.py` lines 650-702
- `parallel_evaluator.py` lines 67-96

If one is modified without the other, training and evaluation use different reward functions, causing silent bugs.

#### Issue 3: Monolithic Training Driver

`train_ga_parallel.py` at 777 lines contains:

- Population initialization
- Parallel evaluation orchestration
- Visual display logic
- Evolution logic (crossover, mutation, selection)
- Analytics integration
- Adaptive mutation
- Best agent tracking
- Game window management

This should be split into focused modules.

#### Issue 5: Hardcoded Hyperparameters

Training hyperparameters are scattered and hardcoded throughout `train_ga_parallel.py`:

```python
# train_ga_parallel.py - hardcoded values buried in code
population_size=25,
num_generations=500,
mutation_probability=0.05,
crossover_probability=0.7,
mutation_gaussian_sigma=0.1,
seeds_per_agent=20,
max_steps=1500,
```

These should be centralized in a config file for easy experimentation.

#### Issue 4: Dead and Broken Code

| File                              | Status     | Issue                                                                            |
| :-------------------------------- | :--------- | :------------------------------------------------------------------------------- |
| `ga_fitness.py`                   | **Broken** | References `self.state_encoder` which is never defined                           |
| `ga_trainer.py`                   | **Broken** | `evaluate_individual()` passes raw vector to `run_episode()` which expects Agent |
| `gnn.py`, `policies.py`, `sac.py` | **Empty**  | 0 lines each - just placeholder files                                            |

---

## 3. Proposed Architecture

### 3.1. New Folder Structure

```
ai_agents/
├── __init__.py
├── base_agent.py                    # Abstract interface (moved from training/base/)
│
├── policies/                        # Network architectures
│   ├── __init__.py
│   ├── feedforward.py               # MLP: input → hidden → output (extracted from nn_ga_agent.py)
│   └── linear.py                    # Linear: input → output (from ga_agent.py, kept for reference)
│
└── neuroevolution/                  # Neuroevolution agents
    ├── __init__.py
    └── nn_agent.py                  # Wraps a policy, implements BaseAgent

training/
├── __init__.py
│
├── config/                          # Centralized configuration
│   ├── __init__.py
│   ├── rewards.py                   # Single source of truth for reward configs
│   └── genetic_algorithm.py         # GA hyperparameters (population, mutation, etc.)
│
├── core/                            # Shared infrastructure
│   ├── __init__.py
│   ├── episode_runner.py            # Runs single episode (from base/)
│   ├── episode_result.py            # Episode data container (from base/)
│   ├── population_evaluator.py      # Parallel evaluation logic (extracted)
│   └── display_manager.py           # Visual display logic (extracted)
│
├── methods/                         # Training method implementations
│   ├── __init__.py
│   └── genetic_algorithm/
│       ├── __init__.py
│       ├── driver.py                # GA training loop (extracted from train_ga_parallel.py)
│       ├── operators.py             # Crossover, mutation (MOVED from ai_agents/)
│       └── selection.py             # Tournament selection, elitism (extracted)
│
├── analytics/                       # UNCHANGED (already well-structured)
│   └── ... (existing modular structure)
│
└── scripts/                         # Entry points
    └── train_ga.py                  # Main entry point (thin wrapper)
```

### 3.2. Key Changes Explained

#### Moving `operators.py` to `training/`

```python
# BEFORE: ai_agents/neuroevolution/genetic_algorithm/operators.py
# This is TRAINING logic, not agent logic!

def mutate_gaussian(individual, config):
    """Mutate an individual's genes."""  # Training operation
    ...

def crossover_blend(parent1, parent2):
    """Create offspring from two parents."""  # Training operation
    ...
```

```python
# AFTER: training/methods/genetic_algorithm/operators.py
# Now correctly located with other training logic
```

#### Separating Network from Agent

```python
# BEFORE: ai_agents/.../nn_ga_agent.py (158 lines)
# Mixes network architecture with agent interface

class NeuralNetworkGAAgent:
    def __init__(self, weights, ...):
        # Network setup
        self.W1 = ...
        self.b1 = ...
        # Agent setup
        self.state_encoder = ...
```

```python
# AFTER: Split into two focused files

# ai_agents/policies/feedforward.py (~60 lines)
class FeedforwardPolicy:
    """Just the network - weights, forward pass, activation."""
    def __init__(self, weights, input_size, hidden_size, output_size):
        self.W1, self.b1, self.W2, self.b2 = self._unpack(weights)

    def forward(self, x):
        hidden = np.tanh(x @ self.W1 + self.b1)
        return sigmoid(hidden @ self.W2 + self.b2)

# ai_agents/neuroevolution/nn_agent.py (~40 lines)
class NNAgent(BaseAgent):
    """Wraps a policy to implement the agent interface."""
    def __init__(self, weights, policy_class, config):
        self.policy = policy_class(weights, ...)

    def get_action(self, state):
        return self.policy.forward(state)
```

#### Centralizing Reward Configuration

```python
# BEFORE: Duplicated in two files
# train_ga_parallel.py:650-702
# parallel_evaluator.py:67-96

# AFTER: training/config/rewards.py (single source of truth)
REWARD_PRESETS = {
    "default": [
        (VelocitySurvivalBonus, {"reward_multiplier": 3.0, "max_velocity_cap": 15.0}),
        (DistanceBasedKillReward, {"max_reward_per_kill": 15.0, ...}),
        (ConservingAmmoBonus, {"hit_bonus": 12.0, "shot_penalty": -5.0}),
        (ExplorationBonus, {"grid_rows": 3, "grid_cols": 4, "bonus_per_cell": 10.0}),
        (DeathPenalty, {"penalty": -150.0}),
    ]
}

def create_reward_calculator(preset="default"):
    calc = ComposableRewardCalculator()
    for component_class, kwargs in REWARD_PRESETS[preset]:
        calc.add_component(component_class(**kwargs))
    return calc
```

#### Centralizing Hyperparameters

```python
# BEFORE: Hardcoded constants scattered in train_ga_parallel.py
# population_size=25,
# mutation_probability=0.05,
# seeds_per_agent=20

# AFTER: training/config/genetic_algorithm.py
class GAConfig:
    POPULATION_SIZE = 25
    NUM_GENERATIONS = 500
    MUTATION_RATE = 0.05
    SEEDS_PER_AGENT = 20
    # ...
```

---

## 4. Migration Path

### Phase 1: Centralize Configuration (Rewards & Hyperparameters)

| Step | Task                                                               | Files Affected |
| :--- | :----------------------------------------------------------------- | :------------- |
| 1.1  | Create `training/config/` folder                                   | New folder     |
| 1.2  | Create `training/config/rewards.py` with current reward setup      | New file       |
| 1.3  | Create `training/config/genetic_algorithm.py` with GA params       | New file       |
| 1.4  | Update `train_ga_parallel.py` to import from both config files     | Modify         |
| 1.5  | Update `parallel_evaluator.py` to import from `config/rewards.py`  | Modify         |
| 1.6  | Verify training still works identically                            | Test           |

**Outcome:** Configuration centralized. Single source of truth for rewards and hyperparameters.

### Phase 2: Restructure Core Infrastructure

| Step | Task                                                             | Files Affected |
| :--- | :--------------------------------------------------------------- | :------------- |
| 2.1  | Create `training/core/` folder                                   | New folder     |
| 2.2  | Move `base/episode_runner.py` to `core/`                         | Move           |
| 2.3  | Move `base/episode_result.py` to `core/`                         | Move           |
| 2.4  | Extract `PopulationEvaluator` class from `parallel_evaluator.py` | Extract        |
| 2.5  | Extract display logic to `core/display_manager.py`               | Extract        |
| 2.6  | Update imports across codebase                                   | Modify         |
| 2.7  | Delete empty `base/` folder                                      | Delete         |

**Outcome:** Core infrastructure is modular and reusable.

### Phase 3: Restructure Agent Code

| Step | Task                                                                            | Files Affected |
| :--- | :------------------------------------------------------------------------------ | :------------- |
| 3.1  | Create `ai_agents/policies/` folder                                             | New folder     |
| 3.2  | Extract network architecture from `nn_ga_agent.py` to `policies/feedforward.py` | Extract        |
| 3.3  | Move `ga_agent.py` to `policies/linear.py`                                      | Move & rename  |
| 3.4  | Create `ai_agents/neuroevolution/nn_agent.py` (thin wrapper)                    | New file       |
| 3.5  | Move `BaseAgent` from `training/base/` to `ai_agents/base_agent.py`             | Move           |
| 3.6  | Update imports across codebase                                                  | Modify         |

**Outcome:** Network architectures are decoupled from agent interface.

### Phase 4: Modularize GA Training

| Step | Task                                                                               | Files Affected |
| :--- | :--------------------------------------------------------------------------------- | :------------- |
| 4.1  | Create `training/methods/genetic_algorithm/` folder                                | New folder     |
| 4.2  | **Move** `operators.py` from `ai_agents/` to `training/methods/genetic_algorithm/` | Move           |
| 4.3  | Extract selection logic to `selection.py`                                          | Extract        |
| 4.4  | Extract GA driver logic to `driver.py`                                             | Extract        |
| 4.5  | Refactor `train_ga_parallel.py` to use extracted modules                           | Modify         |
| 4.6  | Verify GA training still works identically                                         | Test           |

**Outcome:** GA training logic is modular and focused.

### Phase 5: Cleanup

| Step | Task                                                          | Files Affected |
| :--- | :------------------------------------------------------------ | :------------- |
| 5.1  | Delete `ga_fitness.py` (broken, unused)                       | Delete         |
| 5.2  | Delete `ga_trainer.py` (broken, superseded)                   | Delete         |
| 5.3  | Delete empty RL stubs (`gnn.py`, `policies.py`, `sac.py`)     | Delete         |
| 5.4  | Delete `env_wrapper.py` (partial, unused)                     | Delete         |
| 5.5  | Create `training/scripts/` folder for entry points            | New folder     |
| 5.6  | Move/refactor `train_ga_parallel.py` to `scripts/train_ga.py` | Move           |
| 5.7  | Update all documentation                                      | Docs           |

**Outcome:** Clean codebase with no dead code.

---

## 5. File Size Targets

| File                                     | Current Lines | Target Lines                 | Change    |
| :--------------------------------------- | :------------ | :--------------------------- | :-------- |
| `train_ga_parallel.py`                   | 777           | ~100 (entry point only)      | -87%      |
| `parallel_evaluator.py`                  | 478           | ~200 (focused on evaluation) | -58%      |
| `nn_ga_agent.py`                         | 158           | ~40 (just wraps policy)      | -75%      |
| `methods/genetic_algorithm/driver.py`    | N/A           | ~150                         | New       |
| `methods/genetic_algorithm/operators.py` | 108           | ~108                         | Moved     |
| `methods/genetic_algorithm/selection.py` | N/A           | ~50                          | New       |
| `core/population_evaluator.py`           | N/A           | ~200                         | Extracted |
| `core/display_manager.py`                | N/A           | ~100                         | Extracted |
| config/rewards.py                      | N/A           | ~80                          | New       |
| config/genetic_algorithm.py            | N/A           | ~30                          | New       |
| `policies/feedforward.py`                | N/A           | ~60                          | Extracted |

**Total: From ~1,500 lines in 3 large files to ~1,100 lines across 10 focused files.**

---

## 6. What This Enables (Future Work)

Once refactored, the codebase will be ready for:

1. **Adding Evolution Strategies** - Create `training/methods/evolution_strategies/driver.py`, reuse everything else
2. **Adding NEAT** - Create `training/methods/neat/driver.py` + `ai_agents/neuroevolution/neat_agent.py`
3. **Adding RL** - Create `ai_agents/reinforcement_learning/sac/` with internal learning
4. **Experimenting with rewards** - Add presets to `config/rewards.py`, switch via config
5. **New network architectures** - Add to `ai_agents/policies/`, usable by any training method

**But those are separate efforts, not part of this refactor.**

---

## 7. Success Criteria

The refactor is complete when:

1. **Clear separation:** `ai_agents/` contains only agent/network logic; `training/` contains only training logic
2. **Zero duplication:** Reward config exists in exactly one place
3. **No dead code:** All broken/unused files are deleted
4. **Modularity:** No file exceeds ~200 lines; each has single responsibility
5. **Backward compatibility:** Training still works identically after refactor
6. **All tests pass:** (if tests exist)

---

## 8. Appendix: Before vs After

### Before (Current)

```
ai_agents/neuroevolution/genetic_algorithm/
├── ga_agent.py          (81 lines - works but superseded)
├── nn_ga_agent.py       (158 lines - agent + network combined)
├── operators.py         (108 lines - WRONG LOCATION)
├── ga_trainer.py        (119 lines - broken)
└── ga_fitness.py        (27 lines - broken)

ai_agents/reinforcement_learning/
├── env_wrapper.py       (203 lines - partial, unused)
├── gnn.py               (0 lines - empty)
├── policies.py          (0 lines - empty)
└── sac.py               (0 lines - empty)

training/
├── train_ga.py          (593 lines)
├── train_ga_parallel.py (777 lines - monolithic)
├── parallel_evaluator.py (478 lines - duplicates rewards)
└── base/                (3 files - fine)
```

**Problems:** Duplication, wrong locations, dead code, monolithic files.

### After (Proposed)

```
ai_agents/
├── base_agent.py        (30 lines)
├── policies/
│   ├── feedforward.py   (60 lines)
│   └── linear.py        (40 lines)
└── neuroevolution/
    └── nn_agent.py      (40 lines)

training/
├── config/
│   └── rewards.py       (80 lines - SINGLE SOURCE OF TRUTH)
├── core/
│   ├── episode_runner.py (130 lines)
│   ├── episode_result.py (20 lines)
│   ├── population_evaluator.py (200 lines)
│   └── display_manager.py (100 lines)
├── methods/genetic_algorithm/
│   ├── driver.py        (150 lines)
│   ├── operators.py     (108 lines - CORRECT LOCATION)
│   └── selection.py     (50 lines)
├── analytics/           (unchanged)
└── scripts/
    └── train_ga.py      (100 lines - entry point)
```

**Result:** Clear structure, no duplication, no dead code, focused modules.
