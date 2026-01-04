# Genetic Algorithm Implementation

## Goal and Scope

**Deliverables:**

- `ai_agents/genetic_algorithm/` directory structure
- `ai_agents/genetic_algorithm/ga_agent.py` - GA agent implementing BaseAgent interface
- `ai_agents/genetic_algorithm/ga_trainer.py` - DEAP-based evolutionary training loop
- `ai_agents/genetic_algorithm/operators.py` - Mutation and crossover operators
- `ai_agents/genetic_algorithm/fitness.py` - Fitness evaluation using EpisodeRunner
- `training/train_ga.py` - **Visual training entry point** - runs GA training with real-time game visualization
- Working GA implementation that can train and evolve parameter vectors
- Integration with all infrastructure (StateEncoder, ActionInterface, RewardCalculator, BaseAgent, EpisodeRunner)
- **Real-time visualization** - watch the AI learn and improve generation by generation in the game window

**Out of Scope:**

- Advanced GA techniques (niching, speciation, etc.) - can be added later
- Multi-objective optimization - future enhancement
- Parallel evaluation (can be added incrementally)
- Training dashboard integration (deferred until all AIs work)
- **Note**: Real-time visualization during training IS in scope - this is a core requirement for observing AI learning

## Context and Justification

**Why Now:**

- All prerequisite infrastructure is complete (plans 001-006)
- GA is the first AI method to implement (incremental approach)
- GA provides a good baseline for comparison with other methods
- DEAP is a mature library well-suited for this task
- GA implementation will validate the shared infrastructure design
- **Visualization is core to the project** - the README emphasizes "watchability, smoothness, and qualitative decision-making" as key evaluation criteria, not just metrics

**What It Enables:**

- First working AI method in the system
- Validates BaseAgent, EpisodeRunner, StateEncoder, ActionInterface design
- Provides baseline performance for comparison
- Demonstrates the evolutionary training paradigm
- Foundation for understanding how parameter vectors control behaviour
- **Real-time visualization of AI learning** - watch the AI improve generation by generation
- **Qualitative behavioural analysis** - observe movement patterns, aiming strategies, and decision-making in real-time

**Rejected Alternatives:**

- **Neural network-based GA**: GA focuses on parameter vectors, not neural networks (that's NEAT)
- **Custom GA implementation**: DEAP provides proven, tested operators and framework
- **Different state representation**: Using VectorEncoder as designed in plan 004

**Key Requirements:**

- Must implement BaseAgent interface (from plan 005)
- Must use VectorEncoder for state representation (from plan 004)
- Must use ActionInterface for actions (from plan 004)
- Must use RewardCalculator for fitness (from plan 003)
- Must use EpisodeRunner for evaluation (from plan 005)
- Must use DEAP for evolutionary algorithm framework
- Parameter vectors must encode control policy (reflexive/heuristic behaviour)
- **Must provide real-time visualization** - game window must be visible during training
- **Must display training progress** - show generation number, fitness, best agent performance on screen
- **Must allow watching AI learn** - observe behavioural changes as the population evolves

## Interfaces and Contracts

### GA Agent Interface

**Class:** `GAAgent` (in `ai_agents/genetic_algorithm/ga_agent.py`)

**Implements:** `BaseAgent` interface (from plan 005)

**Core Methods:**

```python
class GAAgent(BaseAgent):
    def __init__(self, parameter_vector: List[float], state_encoder: VectorEncoder, action_interface: ActionInterface):
        """
        Initialize GA agent with parameter vector.

        Args:
            parameter_vector: List of floats encoding control policy
            state_encoder: VectorEncoder instance for state representation
            action_interface: ActionInterface instance for action conversion
        """
        self.parameter_vector = parameter_vector
        self.state_encoder = state_encoder
        self.action_interface = action_interface

    def get_action(self, state: List[float]) -> List[float]:
        """
        Get action from state using parameter vector.

        Args:
            state: Encoded state vector from VectorEncoder

        Returns:
            Action vector [left, right, thrust, shoot]
        """
        pass

    def reset(self) -> None:
        """
        Reset agent state (no internal state for GA, but required by BaseAgent).
        """
        pass
```

**Parameter Vector Design:**

The parameter vector encodes a control policy. Options:

1. **Linear Policy**: Direct mapping from state to action

   - `action[i] = sum(state[j] * parameter_vector[i * state_size + j])`
   - Size: `action_size * state_size` (e.g., 4 \* 18 = 72 parameters)

2. **Threshold Policy**: Learned thresholds for state features

   - Compare state features to thresholds, combine with weights
   - More interpretable, fewer parameters

3. **Heuristic Policy**: Parameters control heuristic rules
   - Distance thresholds, angle preferences, velocity preferences
   - Most interpretable, fewest parameters

**Initial Choice:** Start with linear policy (simple, works well), can experiment with others later.

**Invariants:**

- Parameter vector size is fixed for a given state encoder configuration
- Actions are always in format `[left, right, thrust, shoot]`
- Agent uses VectorEncoder (no direct game access)
- Agent uses ActionInterface for action conversion

### GA Trainer Interface

**Class:** `GATrainer` (in `ai_agents/genetic_algorithm/ga_trainer.py`)

**Core Methods:**

```python
class GATrainer:
    def __init__(self, config: Dict):
        """
        Initialize GA trainer with configuration.

        Args:
            config: Configuration dict with:
                - population_size: int
                - num_generations: int
                - mutation_rate: float
                - crossover_rate: float
                - tournament_size: int
                - state_encoder_config: Dict
                - reward_calculator_config: Dict
        """
        pass

    def train(self) -> GAAgent:
        """
        Run evolutionary training loop.

        Returns:
            Best agent from final generation
        """
        pass

    def evaluate_individual(self, individual: List[float]) -> float:
        """
        Evaluate fitness of an individual parameter vector.

        Args:
            individual: Parameter vector

        Returns:
            Fitness score (total reward from episode)
        """
        pass
```

**Training Loop:**

1. Initialize population (random parameter vectors)
2. For each generation:
   - Evaluate all individuals (run episodes, collect fitness)
   - Select parents (tournament selection)
   - Create offspring (crossover + mutation)
   - Replace population (elitism + new offspring)
3. Return best individual

**Invariants:**

- Uses EpisodeRunner for fitness evaluation
- Uses RewardCalculator for episode rewards
- Uses VectorEncoder for state encoding
- Uses ActionInterface for action conversion
- All individuals have same parameter vector size

### Visualization and Training Display

**Training Entry Point:** `train_ga.py` (in `training/train_ga.py`)

**Core Requirements:**

- Must create and display game window using `arcade.run()`
- Must show real-time training progress on screen:
  - Current generation number
  - Best fitness in current generation
  - Average fitness in current generation
  - Current individual being evaluated (optional)
  - Episode statistics (steps, reward, kills, accuracy)
- Must allow watching the best agent from each generation play
- Must use `arcade.schedule()` to integrate training updates with game rendering
- Must display metrics overlay similar to `train_agent.py` approach

**Visualization Strategy:**

1. **Create game window** - Initialize `AsteroidsGame` window
2. **Schedule training updates** - Use `arcade.schedule()` to run GA training steps
3. **Render best agent** - Show the best agent from current generation playing
4. **Display metrics** - Overlay training statistics on game window
5. **Generation transitions** - Optionally pause between generations to observe best agent

**Implementation Pattern:**

Similar to `train_agent.py`'s `AIDriver` class:

- Create game window
- Schedule update function that runs GA training steps
- Hook into `game.on_draw()` to display training metrics
- Use `arcade.run()` to start the game loop

**Key Difference from Headless Training:**

- Headless: `EpisodeRunner.run_episode()` manually calls `game.on_update()` in a loop
- Visual: Training uses `arcade.schedule()` and `arcade.run()` so rendering happens automatically
- Visual training may be slower but enables real-time observation of learning

### Mutation Operators

**File:** `ai_agents/genetic_algorithm/operators.py`

**Core Operators:**

```python
def mutate_gaussian(individual: List[float], mu: float, sigma: float, indpb: float) -> Tuple[List[float]]:
    """
    Gaussian mutation: add noise to parameters.

    Args:
        individual: Parameter vector
        mu: Mean of Gaussian (usually 0)
        sigma: Standard deviation
        indpb: Independent probability of mutating each parameter

    Returns:
        Mutated individual (tuple for DEAP)
    """
    pass

def mutate_uniform(individual: List[float], low: float, high: float, indpb: float) -> Tuple[List[float]]:
    """
    Uniform mutation: replace parameter with random value in range.

    Args:
        individual: Parameter vector
        low: Lower bound
        high: Upper bound
        indpb: Independent probability of mutating each parameter

    Returns:
        Mutated individual (tuple for DEAP)
    """
    pass
```

**Crossover Operators:**

```python
def crossover_blend(individual1: List[float], individual2: List[float], alpha: float) -> Tuple[List[float], List[float]]:
    """
    Blend crossover (BLX-alpha): create offspring between parents.

    Args:
        individual1: First parent
        individual2: Second parent
        alpha: Blend factor

    Returns:
        Two offspring (tuples for DEAP)
    """
    pass

def crossover_arithmetic(individual1: List[float], individual2: List[float]) -> Tuple[List[float], List[float]]:
    """
    Arithmetic crossover: weighted average of parents.

    Args:
        individual1: First parent
        individual2: Second parent

    Returns:
        Two offspring (tuples for DEAP)
    """
    pass
```

**Invariants:**

- Mutation preserves parameter vector size
- Crossover produces two offspring of same size
- Operators work with DEAP's expected format (tuples)

### Fitness Evaluation

**File:** `ai_agents/genetic_algorithm/fitness.py`

**Core Function:**

```python
def evaluate_fitness(individual: List[float],
                     state_encoder: VectorEncoder,
                     action_interface: ActionInterface,
                     episode_runner: EpisodeRunner,
                     reward_calculator: RewardCalculator,
                     num_episodes: int = 1) -> float:
    """
    Evaluate fitness of parameter vector by running episodes.

    Args:
        individual: Parameter vector
        state_encoder: VectorEncoder instance
        action_interface: ActionInterface instance
        episode_runner: EpisodeRunner instance
        reward_calculator: RewardCalculator instance
        num_episodes: Number of episodes to average (for robustness)

    Returns:
        Average total reward across episodes
    """
    pass
```

**Fitness Strategy:**

- Run one or more episodes per individual
- Use total episode reward as fitness
- Average across multiple episodes for robustness (optional)
- Higher reward = better fitness

**Invariants:**

- Uses EpisodeRunner (no direct game access)
- Uses RewardCalculator for rewards
- Returns single float (fitness score)

## Impacted Areas

**Files to Create:**

- `ai_agents/genetic_algorithm/__init__.py` - Package init
- `ai_agents/genetic_algorithm/ga_agent.py` - GA agent implementation
- `ai_agents/genetic_algorithm/ga_trainer.py` - Training loop
- `ai_agents/genetic_algorithm/operators.py` - Mutation and crossover
- `ai_agents/genetic_algorithm/fitness.py` - Fitness evaluation
- `ai_agents/genetic_algorithm/config.py` - GA-specific configuration (optional)

**Files to Modify:**

- `train_agent.py` - Add GA training entry point (or create separate `train_ga.py`)
- Configuration system (plan 006) - Add GA configuration section

**Dependencies:**

- Requires all infrastructure plans (001-006):
  - EnvironmentTracker and MetricsTracker (plans 001-002)
  - RewardCalculator (plan 003)
  - StateEncoder, VectorEncoder, ActionInterface (plan 004)
  - BaseAgent, EpisodeRunner (plan 005)
  - Configuration system (plan 006)
- External: DEAP library

**No Schema/State Machine Changes:**

- Game entities unchanged
- No CLI/config changes (beyond adding GA config)

## Incremental Implementation

### Step 1: Set up GA directory structure and dependencies

**Intent**: Create package structure and install DEAP

**Implementation:**

- [x] Create `ai_agents/neuroevolution/genetic_algorithm/` directory
- [x] Create `ai_agents/neuroevolution/genetic_algorithm/__init__.py`
- [x] Install DEAP: `pip install deap`
- [x] Verify DEAP installation

**Verification**: Can import DEAP, directory structure exists

### Step 2: Implement GAAgent

**Intent**: Create GA agent that implements BaseAgent interface

**Implementation:**

- [x] Create `ai_agents/neuroevolution/genetic_algorithm/ga_agent.py`
- [x] Implement `GAAgent.__init__()`:
  - Store parameter vector
  - Store state_encoder and action_interface
  - Calculate parameter vector size based on state encoder
- [x] Implement `get_action()`:
  - Encode state using VectorEncoder
  - Apply linear policy (or chosen policy type)
  - Convert action using ActionInterface
  - Return game input
- [x] Implement `reset()`:
  - No-op (GA has no internal state)
- [x] Add docstrings and type hints
- [x] Test with mock state encoder and action interface

**Verification**: GAAgent can be instantiated, implements BaseAgent, produces actions

### Step 3: Implement fitness evaluation

**Intent**: Create fitness function that uses EpisodeRunner

**Implementation:**

- [x] Create `ai_agents/neuroevolution/genetic_algorithm/ga_fitness.py`
- [x] Implement `evaluate_ga_fitness()`:
  - Create GAAgent from parameter vector
  - Run episode(s) using EpisodeRunner
  - Get EpisodeResult from EpisodeRunner
  - Extract `total_reward` from EpisodeResult (this is the fitness)
  - Note: `total_reward` comes from RewardCalculator, which uses MetricsTracker
    - RewardCalculator.calculate_step_reward() uses MetricsTracker each step
    - RewardCalculator.calculate_episode_reward() uses MetricsTracker at episode end
    - Reward components (AccuracyBonus, KPMBonus, etc.) use MetricsTracker metrics
  - Return average fitness across multiple episodes (if num_episodes > 1)
- [x] Handle edge cases (episode failures, etc.)
- [x] Add docstrings and type hints explaining the reward/metrics flow
- [x] Test with mock EpisodeRunner

**Verification**: Fitness function works with EpisodeRunner, returns valid fitness scores

**Note on MetricsTracker Usage:**

- MetricsTracker is used indirectly through RewardCalculator
- EpisodeRunner updates MetricsTracker each step
- RewardCalculator components use MetricsTracker to calculate rewards (accuracy, kills, time_alive, etc.)
- Fitness function uses EpisodeResult.total_reward (which aggregates all RewardCalculator rewards)
- This design keeps fitness evaluation simple: just use total_reward as fitness

### Step 4: Implement mutation and crossover operators

**Intent**: Create DEAP-compatible genetic operators

**Implementation:**

- [x] Create `ai_agents/neuroevolution/genetic_algorithm/operators.py`
- [x] Implement `mutate_gaussian()`:
  - Add Gaussian noise to parameters
  - Respect mutation probability
  - Return tuple (DEAP format)
- [x] Implement `mutate_uniform()`:
  - Replace parameters with uniform random values
  - Respect mutation probability
  - Return tuple (DEAP format)
- [x] Implement `crossover_blend()`:
  - Create offspring between parents
  - Return two tuples (DEAP format)
- [x] Implement `crossover_arithmetic()`:
  - Weighted average of parents
  - Return two tuples (DEAP format)
- [x] Add docstrings and type hints
- [x] Test operators independently

**Verification**: Operators work correctly, produce valid parameter vectors, compatible with DEAP

### Step 5: Implement GA trainer

**Intent**: Create evolutionary training loop using DEAP

**Implementation:**

- [x] Create `ai_agents/neuroevolution/genetic_algorithm/ga_trainer.py`
- [x] Implement `GATrainer.__init__()`:
  - Parse configuration
  - Initialize DEAP types (Individual, Population)
  - Register operators with DEAP
  - Set up state encoder, action interface, episode runner
- [x] Implement `evaluate_individual()`:
  - Call fitness evaluation function
  - Return fitness score
- [x] Implement `train()`:
  - Initialize population (random parameter vectors)
  - For each generation:
    - Evaluate population
    - Select parents (tournament selection)
    - Apply crossover and mutation
    - Replace population (elitism)
  - Return best agent
- [ ] Add logging/progress tracking
- [ ] Add docstrings and type hints
- [ ] Test with small population and few generations

**Verification**: Trainer runs, evolves population, returns best agent

### Step 6: Integrate with configuration system

**Intent**: Add GA configuration to configuration system

**Implementation:**

- [ ] Add GA configuration section to config system (plan 006):
  - Population size
  - Number of generations
  - Mutation rate and type
  - Crossover rate and type
  - Tournament size
  - State encoder configuration
  - Reward calculator configuration
- [ ] Update GATrainer to use configuration
- [ ] Test configuration loading

**Verification**: GA can be configured via configuration system

### Step 7: Create visual training entry point

**Intent**: Create script to run GA training with real-time visualization

**Implementation:**

- [ ] Create `training/train_ga.py`:
  - Import `AsteroidsGame`, `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `SCREEN_TITLE`
  - Create game window: `window = AsteroidsGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)`
  - Call `window.setup()` to initialize game
  - Initialize GATrainer with game instance
  - Create training driver class (similar to `AIDriver` in `train_agent.py`):
    - Store game window and GATrainer
    - Track current generation, population, best agent
    - Create info text overlay for training metrics
    - Hook into `game.on_draw()` to display metrics
  - Implement `update()` method scheduled with `arcade.schedule()`:
    - Run one generation of GA training
    - Update best agent if fitness improved
    - Display best agent playing (set game inputs from best agent)
    - Update info text with generation, fitness, metrics
    - Handle generation transitions
  - Call `arcade.run()` to start visual training loop
- [ ] Display training metrics on screen:
  - Generation number (e.g., "Generation: 5/100")
  - Best fitness (e.g., "Best Fitness: 1234.56")
  - Average fitness (e.g., "Avg Fitness: 987.65")
  - Current episode stats (steps, reward, kills, accuracy)
  - Best agent performance indicators
- [ ] Add command-line arguments (optional):
  - `--headless`: Run without visualization (faster, for long training)
  - `--generations`: Number of generations
  - `--population-size`: Population size
- [ ] Add logging to console (generation summaries, fitness improvements)
- [ ] Test visual training:
  - Window opens and displays game
  - Training metrics update on screen
  - Can watch best agent play
  - Training progresses generation by generation

**Verification**:

- Can run GA training with `python training/train_ga.py`
- Game window opens and displays Asteroids game
- Training metrics visible on screen
- Can watch AI learn and improve over generations
- Best agent plays visibly in game window

### Step 8: Add agent save/load

**Intent**: Save and load GA agents

**Implementation:**

- [ ] Implement `save_agent()` in GAAgent or utility:
  - Serialize parameter vector
  - Save configuration (state encoder, etc.)
  - Save to file (JSON or pickle)
- [ ] Implement `load_agent()`:
  - Load parameter vector
  - Reconstruct GAAgent
  - Return agent
- [ ] Integrate with agent save/load utilities (plan 006)
- [ ] Test save/load cycle

**Verification**: Can save and load GA agents, loaded agents work correctly

### Step 9: Testing and validation

**Intent**: Comprehensive testing of GA implementation

**Implementation:**

- [ ] Unit tests:
  - GAAgent action generation
  - Fitness evaluation
  - Mutation operators
  - Crossover operators
- [ ] Integration tests:
  - Full training loop (small population)
  - Agent save/load
  - Configuration loading
- [ ] Manual testing:
  - Run training for several generations
  - Verify fitness improves
  - Test trained agent in game
  - Verify agent behaviour

**Verification**: All tests pass, GA trains successfully, agents show learning

## Testing and Validation

**Unit Tests:**

- [ ] GAAgent: action generation, BaseAgent interface compliance
- [ ] Fitness evaluation: works with EpisodeRunner, returns valid scores
- [ ] Mutation operators: produce valid parameter vectors
- [ ] Crossover operators: produce valid offspring
- [ ] Configuration: loads correctly

**Integration Tests:**

- [ ] Full training loop: runs without errors, fitness improves
- [ ] Agent save/load: saves and loads correctly
- [ ] Works with all infrastructure: StateEncoder, ActionInterface, RewardCalculator, EpisodeRunner

**Manual Testing:**

```python
# Test visual GA training
# Run: python training/train_ga.py

# Expected behavior:
# 1. Game window opens showing Asteroids game
# 2. Training metrics displayed on screen (generation, fitness, etc.)
# 3. Best agent from each generation plays visibly
# 4. Can observe AI learning and improving over generations
# 5. Metrics update in real-time as training progresses

# Test headless GA training (optional)
# Run: python training/train_ga.py --headless --generations 50

# Test trained agent
from ai_agents.neuroevolution.genetic_algorithm.ga_agent import GAAgent
from training.base.EpisodeRunner import EpisodeRunner
# ... run episode with best_agent ...
```

**Expected Signals:**

- GA training runs without errors
- **Game window opens and displays game during training**
- **Training metrics visible on screen (generation, fitness, stats)**
- **Can watch best agent play in real-time**
- **Observe behavioural improvements over generations**
- Fitness improves over generations
- Trained agents show reasonable behaviour
- Agents can be saved and loaded
- All infrastructure components work together

## Risks and Failure Modes

**Parameter Vector Design Issues:**

- **Risk**: Parameter vector too large/small, poor policy representation
- **Mitigation**: Start with simple linear policy, experiment with sizes, validate with small tests
- **Detection**: Test with known-good parameter vectors, verify actions are reasonable

**Fitness Evaluation Issues:**

- **Risk**: Fitness too noisy, doesn't reflect true performance
- **Mitigation**: Average over multiple episodes, use consistent reward structure
- **Detection**: Monitor fitness variance, check if best agents actually perform well

**Evolutionary Algorithm Issues:**

- **Risk**: Population converges too quickly or not at all
- **Mitigation**: Tune mutation/crossover rates, use appropriate selection pressure
- **Detection**: Monitor population diversity, check convergence patterns

**Integration Issues:**

- **Risk**: GA doesn't work with infrastructure components
- **Mitigation**: Test each component integration separately, use type hints
- **Detection**: Integration tests, verify all interfaces match

**Performance Issues:**

- **Risk**: Training too slow (fitness evaluation is expensive)
- **Mitigation**: Optimize fitness evaluation, consider parallel evaluation later
- **Detection**: Profile training time, check bottlenecks

**Visualization Issues:**

- **Risk**: Training loop conflicts with arcade rendering, window doesn't update
- **Mitigation**: Use `arcade.schedule()` properly, ensure `arcade.run()` is called, test rendering
- **Detection**: Window doesn't open, game doesn't render, metrics don't update

- **Risk**: Training too slow with visualization (rendering overhead)
- **Mitigation**: Option for headless mode (`--headless` flag), optimize rendering, consider showing only best agent
- **Detection**: Training takes significantly longer than headless mode

- **Risk**: Metrics overlay blocks game view or is unreadable
- **Mitigation**: Position metrics carefully, use readable fonts/colors, make overlay optional
- **Detection**: Can't see game clearly, metrics hard to read

## Exit Criteria

**Correctness:**

- [ ] GAAgent implements BaseAgent interface correctly
- [ ] GA training loop runs without errors
- [ ] Fitness evaluation works with EpisodeRunner
- [ ] Mutation and crossover operators work correctly
- [ ] Agents can be saved and loaded

**Integration:**

- [ ] Works with all infrastructure (StateEncoder, ActionInterface, RewardCalculator, BaseAgent, EpisodeRunner)
- [ ] Configuration system supports GA
- [ ] Training produces trained agents

**Functionality:**

- [ ] GA can train for multiple generations
- [ ] Fitness improves over generations (or at least doesn't degrade)
- [ ] Trained agents show reasonable behaviour in game
- [ ] Agents can be evaluated and compared
- [ ] **Visual training works** - game window displays during training
- [ ] **Training metrics visible** - generation, fitness, stats displayed on screen
- [ ] **Can watch AI learn** - observe behavioural improvements over generations
- [ ] **Best agent plays visibly** - see the best agent from each generation in action

**Code Quality:**

- [ ] All classes have comprehensive docstrings
- [ ] Type hints added to all public methods
- [ ] Code is testable and tested
- [ ] Follows project coding standards

**Documentation:**

- [ ] `plans/README.md` updated with plan status
- [ ] `plans/ARCHITECTURE.md` updated with GA implementation
- [ ] Usage examples in docstrings
- [ ] Configuration documented

## Future Considerations

**Immediate Follow-ons:**

- Tune hyperparameters (population size, mutation rate, etc.)
- Experiment with different parameter vector designs
- Add more sophisticated selection methods
- Add elitism and other advanced GA techniques

**Advanced GA Features:**

- Niching and speciation (maintain diversity)
- Multi-objective optimization (Pareto fronts)
- Adaptive mutation rates
- Parallel fitness evaluation
- Island models (multiple populations)

**Policy Design Experiments:**

- Try different policy representations (threshold, heuristic, etc.)
- Compare interpretability vs performance
- Analyze evolved parameter vectors

**Visualization Enhancements:**

- Option to show multiple agents playing simultaneously (population view)
- Generation-by-generation replay (watch evolution of best agent)
- Fitness curve visualization (plot fitness over generations)
- Behavioural comparison tools (compare agents from different generations)

**Integration with Dashboard:**

- Add GA to training dashboard (when implemented)
- Real-time visualization of population fitness
- Generation-by-generation progress tracking

---

**Status**: planned

**Dependencies:**

- Plans 001-006 must be complete before starting this plan
- DEAP library must be installed

**Last Updated**: 2025-01-XX
