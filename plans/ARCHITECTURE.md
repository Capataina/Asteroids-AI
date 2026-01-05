# Architecture Overview

Top-down view of the AsteroidsAI codebase structure and responsibilities.

## Repository Structure

```
Asteroids AI/
├── Asteroids.py                  # Main visual game (arcade.Window)
├── game/
│   ├── classes/                  # Game entity classes
│   │   ├── player.py             # Player ship (movement, shooting)
│   │   ├── bullet.py             # Bullet projectiles
│   │   └── asteroid.py           # Asteroids (HP, fragmentation)
│   ├── headless_game.py          # Headless game for parallel evaluation
│   └── sprites/                  # Image assets
├── ai_agents/
│   ├── neuroevolution/
│   │   └── genetic_algorithm/
│   │       ├── ga_agent.py       # GA agent implementing BaseAgent
│   │       ├── ga_trainer.py     # GA configuration and operators container
│   │       ├── ga_fitness.py     # Fitness evaluation (NOTE: broken, not used)
│   │       └── operators.py      # Mutation and crossover operators
│   └── reinforcement_learning/
│       └── gnn_and_sac/
│           ├── env_wrapper.py    # Graph-based RL wrapper (legacy)
│           ├── gnn.py            # Graph neural network models
│           ├── policies.py       # Policy implementations
│           └── sac.py            # Soft Actor-Critic RL algorithm
├── interfaces/
│   ├── EnvironmentTracker.py     # Current state snapshot, game access
│   ├── MetricsTracker.py         # Aggregated episode statistics
│   ├── RewardCalculator.py       # Component-based reward system
│   ├── StateEncoder.py           # Abstract base class for state encoders
│   ├── ActionInterface.py        # Action validation and normalization
│   ├── encoders/
│   │   └── VectorEncoder.py      # Fixed-size vector for GA
│   └── rewards/                  # Individual reward components
│       ├── SurvivalBonus.py
│       ├── KillAsteroid.py
│       ├── ChunkBonus.py
│       ├── AccuracyBonus.py
│       ├── NearMiss.py
│       ├── KPMBonus.py
│       ├── ShootingPenalty.py
│       ├── FacingAsteroidBonus.py
│       ├── MaintainingMomentumBonus.py
│       ├── ConservingAmmoBonus.py
│       ├── LeadingTargetBonus.py
│       ├── MovingTowardDangerBonus.py
│       └── SpacingFromWallsBonus.py
├── training/
│   ├── base/
│   │   ├── BaseAgent.py          # Abstract agent interface
│   │   ├── EpisodeRunner.py      # Episode execution (visual display)
│   │   └── EpisodeResult.py      # Episode result dataclass
│   ├── train_ga.py               # Original GA training (superseded)
│   ├── train_ga_parallel.py      # Parallel GA training driver (PRIMARY)
│   ├── parallel_evaluator.py     # Parallel fitness evaluation
│   └── analytics.py              # Training analytics and reporting
├── tests/
│   ├── test_ga_dimensions.py     # GA dimension tests
│   └── test_kill_asteroid_reward.py
└── train_agent.py                # Legacy training loop (not used for GA)
```

## Core Subsystems

### Game Core (`Asteroids.py` + `game/headless_game.py`)

- **Asteroids.py**: Visual game with arcade.Window for display
  - Handles rendering, keyboard input, visual feedback
  - Used during training to display best agent playing
  - Uses `arcade.schedule()` for asteroid spawning

- **HeadlessAsteroidsGame**: Fast game simulation without rendering
  - Used for parallel evaluation of agents
  - Independent RNG instance per game for reproducible, thread-safe evaluation
  - Manual collision detection with explicit radii (no textures loaded)

### Game Entities (`game/classes/`)

- **Player**: Movement (thrust, rotation), shooting with cooldown
- **Bullet**: Projectile with lifetime, velocity
- **Asteroid**: HP-based destruction, fragmentation into smaller asteroids, RNG support

### AI Interface Layer (`interfaces/`)

- **EnvironmentTracker**: Current state snapshot, derived metrics
  - Provides access to player, asteroids, bullets
  - Calculates nearest asteroids, distances
  - Stable API for game state access

- **MetricsTracker**: Aggregated statistics over episode
  - Tracks: shots_fired, hits, kills, time_alive
  - Calculates: accuracy, kills_per_minute

- **RewardCalculator**: Component-based reward system
  - `ComposableRewardCalculator` with pluggable components
  - Active components: KillAsteroid, AccuracyBonus, FacingAsteroidBonus, MaintainingMomentumBonus
  - Components track state (prev_kills, prev_time) for delta-based rewards

- **StateEncoder + VectorEncoder**: State encoding for agents
  - VectorEncoder: Fixed-size vector (16 features with 2 asteroids)
  - 6 player features + 5 features × num_asteroids

- **ActionInterface**: Action validation and conversion
  - Validates action format [left, right, thrust, shoot]
  - Converts to game input booleans via 0.5 threshold

### GA Implementation (`ai_agents/neuroevolution/genetic_algorithm/`)

- **GAAgent**: Implements BaseAgent with linear policy
  - Parameter vector size: state_size × action_size (e.g., 16 × 4 = 64)
  - Linear policy: action[i] = sum(weights × state)

- **GATrainer**: Configuration container (not the actual training loop!)
  - Stores hyperparameters and creates operators
  - `train()` method exists but is NOT used by parallel training

- **GAGeneticOperators**: Mutation and crossover operators
  - mutate_gaussian: Adds Gaussian noise per gene
  - mutate_uniform: Replaces genes with uniform random
  - crossover_blend: Weighted average of parents

### Parallel Training (`training/`)

- **train_ga_parallel.py**: Main training entry point
  - `ParallelGATrainingDriver`: Actual GA training loop
  - Uses arcade.schedule() for visual updates
  - Displays best agent from each generation

- **parallel_evaluator.py**: Parallel fitness evaluation
  - `evaluate_population_parallel()`: Evaluates all agents simultaneously
  - Uses ThreadPoolExecutor for parallelism
  - Each agent gets same random seed for fair comparison

- **EpisodeRunner**: Episode execution for visual display
  - Used during best agent display phase
  - NOT used for parallel evaluation

## Data Flow

### Current Parallel Training Flow

1. **Initialization**: `ParallelGATrainingDriver._initialize_population()`
   - Creates random 64-dimensional parameter vectors
   - Population size: 100 agents

2. **Parallel Evaluation**: `evaluate_population_parallel()`
   - Creates HeadlessAsteroidsGame per agent
   - All agents use same random seed for fair comparison
   - Returns fitness scores and behavioral metrics

3. **Display Phase**: Best agent plays visually
   - Uses same seed as evaluation for reproducibility
   - EpisodeRunner controls visual game stepping
   - Updates display with training metrics

4. **Evolution**: `ParallelGATrainingDriver._evolve_generation()`
   - Tournament selection (size=3)
   - Crossover blend (70% probability)
   - Gaussian mutation (all offspring)
   - Elitism: Top 20% survive

5. **Next Generation**: Loop back to step 2

### Reward Flow

1. **Per-Step Rewards**: `RewardCalculator.calculate_step_reward()`
   - KillAsteroid: +100 per asteroid destroyed (delta-based)
   - AccuracyBonus: +2/sec × accuracy (if accuracy > 25%)
   - FacingAsteroidBonus: +2/sec when facing asteroids
   - MaintainingMomentumBonus: +0.5/sec moving, -1/sec stationary

2. **Episode Rewards**: `RewardCalculator.calculate_episode_reward()`
   - Currently returns 0 for all active components
   - Available for end-of-episode bonuses

## Implementation Status

### Completed Infrastructure

- **EnvironmentTracker**: Game state access
- **MetricsTracker**: Episode statistics
- **RewardCalculator**: Component-based rewards (12 components implemented)
- **StateEncoder + VectorEncoder**: State encoding
- **ActionInterface**: Action validation
- **BaseAgent + EpisodeRunner**: Episode execution
- **Parallel GA Training**: Full implementation with visualization

### Known Issues (As of 2026-01-05)

1. **EpisodeRunner.py:124-126**: Episode reward calculated inside loop
   - Should be outside the while loop (only affects display, not training)

2. **ga_trainer.py**: Contains bugs but NOT used for training
   - `train()` method has min/max confusion
   - `elitism()` selects worst instead of best
   - train_ga_parallel.py implements its own correct logic

3. **ga_fitness.py**: Broken (missing attributes)
   - References `self.state_encoder` never initialized
   - Not used by current training pipeline

4. **operators.py**: crossover_alpha parameter ignored
   - Uses crossover_probability as blend factor instead

5. **VectorEncoder**: Asteroids not sorted by distance
   - Gets asteroids in arbitrary order, not nearest-first

## Configuration

### Current GA Hyperparameters (train_ga_parallel.py)

```python
population_size = 100
num_generations = 500
mutation_probability = 0.20      # Per-gene probability
crossover_probability = 0.7
mutation_gaussian_sigma = 0.15
elitism = 20%                    # Top 20% survive
tournament_size = 3
max_steps = 1500                 # Per episode
```

### Current Reward Configuration

```python
KillAsteroid(reward_per_asteroid=100.0)
AccuracyBonus(bonus_per_second=2.0)
FacingAsteroidBonus(bonus_per_second=2.0)
MaintainingMomentumBonus(bonus_per_second=0.5, penalty_per_second=-1.0)
```

## Future Considerations

### Immediate Fixes Needed

- Fix EpisodeRunner episode reward calculation
- Fix VectorEncoder to sort asteroids by distance
- Remove or fix broken ga_fitness.py

### Infrastructure Enhancements

- Configuration system (plan 006)
- Agent save/load functionality
- Additional AI methods (NEAT, ES, GP, GNN+SAC)

### Advanced Features

- Training dashboard with multiple AI methods
- Parallel episode evaluation on GPU
- Behavioral novelty metrics
- Policy visualization tools
