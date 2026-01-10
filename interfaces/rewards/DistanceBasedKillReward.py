import math
from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker


class DistanceBasedKillReward(RewardComponent):
    """
    Rewards asteroid kills based on proximity - killing close asteroids gives more reward.

    This incentivizes the agent to prioritize threats (close asteroids) rather than
    randomly shooting at distant targets. The reward is scaled based on where the
    closest asteroid is when the kill occurs:
    - If closest asteroid is very close: full reward (immediate threat eliminated)
    - If closest asteroid is far away: minimal reward (no urgent threat)

    The reward is normalized between min_distance (full reward) and max_distance (zero reward).
    """

    def __init__(
        self,
        max_reward_per_kill: float = 15.0,
        min_distance: float = 50.0,
        max_distance: float = 400.0
    ):
        """
        Args:
            max_reward_per_kill: Maximum reward when killing an asteroid at min_distance.
            min_distance: Distance at which kills give full reward.
            max_distance: Distance at which kills give zero reward.
        """
        self.name = "DistanceBasedKillReward"
        self.max_reward_per_kill = max_reward_per_kill
        self.min_distance = min_distance
        self.max_distance = max_distance
        self.prev_kills = 0
        self.prev_closest_distance = None

    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker, debug: bool = False) -> float:
        current_kills = metrics_tracker.get_total_kills()
        delta_kills = current_kills - self.prev_kills

        # Track closest asteroid distance for next frame's kill calculation
        current_closest_distance = env_tracker.get_distance_to_nearest_asteroid()

        reward = 0.0

        if delta_kills > 0 and self.prev_closest_distance is not None:
            # Use the closest asteroid distance from BEFORE the kill
            # This represents how close the threat was when the agent was shooting
            distance = self.prev_closest_distance

            # Normalize distance to [0, 1] where 0 = far (max_distance), 1 = close (min_distance)
            # Clamp to valid range
            clamped_distance = max(self.min_distance, min(self.max_distance, distance))

            # Linear interpolation: min_distance -> 1.0, max_distance -> 0.0
            proximity_multiplier = 1.0 - (clamped_distance - self.min_distance) / (self.max_distance - self.min_distance)

            # Calculate reward for all kills this frame
            reward = delta_kills * self.max_reward_per_kill * proximity_multiplier

            if debug:
                print(f"DistanceBasedKillReward: kills={delta_kills}, closest_dist={distance:.1f}, "
                      f"multiplier={proximity_multiplier:.2f}, reward={reward:.2f}")

        self.prev_kills = current_kills
        self.prev_closest_distance = current_closest_distance

        return reward

    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        return 0.0

    def reset(self) -> None:
        self.prev_kills = 0
        self.prev_closest_distance = None
