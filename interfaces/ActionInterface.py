from typing import List, Dict
import math

class ActionInterface:
  def __init__(self, action_space_type: str, turn_deadzone: float = 0.0):
    """
    Initialize the action interface.

    Args:
      action_space_type: The type of action space to use.
      turn_deadzone: Deadzone threshold for turn input. Turn values within
                     [-deadzone, +deadzone] will result in no turning.
                     Default 0.0 means any non-zero turn value triggers turning.
                     A small value like 0.03 allows the AI to express "don't turn"
                     without requiring perfect 0.5 output from sigmoid.
    """

    if action_space_type not in ["boolean", "continuous"]:
      raise ValueError(f"Invalid action space type: {action_space_type}")
    self.action_space_type = action_space_type
    self.turn_deadzone = turn_deadzone

  def validate(self, action: List[float]) -> bool:
    """
    Validate the action values. Check length, range, NaN/inf.

    Args:
      action: The action to validate.

    Returns:
      True if the action is valid, raises ValueError otherwise.
    """
    if len(action) not in (3, 4):
      raise ValueError(f"Invalid action length: {len(action)} (expected 3 or 4)")
    
    # Check for NaN or inf values
    for value in action:
      if not isinstance(value, (int, float)) or math.isnan(value) or math.isinf(value):
        raise ValueError(f"Invalid action values (NaN or inf): {action}")
    
    # For boolean mode, we accept continuous values that will be thresholded
    # No need to check exact 0/1 since normalize() will handle the conversion
    return True

  def normalize(self, action: List[float]) -> List[float]:
    """
    Normalize the action values to the valid range. Use clamp to 0-1 range.

    Args:
      action: The action to normalize.

    Returns:
      The normalized action.
    """
    # Clamp values to [0, 1] range (don't call validate, just normalize)
    return [max(0.0, min(float(value), 1.0)) for value in action]

  def to_game_input(self, action: List[float]) -> Dict[str, bool]:
    """
    Convert the action to the game input format. Use threshold at 0.5 for all types of action spaces for now.

    Args:
      action: The action to convert.

    Returns:
      The game input format.
    """
    if self.action_space_type not in ["boolean", "continuous"]:
      raise ValueError(f"Invalid action space type: {self.action_space_type}")

    # Use configurable deadzone: turn values within [-deadzone, +deadzone] result in no turning.
    # This allows AI to express "don't turn" without requiring exact 0.5 output.
    turn_threshold = self.turn_deadzone
    left_pressed = False
    right_pressed = False

    if len(action) == 3:
      # Signed turn control: action[0] in [0,1] -> turn_value in [-1,1].
      turn_value = (action[0] * 2.0) - 1.0
      if turn_value > turn_threshold:
        right_pressed = True
      elif turn_value < -turn_threshold:
        left_pressed = True
      up_pressed = action[1] > 0.5
      space_pressed = action[2] > 0.5
    else:
      # Legacy compatibility: derive signed turn from left/right difference.
      turn_value = action[1] - action[0]
      if turn_value > turn_threshold:
        right_pressed = True
      elif turn_value < -turn_threshold:
        left_pressed = True
      up_pressed = action[2] > 0.5
      space_pressed = action[3] > 0.5

    return {
      "left_pressed": left_pressed,
      "right_pressed": right_pressed,
      "up_pressed": up_pressed,
      "space_pressed": space_pressed,
    }

  def get_action_space_size(self) -> int:
    """
    Get the size of the action space.
    Return 4 for both boolean and continuous action spaces.

    Returns:
      The size of the action space.
    """
    if self.action_space_type == "boolean":
      return 3
    elif self.action_space_type == "continuous":
      return 3
    else:
      raise ValueError(f"Invalid action space type: {self.action_space_type}")
