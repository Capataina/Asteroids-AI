from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker
import math


class LeadingTargetBonus(RewardComponent):
    """
    Rewards firing a shot while aiming ahead of an asteroid's trajectory.
    This is an event-based reward that encourages predictive aiming.
    """
    
    def __init__(self, bonus_per_shot: float = 40.0, prediction_time: float = 0.5, alignment_threshold: float = 0.9):
        self.name = "LeadingTargetBonus"
        self.bonus_per_shot = bonus_per_shot
        self.prediction_time = prediction_time  # How far in seconds to predict ahead
        self.alignment_threshold = alignment_threshold
        self.prev_shots = 0
    
    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
        current_shots = metrics_tracker.get_total_shots_fired()
        
        # Check if a shot was fired this step
        if current_shots <= self.prev_shots:
            return 0.0
        
        self.prev_shots = current_shots
        
        player = env_tracker.get_player()
        nearest_asteroid = env_tracker.get_nearest_asteroid()
        
        if player is None or nearest_asteroid is None:
            return 0.0
        
        # Predict where the asteroid will be in `prediction_time` seconds
        # Note: A simple linear prediction. A smarter version could use bullet speed.
        predicted_x = nearest_asteroid.center_x + nearest_asteroid.change_x * self.prediction_time * 60
        predicted_y = nearest_asteroid.center_y + nearest_asteroid.change_y * self.prediction_time * 60
        
        # Calculate the angle from the player to this predicted position
        dx = predicted_x - player.center_x
        dy = predicted_y - player.center_y
        angle_to_predicted = math.degrees(math.atan2(dy, dx))
        
        # Calculate how well the player's aim aligns with the predicted position
        angle_diff = abs(player.angle - angle_to_predicted)
        angle_diff = min(angle_diff, 360 - angle_diff) # Find the shortest angle
        
        # The score is 1.0 for perfect alignment, 0.0 for 180 degrees off
        leading_score = 1.0 - (angle_diff / 180.0)
        
        # If the shot was well-aligned with the predicted path, give a bonus
        if leading_score > self.alignment_threshold:
            return self.bonus_per_shot
        
        return 0.0
    
    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        return 0.0
    
    def reset(self) -> None:
        self.prev_shots = 0
