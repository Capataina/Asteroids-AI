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
    # Encode state using VectorEncoder
    encoded_state = self.state_encoder.encode(state)

    # Apply linear policy (or chosen policy type)
    action = self.apply_linear_policy(encoded_state)

    # Convert action using ActionInterface
    game_input = self.action_interface.to_game_input(action)

    return [game_input["left_pressed"], game_input["right_pressed"], game_input["up_pressed"], game_input["space_pressed"]]

  def reset(self) -> None:
    """
    Reset agent state for new episode.
    """
    # No-op for GA agent
    pass

  def apply_linear_policy(self, encoded_state: List[float]) -> List[float]:
    """
    Apply linear policy to encoded state.
    
    Args:
      encoded_state: Encoded state vector from VectorEncoder
    
    Returns:
      Action vector [left, right, thrust, shoot]
    """
    return [sum(self.parameter_vector[i * len(encoded_state):(i + 1) * len(encoded_state)] * encoded_state) for i in range(4)]
