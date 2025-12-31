from abc import ABC, abstractmethod
from typing import Any
from interfaces.EnvironmentTracker import EnvironmentTracker

class StateEncoder(ABC):
  @abstractmethod
  def encode(self, environment_tracker: EnvironmentTracker) -> Any:
    """
    Encode the environment tracker state into a representation.

    Args:
      environment_tracker: The environment tracker to encode.

    Returns:
      The encoded state.
    """
    pass

  @abstractmethod
  def get_state_size(self) -> int:
    """
    Get the size of the encoded state.

    Returns:
      The size of the encoded state.
    """
    pass

  @abstractmethod
  def reset(self) -> None:
    """
    Reset the encoder to its initial state.
    """
    pass