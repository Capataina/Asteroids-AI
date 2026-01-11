# Asteroids AI: Consolidated Implementation Plan

## Introduction

This document outlines the implementation plan and current architecture of the Asteroids AI project. It consolidates the original, incremental plans into a single, up-to-date reference that reflects the project's status as of January 2026. The project has been implemented following a modular, interface-driven design to support multiple AI paradigms, with the first paradigm—a Genetic Algorithm with Neuroevolution—now complete.

---

## Phase 1: Core Infrastructure (Completed)

This foundational phase focused on decoupling the AI from the core game simulation. All components in this phase are complete and in use.

### 1.1. State & Metrics Tracking

- **`EnvironmentTracker`**: A dedicated class that provides a clean, read-only API to the game's state (player, asteroids, bullets) at any given moment. This prevents AI agents from having direct, brittle access to game internals.
- **`MetricsTracker`**: A class that aggregates statistics over the course of an episode (e.g., total kills, shots fired, accuracy, time alive). It provides the raw data necessary for calculating fitness and analyzing agent performance.

### 1.2. Composable Reward System

- **`RewardCalculator`**: A modular system that calculates an agent's fitness score by summing the outputs of individual, swappable "reward components." This allows for flexible and experimental reward shaping without altering agent or game logic.
- **Reward Components**: The system includes various components such as `KillAsteroid`, `AccuracyBonus`, `SurvivalBonus`, `ShootingPenalty`, and `MaintainingMomentumBonus`, which are combined to produce the final fitness score.

---

## Phase 2: Standardized AI Interfaces (Completed)

This phase established a set of abstract interfaces to ensure that all current and future AI agents interact with the environment in a standardized way.

- **`BaseAgent`**: An abstract base class that all agents must implement. It defines the core `get_action(state)` method, ensuring that any agent can be used by the training pipeline.
- **`StateEncoder`**: An abstract base class for converting raw game state from the `EnvironmentTracker` into a format suitable for an AI agent.
  - **`VectorEncoder`**: The primary implementation used for the GA, which converts the game state into a fixed-size, normalized vector. This vector includes features for the player and the N nearest asteroids.
- **`ActionInterface`**: A class that standardizes the action format. It validates and converts the AI's output (a vector of floats) into boolean game commands (e.g., `left_pressed`, `up_pressed`).

---

## Phase 3: Genetic Algorithm with Neuroevolution (Completed)

The initial AI paradigm implemented is a Genetic Algorithm (GA) that evolves the weights of a neural network policy. This implementation is more advanced than the originally planned simple linear policy and is highly optimized for speed.

### 3.1. Policy Representation: Neural Network

- **`NeuralNetworkGAAgent`**: The agent policy is not a simple linear vector but a full feedforward neural network. The GA evolves the flattened weights and biases of this network.
- **Architecture**: The default network architecture is Input(16) → Hidden(24, tanh) → Output(4, sigmoid), resulting in 508 parameters to be evolved per agent.

### 3.2. Training Pipeline: Parallel Evaluation

- **`train_ga_parallel.py`**: This is the main entry point for training. It orchestrates the entire GA lifecycle.
- **High-Speed Headless Evaluation**: The fitness of the entire agent population is evaluated simultaneously in the background. This is achieved by using a `ThreadPoolExecutor` where each agent runs in its own fast, non-visual `HeadlessAsteroidsGame` instance. This parallelization provides a significant speedup over sequential evaluation.
- **Custom Evolution Loop**: The training driver implements a custom evolutionary loop featuring:
  - Tournament selection
  - Blend crossover
  - Gaussian mutation
  - Elitism (the top N% of agents are preserved across generations)

### 3.3. Visualization & Generalization Testing

- **Fresh Game Display**: After each generation's parallel evaluation, the single best-performing agent is run in the main visual `AsteroidsGame`.
- **Testing Generalization, Not Replaying**: This visual display uses a **new, random seed**. It is not a replay of the evaluation run. This serves as a crucial test of the agent's ability to **generalize** its learned skills to unseen scenarios, providing a more honest assessment of its capabilities.

---

## Phase 4: Future Work (Planned)

With the core infrastructure and the first AI paradigm in place, future work will focus on improving usability, analytics, and expanding the roster of AI agents.

### 4.1. Configuration System

- **Goal**: Replace the hardcoded hyperparameters in `train_ga_parallel.py` with a flexible configuration system (e.g., using YAML or JSON files).
- **Status**: Not implemented. This is a high-priority next step to enable easier experimentation and reproducible research.
- **Features**:
  - Manage GA hyperparameters (population size, mutation rates, etc.).
  - Configure the `VectorEncoder` (e.g., number of asteroids to track).
  - Enable/disable and tune `RewardCalculator` components.

### 4.2. Advanced Analytics & Data Tracking

- **Goal**: Implement the comprehensive analytics and data schema enhancements outlined in the research documents.
- **Status**: Partially implemented (basic analytics exist). The full, detailed proposal is the next step for deeper insights.
- **Key Features to Implement**:
  - **Persist Fresh Game Performance**: Systematically save the generalization test results for analysis.
  - **Track Population Distributions**: Save per-agent data arrays to analyze fitness and behavioral distributions, not just averages.
  - **Add Action-Level Metrics**: Directly track action frequencies to move from inferring behavior to observing it.

### 4.3. Additional AI Paradigms

- **Goal**: Implement other AI methods to compare against the GA baseline, fulfilling the project's core mission.
- **Status**: Not started. The completed infrastructure (Interfaces, Trackers, etc.) is designed to support this.
- **Candidates**:
  - **Reinforcement Learning**: GNN+SAC (Graph Neural Network with Soft Actor-Critic).
  - **Neuroevolution**: NEAT (NeuroEvolution of Augmenting Topologies).
  - **Genetic Programming**: Evolving symbolic expression trees as policies.
