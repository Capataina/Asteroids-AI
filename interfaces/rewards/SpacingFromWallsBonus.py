from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker


class SpacingFromWallsBonus(RewardComponent):
    """
    Penalizes being too close to screen edges.
    Encourages staying away from walls where maneuverability is limited.
    """
    
    def __init__(self, penalty_per_second: float = -2.0, min_margin: float = 100.0, screen_width: float = 800, screen_height: float = 600):
        self.name = "SpacingFromWallsBonus"
        self.penalty_per_second = penalty_per_second
        self.min_margin = min_margin
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.prev_time_alive = 0.0
    
    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
        current_time = metrics_tracker.get_time_alive()
        delta_time = max(0.0, current_time - self.prev_time_alive)
        self.prev_time_alive = current_time
        
        player = env_tracker.get_player()
        
        if player is None:
            return 0.0
        
        # Calculate distance to nearest edge
        distance_to_edge = min(
            player.center_x,                    # Left edge
            self.screen_width - player.center_x,  # Right edge
            player.center_y,                    # Bottom edge
            self.screen_height - player.center_y  # Top edge
        )
        
        # Only penalize if within the margin
        if distance_to_edge < self.min_margin:
            edge_penalty = (self.min_margin - distance_to_edge) / self.min_margin
            return delta_time * self.penalty_per_second * edge_penalty
        else:
            return 0.0
    
    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        return 0.0
    
    def reset(self) -> None:
        self.prev_time_alive = 0.0
