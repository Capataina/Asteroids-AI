from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker
from game.classes.asteroid import Asteroid
from typing import List

class NearMiss(RewardComponent):
  def __init__(self, reward_per_near_miss: float = 15.0, safe_distance: float = 50.0):
    self.name = "NearMiss"
    self.reward_per_near_miss = reward_per_near_miss
    self.safe_distance = safe_distance
    self.rewarded_asteroids = []

  def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:

    # We get the nearest asteroids under a certain distance
    nearest_asteroids = env_tracker.get_asteroids_in_range(self.safe_distance)

    # For each asteroid, we only reward the player once
    for asteroid in nearest_asteroids:
      if asteroid not in self.rewarded_asteroids:
        reward = self.reward_per_near_miss
        self.rewarded_asteroids.append(asteroid)
        return reward
    
    return 0.0

  def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
    return 0.0

  def reset(self) -> None:
    self.rewarded_asteroids = []