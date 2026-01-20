from typing import Dict, List, Optional
import math
from interfaces.RewardCalculator import RewardComponent
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker
from game import globals

class TargetLockReward(RewardComponent):
    """
    Rewards the agent for keeping the nearest asteroid within a narrow aiming cone.
    Encourages "locking on" to targets rather than spinning blindly.
    """
    def __init__(self, 
                 aim_cone_degrees: float = 15.0, 
                 reward_per_frame: float = 0.5,
                 max_distance: float = 400.0,
                 num_targets: int = 1):
        self.name = "TargetLockReward"
        self.aim_cone_degrees = aim_cone_degrees
        self.reward_per_frame = reward_per_frame
        self.max_distance = max_distance
        self.num_targets = num_targets

    def calculate_step_reward(self, tracker: EnvironmentTracker, metrics: MetricsTracker) -> float:
        player = tracker.get_player()
        if player is None:
            return 0.0

        nearest_asteroids = tracker.get_nearest_asteroids(self.num_targets)
        if not nearest_asteroids:
            return 0.0

        total_reward = 0.0
        
        # Check lock on closest targets
        for ast in nearest_asteroids:
            # Calculate relative vector (wrapped)
            rel_x = ast.center_x - player.center_x
            rel_y = ast.center_y - player.center_y
            
            # Manual wrap check (tracker handles this but getting raw coords is safer)
            if abs(rel_x) > globals.SCREEN_WIDTH / 2:
                rel_x = -1 * math.copysign(globals.SCREEN_WIDTH - abs(rel_x), rel_x)
            if abs(rel_y) > globals.SCREEN_HEIGHT / 2:
                rel_y = -1 * math.copysign(globals.SCREEN_HEIGHT - abs(rel_y), rel_y)
                
            dist = math.sqrt(rel_x**2 + rel_y**2)
            
            if dist > self.max_distance:
                continue

            # Calculate angle to target
            target_angle = math.degrees(math.atan2(rel_x, rel_y)) # arcade 0 is up
            
            # Calculate angle difference
            angle_diff = target_angle - player.angle
            while angle_diff > 180: angle_diff -= 360
            while angle_diff < -180: angle_diff += 360
            
            # Check if within cone
            if abs(angle_diff) <= self.aim_cone_degrees:
                # Reward scales with alignment precision (closer to center = more points)
                alignment_bonus = 1.0 - (abs(angle_diff) / self.aim_cone_degrees)
                total_reward += self.reward_per_frame * alignment_bonus

        return total_reward

    def calculate_episode_reward(self, metrics: MetricsTracker) -> float:
        return 0.0

    def reset(self):
        pass
