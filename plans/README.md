# AsteroidsAI

**AsteroidsAI** is a modular research framework for benchmarking AI paradigms on a custom _Asteroids_ environment. It focuses on emergent behavior, generalization, and visual quality, not just high scores.

---

## 🚀 Key Features

- **Modular Architecture**: Swap agents (GA, RL, NEAT), rewards, and state encoders without touching game logic.
- **Sim-to-Real Parity**: A headless simulation (`headless_game.py`) runs 1000x faster than the visual game (`Asteroids.py`) while maintaining **100% physics and hitbox parity** via a shared `globals.py`.
- **Toroidal Perception**: Agents perceive the game world correctly across screen wraps (a common pitfall in Asteroids AI).
- **Parallel Training**: Multithreaded evaluation pipeline maximizes CPU usage.
- **Deep Analytics**: Automated report generation (`training_summary.md`) tracks not just score, but behavioral archetypes ("Sniper" vs "Dogfighter"), population health, and generalization capability.

---

## 🛠️ Architecture

The project is split into clean layers:

1.  **Game Layer**: The core simulation.
    - `game/globals.py`: Single source of truth for physics constants.
    - `Asteroids.py`: Visual game with Debug Mode (Press 'D').
    - `game/headless_game.py`: Fast simulation for training.
2.  **Interface Layer**: The bridge between Game and AI.
    - `VectorEncoder`: Converts game state to neural inputs (now with Screen Wrap awareness).
    - `RewardCalculator`: Composable reward system (Velocity, Accuracy, Kills).
3.  **Agent Layer**: The brains.
    - `NeuralNetworkGAAgent`: Feedforward network trained via Genetic Algorithm.
4.  **Training Layer**: The loop.
    - `train_ga_parallel.py`: Manages the evolutionary process.
    - `parallel_evaluator.py`: Runs the simulations.

---

## 📊 Analytics & Reporting

The system generates a comprehensive `training_summary.md` after every run. Key metrics include:

- **Generalization Grade**: A-F rating based on how well the agent performs on a _fresh_ map compared to its training seeds.
- **Behavioral Classification**: Automatically detects strategy (e.g., "Turret" = stationary shooter, "Dogfighter" = fast mover).
- **Efficiency**: Shots per Kill, Exploration Rate, and Reaction Time.
- **Health**: Warnings for stagnation or diversity collapse.

---

## 🏃 Running the Project

### 1. Play the Game (Manual)

Test the physics or just have fun.

```bash
python Asteroids.py
```

- **Controls**: Arrow Keys to move, Space to shoot.
- **Debug Mode**: Press `D` to toggle hitbox visualization.

### 2. Train the AI

Start the parallel Genetic Algorithm training loop.

```bash
python training/train_ga_parallel.py
```

- **What to watch**: The console will log progress. Every generation, the best agent will play a visual game on screen so you can see its behavior evolving.
- **Output**: Check `training_summary.md` and `training_data.json` for results.

---

## 📜 Recent Updates (Jan 2026)

- **Fixed Blindness**: Fixed a bug where agents couldn't see across screen edges.
- **Fixed Hitboxes**: Standardized collision radii across visual/headless modes.
- **Anti-Overfitting**: Increased training rigor to 12 seeds per agent to force robust learning.
- **New Rewards**: Introduced `VelocitySurvivalBonus` to cure "camping" behavior.

---

## 🔮 Roadmap

- [ ] **Config System**: Move hardcoded params to `config.yaml`.
- [ ] **RL Agent**: Implement Graph Neural Network + Soft Actor-Critic (GNN-SAC).
- [ ] **NEAT**: Integrate NeuroEvolution of Augmenting Topologies.
- [ ] **Competitive**: Multi-agent dogfighting.
