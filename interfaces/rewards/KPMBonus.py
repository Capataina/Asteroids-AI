from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker

from typing import List

class KPMBonus(RewardComponent):
  def __init__(self, bonus_per_kpm: float = 1.0, window_seconds: float = 10.0):
    self.name = "KPMBonus"
    self.bonus_per_kpm = bonus_per_kpm
    self.window_seconds = window_seconds
    self.kill_timestamps: List[float] = []
    self.prev_time_alive = 0.0

  def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
    current_time = metrics_tracker.get_time_alive()
    current_kills = metrics_tracker.get_total_kills()
    
    if current_kills > len(self.kill_timestamps):
      for _ in range(current_kills - len(self.kill_timestamps)):
        self.kill_timestamps.append(current_time)
    
    cutoff_time = current_time - self.window_seconds
    self.kill_timestamps = [t for t in self.kill_timestamps if t > cutoff_time]
    
    if current_time > 0:
      window_kpm = (len(self.kill_timestamps) / min(self.window_seconds, current_time)) * 60
    else:
      window_kpm = 0.0
    
    delta_time = current_time - self.prev_time_alive
    self.prev_time_alive = current_time
    
    # Guard against negative delta (should not happen, but prevents negative rewards)
    delta_time = max(0.0, delta_time)
    delta_time_minutes = delta_time / 60.0

    return delta_time_minutes * window_kpm * self.bonus_per_kpm if window_kpm > 0 else 0.0

  def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
    return 0.0  # KPMBonus only gives step rewards, not episode rewards