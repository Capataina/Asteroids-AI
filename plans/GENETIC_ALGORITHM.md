# Genetic Algorithm Implementation

## Scope / Purpose

The Genetic Algorithm (GA) serves as the baseline AI paradigm for the AsteroidsAI project. Its purpose is to evolve a neural network policy that can survive and destroy asteroids efficiently. It establishes the benchmark for performance, stability, and training speed against which future methods (like RL or NEAT) will be compared.

## Current Implemented System

### Policy Architecture

- **Feedforward Neural Network**: A standard MLP architecture used for the agent's brain.
- **Input Vector**: A 16-dimensional vector containing normalized player and environment state data.
- **Hidden Layer**: A single hidden layer with 24 neurons using `tanh` activation.
- **Output Layer**: 4 output neurons with `sigmoid` activation corresponding to game controls (Thrust, Left, Right, Shoot).
- **Parameter Encoding**: Weights and biases are flattened into a single contiguous float vector (genome) for evolutionary operators.

### Evolutionary Pipeline

- **GADriver**: The central controller that manages the population state and executes the evolution loop.
- **Population Management**: Maintains a fixed-size population of agents (Default: 25) throughout the training process.
- **Tournament Selection**: Selects parents for reproduction using tournaments of size 3 to maintain selection pressure.
- **Blend Crossover (BLX-alpha)**: Combines parent genes to create offspring that explore the continuous space between and around parent values.
- **Gaussian Mutation**: Applies random noise to genome weights to introduce genetic diversity.
- **Adaptive Mutation**: Automatically increases mutation rate and sigma if the population fitness stagnates for more than 10 generations.
- **Elitism**: Preserves the top 10% of agents and the all-time best agent unchanged in the next generation to prevent performance regression.

### Evaluation System

- **Parallel Execution**: Utilizes `ThreadPoolExecutor` to evaluate the entire population simultaneously across available CPU cores.
- **Headless Simulation**: Uses `headless_game.py` for high-speed, rendering-free evaluation of agent performance.
- **Robustness Seeding**: Evaluates each agent on 20 different random seeds to calculate an average fitness, reducing the impact of luck.
- **Generalization Testing**: Evaluates the best agent of each generation on a fresh, unseen seed to measure true skill generalization.
- **Physics Parity Enforcement**: Forces both the headless training simulation and the visual "Fresh Game" to update at a fixed 1/60s timestep to prevent physics divergence.
- **Toroidal Distance Calculation**: The `EnvironmentTracker` correctly computes distances across screen boundaries, ensuring agents perceive wrapped threats.

### Configuration

- **Centralized Config**: All GA hyperparameters are defined in `training/config/genetic_algorithm.py`.
- **Population Settings**: Controls for population size and number of generations.
- **Operator Probabilities**: Settings for mutation rate, crossover rate, and mutation sigma.
- **Evaluation Settings**: Controls for seeds per agent and maximum steps per episode.
- **Network Architecture**: Settings for input size (via asteroid count) and hidden layer size.

## Implemented Outputs / Artifacts

- **Trained Agent Weights**: The best performing agent's neural network weights are preserved in memory.
- **JSON Analytics**: A comprehensive `training_data.json` file containing full history of fitness and behavioral metrics.
- **Markdown Summary**: A `training_summary.md` report with generated charts, heatmaps, and trend analysis.
- **Visual Playback**: A real-time windowed display of the best agent playing a fresh game after each generation.
- **Console Telemetry**: Detailed real-time logs of generation progress, fitness statistics (Min/Avg/Max), and behavioral averages.

## In Progress / Partially Implemented

- **Speciation**: Basic diversity is maintained via random seeds, but explicit species tracking is not yet fully implemented.
- **Reaction Time Metrics**: Logic exists to track input changes, but specific reaction time analysis is not yet fully integrated into reports.

## Planned / Missing / To Be Changed

- **Novelty Search**: Plan to add behavioral novelty as a fitness component to encourage diverse strategies (e.g., exploring corners vs. circling center).
- **Hyperparameter Optimization**: Plan to implement a meta-search to automatically find optimal mutation rates and population sizes.
- **Crossover Enhancements**: Plan to experiment with geometric crossover or other operator variants to improve convergence speed.
- **Multi-Episode Validation**: Plan to update the "Fresh Game" visualizer to run 5-10 episodes and report the average, aligning it with the multi-seed training metric.

## Notes / Design Considerations

- **Evaluation Bottleneck**: The primary performance bottleneck is the simulation time, which scales linearly with `SEEDS_PER_AGENT` (20).
- **Generalization Gap**: A discrepancy between training fitness and fresh game performance is the primary indicator of overfitting vs. true learning.
- **Physics & Perception Consistency**:

  - **Deductive Logic (Root Cause Analysis)**: We observed that agents transitioning to Generation N+1 (facing new seeds) maintained high performance/accuracy, whereas the same agents playing the 'Fresh Game' (also a new seed) failed catastrophically. This logical discrepancy proved the issue was not just "unseen seed" difficulty, but a fundamental environmental difference.
  - **Identified Issue**: This deduction led to the discovery that the 'Fresh Game' was running on variable `delta_time` (Real-Time Physics) while Training ran on fixed `1/60s` (Simulation Physics). This caused agents to "hallucinate" asteroid positions due to "time travel" drift in their aim. Additionally, the `EnvironmentTracker` failed to calculate toroidal (screen-wrapped) distances, creating blind spots.
  - **Resolution**: Both environments now force a strict 1/60s physics update, and the tracker correctly computes wrapped distances. This aligns the laws of physics across both modes.

- **Variance vs. Systematic Failure**:
  - **Status**: Physics parity fixes (fixed timestep + wrapping) were deployed. Initial results show _partial_ success: some agents now achieve parity (Grade A, Ratio 1.05), proving the environments are aligned.
  - **Issue**: However, _significant_ variance remains (many Grade F failures). This confirms that while the systematic 'physics blindness' is fixed, the policy is brittle and the single-seed test is too volatile.
  - **Next Step**: Future work must focus on **Multi-Episode Validation** (averaging 5-10 fresh games) to smooth out this variance and provide a reliable metric.

## Discarded / Obsolete / No Longer Relevant

- **Linear Policy**: Initial implementation used a simple linear mapping without hidden layers. It was discarded because it could not capture non-linear XOR-like logic required for advanced dodging.
- **Sequential Evaluation**: The original system evaluated agents one-by-one. This was discarded in favor of parallel evaluation, yielding a ~20x speedup.
- **Single-Seed Training**: Training agents on a fixed seed was discarded as it led to agents memorizing specific asteroid trajectories rather than learning general physics rules.
