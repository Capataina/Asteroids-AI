# Plans Index

This directory contains implementation plans for features, refactors, and milestones.

## Active Plans

| Plan                                                                                 | Purpose                                                                     | Status      | Last Updated |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- | ----------- | ------------ |
| [001_environment_tracker.md](001_environment_tracker.md)                             | Implement EnvironmentTracker and MetricsTracker for unified AI state access | in_progress | 2025         |
| [002_metrics_tracker.md](002_metrics_tracker.md)                                     | Complete MetricsTracker implementation for episode-level statistics         | planned     | 2025         |
| [003_reward_system.md](003_reward_system.md)                                         | Component-based RewardCalculator system and score removal from game logic   | planned     | 2025         |
| [004_state_action_interfaces.md](004_state_action_interfaces.md)                     | Standardize state encoders and action interface for all AI methods          | planned     | 2025         |
| [005_base_agent_episode_infrastructure.md](005_base_agent_episode_infrastructure.md) | Create BaseAgent interface and EpisodeRunner shared infrastructure          | planned     | 2025         |
| [006_configuration_utilities.md](006_configuration_utilities.md)                     | Configuration system and agent save/load utilities                          | planned     | 2025         |

## Plan Status

**Note:** Plans 003 is now fully expanded with component-based architecture. Plans 002, 004-006 are currently skeleton plans that outline direction and goals. They will be expanded into full implementation plans once their prerequisite plans are completed. These skeleton plans focus on **what** we want to implement rather than **how** to implement it, keeping the design flexible as we progress.

## Implementation Order

These plans represent the preliminary infrastructure needed before implementing any AI methods:

1. **001_environment_tracker** - Complete EnvironmentTracker (event detection) and MetricsTracker
2. **002_metrics_tracker** - Complete MetricsTracker implementation (if not fully covered in 001)
3. **003_reward_system** - Component-based RewardCalculator system (modular, composable components) and score removal from game
4. **004_state_action_interfaces** - State encoders and action standardization
5. **005_base_agent_episode_infrastructure** - BaseAgent and EpisodeRunner (integrates all previous infrastructure into training loop)
6. **006_configuration_utilities** - Configuration and utilities

**Important**: Plans 002-004 create infrastructure components but do NOT modify `train_agent.py`. Plan 005 (BaseAgent/EpisodeRunner) is responsible for integrating all infrastructure (MetricsTracker, RewardCalculator, StateEncoder, ActionInterface) into the training loop. The current `train_agent.py` is temporary/legacy code that will be refactored in plan 005.

After these plans are complete, we can begin implementing the 5 AI methods:

- Genetic Algorithms (GA) - DEAP
- Genetic Programming (GP) - DEAP
- Evolution Strategies (ES) - TensorFlow
- Neuroevolution (NEAT) - Python-NEAT
- Graph-Based RL (GNN+SAC) - PyTorch

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the repository structure and subsystem overview.
