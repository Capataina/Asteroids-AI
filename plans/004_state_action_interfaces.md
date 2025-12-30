# State and Action Interface Standardization

## Goal and Scope

**Deliverables:**

- `interfaces/StateEncoder` base class and interface
- Vector encoder implementation (for GA/ES/NEAT)
- Graph encoder refactoring (for GNN)
- Sensor encoder (optional, for future use)
- `interfaces/ActionInterface` for action standardization
- Consistent state/action format across all AI methods

**Out of Scope:**

- Specific feature engineering details (will be refined during implementation)
- Advanced encodings (future enhancement)
- Action space modifications (future enhancement)

## Context and Justification

**Why Now:**

- Different AI methods need different state representations
- Current graph encoding is tightly coupled to PyTorch
- Need consistent interface for all AI methods
- Vector encoding needed for GA/ES/NEAT
- Action format needs standardization

**What It Enables:**

- Swappable state encodings for experimentation
- Consistent interface for all AI methods
- Easy to add new encodings
- Clean separation: state encoding separate from AI logic

**Key Requirements:**

- Must use EnvironmentTracker as input
- Must support different representation types (vector, graph, sensor)
- Must normalize/standardize outputs appropriately
- Actions must be in consistent format

## Interfaces and Contracts

### StateEncoder Base Interface

**Core Methods:**
- `encode(env_tracker) -> state` - Convert tracker state to AI representation
- `get_state_size() -> int` - Size of encoded state (for fixed-size encodings)
- `reset()` - Reset any internal state (if needed)

**Encoder Types:**

1. **VectorEncoder** - Fixed-size vector for GA/ES/NEAT
   - Features: player position, velocity, angle, nearest asteroid, distances, etc.
   - Normalized values
   - Fixed dimensionality

2. **GraphEncoder** - Graph representation for GNN
   - Nodes: player, asteroids, bullets
   - Edges: proximity-based
   - PyTorch Geometric format

3. **SensorEncoder** - Sensor-based encoding (optional)
   - Nearest N asteroids
   - Relative positions
   - Distance/angle features

### ActionInterface

**Core Methods:**
- `validate(action) -> bool` - Check action validity
- `normalize(action) -> action` - Normalize action values
- `get_action_space_size() -> int` - Size of action space

**Action Format:**

- Standard: `[left, right, thrust, shoot]`
- Can be boolean or continuous (0.0-1.0)
- Must be consistent across all AI methods

**Invariants:**

- State encoders use only EnvironmentTracker
- Actions are in standard format
- Encoders handle edge cases (empty lists, etc.)

## Impacted Areas

**Files to Create:**

- `interfaces/StateEncoder.py` (base class)
- `interfaces/encoders/vector.py`
- `interfaces/encoders/graph.py` (refactor existing)
- `interfaces/encoders/sensor.py` (optional)
- `interfaces/ActionInterface.py`

**Files to Modify:**

- `ai_agents/reinforcement_learning/gnn_and_sac/env_wrapper.py` - Use GraphEncoder (deferred: wrapper refactoring happens after infrastructure complete)
- **Note**: `train_agent.py` integration is deferred to plan 005 (BaseAgent/EpisodeRunner infrastructure). StateEncoder and ActionInterface will be integrated via EpisodeRunner, not directly into current `train_agent.py`.
- All future AI methods will use these interfaces

**Dependencies:**

- Requires EnvironmentTracker (complete)
- Will be used by BaseAgent and EpisodeRunner (next plan)

## Implementation Notes

**Vector Encoding:**

- Extract relevant features from EnvironmentTracker
- Normalize all values (0-1 range typically)
- Fixed size for compatibility with GA/ES/NEAT
- Features: player state, nearest asteroid, distances, velocities, etc.

**Graph Encoding:**

- Refactor existing graph construction logic
- Keep PyTorch Geometric format for GNN
- Make it a proper StateEncoder subclass
- Use EnvironmentTracker instead of direct game access

**Action Standardization:**

- All AI methods output same action format
- Validation ensures actions are in valid range
- Normalization handles different output types

## Testing and Validation

**Unit Tests:**

- Each encoder independently
- State size consistency
- Normalization correctness
- Edge cases (empty lists, etc.)

**Integration Tests:**

- Works with EnvironmentTracker
- Actions are in correct format
- Encoders produce expected output

## Exit Criteria

**Correctness:**

- All encoders work correctly
- Actions are standardized
- No direct game access in encoders

**Integration:**

- Works with tracking infrastructure
- Ready for BaseAgent use
- Consistent across all methods

## Future Considerations

**Follow-ons:**

- More encoder types
- Feature engineering experiments
- State compression/abstraction
- Multi-scale encodings
- Attention mechanisms

---

**Note:** This is a skeleton plan file. Once plans 001-003 are completed, this plan will be expanded into a full implementation plan with detailed steps, encoder specifications, and risk analysis.

