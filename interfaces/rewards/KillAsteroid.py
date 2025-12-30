from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker

class KillAsteroid(RewardComponent):
  def __init__(self, reward_per_asteroid: float = 10.0):
    self.name = "KillAsteroid"
    self.reward_per_asteroid = reward_per_asteroid
    self.prev_kills = 0

  def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
    current_kills = metrics_tracker.get_total_kills()

    if current_kills == self.prev_kills:
      return 0.0

    if current_kills != self.prev_kills:
      delta_kills = current_kills - self.prev_kills
      self.prev_kills = current_kills
      return delta_kills * self.reward_per_asteroid


  def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
    return 0.0

  def reset(self) -> None:
    self.prev_kills = 0