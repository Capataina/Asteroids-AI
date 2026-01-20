import math
from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker

class VelocityKillBonus(RewardComponent):
    """
    Rewards the agent for destroying an asteroid, with the reward amount
    scaled by the player's velocity at the time of the kill.
    A stationary kill yields zero points.
    """
    def __init__(self, bonus_per_kill: float = 50.0, max_speed_for_full_bonus: float = 10.0):
        """
        Args:
            bonus_per_kill: The maximum reward awarded for a kill at or above max_speed.
            max_speed_for_full_bonus: The speed at which the maximum bonus is awarded.
        """
        self.name = "VelocityKillBonus"
        self.bonus_per_kill = bonus_per_kill
        self.max_speed = max_speed_for_full_bonus
        self.prev_total_kills = 0

    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker, debug: bool = False) -> float:
        reward = 0.0
        current_kills = metrics_tracker.get_total_kills()
        
        # Check if one or more kills occurred since the last step
        if current_kills > self.prev_total_kills:
            num_kills = current_kills - self.prev_total_kills
            
            player = env_tracker.get_player()
            if player:
                # Calculate current speed
                speed = math.sqrt(player.change_x**2 + player.change_y**2)
                
                # Normalize speed to a factor between 0 and 1
                speed_factor = min(speed / self.max_speed, 1.0)
                
                # Calculate reward for the kills this step
                reward = num_kills * self.bonus_per_kill * speed_factor

                if debug:
                    print(f"VelocityKillBonus: {num_kills} kill(s) at speed {speed:.2f}. "
                          f"Factor: {speed_factor:.2f}. Reward: {reward:.2f}")

        self.prev_total_kills = current_kills
        return reward

    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        return 0.0

    def reset(self):
        self.prev_total_kills = 0
