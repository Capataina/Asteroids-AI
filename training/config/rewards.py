from interfaces.RewardCalculator import ComposableRewardCalculator
from interfaces.rewards.SurvivalBonus import SurvivalBonus
from interfaces.rewards.VelocitySurvivalBonus import VelocitySurvivalBonus
from interfaces.rewards.KillAsteroid import KillAsteroid
from interfaces.rewards.ChunkBonus import ChunkBonus
from interfaces.rewards.NearMiss import NearMiss
from interfaces.rewards.AccuracyBonus import AccuracyBonus
from interfaces.rewards.KPMBonus import KPMBonus
from interfaces.rewards.ShootingPenalty import ShootingPenalty
from interfaces.rewards.FacingAsteroidBonus import FacingAsteroidBonus
from interfaces.rewards.ProximityFacingBonus import ProximityFacingBonus
from interfaces.rewards.DistanceBasedKillReward import DistanceBasedKillReward
from interfaces.rewards.ConservingAmmoBonus import ConservingAmmoBonus
from interfaces.rewards.LeadingTargetBonus import LeadingTargetBonus
from interfaces.rewards.MovingTowardDangerBonus import MovingTowardDangerBonus
from interfaces.rewards.SpacingFromWallsBonus import SpacingFromWallsBonus
from interfaces.rewards.MaintainingMomentumBonus import MaintainingMomentumBonus
from interfaces.rewards.DeathPenalty import DeathPenalty
from interfaces.rewards.ProximityPenalty import ProximityPenalty
from interfaces.rewards.VelocityKillBonus import VelocityKillBonus
from interfaces.rewards.ExplorationBonus import ExplorationBonus
from game import globals

REWARD_PRESETS = {
    "default": [
        # Survival - keep meaningful but avoid dominating the total reward.
        (VelocitySurvivalBonus, {"reward_multiplier": 1.5, "max_velocity_cap": 15.0}),

        # Kills - dynamic scaling; keep strong but not a runaway winner.
        (DistanceBasedKillReward, {"max_reward_per_kill": 18.0, "min_reward_fraction": 0.15}),

        # Accuracy - reduce hit reward so it is clearly below kill reward.
        (ConservingAmmoBonus, {"hit_bonus": 4.0, "shot_penalty": -2.0}),

        # Exploration - small, consistent bonus to promote traversal.
        (ExplorationBonus, {"screen_width": globals.SCREEN_WIDTH, "screen_height": globals.SCREEN_HEIGHT, "grid_rows": 3, "grid_cols": 4, "bonus_per_cell": 5.0}),

        # Death penalty - scaled to make early deaths meaningfully worse than late deaths.
        (DeathPenalty, {"penalty": -150.0, "early_death_scale": 1.0}),
    ]
}

def create_reward_calculator(
    preset: str = "default",
    max_steps: int | None = None,
    frame_delay: float | None = None
):
    calc = ComposableRewardCalculator()
    if preset not in REWARD_PRESETS:
        raise ValueError(f"Unknown reward preset: {preset}")

    max_time_alive = None
    if max_steps is not None and frame_delay is not None:
        max_time_alive = max_steps * frame_delay

    for component_class, kwargs in REWARD_PRESETS[preset]:
        component_kwargs = dict(kwargs)
        if component_class is DeathPenalty and max_time_alive is not None:
            component_kwargs["max_time_alive"] = max_time_alive
        calc.add_component(component_class(**component_kwargs))
    return calc
