# Plans Index

This directory contains implementation plans for features, refactors, and milestones.

## Active Plans

| Plan                                                                                 | Purpose                                                                     | Status      | Last Updated |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- | ----------- | ------------ |
| [001_environment_tracker.md](001_environment_tracker.md)                             | Implement EnvironmentTracker and MetricsTracker for unified AI state access | complete    | 2025         |
| [002_metrics_tracker.md](002_metrics_tracker.md)                                     | Complete MetricsTracker implementation for episode-level statistics         | complete    | 2025         |
| [003_reward_system.md](003_reward_system.md)                                         | Component-based RewardCalculator system and score removal from game logic   | complete    | 2025         |
| [004_state_action_interfaces.md](004_state_action_interfaces.md)                     | Standardize state encoders and action interface (GA-first, extensible)     | planned     | 2025         |
| [005_base_agent_episode_infrastructure.md](005_base_agent_episode_infrastructure.md) | Create BaseAgent interface and EpisodeRunner (GA-first, extensible)       | planned     | 2025         |
| [006_configuration_utilities.md](006_configuration_utilities.md)         | Configuration system and agent save/load utilities (GA-first, extensible) | planned     | 2025         |
| [007_genetic_algorithm_implementation.md](007_genetic_algorithm_implementation.md) | Implement Genetic Algorithm using DEAP                                      | planned     | 2025         |

## Plan Status

**Completed Plans:**
- **001_environment_tracker**: EnvironmentTracker and MetricsTracker implemented and integrated
- **002_metrics_tracker**: MetricsTracker complete with episode-level statistics
- **003_reward_system**: Component-based RewardCalculator system complete with 6 reward components, score removed from game

**Expanded Plans:**
- **004_state_action_interfaces**: Fully expanded with detailed implementation steps, encoder specifications, and testing requirements (GA-first approach)
- **007_genetic_algorithm_implementation**: Fully expanded with detailed GA implementation plan

**Skeleton Plans:**
- **005_base_agent_episode_infrastructure**: Skeleton plan outlining BaseAgent interface and EpisodeRunner (GA-first approach)
- **006_configuration_utilities**: Skeleton plan outlining configuration system and utilities (GA-first approach)

**Note:** Plans 001-003 are complete. Plan 004 is fully expanded with GA-first approach. Plans 005-006 are skeleton plans with GA-first approach noted. Plan 007 is the GA implementation plan. All infrastructure plans (004-006) focus on GA requirements first, with extensibility for other AI methods.

## Implementation Order

**Incremental Approach - GA First:**

The infrastructure plans (004-006) are designed to support all AI methods, but the initial implementation focuses on **Genetic Algorithms (GA) requirements only**. The infrastructure is extensible, allowing us to add support for other AI methods incrementally as each is implemented.

### Infrastructure Phase (Plans 001-006)

1. **001_environment_tracker** - ✅ Complete: EnvironmentTracker and MetricsTracker implemented
2. **002_metrics_tracker** - ✅ Complete: MetricsTracker implementation complete
3. **003_reward_system** - ✅ Complete: Component-based RewardCalculator system with 6 components, score removed from game
4. **004_state_action_interfaces** - 🔄 Planned: State encoders and ActionInterface (GA-first: VectorEncoder, extensible for others)
5. **005_base_agent_episode_infrastructure** - ⏳ Pending: BaseAgent and EpisodeRunner (GA-first, extensible)
6. **006_configuration_utilities** - ⏳ Pending: Configuration and utilities (GA-first, extensible)

**Important**: Plans 001-004 create infrastructure components but do NOT modify `train_agent.py`. Plan 005 (BaseAgent/EpisodeRunner) is responsible for integrating all infrastructure (EnvironmentTracker, MetricsTracker, RewardCalculator, StateEncoder, ActionInterface) into the training loop. The current `train_agent.py` is temporary/legacy code that will be refactored in plan 005.

**Current Progress:**
- ✅ Core tracking infrastructure (plans 001-002)
- ✅ Reward system (plan 003)
- 🔄 State/action interfaces (plan 004) - next to implement (GA-focused)
- ⏳ Episode infrastructure (plan 005) - blocked on plan 004 (GA-focused)
- ⏳ Configuration (plan 006) - blocked on plan 005 (GA-focused)

### AI Implementation Phase

After infrastructure plans (001-006) are complete, we begin implementing AI methods:

7. **007_genetic_algorithm_implementation** - ⏳ Planned: First AI method implementation using DEAP

**Future AI Methods** (to be implemented after GA):
- Genetic Programming (GP) - DEAP
- Evolution Strategies (ES) - TensorFlow
- Neuroevolution (NEAT) - Python-NEAT
- Graph-Based RL (GNN+SAC) - PyTorch

**Strategy**: Each AI method will be implemented incrementally. As new methods are added, the shared infrastructure (BaseAgent, EpisodeRunner, StateEncoder, etc.) will be extended if needed, but the core design supports all methods from the start.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the repository structure and subsystem overview.
