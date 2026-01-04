import deap
from typing import List
from interfaces.StateEncoder import StateEncoder
from interfaces.ActionInterface import ActionInterface
from training.base.BaseAgent import BaseAgent

class GAAgent(BaseAgent):
  def __init__(self, parameter_vector: List[float], state_encoder: StateEncoder, action_interface: ActionInterface):
    """
    Initialize GA agent with parameter vector.

    Args:
      parameter_vector: List of floats encoding control policy
      state_encoder: VectorEncoder instance for state representation
      action_interface: ActionInterface instance for action conversion
    """
    # Ensure parameter_vector is a flat list of floats
    self.parameter_vector = [float(x) for x in parameter_vector]
    self.state_encoder = state_encoder
    self.action_interface = action_interface

  def get_action(self, state: List[float]) -> List[float]:
    """
    Get action from state using parameter vector.

    Args:
      state: Encoded state vector from VectorEncoder (already encoded, don't encode again!)

    Returns:
      Action vector [left, right, thrust, shoot] with values in [0.0, 1.0]
    """
    # State is already encoded (it's a list of floats), use it directly
    # Apply linear policy to the encoded state
    action = self.apply_linear_policy(state)

    # Return action vector (ActionInterface will handle conversion to game inputs)
    return action

  def reset(self) -> None:
    """
    Reset agent state for new episode.
    """
    # No-op for GA agent
    pass

  def apply_linear_policy(self, encoded_state: List[float]) -> List[float]:
    """
    Apply linear policy to encoded state.
    
    Linear policy: action[i] = sum(parameter_vector[i*state_size + j] * state[j] for j in range(state_size))
    
    Args:
      encoded_state: Encoded state vector from VectorEncoder (flat list of floats)
    
    Returns:
      Action vector [left, right, thrust, shoot]
    """
    state_size = len(encoded_state)
    actions = []
    
    for i in range(4):  # 4 actions: left, right, thrust, shoot
      # Get weights for this action
      start_idx = i * state_size
      end_idx = (i + 1) * state_size
      
      # Ensure we have enough parameters
      if end_idx > len(self.parameter_vector):
        # Not enough parameters, use available ones and pad with zeros
        action_value = 0.0
        for j in range(state_size):
          param_idx = start_idx + j
          if param_idx < len(self.parameter_vector):
            action_value += self.parameter_vector[param_idx] * encoded_state[j]
      else:
        # Compute dot product: sum(weights[j] * state[j])
        action_value = sum(self.parameter_vector[start_idx + j] * encoded_state[j] 
                          for j in range(state_size))
      
      actions.append(action_value)
    
    return actions
