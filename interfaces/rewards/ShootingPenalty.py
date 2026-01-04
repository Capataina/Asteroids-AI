from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker

class ShootingPenalty(RewardComponent):
    """
    Penalizes the agent for wasting ammo.
    Encourages deliberate, accurate shooting rather than spray-and-pray.
    """
    
    def __init__(self, penalty_per_shot: float = -0.5):
        self.name = "ShootingPenalty"
        self.penalty_per_shot = penalty_per_shot
        self.prev_shots = 0
    
    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
        current_shots = metrics_tracker.get_total_shots_fired()
        
        if current_shots == self.prev_shots:
            return 0.0
        
        delta_shots = current_shots - self.prev_shots
        self.prev_shots = current_shots
        
        # Small penalty for each shot fired
        # This is balanced by kill rewards, so accurate shooting is net positive
        return delta_shots * self.penalty_per_shot
    
    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        return 0.0
    
    def reset(self) -> None:
        self.prev_shots = 0
