import math
from typing import List, Optional
from game.classes import asteroid, bullet
from game.classes import player
from game.classes.player import Player
from interfaces.EnvironmentTracker import EnvironmentTracker

from game import globals

class VectorEncoder:
  """
  Encodes game state into a fixed-size vector for neural network input.
  """

  def __init__(
      self,
      screen_width: int = globals.SCREEN_WIDTH,
      screen_height: int = globals.SCREEN_HEIGHT,
      num_nearest_asteroids: int = 8,
      num_nearest_bullets: int = 8,
      include_bullets: bool = False,
      include_global: bool = False,
      max_player_velocity: Optional[float] = None,
      max_asteroid_velocity: Optional[float] = None,
      max_asteroid_size: Optional[float] = None,
      max_asteroid_hp: Optional[float] = None
  ):
    """
    Initialize the VectorEncoder.
    """
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.num_nearest_asteroids = num_nearest_asteroids
    self.num_nearest_bullets = num_nearest_bullets
    self.include_bullets = include_bullets
    self.include_global = include_global

    # Max diagonal distance for normalization
    self.max_distance = math.sqrt(screen_width**2 + screen_height**2)

    # Velocity bounds for normalization
    # Terminal velocity = accel / (1 - friction)
    default_player_max = globals.PLAYER_ACCELERATION / (1 - globals.PLAYER_FRICTION)
    self.max_player_velocity = max_player_velocity if max_player_velocity is not None else default_player_max
    
    self.max_asteroid_velocity = max_asteroid_velocity if max_asteroid_velocity is not None else globals.ASTEROID_SPEED_SMALL

    # Max relative velocity (player + asteroid can approach each other)
    self.max_relative_velocity = self.max_player_velocity + self.max_asteroid_velocity

    # Asteroid size bounds
    self.max_asteroid_size = max_asteroid_size if max_asteroid_size is not None else globals.ASTEROID_SCALE_LARGE
    self.max_asteroid_hp = max_asteroid_hp if max_asteroid_hp is not None else float(globals.ASTEROID_HP_LARGE)

    self.validate_parameters()

  def validate_parameters(self):
    """Validate the parameters."""
    if type(self.screen_width) != int or type(self.screen_height) != int:
      raise ValueError("screen_width and screen_height must be integers")
    if type(self.num_nearest_asteroids) != int:
      raise ValueError("num_nearest_asteroids must be an integer")
    if type(self.num_nearest_bullets) != int:
      raise ValueError("num_nearest_bullets must be an integer")
    if type(self.include_bullets) != bool or type(self.include_global) != bool:
      raise ValueError("include_bullets and include_global must be booleans")
    if self.screen_width <= 0 or self.screen_height <= 0:
      raise ValueError("screen_width and screen_height must be positive")
    if self.max_player_velocity <= 0 or self.max_asteroid_velocity <= 0:
      raise ValueError("max velocities must be positive")
    if self.max_asteroid_size <= 0 or self.max_asteroid_hp <= 0:
      raise ValueError("max_asteroid_size and max_asteroid_hp must be positive")
    return True

  def encode(self, env_tracker: EnvironmentTracker) -> List[float]:
    """
    Encode the environment state into a flat vector.

    Returns:
      Flat list of floats representing the state.
    """
    player = env_tracker.get_player()

    if player is None:
      # Return zeros for dead player
      return [0.0] * self.get_state_size()

    result = []

    # Encode player state (egocentric velocity)
    result.extend(self.encode_player(player))

    # Encode nearest asteroids (egocentric position and dynamics)
    result.extend(self.encode_asteroids(env_tracker, player))

    return result

  def encode_player(self, player: Player) -> List[float]:
    """
    Encode player state in egocentric frame.

    Returns:
      [forward_velocity, lateral_velocity, shoot_cooldown]
    """
    # Get player's facing direction as unit vector
    angle_rad = math.radians(player.angle)
    facing_x = math.sin(angle_rad)  # Forward direction X
    facing_y = math.cos(angle_rad)  # Forward direction Y

    # Perpendicular (right) direction
    right_x = facing_y   # cos(angle) = sin(angle + 90)
    right_y = -facing_x  # -sin(angle) = cos(angle + 90)

    # Project velocity onto facing direction (forward velocity)
    forward_velocity = player.change_x * facing_x + player.change_y * facing_y

    # Project velocity onto right direction (lateral velocity)
    lateral_velocity = player.change_x * right_x + player.change_y * right_y
    
    # Encode shoot cooldown (0 = ready to fire, 1 = full cooldown)
    normalized_cooldown = 0.0
    if player.shoot_cooldown > 0:
        normalized_cooldown = self._clamp(player.shoot_timer / player.shoot_cooldown, 0.0, 1.0)

    return [
      self._clamp(forward_velocity / self.max_player_velocity, -1.0, 1.0),
      self._clamp(lateral_velocity / self.max_player_velocity, -1.0, 1.0),
      normalized_cooldown
    ]

  def encode_asteroids(self, env_tracker: EnvironmentTracker, player: Player) -> List[float]:
    """
    Encode nearest asteroids in egocentric frame.

    Returns:
      Flat list of asteroid features: [dist, angle, closing_speed, size] per asteroid
    """
    nearest_asteroids = env_tracker.get_nearest_asteroids(self.num_nearest_asteroids)

    result = []
    for i in range(self.num_nearest_asteroids):
      if i < len(nearest_asteroids):
        result.extend(self.encode_asteroid(nearest_asteroids[i], player))
      else:
        # Pad with zeros for missing asteroids
        # Use "safe" default: far away, straight ahead, not approaching, small
        result.extend([1.0, 0.0, 0.0, 0.0])

    return result

  def encode_asteroid(self, ast: asteroid.Asteroid, player: Player) -> List[float]:
    """
    Encode a single asteroid in egocentric frame.

    Returns:
      [distance, angle_to_target, closing_speed, size]
    """
    # Calculate relative position (world frame)
    rel_x = ast.center_x - player.center_x
    rel_y = ast.center_y - player.center_y

    # Handle screen wrapping (Toroidal distance)
    # If distance is more than half the screen, the other way is shorter
    if abs(rel_x) > self.screen_width / 2:
        rel_x = -1 * math.copysign(self.screen_width - abs(rel_x), rel_x)
    
    if abs(rel_y) > self.screen_height / 2:
        rel_y = -1 * math.copysign(self.screen_height - abs(rel_y), rel_y)

    # Calculate distance (CORRECT calculation)
    distance = math.sqrt(rel_x * rel_x + rel_y * rel_y)

    # Normalize distance to [0, 1]
    normalized_distance = min(distance / self.max_distance, 1.0)

    # Calculate angle to asteroid (world frame)
    # atan2 returns angle in radians, measured from +Y axis
    asteroid_angle = math.degrees(math.atan2(rel_x, rel_y))

    # Calculate angle to turn to face asteroid
    # Positive = turn right, Negative = turn left
    angle_to_target = asteroid_angle - player.angle

    # Normalize to [-180, +180]
    while angle_to_target > 180:
      angle_to_target -= 360
    while angle_to_target < -180:
      angle_to_target += 360

    # Normalize to [-1, 1]
    normalized_angle = angle_to_target / 180.0

    # Calculate closing speed (positive = getting closer)
    rel_vx = ast.change_x - player.change_x
    rel_vy = ast.change_y - player.change_y

    if distance > 0.001:  # Avoid division by zero
      # Project relative velocity onto direction vector (toward asteroid)
      # Negative because we want positive = approaching
      closing_speed = -(rel_x * rel_vx + rel_y * rel_vy) / distance
    else:
      closing_speed = 0.0

    # Normalize closing speed
    normalized_closing_speed = self._clamp(closing_speed / self.max_relative_velocity, -1.0, 1.0)

    # Normalize asteroid size
    normalized_size = min(ast.this_scale / self.max_asteroid_size, 1.0)

    return [
      normalized_distance,
      normalized_angle,
      normalized_closing_speed,
      normalized_size,
    ]

  def get_state_size(self) -> int:
    """
    Get the size of the encoded state vector.

    Returns:
      Number of features in the encoded state.
    """
    size = 3  # Player features (forward_velocity, lateral_velocity, shoot_cooldown)
    size += 4 * self.num_nearest_asteroids  # Asteroid features (distance, angle, closing_speed, size)
    return size

  def _clamp(self, value: float, min_val: float, max_val: float) -> float:
    """Clamp a value to a range."""
    return max(min_val, min(max_val, value))

  def reset(self) -> None:
    """Reset any internal state (if needed)."""
    pass

  def clone(self) -> 'VectorEncoder':
    """Create a copy of this encoder."""
    return VectorEncoder(
        screen_width=self.screen_width,
        screen_height=self.screen_height,
        num_nearest_asteroids=self.num_nearest_asteroids,
        num_nearest_bullets=self.num_nearest_bullets,
        include_bullets=self.include_bullets,
        include_global=self.include_global,
        max_player_velocity=self.max_player_velocity,
        max_asteroid_velocity=self.max_asteroid_velocity,
        max_asteroid_size=self.max_asteroid_size,
        max_asteroid_hp=self.max_asteroid_hp
    )
