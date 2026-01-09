import math
from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker

class ProximityPenalty(RewardComponent):
    """
    Applies a penalty for being too close to the nearest asteroid.
    The closer the asteroid, the larger the penalty.
    """
    def __init__(self, danger_zone_radius: float = 100.0, max_penalty_per_second: float = -10.0):
        """
        Args:
            danger_zone_radius: The distance at which the penalty starts to apply.
            max_penalty_per_second: The penalty applied per second when the distance is zero. Must be negative.
        """
        self.name = "ProximityPenalty"
        self.danger_zone_radius = danger_zone_radius
        # Ensure penalty is negative
        self.max_penalty_per_second = -abs(max_penalty_per_second)
        self.prev_time_alive = 0.0

    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker, debug: bool = False) -> float:
        current_time = metrics_tracker.get_time_alive()
        delta_time = max(0.0, current_time - self.prev_time_alive)
        self.prev_time_alive = current_time

        if delta_time == 0.0:
            return 0.0

        distance = env_tracker.get_distance_to_nearest_asteroid()

        if distance is not None and distance < self.danger_zone_radius:
            # Penalty is inversely proportional to distance within the danger zone
            # Factor is 1.0 at distance 0, and 0.0 at danger_zone_radius
            penalty_factor = (self.danger_zone_radius - distance) / self.danger_zone_radius
            
            # Apply a non-linear scaling to make it more punishing at very close ranges
            penalty_factor = penalty_factor ** 2

            penalty = self.max_penalty_per_second * penalty_factor * delta_time
            return penalty
            
        return 0.0

    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        return 0.0

    def reset(self):
        self.prev_time_alive = 0.0
