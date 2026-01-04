from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker
import math


class MaintainingMomentumBonus(RewardComponent):
    """
    Rewards maintaining reasonable velocity, penalizes sitting still.
    Encourages constant movement which is crucial for survival.
    """
    
    def __init__(self, bonus_per_second: float = 3.0, penalty_per_second: float = -3.0, 
                 optimal_min_velocity: float = 3.0, optimal_max_velocity: float = 8.0):
        self.name = "MaintainingMomentumBonus"
        self.bonus_per_second = bonus_per_second
        self.penalty_per_second = penalty_per_second
        self.optimal_min_velocity = optimal_min_velocity
        self.optimal_max_velocity = optimal_max_velocity
        self.prev_time_alive = 0.0
    
    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
        current_time = metrics_tracker.get_time_alive()
        delta_time = max(0.0, current_time - self.prev_time_alive)
        self.prev_time_alive = current_time
        
        player = env_tracker.get_player()
        
        if player is None:
            return 0.0
        
        # Calculate velocity magnitude
        velocity_magnitude = math.sqrt(player.change_x ** 2 + player.change_y ** 2)
        
        # Penalize sitting still
        if velocity_magnitude < 1.0:
            return delta_time * self.penalty_per_second
        
        # Reward good velocity range
        elif self.optimal_min_velocity <= velocity_magnitude <= self.optimal_max_velocity:
            return delta_time * self.bonus_per_second
        
        # Neutral for other velocities
        else:
            return 0.0
    
    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        return 0.0
    
    def reset(self) -> None:
        self.prev_time_alive = 0.0
