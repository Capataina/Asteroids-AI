from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker
import math

# This reward component is used to reward the player for moving across chunk boundaries.
# A chunk is a square area of the map.
# This is to encourage the player to explore the map and not get stuck or camp an area.
class ChunkBonus(RewardComponent):

  def __init__(self, chunk_size: float = 128.0, reward_multiplier: float = 5.0):
    self.name = "ChunkBonus"
    self.prev_chunk_x = None
    self.prev_chunk_y = None
    self.chunk_size = chunk_size
    self.reward_multiplier = reward_multiplier

  def get_chunk_coords(self, x: float, y: float) -> tuple[int, int]:
    """Convert world coordinates to chunk coordinates."""
    chunk_x = math.floor(x / self.chunk_size)
    chunk_y = math.floor(y / self.chunk_size)
    return (chunk_x, chunk_y)

  def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
    player = env_tracker.get_player()

    if player is None:
      return 0.0

    current_x = player.center_x
    current_y = player.center_y
    current_chunk_x, current_chunk_y = self.get_chunk_coords(current_x, current_y)

    if self.prev_chunk_x is None or self.prev_chunk_y is None:
      self.prev_chunk_x = current_chunk_x
      self.prev_chunk_y = current_chunk_y
      return 0.0

    if current_chunk_x != self.prev_chunk_x or current_chunk_y != self.prev_chunk_y:
      self.prev_chunk_x = current_chunk_x
      self.prev_chunk_y = current_chunk_y
      return self.reward_multiplier

    return 0.0

  def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
    return 0.0

  def reset(self) -> None:
    self.prev_chunk_x = None
    self.prev_chunk_y = None