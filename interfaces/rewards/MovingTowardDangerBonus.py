from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker
import math


class MovingTowardDangerBonus(RewardComponent):
    """
    Rewards moving toward asteroids when safe to engage.
    Encourages aggressive play and prevents passive behavior.
    """
    
    def __init__(self, bonus_per_second: float = 5.0, min_safe_distance: float = 200.0):
        self.name = "MovingTowardDangerBonus"
        self.bonus_per_second = bonus_per_second
        self.min_safe_distance = min_safe_distance
        self.prev_time_alive = 0.0
    
    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
        current_time = metrics_tracker.get_time_alive()
        delta_time = max(0.0, current_time - self.prev_time_alive)
        self.prev_time_alive = current_time
        
        player = env_tracker.get_player()
        nearest_asteroid = env_tracker.get_nearest_asteroid()
        
        if player is None or nearest_asteroid is None:
            return 0.0
        
        # Calculate distance to asteroid
        dx = nearest_asteroid.center_x - player.center_x
        dy = nearest_asteroid.center_y - player.center_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Only reward approaching when far enough (safe to engage)
        if distance < self.min_safe_distance:
            return 0.0  # Too close, don't encourage suicide
        
        # Calculate if velocity is toward asteroid
        velocity_magnitude = math.sqrt(player.change_x ** 2 + player.change_y ** 2)
        if velocity_magnitude < 0.1:
            return 0.0  # Not moving
        
        velocity_angle = math.atan2(player.change_x, player.change_y)
        target_angle = math.atan2(dx, dy)
        
        # Calculate alignment between velocity and target direction
        angle_diff = abs(velocity_angle - target_angle)
        alignment = math.cos(angle_diff)
        
        # Only reward moving toward (positive alignment)
        if alignment > 0:
            return delta_time * self.bonus_per_second * alignment
        else:
            return 0.0
    
    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        return 0.0
    
    def reset(self) -> None:
        self.prev_time_alive = 0.0
