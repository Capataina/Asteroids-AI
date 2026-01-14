import math
from typing import Optional, List
from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker


class DistanceBasedKillReward(RewardComponent):
    """
    Rewards asteroid kills based on proximity - killing close asteroids gives more reward.

    This incentivizes the agent to prioritize threats (close asteroids) rather than
    randomly shooting at distant targets. The reward is dynamically scaled based on
    the current asteroid distribution:
    - If closest asteroid is the nearest on screen: full reward
    - If closest asteroid is the furthest on screen: zero reward

    The scaling range is determined dynamically from the actual asteroid positions,
    not hardcoded distances. This adapts to varying asteroid densities and distributions.
    """

    def __init__(
        self,
        max_reward_per_kill: float = 15.0,
        min_reward_fraction: float = 0.1
    ):
        """
        Args:
            max_reward_per_kill: Maximum reward when killing the closest asteroid.
            min_reward_fraction: Minimum reward as fraction of max (0.0 = no reward for furthest,
                                 0.1 = 10% reward for furthest). Prevents zero reward entirely.
        """
        self.name = "DistanceBasedKillReward"
        self.max_reward_per_kill = max_reward_per_kill
        self.min_reward_fraction = min_reward_fraction
        self.prev_kills = 0
        self.prev_closest_distance: Optional[float] = None
        self.prev_all_distances: List[float] = []

    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker, debug: bool = False) -> float:
        current_kills = metrics_tracker.get_total_kills()
        delta_kills = current_kills - self.prev_kills

        # Track asteroid distances for next frame's kill calculation
        current_closest_distance = env_tracker.get_distance_to_nearest_asteroid()
        current_all_distances = env_tracker.all_asteroids_distance_to_player()

        reward = 0.0

        if delta_kills > 0 and self.prev_closest_distance is not None and len(self.prev_all_distances) > 0:
            # Use distances from BEFORE the kill
            distance = self.prev_closest_distance
            all_distances = self.prev_all_distances

            # Get dynamic range from actual asteroid positions
            min_dist = min(all_distances)
            max_dist = max(all_distances)

            # Calculate proximity multiplier based on dynamic range
            if max_dist > min_dist:
                # Normalize: closest (min_dist) -> 1.0, furthest (max_dist) -> min_reward_fraction
                normalized = (distance - min_dist) / (max_dist - min_dist)
                # Invert so closer = higher, and scale to [min_reward_fraction, 1.0]
                proximity_multiplier = 1.0 - normalized * (1.0 - self.min_reward_fraction)
            else:
                # All asteroids at same distance (rare), give full reward
                proximity_multiplier = 1.0

            # Calculate reward for all kills this frame
            reward = delta_kills * self.max_reward_per_kill * proximity_multiplier

            if debug:
                print(f"DistanceBasedKillReward: kills={delta_kills}, closest_dist={distance:.1f}, "
                      f"range=[{min_dist:.1f}, {max_dist:.1f}], multiplier={proximity_multiplier:.2f}, reward={reward:.2f}")

        self.prev_kills = current_kills
        self.prev_closest_distance = current_closest_distance
        self.prev_all_distances = current_all_distances

        return reward

    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        return 0.0

    def reset(self) -> None:
        self.prev_kills = 0
        self.prev_closest_distance = None
