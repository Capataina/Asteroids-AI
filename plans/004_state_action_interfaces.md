# State and Action Interface Standardization

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

**Files to Create:**

- `interfaces/StateEncoder.py` - Abstract base class
- `interfaces/encoders/__init__.py` - Package init
- `interfaces/encoders/VectorEncoder.py` - Vector encoder implementation
- `interfaces/encoders/GraphEncoder.py` - Graph encoder (refactored from env_wrapper)
- `interfaces/ActionInterface.py` - Action interface

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

- [ ] Create `interfaces/StateEncoder.py`
- [ ] Define abstract base class with `encode()`, `get_state_size()`, `reset()`
- [ ] Add docstrings and type hints
- [ ] Import EnvironmentTracker

**Verification**: Can import StateEncoder, cannot instantiate (abstract), can create subclass

### Step 2: Create ActionInterface

**Intent**: Standardize action format and validation

**Implementation:**

- [ ] Create `interfaces/ActionInterface.py`
- [ ] Implement `__init__()` with action_space_type parameter
- [ ] Implement `validate()` - check length, range, NaN/inf
- [ ] Implement `normalize()` - clamp to [0, 1] range
- [ ] Implement `to_game_input()` - convert to game boolean inputs
- [ ] Implement `get_action_space_size()` - return 4
- [ ] Add docstrings and type hints

**Verification**: Can instantiate ActionInterface, validate actions, convert to game inputs correctly

### Step 3: Implement VectorEncoder

**Intent**: Create fixed-size vector encoding for GA/ES/NEAT

**Implementation:**

- [ ] Create `interfaces/encoders/__init__.py`
- [ ] Create `interfaces/encoders/VectorEncoder.py`
- [ ] Implement `__init__()` with parameters:
  - `screen_width: int = 800`
  - `screen_height: int = 600`
  - `num_nearest_asteroids: int = 2` (configurable)
  - `include_bullets: bool = False` (optional)
  - `include_global: bool = False` (optional)
- [ ] Implement `encode()`:
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
- [ ] Implement `get_state_size()` - return calculated size based on configuration
- [ ] Implement `reset()` - no-op (no internal state)
- [ ] Add helper methods:
  - `_normalize_position()`
  - `_normalize_velocity()`
  - `_normalize_distance()`
  - `_calculate_relative_position()`

**Verification**:

- VectorEncoder produces fixed-size vectors
- Values are normalized correctly (0-1 range)
- Handles edge cases (empty lists, None values)
- Vector size matches `get_state_size()`

### Step 4: Implement GraphEncoder

**Intent**: Refactor existing graph encoding to use EnvironmentTracker

**Implementation:**

- [ ] Create `interfaces/encoders/GraphEncoder.py`
- [ ] Copy graph construction logic from `env_wrapper.py._get_graph_state()`
- [ ] Refactor to use EnvironmentTracker:
  - Replace `self.game.player` with `env_tracker.get_player()`
  - Replace `self.game.asteroid_list` with `env_tracker.get_all_asteroids()`
  - Replace `self.game.bullet_list` with `env_tracker.get_all_bullets()`
  - Replace `self.game.width/height` with parameters or constants
- [ ] Implement `__init__()` with parameters:
  - `screen_width: int = 800`
  - `screen_height: int = 600`
  - `max_velocity_player: float = 10.0`
  - `max_velocity_asteroid: float = 5.0`
- [ ] Implement `encode()`:
  - Extract node features (player, asteroids, bullets)
  - Create node type tensor
  - Create edge_index (empty for now, can add proximity edges later)
  - Create PyTorch Geometric Data object
  - Handle edge cases (no player, empty lists)
- [ ] Implement `get_state_size()` - return -1 (variable-size)
- [ ] Implement `reset()` - no-op (no internal state)
- [ ] Add helper methods:
  - `_extract_player_features()`
  - `_extract_asteroid_features()`
  - `_extract_bullet_features()`
  - `_create_graph_data()`

**Verification**:

- GraphEncoder produces PyTorch Geometric Data objects
- Node features match original implementation
- Works with EnvironmentTracker (no direct game access)
- Handles edge cases (empty lists, None values)

### Step 5: Test encoders independently

**Intent**: Verify encoders work correctly with EnvironmentTracker

**Implementation:**

- [ ] Create test file `tests/test_state_encoders.py`
- [ ] Test VectorEncoder:
  - Test with player only
  - Test with player + asteroids
  - Test with empty asteroid list
  - Test normalization (values in 0-1 range)
  - Test vector size consistency
- [ ] Test GraphEncoder:
  - Test with player only
  - Test with player + asteroids + bullets
  - Test with empty lists
  - Test PyTorch Geometric format
  - Test node type assignment
- [ ] Test ActionInterface:
  - Test boolean mode conversion
  - Test continuous mode conversion
  - Test validation (valid/invalid actions)
  - Test normalization

**Verification**: All tests pass, encoders produce expected outputs

### Step 6: Document encoder usage

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
- [ ] GraphEncoder: node features, graph construction, edge cases
- [ ] ActionInterface: validation, normalization, conversion

**Integration Tests:**

- [ ] Encoders work with EnvironmentTracker
- [ ] ActionInterface converts actions correctly
- [ ] Encoders handle all edge cases (empty lists, None values)
- [ ] VectorEncoder produces consistent vector sizes
- [ ] GraphEncoder produces valid PyTorch Geometric objects

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

# Test GraphEncoder
from interfaces.encoders.GraphEncoder import GraphEncoder

encoder = GraphEncoder(screen_width=800, screen_height=600)
state = encoder.encode(tracker)
assert isinstance(state, torch_geometric.data.Data)
assert state.x.shape[1] == 6  # 6 features per node

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

**Graph Format Issues:**

- **Risk**: GraphEncoder produces invalid PyTorch Geometric objects
- **Mitigation**: Follow PyTorch Geometric Data format exactly, test with PyG validation
- **Detection**: Integration tests verify graph structure

**Action Conversion Errors:**

- **Risk**: ActionInterface converts actions incorrectly, breaking game input
- **Mitigation**: Test conversion thoroughly, match existing behavior
- **Detection**: Unit tests for all conversion scenarios

**Performance:**

- **Risk**: Encoding adds significant latency to training loop
- **Mitigation**: Encoders should be efficient (O(n) for n entities), profile if needed
- **Detection**: Profile encoding time, should be <1ms per step

**Refactoring Risks:**

- **Risk**: GraphEncoder refactoring breaks existing GNN training
- **Mitigation**: Keep output format identical, test with existing code
- **Detection**: Integration tests with existing env_wrapper

## Exit Criteria

**Correctness:**

- [ ] All encoders implement StateEncoder interface
- [ ] VectorEncoder produces fixed-size normalized vectors
- [ ] GraphEncoder produces valid PyTorch Geometric objects
- [ ] ActionInterface validates and converts actions correctly
- [ ] All encoders use EnvironmentTracker (no direct game access)
- [ ] Edge cases handled gracefully (no crashes)

**Integration:**

- [ ] Encoders work with EnvironmentTracker
- [ ] ActionInterface converts to game input format correctly
- [ ] Encoders are ready for BaseAgent use (plan 005)
- [ ] GraphEncoder output matches original format (for compatibility)

**Code Quality:**

- [ ] All classes have comprehensive docstrings
- [ ] Type hints added to all public methods
- [ ] Code is testable (encoders can be instantiated independently)
- [ ] No direct game access in encoders (only EnvironmentTracker)

**Functionality:**

- [ ] VectorEncoder supports configurable feature sets
- [ ] GraphEncoder maintains PyTorch Geometric compatibility
- [ ] ActionInterface supports boolean and continuous modes
- [ ] All encoders handle edge cases (empty lists, None values)

**Documentation:**

- [ ] `plans/README.md` updated with plan status
- [ ] `plans/ARCHITECTURE.md` updated with encoder interfaces
- [ ] Usage examples in docstrings

## Future Considerations

**Follow-ons (After Plan 005):**

- Refactor `AsteroidsGraphEnv` to use GraphEncoder (currently uses `_get_graph_state()`)
- Integrate encoders with BaseAgent and EpisodeRunner
- Add proximity-based edges to GraphEncoder
- Add SensorEncoder (optional, for sensor-based encoding)
- Feature engineering experiments (different feature sets)

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

**Last Updated**: 2025-01-XX (expanded from skeleton plan)
