# Historical Notes & Design Decisions

## Introduction

This document archives the key historical context, bugfixes, and design decisions that have shaped the Asteroids AI project. It is intended to provide background for new developers and to preserve the reasoning behind major architectural shifts.

---

## Part 1: The Genetic Algorithm's Implementation Journey

The initial Genetic Algorithm (GA) implementation was non-functional due to a series of critical bugs. Fixing these was the turning point that enabled meaningful learning.

### 1.1. Critical GA Bugfixes (January 2026)

A summary of the four catastrophic bugs that were fixed:

1.  **Wrong-Sized Mutation**: The mutation operator was returning a vector with fewer genes than the original, catastrophically breaking the population's structure each generation. The fix ensured the mutated vector always has the same dimensionality as the parent.
2.  **Incomplete Crossover**: The crossover operator was only returning one child instead of two, halving the genetic diversity from crossover events. The fix was to correctly generate and return both offspring.
3.  **State Dimensionality Mismatch**: The population was initialized with parameter vectors that were too small to represent a complete policy (`state_size` instead of `state_size * action_size`), meaning agents could never learn a full set of behaviors. This was corrected to initialize individuals with the proper number of parameters for the policy network.
4.  **Random Tournament Selection**: The selection operator was choosing parents randomly, providing zero selection pressure and making the GA equivalent to a random search. This was replaced with a proper tournament selection implementation that correctly identifies and selects the fittest individuals for reproduction.

These fixes transformed the GA from a random search into a functional evolutionary algorithm, after which genuine fitness improvements began to be observed.

### 1.2. Policy Architecture Research: From Linear to Neural Network

The original plan was to use a simple linear policy. However, research and initial experiments revealed its limitations.

- **Observed Behavior with Linear Policy**: Agents adopted a "sit and shoot in one direction" strategy. They would not aim, dodge, or react.
- **Root Cause**: A linear policy can only learn simple, direct relationships between state and action (e.g., "if asteroid is to the right, turn right"). It cannot learn complex, conditional logic (e.g., "**if** an asteroid is close **and** moving towards me, **then** dodge"). The optimal strategy for a linear agent was to find a fixed firing direction that maximized the chance of a lucky hit.
- **The Solution: Non-Linearity**: To enable more sophisticated behaviors, a **feedforward neural network** was chosen as the policy architecture. The hidden layers of a neural network allow it to learn "hidden concepts" and complex, non-linear combinations of its inputs. It can learn to represent concepts like "danger level" or "optimal firing solution" as an intermediate step.
- **Current Architecture**: The GA now evolves the weights and biases of a `NeuralNetworkGAAgent` with a `tanh` hidden layer. This allows for the emergence of advanced behaviors like aiming and dodging, which were impossible with a linear policy.

---

## Part 2: Training & Evaluation Architecture

To accelerate the training process, the project moved from a sequential evaluation model to a parallel one.

- **Original Method**: Each agent in the population was evaluated one-by-one in the visual game window. This was slow, taking several minutes per generation.
- **Current Method (`train_ga_parallel.py`)**:
  - **Headless Evaluation**: The entire population is evaluated simultaneously using a `ThreadPoolExecutor`. Each agent runs in a separate, fast, non-visual `HeadlessAsteroidsGame` instance. This provides a massive speedup (e.g., from 10 minutes per generation to ~30 seconds).
  - **Visual Generalization Test**: After the headless evaluation, only the single best agent from the generation is displayed in the main visual game window. Critically, this visual run uses a **fresh, random seed**, serving as a test of the agent's ability to generalize its skills to a new, unseen scenario.

---

## Part 3: Game & Reward Balancing

Early in development, agent behavior was poor due to imbalanced game physics and reward signals. Several key changes were made to encourage more intelligent play.

### 3.1. Physics Adjustments

- **Problem**: The player ship was too fast, accelerating and turning at a rate that made precise control difficult for an evolving agent. The fire rate was also high, encouraging "spray-and-pray" tactics.
- **Solution**:
  - Ship acceleration and rotation speed were reduced by ~40-50%.
  - The weapon's shoot cooldown was more than doubled, effectively halving the fire rate.
- **Impact**: These changes made gameplay more realistic and forced the agent to be more deliberate with its actions. Precise aiming became more important than overwhelming the screen with bullets.

### 3.2. Reward System Tuning

- **Problem**: Initial reward values were scaled for very short episodes. With longer episodes, time-based bonuses (e.g., `AccuracyBonus`) would balloon into the tens of thousands, dwarfing the reward for actually killing an asteroid. Agents learned to play passively and rack up time-based rewards rather than engaging with the primary objective.
- **Solution**: The reward structure was re-scaled for longer episodes, with a clear philosophy:
  1.  **Kills are the primary objective**: `KillAsteroid` reward was doubled to **100 points**.
  2.  **Behavioral shaping should guide, not dominate**: Time-based bonuses for accuracy and facing asteroids were drastically reduced (e.g., from 15 points/sec to **2 points/sec**).
  3.  **Penalties for inefficient play**: A `ShootingPenalty` was introduced to apply a small negative score for every shot fired, making "spray-and-pray" a costly, losing strategy.
- **Impact**: This rebalancing made killing asteroids the most profitable action, correctly incentivizing agents to be aggressive and efficient. Fitness scores became more interpretable, with a score of 1000 now clearly mapping to ~10 kills plus some behavioral bonuses.

---

## Part 4: Future Research & Design Decisions

This section contains analysis of more advanced concepts that have been considered for the project.

### 4.1. Research Note: Introspective Learning

- **Concept**: "Introspective" or "reward-aware" learning involves adding performance metrics (e.g., current accuracy, cumulative reward) to the agent's state vector. The theory is that the agent could learn to reason about its own performance and adjust its strategy accordingly (e.g., "my accuracy is low, I should shoot less").
- **Analysis**: This approach is common in Reinforcement Learning (RL), where agents can update their policy mid-episode. However, it is rare and often ineffective in standard Genetic Algorithms. Our GA agents use a fixed policy (their neural network weights) for the entire duration of an episode. They cannot change their behavior mid-episode based on a poor reward signal. The evolutionary "learning" only happens between generations.
- **Conclusion & Decision**: The complexity and potential for learning spurious correlations (e.g., confusing the cause and effect of a high reward) outweigh the potential benefits for our current GA implementation. Direct, immediate behavioral shaping rewards (e.g., `FacingAsteroidBonus`) are a more effective and straightforward way to guide learning. This idea has been **deferred** unless a more advanced, online-learning agent architecture (like RL or a recurrent network) is introduced.
