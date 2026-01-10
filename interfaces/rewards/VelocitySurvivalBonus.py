from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker
import math

class VelocitySurvivalBonus(RewardComponent):
    """
    Rewards survival proportional to movement velocity.
    Encourages the agent to stay alive WHILE moving, not camping.
    """

    def __init__(self, reward_multiplier: float = 2.0, max_velocity_cap: float = 10.0):
        """
        Args:
            reward_multiplier: Points per second per unit of velocity.
            max_velocity_cap: Velocity magnitude at which reward saturates (prevents infinite scaling).
        """
        self.name = "VelocitySurvivalBonus"
        self.reward_multiplier = reward_multiplier
        self.max_velocity_cap = max_velocity_cap
        self.prev_time_alive = 0.0

    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
        current_time_alive = metrics_tracker.get_time_alive()
        delta_time = current_time_alive - self.prev_time_alive
        self.prev_time_alive = current_time_alive
        
        # Guard against negative delta or dead player (though tracker shouldn't update if dead)
        if delta_time <= 0 or not env_tracker.is_player_alive():
            return 0.0

        # Get current velocity magnitude
        player = env_tracker.get_player()
        if not player:
            return 0.0

        velocity_x = player.change_x
        velocity_y = player.change_y
        speed = math.sqrt(velocity_x**2 + velocity_y**2)
        
        # Clamp speed to avoid exploiting physics glitches for massive score
        effective_speed = min(speed, self.max_velocity_cap)
        
        # Reward is time * speed * multiplier
        # Example: 1.0 second * 5.0 speed * 2.0 mult = 10 points
        return delta_time * effective_speed * self.reward_multiplier

    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        return 0.0

    def reset(self) -> None:
        self.prev_time_alive = 0.0
