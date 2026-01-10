import math
from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker


class ProximityFacingBonus(RewardComponent):
    """
    Rewards agent for facing toward nearby asteroids, with proximity weighting.

    Unlike the original FacingAsteroidBonus which rewarded facing ANY asteroid
    (leading to spinning exploits), this version only rewards facing CLOSE asteroids:
    - Closest asteroid: 100% of bonus
    - 2nd closest: 50% of bonus
    - 3rd closest: 25% of bonus
    - 4th+ closest: 0% bonus

    This encourages the agent to aim at actual threats rather than spinning in place.
    """

    def __init__(self, bonus_per_second: float = 10.0):
        """
        Args:
            bonus_per_second: Maximum bonus per second when perfectly facing closest asteroid.
        """
        self.name = "ProximityFacingBonus"
        self.bonus_per_second = bonus_per_second
        self.prev_time_alive = 0.0

        # Proximity weights for closest asteroids
        self.proximity_weights = [1.0, 0.5, 0.25]  # 1st, 2nd, 3rd closest

    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker, debug: bool = False) -> float:
        current_time = metrics_tracker.get_time_alive()
        delta_time = max(0.0, current_time - self.prev_time_alive)
        self.prev_time_alive = current_time

        player = env_tracker.get_player()
        if player is None:
            return 0.0

        # Get the 3 nearest asteroids (only these contribute to reward)
        nearest_asteroids = env_tracker.get_nearest_asteroids(3)

        if not nearest_asteroids:
            return 0.0

        total_facing_score = 0.0

        for i, asteroid in enumerate(nearest_asteroids):
            if i >= len(self.proximity_weights):
                break

            # Calculate angle to this asteroid
            dx = asteroid.center_x - player.center_x
            dy = asteroid.center_y - player.center_y

            # atan2(dx, dy) to match the game's coordinate system where angle 0 is up
            angle_to_asteroid = math.degrees(math.atan2(dx, dy))

            # Calculate how well we're facing it (angle difference)
            angle_diff = abs(player.angle - angle_to_asteroid)
            # Normalize to 0-180 range (shortest angle)
            if angle_diff > 180:
                angle_diff = 360 - angle_diff

            # Convert to facing score (1.0 = perfect alignment, 0.0 = opposite direction)
            facing_score = 1.0 - (angle_diff / 180.0)

            # Apply quadratic curve (makes it easier to learn - more reward near alignment)
            facing_score = facing_score ** 2

            # Apply proximity weight
            weighted_score = facing_score * self.proximity_weights[i]
            total_facing_score += weighted_score

            if debug:
                print(f"  Asteroid {i+1}: angle_diff={angle_diff:.1f}, facing={facing_score:.2f}, weight={self.proximity_weights[i]}, contribution={weighted_score:.3f}")

        reward = delta_time * self.bonus_per_second * total_facing_score

        if debug:
            print(f"ProximityFacingBonus: delta_time={delta_time:.4f}, current_time={current_time:.4f}, total_score={total_facing_score:.3f}, reward={reward:.3f}")

        return reward

    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        return 0.0

    def reset(self) -> None:
        self.prev_time_alive = 0.0
