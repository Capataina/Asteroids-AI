from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker

class SurvivalBonus(RewardComponent):

  def __init__(self, reward_multiplier: float = 1.0):
    self.name = "SurvivalBonus"
    self.reward_multiplier = reward_multiplier
    self.prev_time_alive = 0.0

  def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
    current_time_alive = metrics_tracker.get_time_alive()
    delta_time = current_time_alive - self.prev_time_alive
    self.prev_time_alive = current_time_alive
    # Guard against negative delta (should not happen, but prevents negative rewards)
    return max(0.0, delta_time * self.reward_multiplier)

  def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
    return 0.0

  def reset(self) -> None:
    self.prev_time_alive = 0.0







