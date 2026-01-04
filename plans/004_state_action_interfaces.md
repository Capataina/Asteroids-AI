# State and Action Interface Standardization

## Implementation Strategy

**Incremental Approach - GA First:**

This plan establishes the foundation for state and action interfaces that will be shared across all AI methods. However, the initial implementation focuses on **Genetic Algorithms (GA) requirements only**. The infrastructure is designed to be extensible, allowing us to add support for other AI methods (ES, NEAT, GP, GNN) incrementally as each is implemented.

**Phase 1 (Current):** Implement interfaces needed for GA:

- StateEncoder base class (foundation for all encoders)
- VectorEncoder (fixed-size vector for GA)
- ActionInterface (verify/adjust for GA)

**Phase 2+ (Future):** As other AI methods are implemented:

- GraphEncoder will be added when implementing GNN
- Additional encoders can be added for ES, NEAT, GP as needed
- The shared StateEncoder base class ensures consistency

This approach allows us to:

- Get GA working quickly with proper infrastructure
- Validate the interface design with real usage
- Evolve the infrastructure based on actual needs
- Avoid over-engineering for methods not yet implemented

## Goal and Scope

**Deliverables:**

- `interfaces/StateEncoder.py` - Abstract base class for state encoders
- `interfaces/encoders/VectorEncoder.py` - Fixed-size vector encoding for GA/ES/NEAT
- `interfaces/encoders/GraphEncoder.py` - Graph encoding for GNN (refactored from existing)
- `interfaces/ActionInterface.py` - Action validation and normalization interface
- Consistent state/action format across all AI methods
- All encoders use EnvironmentTracker (no direct game access)

**Out of Scope:**

- Sensor encoder (optional, can be added later if needed)
- Advanced encodings (attention mechanisms, multi-scale, etc.)
- Action space modifications (sticking with 4 actions: left, right, thrust, shoot)
- Edge construction for graph encoder (can be added incrementally)

## Context and Justification

**Why Now:**

- Different AI methods need different state representations:
  - **GA/ES/NEAT**: Fixed-size vector (neural network input)
  - **GNN+SAC**: Graph representation (PyTorch Geometric)
- Current graph encoding in `env_wrapper.py` directly accesses `self.game.*` (61 references)
- Need consistent interface for all AI methods
- Vector encoding doesn't exist yet (needed for 3 of 5 AI methods)
- Action format needs standardization (currently boolean threshold in wrapper)

**What It Enables:**

- Swappable state encodings for experimentation
- Consistent interface for all AI methods
- Easy to add new encodings without modifying AI code
- Clean separation: state encoding separate from AI logic
- Standardized action format (boolean or continuous)
- All encoders use EnvironmentTracker (stable API)

**Rejected Alternatives:**

- **Single encoder type**: Different methods need different representations
- **Keep direct game access**: Too fragile, breaks when game changes
- **Action format per method**: Inconsistent, harder to compare methods

**Key Requirements:**

- Must use EnvironmentTracker as input (no direct game access)
- Must support different representation types (vector, graph)
- Must normalize/standardize outputs appropriately
- Actions must be in consistent format: `[left, right, thrust, shoot]`
- Encoders must handle edge cases (empty lists, None values)

## Interfaces and Contracts

### StateEncoder Base Interface

**Abstract Base Class:** `StateEncoder` (in `interfaces/StateEncoder.py`)

```python
from abc import ABC, abstractmethod
from typing import Any
from interfaces.EnvironmentTracker import EnvironmentTracker

class StateEncoder(ABC):
    @abstractmethod
    def encode(self, env_tracker: EnvironmentTracker) -> Any:
        """
        Convert EnvironmentTracker state to AI representation.

        Args:
            env_tracker: EnvironmentTracker instance with current game state

        Returns:
            Encoded state (type depends on encoder: vector, graph, etc.)
        """
        pass

    @abstractmethod
    def get_state_size(self) -> int:
        """
        Get the size of encoded state (for fixed-size encodings).
        Returns -1 for variable-size encodings (e.g., graphs).

        Returns:
            State size (int) or -1 if variable-size
        """
        pass

    def reset(self) -> None:
        """
        Reset any internal state (if needed).
        Default implementation does nothing.
        """
        pass
```

**Invariants:**

- `encode()` uses only EnvironmentTracker (no direct game access)
- `encode()` handles edge cases gracefully (empty lists, None values)
- `get_state_size()` returns consistent value (or -1 for variable-size)
- `reset()` is called at episode start (if encoder has internal state)

### VectorEncoder Interface

**Class:** `VectorEncoder` (in `interfaces/encoders/VectorEncoder.py`)

**Features to Encode:**

1. **Player State** (6 features):

   - Normalized x position (0-1)
   - Normalized y position (0-1)
   - Normalized x velocity (-1 to 1, clamped)
   - Normalized y velocity (-1 to 1, clamped)
   - Sin of angle (direction)
   - Cos of angle (direction)

2. **Nearest Asteroid** (6 features, or zeros if none):

   - Normalized relative x position (-1 to 1)
   - Normalized relative y position (-1 to 1)
   - Normalized distance (0-1, using max possible distance)
   - Normalized relative x velocity (-1 to 1)
   - Normalized relative y velocity (-1 to 1)
   - Normalized size (0-1)

3. **Nearest N Asteroids** (optional, for richer representation):

   - If encoding nearest 3 asteroids: 18 features (3 × 6)
   - If no asteroid at position: zeros

4. **Nearest Bullet** (optional, 4 features):

   - Normalized relative x position
   - Normalized relative y position
   - Normalized distance
   - Normalized relative velocity magnitude

5. **Global State** (optional, 2 features):
   - Normalized asteroid count (0-1, using max expected)
   - Normalized bullet count (0-1, using max expected)

**Total Vector Size:**

- **Minimal**: 12 features (player + nearest asteroid)
- **Recommended**: 18 features (player + nearest 2 asteroids)
- **Extended**: 24+ features (player + nearest 3 asteroids + bullet + global)

**Normalization:**

- Positions: Divide by screen dimensions (800, 600)
- Velocities: Divide by max expected velocity (10.0 for player, 5.0 for asteroids)
- Distances: Divide by max possible distance (diagonal: sqrt(800² + 600²) ≈ 1000)
- Angles: Convert to sin/cos (already normalized -1 to 1)
- Counts: Divide by max expected (e.g., 20 asteroids, 10 bullets)

**Edge Cases:**

- No player: Return zeros for player features (shouldn't happen, but handle gracefully)
- No asteroids: Return zeros for asteroid features
- No bullets: Return zeros for bullet features
- Empty lists: Return zeros for all features

### GraphEncoder Interface

**Class:** `GraphEncoder` (in `interfaces/encoders/GraphEncoder.py`)

**Refactoring from:** `ai_agents/reinforcement_learning/gnn_and_sac/env_wrapper.py._get_graph_state()`

**Node Features:**

1. **Player Node** (6 features, type 0):

   - Normalized x position
   - Normalized y position
   - Normalized x velocity
   - Normalized y velocity
   - Sin of angle
   - Cos of angle

2. **Asteroid Nodes** (6 features, type 1):

   - Normalized x position
   - Normalized y position
   - Normalized x velocity
   - Normalized y velocity
   - Normalized size (scale / 1.25)
   - Normalized HP (hp / 3.0)

3. **Bullet Nodes** (6 features, type 2):
   - Normalized x position
   - Normalized y position
   - Normalized x velocity
   - Normalized y velocity
   - Normalized lifetime (lifetime / 60.0)
   - Padding (0.0) to match feature dimension

**Edge Construction:**

- **Initial**: No edges (empty edge_index)
- **Future**: Proximity-based edges (within threshold distance)
- **Future**: All-to-all edges (fully connected)

**Output Format:**

- PyTorch Geometric `Data` object:
  - `x`: Node features tensor (num_nodes × 6)
  - `edge_index`: Edge connectivity tensor (2 × num_edges)
  - `node_type`: Node type tensor (num_nodes, long)
  - `num_nodes`: Number of nodes (int)

**Edge Cases:**

- No player: Empty graph or placeholder node
- No asteroids: Graph with only player and bullets
- No bullets: Graph with only player and asteroids
- Empty game: Return minimal graph (player node only)

### ActionInterface Interface

**Class:** `ActionInterface` (in `interfaces/ActionInterface.py`)

**Action Format:**

- Standard: `[left, right, thrust, shoot]`
- Can be boolean (0/1) or continuous (0.0-1.0)
- All AI methods output same format

**Core Methods:**

```python
class ActionInterface:
    def __init__(self, action_space_type: str = "boolean"):
        """
        Initialize action interface.

        Args:
            action_space_type: "boolean" or "continuous"
        """
        self.action_space_type = action_space_type
        self.action_space_size = 4

    def validate(self, action: List[float]) -> bool:
        """
        Check if action is valid.

        Args:
            action: Action vector [left, right, thrust, shoot]

        Returns:
            True if valid, False otherwise
        """
        pass

    def normalize(self, action: List[float]) -> List[float]:
        """
        Normalize action values to valid range.

        Args:
            action: Action vector (may be unnormalized)

        Returns:
            Normalized action vector
        """
        pass

    def to_game_input(self, action: List[float]) -> Dict[str, bool]:
        """
        Convert action vector to game input format.

        Args:
            action: Action vector [left, right, thrust, shoot]

        Returns:
            Dict with keys: left_pressed, right_pressed, up_pressed, space_pressed
        """
        pass

    def get_action_space_size(self) -> int:
        """Return action space size (4)."""
        return 4
```

**Action Conversion:**

- **Boolean mode**: Threshold at 0.5

  - `left_pressed = action[0] > 0.5`
  - `right_pressed = action[1] > 0.5`
  - `up_pressed = action[2] > 0.5`
  - `space_pressed = action[3] > 0.5`

- **Continuous mode**: Use action values directly (0.0-1.0)
  - Can be used for probabilistic actions or soft controls

**Validation:**

- Check length is 4
- Check values are in valid range (0-1 for continuous, any for boolean)
- Check no NaN or infinite values

**Must-Not-Break:**

- Existing `AsteroidsGraphEnv.step()` action format
- Game input handling (left_pressed, right_pressed, etc.)

## Impacted Areas

**Files to Create (Phase 1 - GA):**

- `interfaces/StateEncoder.py` - Abstract base class (shared foundation)
- `interfaces/encoders/__init__.py` - Package init
- `interfaces/encoders/VectorEncoder.py` - Vector encoder implementation (for GA)

**Files to Verify/Modify (Phase 1 - GA):**

- `interfaces/ActionInterface.py` - Action interface (already exists, verify/adjust for GA)

**Files to Create (Phase 2+ - Future):**

- `interfaces/encoders/GraphEncoder.py` - Graph encoder (when implementing GNN)
- Additional encoders as needed for other AI methods

**Files to Modify:**

- `ai_agents/reinforcement_learning/gnn_and_sac/env_wrapper.py` - Use GraphEncoder instead of `_get_graph_state()` (deferred: wrapper refactoring happens after infrastructure complete)
- **Note**: `train_agent.py` integration is deferred to plan 005 (BaseAgent/EpisodeRunner infrastructure). StateEncoder and ActionInterface will be integrated via EpisodeRunner, not directly into current `train_agent.py`.

**Dependencies:**

- Requires EnvironmentTracker (plan 001 - complete)
- Will be used by BaseAgent and EpisodeRunner (plan 005)
- GraphEncoder requires PyTorch and PyTorch Geometric

**No Schema/State Machine Changes:**

- Game entities unchanged
- No CLI/config changes
- Action format unchanged (just standardized)

## Incremental Implementation

### Step 1: Create StateEncoder base class

**Intent**: Establish the foundation for all state encoders

**Implementation:**

- [x] Create `interfaces/StateEncoder.py`
- [x] Define abstract base class with `encode()`, `get_state_size()`, `reset()`
- [x] Add docstrings and type hints
- [x] Import EnvironmentTracker

**Verification**: Can import StateEncoder, cannot instantiate (abstract), can create subclass

### Step 2: Create ActionInterface

**Intent**: Standardize action format and validation

**Implementation:**

- [x] Create `interfaces/ActionInterface.py`
- [x] Implement `__init__()` with action_space_type parameter
- [x] Implement `validate()` - check length, range, NaN/inf
- [x] Implement `normalize()` - clamp to [0, 1] range
- [x] Implement `to_game_input()` - convert to game boolean inputs
- [x] Implement `get_action_space_size()` - return 4
- [x] Add docstrings and type hints

**Verification**: Can instantiate ActionInterface, validate actions, convert to game inputs correctly

### Step 3: Implement VectorEncoder

**Intent**: Create fixed-size vector encoding for GA/ES/NEAT

**Implementation:**

- [x] Create `interfaces/encoders/__init__.py`
- [x] Create `interfaces/encoders/VectorEncoder.py`
- [x] Implement `__init__()` with parameters:
  - `screen_width: int = 800`
  - `screen_height: int = 600`
  - `num_nearest_asteroids: int = 2` (configurable)
  - `num_nearest_bullets: int = 2` (configurable)
  - `include_bullets: bool = False` (optional)
  - `include_global: bool = False` (optional)
  - `max_player_velocity: Optional[float] = None` (optional)
  - `max_asteroid_velocity: Optional[float] = None` (optional)
  - `max_asteroid_size: Optional[float] = None` (optional)
  - `max_asteroid_hp: Optional[float] = None` (optional)
  - `validate_parameters()` - validate parameters
- [x] Implement `encode()`:
  - Get player from `env_tracker.get_player()`
  - Extract player features (position, velocity, angle)
  - Get asteroids from `env_tracker.get_all_asteroids()`
  - Find nearest N asteroids (sort by distance)
  - Extract asteroid features (relative position, distance, velocity, size)
  - Optionally extract bullet features
  - Optionally extract global features (counts)
  - Normalize all values
  - Concatenate into fixed-size vector
  - Handle edge cases (no player, no asteroids, etc.)
- [x] Implement `get_state_size()` - return calculated size based on configuration
- [x] Implement `reset()` - no-op (no internal state)
- [x] Add helper methods:
  - `normalize_position()`
  - `normalize_velocity()`
  - `normalize_distance()`
  - `normalize_angle()`
- [x] Implement `encode_player()`
- [x] Implement `encode_asteroids()`
- [x] Implement `encode_bullets()`
- [x] Implement `encode_global()`

**Verification**:

- VectorEncoder produces fixed-size vectors
- Values are normalized correctly (0-1 range)
- Handles edge cases (empty lists, None values)
- Vector size matches `get_state_size()`

### Step 4: Test encoders independently

**Intent**: Verify encoders work correctly with EnvironmentTracker

**Implementation:**

- [ ] Create test file `tests/test_state_encoders.py`
- [ ] Test VectorEncoder:
  - Test with player only
  - Test with player + asteroids
  - Test with empty asteroid list
  - Test normalization (values in 0-1 range)
  - Test vector size consistency
- [ ] Test ActionInterface:
  - Test boolean mode conversion
  - Test continuous mode conversion
  - Test validation (valid/invalid actions)
  - Test normalization

**Verification**: All tests pass, encoders produce expected outputs

### Step 5: Document encoder usage

**Intent**: Provide examples and usage patterns

**Implementation:**

- [ ] Add usage examples to docstrings
- [ ] Document feature extraction logic
- [ ] Document normalization ranges
- [ ] Document edge case handling

**Verification**: Documentation is clear and complete

## Testing and Validation

**Unit Tests:**

- [ ] StateEncoder base class (cannot instantiate, can subclass)
- [ ] VectorEncoder: feature extraction, normalization, edge cases
- [ ] ActionInterface: validation, normalization, conversion

**Integration Tests:**

- [ ] Encoders work with EnvironmentTracker
- [ ] ActionInterface converts actions correctly
- [ ] Encoders handle all edge cases (empty lists, None values)
- [ ] VectorEncoder produces consistent vector sizes

**Manual Testing:**

```python
# Test VectorEncoder
from interfaces.encoders.VectorEncoder import VectorEncoder
from interfaces.EnvironmentTracker import EnvironmentTracker

encoder = VectorEncoder(screen_width=800, screen_height=600, num_nearest_asteroids=2)
# ... create game and tracker ...
state = encoder.encode(tracker)
assert len(state) == encoder.get_state_size()
assert all(0 <= x <= 1 for x in state)  # Normalized

# Test ActionInterface
from interfaces.ActionInterface import ActionInterface

action_interface = ActionInterface(action_space_type="boolean")
action = [0.7, 0.3, 0.9, 0.1]  # left, right, thrust, shoot
game_input = action_interface.to_game_input(action)
assert game_input["left_pressed"] == True
assert game_input["right_pressed"] == False
```

**Expected Signals:**

- Encoders produce consistent outputs
- Normalization works correctly (values in expected ranges)
- Edge cases handled gracefully (no crashes)
- ActionInterface converts actions correctly
- All tests pass

## Risks and Failure Modes

**Normalization Issues:**

- **Risk**: Values outside expected range, causing training instability
- **Mitigation**: Clamp values to [0, 1] or [-1, 1] as appropriate, document ranges
- **Detection**: Unit tests check normalization ranges

**Edge Case Failures:**

- **Risk**: Encoders crash on empty lists or None values
- **Mitigation**: All encoders handle edge cases, return zeros or empty structures
- **Detection**: Unit tests for all edge cases

**Vector Size Inconsistency:**

- **Risk**: VectorEncoder produces different sizes for different configurations
- **Mitigation**: `get_state_size()` calculates size based on configuration, unit tests verify consistency
- **Detection**: Test vector size matches `get_state_size()` for all configurations

**Action Conversion Errors:**

- **Risk**: ActionInterface converts actions incorrectly, breaking game input
- **Mitigation**: Test conversion thoroughly, match existing behavior
- **Detection**: Unit tests for all conversion scenarios

**Performance:**

- **Risk**: Encoding adds significant latency to training loop
- **Mitigation**: Encoders should be efficient (O(n) for n entities), profile if needed
- **Detection**: Profile encoding time, should be <1ms per step

## Exit Criteria

**Correctness:**

- [ ] StateEncoder base class implemented (shared foundation)
- [ ] VectorEncoder produces fixed-size normalized vectors (for GA)
- [ ] ActionInterface validates and converts actions correctly
- [ ] All encoders use EnvironmentTracker (no direct game access)
- [ ] Edge cases handled gracefully (no crashes)

**Integration:**

- [ ] Encoders work with EnvironmentTracker
- [ ] ActionInterface converts to game input format correctly
- [ ] Encoders are ready for GA implementation and BaseAgent use (plan 005)

**Code Quality:**

- [ ] All classes have comprehensive docstrings
- [ ] Type hints added to all public methods
- [ ] Code is testable (encoders can be instantiated independently)
- [ ] No direct game access in encoders (only EnvironmentTracker)

**Functionality:**

- [ ] VectorEncoder supports configurable feature sets (for GA)
- [ ] ActionInterface supports boolean and continuous modes
- [ ] All encoders handle edge cases (empty lists, None values)
- [ ] Infrastructure ready for GA implementation (plan 007)

**Documentation:**

- [ ] `plans/README.md` updated with plan status
- [ ] `plans/ARCHITECTURE.md` updated with encoder interfaces
- [ ] Usage examples in docstrings

## Future Considerations

**Phase 2+ (After GA Implementation):**

- Add GraphEncoder when implementing GNN (will use same StateEncoder base)
- Add additional encoders for ES, NEAT, GP as needed
- Refactor `AsteroidsGraphEnv` to use GraphEncoder (when implementing GNN)
- Add proximity-based edges to GraphEncoder
- Add SensorEncoder (optional, for sensor-based encoding)
- Feature engineering experiments (different feature sets)

**Follow-ons (After Plan 005):**

- Integrate encoders with BaseAgent and EpisodeRunner
- GA implementation will use these interfaces (plan 007)

**Advanced Encodings:**

- Multi-scale encodings (different resolutions)
- Attention mechanisms (weighted features)
- State compression/abstraction
- Historical state (temporal features)

**Action Space Enhancements:**

- Continuous action space (throttle control)
- Action masking (disable invalid actions)
- Action discretization utilities

**Optimization:**

- Caching computed features (if needed)
- Batch encoding (multiple states at once)
- GPU acceleration for graph encoding

---

**Status**: planned

**Implementation Phases:**

- **Phase 1 (Current)**: GA-focused implementation (StateEncoder base, VectorEncoder, ActionInterface)
- **Phase 2+ (Future)**: Additional encoders added incrementally as other AI methods are implemented

**Last Updated**: 2025-01-XX (revised to reflect GA-first incremental approach)
