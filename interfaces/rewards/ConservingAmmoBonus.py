from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker
import math


class ConservingAmmoBonus(RewardComponent):
    """
    Rewards shooting when well-aligned with target, penalizes random shooting.
    Provides immediate feedback to encourage shot discipline.
    """
    
    def __init__(self, good_shot_bonus: float = 5.0, bad_shot_penalty: float = -5.0, alignment_threshold: float = 0.7):
        self.name = "ConservingAmmoBonus"
        self.good_shot_bonus = good_shot_bonus
        self.bad_shot_penalty = bad_shot_penalty
        self.alignment_threshold = alignment_threshold
        self.prev_shots = 0
    
    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
        current_shots = metrics_tracker.get_total_shots_fired()
        
        # Check if a shot was fired this step
        if current_shots == self.prev_shots:
            return 0.0
        
        # Shot was fired! Evaluate if it was a good shot
        self.prev_shots = current_shots
        
        player = env_tracker.get_player()
        nearest_asteroid = env_tracker.get_nearest_asteroid()
        
        if player is None or nearest_asteroid is None:
            return 0.0
        
        # Calculate alignment with target
        dx = nearest_asteroid.center_x - player.center_x
        dy = nearest_asteroid.center_y - player.center_y
        angle_to_asteroid = math.degrees(math.atan2(dx, dy))
        
        angle_diff = abs(player.angle - angle_to_asteroid)
        angle_diff = min(angle_diff, 360 - angle_diff)
        
        facing_score = 1.0 - (angle_diff / 180.0)
        
        # Reward or penalize based on alignment
        if facing_score > self.alignment_threshold:
            return self.good_shot_bonus  # Good shot!
        else:
            return self.bad_shot_penalty  # Wasted shot!
    
    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        return 0.0
    
    def reset(self) -> None:
        self.prev_shots = 0
