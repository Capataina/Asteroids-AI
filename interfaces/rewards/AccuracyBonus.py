from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker

class AccuracyBonus(RewardComponent):
  def __init__ (self, bonus_per_second: float = 15, min_accuracy: float = 0.25):  # Increased from 8 to 15
    self.name = "AccuracyBonus"
    self.bonus_per_second = bonus_per_second
    self.min_accuracy = min_accuracy
    self.prev_time_alive = 0.0


  def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:

    current_time_alive = metrics_tracker.get_time_alive()
    delta_time = current_time_alive - self.prev_time_alive
    self.prev_time_alive = current_time_alive

    current_accuracy = metrics_tracker.get_accuracy()
    # Guard against negative delta (should not happen, but prevents negative rewards)
    delta_time = max(0.0, delta_time)
    # Removed print statement to avoid spam
    return delta_time * self.bonus_per_second * current_accuracy if current_accuracy > self.min_accuracy else 0.0

  def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
    return 0.0

  def reset(self) -> None:
    self.prev_time_alive = 0.0