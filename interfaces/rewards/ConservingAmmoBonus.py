from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker


class ConservingAmmoBonus(RewardComponent):
    """
    Rewards actual hits on asteroids, penalizes missed shots.

    This provides a clear skill signal: you get rewarded for shots that
    actually connect, not just for aiming in the right direction.
    """

    def __init__(self, hit_bonus: float = 20.0, shot_penalty: float = -5.0, **kwargs):
        """
        Args:
            hit_bonus: Reward given when a bullet hits an asteroid
            shot_penalty: Penalty for each shot fired (encourages conservation)
            **kwargs: Accepts but ignores legacy parameters (good_shot_bonus, bad_shot_penalty, alignment_threshold)
        """
        self.name = "ConservingAmmoBonus"
        self.hit_bonus = hit_bonus
        self.shot_penalty = shot_penalty
        self.prev_shots = 0
        self.prev_hits = 0

    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
        current_shots = metrics_tracker.get_total_shots_fired()
        current_hits = metrics_tracker.get_total_hits()

        reward = 0.0

        # Penalty for each shot fired (discourages spray-and-pray)
        shots_this_step = current_shots - self.prev_shots
        if shots_this_step > 0:
            reward += self.shot_penalty * shots_this_step

        # Bonus for each actual hit (rewards accuracy)
        hits_this_step = current_hits - self.prev_hits
        if hits_this_step > 0:
            reward += self.hit_bonus * hits_this_step

        self.prev_shots = current_shots
        self.prev_hits = current_hits
        return reward

    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        return 0.0

    def reset(self) -> None:
        self.prev_shots = 0
        self.prev_hits = 0
