# Genetic Algorithm Implementation

## Goal and Scope

**Deliverables:**

- `ai_agents/genetic_algorithm/` directory structure
- `ai_agents/genetic_algorithm/ga_agent.py` - GA agent implementing BaseAgent interface
- `ai_agents/genetic_algorithm/ga_trainer.py` - DEAP-based evolutionary training loop
- `ai_agents/genetic_algorithm/operators.py` - Mutation and crossover operators
- `ai_agents/genetic_algorithm/fitness.py` - Fitness evaluation using EpisodeRunner
- Working GA implementation that can train and evolve parameter vectors
- Integration with all infrastructure (StateEncoder, ActionInterface, RewardCalculator, BaseAgent, EpisodeRunner)

**Out of Scope:**

- Advanced GA techniques (niching, speciation, etc.) - can be added later
- Multi-objective optimization - future enhancement
- Parallel evaluation (can be added incrementally)
- Training dashboard integration (deferred until all AIs work)

## Context and Justification

**Why Now:**

- All prerequisite infrastructure is complete (plans 001-006)
- GA is the first AI method to implement (incremental approach)
- GA provides a good baseline for comparison with other methods
- DEAP is a mature library well-suited for this task
- GA implementation will validate the shared infrastructure design

**What It Enables:**

- First working AI method in the system
- Validates BaseAgent, EpisodeRunner, StateEncoder, ActionInterface design
- Provides baseline performance for comparison
- Demonstrates the evolutionary training paradigm
- Foundation for understanding how parameter vectors control behaviour

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

- [ ] Create `ai_agents/neuroevolution/genetic_algorithm/ga_trainer.py`
- [ ] Implement `GATrainer.__init__()`:
  - Parse configuration
  - Initialize DEAP types (Individual, Population)
  - Register operators with DEAP
  - Set up state encoder, action interface, episode runner
- [ ] Implement `evaluate_individual()`:
  - Call fitness evaluation function
  - Return fitness score
- [ ] Implement `train()`:
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

### Step 7: Create training entry point

**Intent**: Create script to run GA training

**Implementation:**

- [ ] Create `train_ga.py` or update `train_agent.py`:
  - Load configuration
  - Initialize GATrainer
  - Run training
  - Save best agent
  - Display results
- [ ] Add command-line arguments (optional)
- [ ] Add logging
- [ ] Test end-to-end training

**Verification**: Can run GA training from command line, produces trained agent

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
# Test GA training
from ai_agents.neuroevolution.genetic_algorithm.ga_trainer import GATrainer
from training.config import load_config

config = load_config("ga_config.yaml")
trainer = GATrainer(config)
best_agent = trainer.train()

# Test trained agent
from ai_agents.neuroevolution.genetic_algorithm.episode_runner import EpisodeRunner
# ... run episode with best_agent ...
```

**Expected Signals:**

- GA training runs without errors
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
