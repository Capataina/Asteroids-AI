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
        # Survival - reduced slightly to balance with kills
        (VelocitySurvivalBonus, {"reward_multiplier": 2.0, "max_velocity_cap": 15.0}),

        # Kills - significantly increased now that bullets properly expire
        # Close-range kills worth more than long-range
        (DistanceBasedKillReward, {"max_reward_per_kill": 75.0, "min_distance": 50.0, "max_distance": 400.0}),

        # Accuracy - higher hit bonus to encourage aimed shots
        (ConservingAmmoBonus, {"hit_bonus": 20.0, "shot_penalty": -3.0}),

        # Exploration - reduced slightly to balance with kills
        (ExplorationBonus, {"screen_width": globals.SCREEN_WIDTH, "screen_height": globals.SCREEN_HEIGHT, "grid_rows": 3, "grid_cols": 4, "bonus_per_cell": 6.0}),

        # Death penalty - keeps agents from being too reckless
        (DeathPenalty, {"penalty": -150.0}),
    ]
}

def create_reward_calculator(preset="default"):
    calc = ComposableRewardCalculator()
    if preset not in REWARD_PRESETS:
        raise ValueError(f"Unknown reward preset: {preset}")
        
    for component_class, kwargs in REWARD_PRESETS[preset]:
        calc.add_component(component_class(**kwargs))
    return calc
