import math
from typing import List, Optional, Tuple
from game.classes import asteroid, player
from game.classes.player import Player
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.StateEncoder import StateEncoder
from game import globals

class HybridEncoder(StateEncoder):
    """
    Hybrid Encoder (The "Fovea" Design).
    
    Combines:
    1. Peripheral Vision (Raycasts): 16 egocentric rays for stable spatial awareness.
    2. Fovea (Object List): 3 nearest asteroids for precision aiming.
    3. Proprioception: Player velocity and cooldown.
    """

    def __init__(
        self,
        screen_width: int = globals.SCREEN_WIDTH,
        screen_height: int = globals.SCREEN_HEIGHT,
        num_rays: int = 16,
        num_fovea_asteroids: int = 3,
        ray_max_distance: float = 0.0, # 0 means auto-calculate (diagonal)
        max_player_velocity: Optional[float] = None,
        max_asteroid_velocity: Optional[float] = None,
        max_asteroid_size: Optional[float] = None
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_rays = num_rays
        self.num_fovea_asteroids = num_fovea_asteroids
        
        # Max diagonal distance
        self.diag_distance = math.sqrt(screen_width**2 + screen_height**2)
        self.ray_max_distance = ray_max_distance if ray_max_distance > 0 else self.diag_distance

        # Normalization bounds (same as VectorEncoder)
        default_player_max = globals.PLAYER_ACCELERATION / (1 - globals.PLAYER_FRICTION)
        self.max_player_velocity = max_player_velocity if max_player_velocity is not None else default_player_max
        self.max_asteroid_velocity = max_asteroid_velocity if max_asteroid_velocity is not None else globals.ASTEROID_SPEED_SMALL
        self.max_relative_velocity = self.max_player_velocity + self.max_asteroid_velocity
        self.max_asteroid_size = max_asteroid_size if max_asteroid_size is not None else globals.ASTEROID_SCALE_LARGE

    def encode(self, env_tracker: EnvironmentTracker) -> List[float]:
        player = env_tracker.get_player()
        if player is None:
            return [0.0] * self.get_state_size()

        result = []
        
        # 1. Proprioception (3 inputs)
        result.extend(self.encode_player(player))
        
        # 2. Fovea - Nearest Asteroids (num_fovea * 4 inputs)
        result.extend(self.encode_fovea(env_tracker, player))
        
        # 3. Peripheral - Raycasts (num_rays * 1 input)
        result.extend(self.encode_rays(env_tracker, player))
        
        return result

    def get_state_size(self) -> int:
        # Player (3) + Fovea (3*4) + Rays (16) = 3 + 12 + 16 = 31 inputs
        return 3 + (self.num_fovea_asteroids * 4) + self.num_rays

    def reset(self) -> None:
        pass

    def clone(self) -> 'HybridEncoder':
        """Create a copy of this encoder."""
        return HybridEncoder(
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            num_rays=self.num_rays,
            num_fovea_asteroids=self.num_fovea_asteroids,
            ray_max_distance=self.ray_max_distance,
            max_player_velocity=self.max_player_velocity,
            max_asteroid_velocity=self.max_asteroid_velocity,
            max_asteroid_size=self.max_asteroid_size
        )

    # --- Helper Methods ---

    def encode_player(self, player: Player) -> List[float]:
        """Encode player velocity and cooldown."""
        # Get player's facing direction
        angle_rad = math.radians(player.angle)
        facing_x = math.sin(angle_rad)
        facing_y = math.cos(angle_rad)
        right_x = facing_y
        right_y = -facing_x

        # Project velocity
        fwd_vel = player.change_x * facing_x + player.change_y * facing_y
        lat_vel = player.change_x * right_x + player.change_y * right_y
        
        cooldown = 0.0
        if player.shoot_cooldown > 0:
            cooldown = self._clamp(player.shoot_timer / player.shoot_cooldown, 0.0, 1.0)

        return [
            self._clamp(fwd_vel / self.max_player_velocity, -1.0, 1.0),
            self._clamp(lat_vel / self.max_player_velocity, -1.0, 1.0),
            cooldown
        ]

    def encode_fovea(self, env_tracker: EnvironmentTracker, player: Player) -> List[float]:
        """Encode N nearest asteroids with full physics detail."""
        nearest = env_tracker.get_nearest_asteroids(self.num_fovea_asteroids)
        result = []
        
        for i in range(self.num_fovea_asteroids):
            if i < len(nearest):
                ast = nearest[i]
                # Reuse the relative physics logic from VectorEncoder
                # 1. Relative Pos (Wrapped)
                rel_x = ast.center_x - player.center_x
                rel_y = ast.center_y - player.center_y
                
                if abs(rel_x) > self.screen_width / 2:
                    rel_x = -1 * math.copysign(self.screen_width - abs(rel_x), rel_x)
                if abs(rel_y) > self.screen_height / 2:
                    rel_y = -1 * math.copysign(self.screen_height - abs(rel_y), rel_y)
                
                dist = math.sqrt(rel_x**2 + rel_y**2)
                
                # 2. Angle to Target (Relative to Ship Heading)
                ast_angle = math.degrees(math.atan2(rel_x, rel_y))
                angle_diff = ast_angle - player.angle
                while angle_diff > 180: angle_diff -= 360
                while angle_diff < -180: angle_diff += 360
                
                # 3. Closing Speed
                rel_vx = ast.change_x - player.change_x
                rel_vy = ast.change_y - player.change_y
                closing_speed = 0.0
                if dist > 0.001:
                    closing_speed = -(rel_x * rel_vx + rel_y * rel_vy) / dist
                
                # Normalize
                norm_dist = min(dist / self.diag_distance, 1.0)
                norm_angle = angle_diff / 180.0
                norm_speed = self._clamp(closing_speed / self.max_relative_velocity, -1.0, 1.0)
                norm_size = min(ast.this_scale / self.max_asteroid_size, 1.0)
                
                result.extend([norm_dist, norm_angle, norm_speed, norm_size])
            else:
                # Padding (Safe State)
                result.extend([1.0, 0.0, 0.0, 0.0])
        return result

    def encode_rays(self, env_tracker: EnvironmentTracker, player: Player) -> List[float]:
        """Cast egocentric rays to detect asteroids."""
        asteroids = env_tracker.get_all_asteroids()
        if not asteroids:
            return [1.0] * self.num_rays

        # Pre-calculate relative asteroid positions (wrapped)
        # This optimization avoids re-calculating wrap for every ray
        targets = []
        for ast in asteroids:
            rel_x = ast.center_x - player.center_x
            rel_y = ast.center_y - player.center_y
            if abs(rel_x) > self.screen_width / 2:
                rel_x = -1 * math.copysign(self.screen_width - abs(rel_x), rel_x)
            if abs(rel_y) > self.screen_height / 2:
                rel_y = -1 * math.copysign(self.screen_height - abs(rel_y), rel_y)
            
            radius = globals.ASTEROID_BASE_RADIUS * ast.this_scale
            targets.append((rel_x, rel_y, radius))

        rays = []
        angle_step = 360.0 / self.num_rays
        
        # Ray 0 is typically "Front" (same as player angle)
        # We start at player.angle and sweep around
        start_angle = player.angle 

        for i in range(self.num_rays):
            ray_angle_deg = start_angle - (i * angle_step) # Scan Left (-), or Right (+)? 
            # Arcade angle: 0=Up (Y+), -90=Right (X+). 
            # Standard Math: 0=Right (X+), 90=Up (Y+).
            # Arcade Rotation: - is Left turn, + is Right turn.
            # Let's match typical sensor sweep: 0, -22.5, -45... (Sweeping Left/CCW?)
            # Or 0, +22.5, +45... (Sweeping Right/CW)
            # Order matters for the Neural Network topology but consistency is key.
            
            ray_rad = math.radians(ray_angle_deg)
            ray_dx = math.sin(ray_rad) # Arcade 0 is Y+, so Sin is X component
            ray_dy = math.cos(ray_rad) # Cos is Y component
            
            min_dist = self.ray_max_distance
            
            # Check intersection with all asteroids
            for tx, ty, rad in targets:
                # Math: Ray Intersection with Circle
                # Ray Origin is (0,0) relative to player
                # Ray Dir is (ray_dx, ray_dy)
                # Circle Center is (tx, ty), Radius rad
                
                # Project Circle Center onto Ray
                # t = Dot(Center, RayDir)
                t = tx * ray_dx + ty * ray_dy
                
                if t < 0: 
                    # Behind the ray start
                    continue 
                    
                if t > self.ray_max_distance + rad:
                    # Too far
                    continue

                # Closest point on ray to circle center
                closest_x = t * ray_dx
                closest_y = t * ray_dy
                
                # Distance from closest point to circle center
                dist_sq = (closest_x - tx)**2 + (closest_y - ty)**2
                
                if dist_sq < rad * rad:
                    # Intersection!
                    # Distance to intersection point = t - sqrt(rad^2 - dist_sq)
                    dt = math.sqrt(rad * rad - dist_sq)
                    hit_dist = t - dt
                    
                    if hit_dist < 0: hit_dist = 0 # Inside asteroid
                    if hit_dist < min_dist:
                        min_dist = hit_dist
            
            # Normalize
            rays.append(min_dist / self.ray_max_distance)
            
        return rays

    def _clamp(self, value: float, min_val: float, max_val: float) -> float:
        return max(min_val, min(max_val, value))
