# Plans Index

This directory contains implementation plans for features, refactors, and milestones.

## Active Plans

| Plan                                                                                 | Purpose                                                                     | Status      | Last Updated |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- | ----------- | ------------ |
| [001_environment_tracker.md](001_environment_tracker.md)                             | Implement EnvironmentTracker and MetricsTracker for unified AI state access | complete    | 2025         |
| [002_metrics_tracker.md](002_metrics_tracker.md)                                     | Complete MetricsTracker implementation for episode-level statistics         | complete    | 2025         |
| [003_reward_system.md](003_reward_system.md)                                         | Component-based RewardCalculator system and score removal from game logic   | complete    | 2025         |
| [004_state_action_interfaces.md](004_state_action_interfaces.md)                     | Standardize state encoders and action interface for all AI methods          | planned     | 2025         |
| [005_base_agent_episode_infrastructure.md](005_base_agent_episode_infrastructure.md) | Create BaseAgent interface and EpisodeRunner shared infrastructure          | planned     | 2025         |
| [006_configuration_utilities.md](006_configuration_utilities.md)                     | Configuration system and agent save/load utilities                          | planned     | 2025         |

## Plan Status

**Completed Plans:**
- **001_environment_tracker**: EnvironmentTracker and MetricsTracker implemented and integrated
- **002_metrics_tracker**: MetricsTracker complete with episode-level statistics
- **003_reward_system**: Component-based RewardCalculator system complete with 6 reward components, score removed from game

**Expanded Plans:**
- **004_state_action_interfaces**: Fully expanded with detailed implementation steps, encoder specifications, and testing requirements

**Skeleton Plans:**
- **005_base_agent_episode_infrastructure**: Skeleton plan outlining BaseAgent interface and EpisodeRunner
- **006_configuration_utilities**: Skeleton plan outlining configuration system and utilities

**Note:** Plans 001-003 are complete. Plan 004 is now fully expanded. Plans 005-006 are skeleton plans that will be expanded once their prerequisites are completed.

## Implementation Order

These plans represent the preliminary infrastructure needed before implementing any AI methods:

1. **001_environment_tracker** - ✅ Complete: EnvironmentTracker and MetricsTracker implemented
2. **002_metrics_tracker** - ✅ Complete: MetricsTracker implementation complete
3. **003_reward_system** - ✅ Complete: Component-based RewardCalculator system with 6 components, score removed from game
4. **004_state_action_interfaces** - 🔄 Planned: State encoders (VectorEncoder, GraphEncoder) and ActionInterface
5. **005_base_agent_episode_infrastructure** - ⏳ Pending: BaseAgent and EpisodeRunner (integrates all previous infrastructure into training loop)
6. **006_configuration_utilities** - ⏳ Pending: Configuration and utilities

**Important**: Plans 001-004 create infrastructure components but do NOT modify `train_agent.py`. Plan 005 (BaseAgent/EpisodeRunner) is responsible for integrating all infrastructure (EnvironmentTracker, MetricsTracker, RewardCalculator, StateEncoder, ActionInterface) into the training loop. The current `train_agent.py` is temporary/legacy code that will be refactored in plan 005.

**Current Progress:**
- ✅ Core tracking infrastructure (plans 001-002)
- ✅ Reward system (plan 003)
- 🔄 State/action interfaces (plan 004) - next to implement
- ⏳ Episode infrastructure (plan 005) - blocked on plan 004
- ⏳ Configuration (plan 006) - blocked on plan 005

After these plans are complete, we can begin implementing the 5 AI methods:

- Genetic Algorithms (GA) - DEAP
- Genetic Programming (GP) - DEAP
- Evolution Strategies (ES) - TensorFlow
- Neuroevolution (NEAT) - Python-NEAT
- Graph-Based RL (GNN+SAC) - PyTorch

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the repository structure and subsystem overview.
