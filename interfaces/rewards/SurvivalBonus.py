from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker

class SurvivalBonus(RewardComponent):

  def __init__(self, reward_multiplier: float = 1.0):
    self.reward_multiplier = reward_multiplier

  def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
    return metrics_tracker.get_time_alive() * self.reward_multiplier

  def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
    return 0.0

  def reset(self) -> None:
    pass







