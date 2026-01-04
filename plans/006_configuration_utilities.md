# Configuration and Utilities

## Implementation Strategy

**Incremental Approach - GA First:**

This plan establishes configuration and utility systems that will be shared across all AI methods. However, the initial implementation focuses on **Genetic Algorithms (GA) requirements only**. The infrastructure is designed to be extensible, allowing us to add support for other AI methods (ES, NEAT, GP, GNN) incrementally as each is implemented.

**Phase 1 (Current):** Implement utilities needed for GA:
- Configuration system for GA hyperparameters
- GA agent save/load functionality
- Episode lifecycle management for GA
- GA-specific utility functions

**Phase 2+ (Future):** As other AI methods are implemented:
- Configuration system will be extended with other method-specific settings
- Agent save/load will support additional agent types
- Utilities will be extended as needed

This approach allows us to:
- Get GA working quickly with proper configuration and utilities
- Validate the configuration/utility design with real usage
- Evolve the infrastructure based on actual needs from GA implementation
- Ensure the shared infrastructure is solid before adding other methods

## Goal and Scope

**Deliverables:**

- Configuration system for swapping components (reward functions, encoders, hyperparameters)
- Agent save/load functionality
- Enhanced episode lifecycle management
- Utility functions for experimentation

**Out of Scope:**

- Advanced configuration UI (future enhancement)
- Configuration validation (can be added incrementally)
- Distributed training configuration (future enhancement)

## Context and Justification

**Why Now:**

- GA implementation (plan 007) needs configuration for hyperparameters
- Need to save/load GA agents for comparison
- Need consistent configuration across GA experiments
- Foundation for experimentation and comparison (starting with GA)

**What It Enables:**

- Easy experimentation with different settings
- Reproducible experiments
- Agent persistence for comparison
- Configuration-driven training

**Key Requirements:**

- Must support swapping: reward functions, state encoders, GA hyperparameters (initially)
- Must support GA agent serialization (extensible for other methods)
- Must be easy to use and extend
- Configuration system must be extensible for future AI methods

## Interfaces and Contracts

### Configuration System

**Core Features (Phase 1 - GA):**
- Reward function selection
- State encoder selection (VectorEncoder for GA)
- GA hyperparameter configuration (population size, mutation rate, crossover rate, etc.)
- Training parameters (episodes, generations, etc.)

**Core Features (Phase 2+ - Future):**
- Additional hyperparameters for other AI methods
- Method-specific configuration sections

**Configuration Format:**

- YAML/JSON files or programmatic
- Easy to modify and experiment
- Supports defaults and overrides

### Agent Save/Load

**Core Methods:**
- `save_agent(agent, path)` - Serialize agent to file
- `load_agent(path) -> agent` - Deserialize agent from file
- Agent format should be method-agnostic where possible

**Use Cases (Phase 1 - GA):**

- Save best GA agents
- Load GA agents for evaluation/comparison
- Resume GA training from checkpoint

**Use Cases (Phase 2+ - Future):**

- Save best agents from each method
- Load for evaluation/comparison across methods
- Resume training from checkpoint for any method

### Episode Lifecycle Enhancements

**Core Features:**
- Clear reset/done conditions
- Episode statistics collection
- Optional callbacks (on_start, on_end)
- Episode metadata

## Impacted Areas

**Files to Create:**

- `training/config.py` (configuration system)
- `training/utils/agent_io.py` (save/load)
- `training/utils/episode_lifecycle.py` (enhanced lifecycle)

**Files to Modify:**

- All trainers will use configuration
- EpisodeRunner may use lifecycle enhancements
- Training scripts will use configuration

**Dependencies:**

- Requires BaseAgent (plan 005)
- Will be used by all AI implementations

## Implementation Notes

**Configuration Design:**

- Simple, extensible format
- Supports component swapping
- Easy to experiment with
- Can be file-based or programmatic

**Agent Serialization:**

- Each AI method handles its own serialization
- Common interface for save/load
- Format should be readable/versioned
- Initially implemented for GA, extensible for other methods

**Lifecycle Management:**

- Clear state transitions
- Optional hooks for customization
- Metadata collection

## Testing and Validation

**Unit Tests:**

- Configuration loading
- Agent save/load
- Lifecycle management

**Integration Tests:**

- Configuration works with trainers
- Agents can be saved and loaded
- Lifecycle works correctly

## Exit Criteria

**Correctness:**

- Configuration system works
- Agents can be saved/loaded
- Lifecycle management works

**Integration:**

- Works with all previous plans (001-005, GA-focused)
- Ready for GA implementation (plan 007)
- Easy to experiment with GA
- Infrastructure ready for future AI methods

## Future Considerations

**Follow-ons:**

- Configuration UI
- Advanced validation
- Experiment tracking
- Hyperparameter optimization
- Distributed configuration

---

**Implementation Phases:**
- **Phase 1 (Current)**: GA-focused implementation (GA configuration, GA agent save/load, GA utilities)
- **Phase 2+ (Future)**: Extended configuration and utilities as other AI methods are added

**Note:** This is a skeleton plan file. Once plans 001-005 are completed, this plan will be expanded into a full implementation plan with detailed steps, configuration format specifications, and risk analysis. The initial implementation will focus on GA requirements, with the infrastructure designed to be extensible for other methods.

