from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker
import math


class LeadingTargetBonus(RewardComponent):
    """
    Rewards aiming ahead of asteroid's trajectory (predictive aiming).
    Teaches agent to lead moving targets for better accuracy.
    """
    
    def __init__(self, bonus_per_second: float = 10.0, prediction_time: float = 0.5):
        self.name = "LeadingTargetBonus"
        self.bonus_per_second = bonus_per_second
        self.prediction_time = prediction_time
        self.prev_time_alive = 0.0
    
    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
        current_time = metrics_tracker.get_time_alive()
        delta_time = max(0.0, current_time - self.prev_time_alive)
        self.prev_time_alive = current_time
        
        player = env_tracker.get_player()
        nearest_asteroid = env_tracker.get_nearest_asteroid()
        
        if player is None or nearest_asteroid is None:
            return 0.0
        
        # Predict where asteroid will be
        predicted_x = nearest_asteroid.center_x + nearest_asteroid.change_x * self.prediction_time * 60
        predicted_y = nearest_asteroid.center_y + nearest_asteroid.change_y * self.prediction_time * 60
        
        # Calculate angle to predicted position
        dx = predicted_x - player.center_x
        dy = predicted_y - player.center_y
        angle_to_predicted = math.degrees(math.atan2(dx, dy))
        
        # Calculate alignment with predicted position
        angle_diff = abs(player.angle - angle_to_predicted)
        angle_diff = min(angle_diff, 360 - angle_diff)
        
        leading_score = 1.0 - (angle_diff / 180.0)
        leading_score = leading_score ** 2
        
        return delta_time * self.bonus_per_second * leading_score
    
    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        return 0.0
    
    def reset(self) -> None:
        self.prev_time_alive = 0.0
