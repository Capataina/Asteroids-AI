from abc import ABC, abstractmethod
from typing import List, Any


class BaseAgent(ABC):
  """
  Abstract base class for all agents.
  """

  @abstractmethod
  def get_action(self, state: Any) -> List[float]:
    """
    Get action from encoded state.

    Args:
      state: 
       - Encoded state from StateEncoder (List[float] for VectorEncoder)

    Returns:
      Action vector [left, right, thrust, shoot] in range [0.0, 1.0]
    """
    pass

  @abstractmethod
  def reset(self) -> None:
    """
    Reset agent state for new episode.
    For evolutionary agents (GA, ES, NEAT, GP), this is typically a no-op
    since they have no internal state. For RL agents, this may reset
    internal state (e.g., RNN hidden state).
    """
    pass