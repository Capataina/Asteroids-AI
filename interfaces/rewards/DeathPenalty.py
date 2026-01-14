from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker


class DeathPenalty(RewardComponent):
    """
    Applies a penalty when the player dies (episode ends due to collision).

    This provides a clear negative signal that dying is bad, helping the agent
    understand that survival matters, not just accumulating points quickly.
    """

    def __init__(
        self,
        penalty: float = -200.0,
        max_time_alive: float | None = None,
        early_death_scale: float = 0.0
    ):
        """
        Args:
            penalty: Negative reward applied when player dies (default: -200)
            max_time_alive: Expected maximum time alive for scaling early deaths.
            early_death_scale: Multiplier applied to the penalty when dying early.
        """
        self.name = "DeathPenalty"
        self.penalty = penalty
        self.max_time_alive = max_time_alive
        self.early_death_scale = early_death_scale
        self.death_applied = False

    def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
        """
        Apply death penalty when player dies (detected by player not in player_list).
        """
        # Check if player died this step (not in player_list anymore)
        if not env_tracker.is_player_alive() and not self.death_applied:
            # Player just died - apply penalty once
            self.death_applied = True
            if self.max_time_alive and self.max_time_alive > 0:
                time_alive = metrics_tracker.get_time_alive()
                normalized = max(0.0, min(time_alive / self.max_time_alive, 1.0))
                scale = 1.0 + self.early_death_scale * (1.0 - normalized)
                return self.penalty * scale
            return self.penalty

        return 0.0

    def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
        # Death penalty is handled in step reward when death is detected
        return 0.0

    def reset(self) -> None:
        self.death_applied = False
