# AsteroidsAI

## Project Description

**AsteroidsAI** is a real-time AI experimentation and benchmarking project built around a custom _Asteroids_-style environment.  
The project is designed as a **modular research playground** for comparing how fundamentally different AI paradigms solve the _same continuous-control problem_ under identical physics, state constraints, and reward structures.

Rather than optimising purely for score or survival time, AsteroidsAI focuses on:

- Emergent behaviour and strategy formation
- Learning dynamics over time
- Representation choices and architectural trade-offs
- Watchability, smoothness, and qualitative decision-making

Each AI method is implemented as a **pluggable module** operating on a shared environment interface, making behavioural differences easy to observe, measure, and reason about.

---

## Core Design Philosophy

- **Single environment, multiple minds** – one simulation, many learning paradigms
- **Modular architecture** – swap agents, state encoders, reward functions, and training loops independently
- **Method-agnostic design** – no hard coupling to specific ML libraries or frameworks
- **Behaviour-first evaluation** – visual and qualitative analysis matters as much as metrics
- **Research extensibility** – designed to grow into more complex experiments over time

---

## Environment Overview

The Asteroids environment is intentionally minimal yet challenging:

- Continuous 2D physics with inertia and rotation
- Dynamic asteroid spawning and fragmentation
- Projectile-based interaction with cooldown constraints
- Partial unpredictability in asteroid trajectories
- Trade-offs between survival, aggression, and precision

These properties make the environment a strong testbed for real-time decision-making under uncertainty, credit assignment, and representation learning.

---

## AI Methods Explored

AsteroidsAI compares several classes of AI techniques, each representing a distinct optimisation philosophy.

### Evolutionary Approaches

- **Neuroevolution with topology growth**  
  Networks evolve both structure and weights, allowing complexity to emerge organically.
  Will most likely use the NEAT algorithm.

- **Evolution Strategies**  
  Population-based optimisation in parameter space over fixed policy representations.
  Will most likely use TensorFlow.

- **Genetic Algorithms**  
  Evolution of hand-designed parameter vectors controlling reflexive or heuristic behaviour.
  Will most likely use DEAP.

- **Genetic Programming**  
  Evolution of symbolic programs or decision trees encoding explicit control logic.
  Will most likely use DEAP.

### Reinforcement Learning

- **Graph-Based Reinforcement Learning**  
  Variable-sized environment state represented as a graph, combined with continuous-control RL algorithms to learn smooth, adaptive policies.
  Will most likely use PyTorch.

Each method interacts with the _same_ environment but may use different internal representations and learning dynamics.

---

## Modular Architecture

AsteroidsAI is structured around clean separation of concerns:

- **Environment Core**
  - Physics, collision detection, spawning, and simulation stepping
  - Deterministic, seedable execution

- **Agent Interface**
  - Standardised state → action boundary
  - Supports continuous and discrete control
  - Allows heterogeneous internal implementations

- **State Encoders**
  - Fixed-size vector encodings
  - Variable-size graph encodings
  - Sensor-based or relative-coordinate representations

- **Training Backends**
  - Evolutionary loops
  - Gradient-based RL loops
  - Hybrid or experimental optimisers

- **Evaluation & Visualisation**
  - Real-time playback
  - Episode metrics
  - Behavioural comparison across agents

This modularity allows components to evolve independently without rewriting the entire system.

---

## Training Dashboard Architecture

AsteroidsAI uses a **parallel training dashboard** that enables real-time comparison of all AI methods:

- **Parallel execution**: All 5 algorithms train simultaneously in separate game instances
- **View switching**: Interactive sidebar allows switching between algorithms to observe their training
- **Continuous training**: All algorithms continue learning even when not actively displayed
- **Fair comparison**: Identical runtime conditions ensure meaningful behavioural comparisons

The dashboard provides a unified interface where researchers can:

- Observe learning dynamics across different paradigms in real time
- Switch views to compare emergent strategies and decision-making patterns
- Monitor training progress (generations, episodes, metrics) for all methods simultaneously
- Compare qualitative behaviours (movement, aiming, risk-taking) side-by-side

This architecture supports the project's goal of understanding how different optimisation philosophies shape intelligent behaviour under identical environmental constraints.

---

## Features & Roadmap

### 🎮 Simulation & Environment

- [x] Continuous 2D physics with inertia and rotation
- [x] Dynamic asteroid spawning and fragmentation
- [x] Bullet cooldowns and collision detection
- [x] Deterministic step loop with configurable randomness
- [ ] Difficulty scaling and curriculum variants
- [ ] Multi-agent or competitive extensions

### 🧠 State Representation

- [x] Ship-centric coordinate transforms
- [x] Nearest-neighbour asteroid encoding
- [x] Temporal awareness (frame stacking)
- [x] Raycasting (lidar) sensors
- [x] Variable-cardinality representations
- [x] Sensor noise and partial observability experiments
- [x] Full graph-based state models

### 🧬 Neuroevolution

- [x] Topology and weight evolution
- [x] Speciation and diversity preservation
- [x] Network complexity control
- [x] Behavioural novelty metrics
- [x] Cross-generation analysis

### 🌱 Evolution Strategies

- [x] Fixed-topology policy optimisation
- [x] Population-based sampling
- [x] Adaptive noise and step-size strategies
- [x] Parallel rollout evaluation
- [x] Hybrid evolution / gradient experiments

### 🧪 Genetic Algorithms

- [x] Parameter-vector control policies
- [x] Mutation and crossover operators
- [x] Environment randomisation stress tests
- [x] Interpretability-focused analysis
- [x] Reflex vs strategy comparisons

### 🌳 Genetic Programming

- [x] Tree-based symbolic controllers
- [x] Arithmetic and logic operators
- [x] Parsimony pressure and bloat control
- [x] Subtree crossover strategies
- [x] Decision-logic visualisation

### 🎯 Reinforcement Learning

- [x] Continuous action policies
- [x] Stochastic exploration mechanisms
- [x] Reward shaping experiments
- [x] Replay and off-policy analysis
- [x] Graph-based encoders for dynamic entities

### 🖥️ Training Dashboard

- [ ] Parallel training infrastructure (all algorithms run simultaneously)
- [ ] Interactive sidebar UI for algorithm selection
- [ ] View switching between active algorithms
- [ ] Real-time metrics display for all methods
- [ ] Training progress indicators (generations, episodes, fitness)
- [ ] Performance optimization for parallel game instances
- [ ] Pause/resume controls for individual algorithms

---

## Reward Design Experiments

Reward shaping is treated as a first-class experimental variable:

- Survival duration
- Asteroids destroyed
- Accuracy and efficiency
- Collision penalties
- Risk-sensitive bonuses (e.g. near misses)

Different reward compositions can be swapped in without modifying agent logic, enabling controlled behavioural studies.

---

## Analysis & Observability

AsteroidsAI emphasises **understanding behaviour**, not just maximising numbers:

- Real-time visual playback of agents
- Episode-level metric logging
- Learning curve comparison across methods
- Qualitative inspection of movement, aiming, and timing
- Cross-agent behavioural contrast under identical conditions

---

## Research & Extension Paths

- Curriculum learning and difficulty progression
- Hybrid evolutionary + gradient-based agents
- Transfer learning across environment variants
- Behavioural clustering and policy analysis
- Neuro-symbolic hybrids
- Integration into larger ML or neuroevolution frameworks

---

## Why Asteroids?

Asteroids is deceptively simple yet deeply expressive:

- Few rules, rich dynamics
- Continuous control with sparse rewards
- Chaotic interactions that punish brittle policies
- Natural support for variable numbers of entities

This makes it an ideal micro-benchmark for studying how different AI paradigms reason, adapt, and generalise in real time.

---

AsteroidsAI is intended as a **comparative lens**:  
a way to observe how optimisation philosophy, representation choice, and learning dynamics shape intelligent behaviour when facing the same fast-moving world.
