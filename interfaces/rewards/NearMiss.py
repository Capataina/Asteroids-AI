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
    # Get all asteroids within near-miss range
    nearby_asteroids = env_tracker.get_asteroids_in_range(self.safe_distance)

    # Reward for each NEW asteroid entering the danger zone
    total_reward = 0.0
    for asteroid in nearby_asteroids:
      if asteroid not in self.rewarded_asteroids:
        total_reward += self.reward_per_near_miss
        self.rewarded_asteroids.append(asteroid)

    return total_reward

  def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
    return 0.0

  def reset(self) -> None:
    self.rewarded_asteroids = []