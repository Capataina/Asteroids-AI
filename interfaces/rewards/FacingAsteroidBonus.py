from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker
import math


class FacingAsteroidBonus(RewardComponent):
    """
    Rewards agent for facing toward nearest asteroid.
    Encourages engagement behavior - agents learn to aim at threats.
    """
    
    def __init__(self, bonus_per_second: float = 15.0):
        self.name = "FacingAsteroidBonus"
        self.bonus_per_second = bonus_per_second
        self.prev_time_alive = 0.0
    
    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
        current_time = metrics_tracker.get_time_alive()
        delta_time = max(0.0, current_time - self.prev_time_alive)
        self.prev_time_alive = current_time
        
        player = env_tracker.get_player()
        nearest_asteroid = env_tracker.get_nearest_asteroid()
        
        if player is None or nearest_asteroid is None:
            return 0.0
        
        # Calculate angle to nearest asteroid
        dx = nearest_asteroid.center_x - player.center_x
        dy = nearest_asteroid.center_y - player.center_y
        angle_to_asteroid = math.degrees(math.atan2(dx, dy))
        
        # Calculate how well we're facing it (angle difference)
        angle_diff = abs(player.angle - angle_to_asteroid)
        # Normalize to 0-180 range (shortest angle)
        angle_diff = min(angle_diff, 360 - angle_diff)
        
        # Convert to facing score (1.0 = perfect alignment, 0.0 = opposite direction)
        facing_score = 1.0 - (angle_diff / 180.0)
        
        # Smooth reward function (quadratic makes it easier to learn)
        facing_score = facing_score ** 2
        
        return delta_time * self.bonus_per_second * facing_score
    
    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        return 0.0
    
    def reset(self) -> None:
        self.prev_time_alive = 0.0
