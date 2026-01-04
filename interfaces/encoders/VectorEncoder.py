import math
from typing import List, Optional
from game.classes import asteroid, bullet
from game.classes import player
from game.classes.player import Player
from interfaces.EnvironmentTracker import EnvironmentTracker

class VectorEncoder:
  def __init__(
      self, 
      screen_width: int = 800, 
      screen_height: int = 600, 
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

    Args:
      screen_width: The width of the screen.
      screen_height: The height of the screen.
      num_nearest_asteroids: The number of nearest asteroids to include.
      num_nearest_bullets: The number of nearest bullets to include.
      include_bullets: Whether to include bullets in the state.
      include_global: Whether to include global state in the state.
      max_player_velocity: Max player velocity for normalization. If None, calculated from physics.
      max_asteroid_velocity: Max asteroid velocity for normalization. If None, calculated from physics.
      max_asteroid_size: Max asteroid size for normalization. If None, uses 1.25 (from Asteroid class).
      max_asteroid_hp: Max asteroid HP for normalization. If None, uses 3.0 (from Asteroid class).
    """
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.num_nearest_asteroids = num_nearest_asteroids
    self.num_nearest_bullets = num_nearest_bullets
    self.include_bullets = include_bullets
    self.include_global = include_global

    # Calculate max velocities from game physics if not provided
    # Player: acceleration=0.3, slowdown=0.99
    # Theoretical max: 0.3 / (1 - 0.99) = 30 per component
    # Use 15 as practical maximum (rarely exceeds this in gameplay)
    self.max_player_velocity = max_player_velocity if max_player_velocity is not None else 15.0
    
    # Asteroids: max_speed ranges 1-3, max component is 3
    # Max magnitude: sqrt(3² + 3²) ≈ 4.24, but we normalize per component
    self.max_asteroid_velocity = max_asteroid_velocity if max_asteroid_velocity is not None else 3.0
    
    # Asteroid size: max scale is 1.25 (from Asteroid.__init__ default)
    self.max_asteroid_size = max_asteroid_size if max_asteroid_size is not None else 1.25
    
    # Asteroid HP: max is 3 (from Asteroid.__init__)
    self.max_asteroid_hp = max_asteroid_hp if max_asteroid_hp is not None else 3.0

    self.validate_parameters()

  def validate_parameters(self):
    """
    Validate the parameters.

    Args:
      None

    Returns:
      True if the parameters are valid, raises ValueError otherwise.
    """
    if type(self.screen_width) != int or type(self.screen_height) != int:
      raise ValueError("screen_width and screen_height must be integers")
    if type(self.num_nearest_asteroids) != int:
      raise ValueError("num_nearest_asteroids must be an integer")
    if type(self.num_nearest_bullets) != int:
      raise ValueError("num_nearest_bullets must be an integer")
    if type(self.include_bullets) != bool or type(self.include_global) != bool:
      raise ValueError("include_bullets and include_global must be booleans")
    if self.include_bullets and self.include_global:
      raise ValueError("include_bullets and include_global cannot be True at the same time")
    if self.screen_width <= 0 or self.screen_height <= 0:
      raise ValueError("screen_width and screen_height must be positive")
    if self.max_player_velocity <= 0 or self.max_asteroid_velocity <= 0:
      raise ValueError("max velocities must be positive")
    if self.max_asteroid_size <= 0 or self.max_asteroid_hp <= 0:
      raise ValueError("max_asteroid_size and max_asteroid_hp must be positive")
    return True

  def encode(self, env_tracker: EnvironmentTracker) -> List[float]:
    """
    Encode the environment tracker state into a vector.
    Returns a flat list of floats.
    """
    # Encode player (returns list of 6 floats)
    player_encoding = self.encode_player(env_tracker)
    
    # Encode asteroids (returns list of lists, need to flatten)
    asteroids_encoding = self.encode_asteroids(env_tracker)
    
    # Encode bullets (returns list of lists, need to flatten)
    bullets_encoding = self.encode_bullets(env_tracker)
    
    # Flatten and concatenate all encodings
    result = player_encoding.copy()
    
    # Flatten asteroids encoding
    for asteroid_features in asteroids_encoding:
      if isinstance(asteroid_features, list):
        result.extend(asteroid_features)
      else:
        result.append(float(asteroid_features))
    
    # Flatten bullets encoding
    for bullet_features in bullets_encoding:
      if isinstance(bullet_features, list):
        result.extend(bullet_features)
      else:
        result.append(float(bullet_features))
    
    return result


  # Encoding Methods

  def encode_player(self, env_tracker: EnvironmentTracker) -> List[float]:
    """
    Encode the player state into a vector.

    Args:
      env_tracker: The environment tracker to use for the state.

    Returns:
      The encoded player state.
    """
    player = env_tracker.get_player()

    if player is None:
      return [0.0] * 6
    
    return [
      self.normalize_position(player.center_x), 
      self.normalize_position(player.center_y), 
      self.normalize_velocity(player.change_x), 
      self.normalize_velocity(player.change_y), 
      self.normalize_angle_sin(player.angle), 
      self.normalize_angle_cos(player.angle), 
    ]


  def encode_asteroids(self, env_tracker: EnvironmentTracker) -> List[List[float]]:
    """
    Encode the asteroids state into a list of vectors.
    Returns a list of lists (one list per asteroid).

    Args:
      asteroids: The asteroids to encode.
      env_tracker: The environment tracker to use for the state.

    Returns:
      List of encoded asteroid states (list of lists).
    """
    asteroids = env_tracker.get_all_asteroids()
    player = env_tracker.get_player()

    if asteroids is None or player is None or len(asteroids) == 0:
      # Return zero-padded encoding for missing asteroids
      return [[0.0] * 5 for _ in range(self.num_nearest_asteroids)]
    
    # Encode available asteroids
    encoded = []
    for i in range(self.num_nearest_asteroids):
      if i < len(asteroids):
        encoded.append(self.encode_asteroid(asteroids[i], player, env_tracker))
      else:
        # Pad with zeros if we have fewer asteroids than expected
        encoded.append([0.0] * 5)
    
    return encoded

  def encode_asteroid(self, asteroid: asteroid.Asteroid, player: Player, env_tracker: EnvironmentTracker) -> List[float]:
    """
    Encode the asteroid state into a vector.

    Args:
      asteroid: The asteroid to encode.
      player: The player to use for relative position and velocity.
      env_tracker: The environment tracker to use for the state.

    Returns:
      The encoded asteroid state.
    """
    
    # Calculate relative position
    relative_x = asteroid.center_x - player.center_x
    relative_y = asteroid.center_y - player.center_y

    # Calculate distance
    distance = player.get_distance(relative_x, relative_y)

    # Calculate relative velocity
    relative_velocity_x = asteroid.change_x - player.change_x
    relative_velocity_y = asteroid.change_y - player.change_y

    return [
      self.normalize_position(relative_x), 
      self.normalize_position(relative_y), 
      self.normalize_distance(distance, env_tracker), 
      self.normalize_velocity(relative_velocity_x), 
      self.normalize_velocity(relative_velocity_y), 
    ]

  def encode_bullets(self, env_tracker: EnvironmentTracker) -> List[List[float]]:
    """
    Encode bullets state into a list of vectors (if include_bullets is True).
    Returns a list of lists (one list per bullet).

    Args:
      bullets: The bullets to encode.
      player: The player to use for relative position and velocity.
      env_tracker: The environment tracker to use for the state.

    Returns:
      List of encoded bullet states (list of lists).
    """
    if not self.include_bullets:
      return []

    bullets = env_tracker.get_all_bullets()
    player = env_tracker.get_player()
    
    if bullets is None or player is None or len(bullets) == 0:
      # Return zero-padded encoding for missing bullets
      return [[0.0] * 5 for _ in range(self.num_nearest_bullets)]
    
    # Encode available bullets
    encoded = []
    for i in range(self.num_nearest_bullets):
      if i < len(bullets):
        encoded.append(self.encode_bullet(bullets[i], player, env_tracker))
      else:
        # Pad with zeros if we have fewer bullets than expected
        encoded.append([0.0] * 5)
    
    return encoded

  def encode_bullet(self, bullet: bullet.Bullet, player: Player, env_tracker: EnvironmentTracker) -> List[float]:
    """
    Encode the bullet state into a vector.

    Args:
      bullet: The bullet to encode.
      player: The player to use for relative position and velocity.
      env_tracker: The environment tracker to use for the state.

    Returns:
      The encoded bullet state.
    """
    if bullet is None or player is None:
      return [0.0] * 4
    
    # Calculate relative position
    relative_x = bullet.center_x - player.center_x
    relative_y = bullet.center_y - player.center_y

    # Calculate distance
    distance = player.get_distance(relative_x, relative_y)

    # Calculate relative velocity
    relative_velocity_x = bullet.change_x - player.change_x
    relative_velocity_y = bullet.change_y - player.change_y
    
    return [
      self.normalize_position(relative_x), 
      self.normalize_position(relative_y), 
      self.normalize_distance(distance, env_tracker), 
      self.normalize_velocity(relative_velocity_x), 
      self.normalize_velocity(relative_velocity_y), 
    ]

  def encode_global(self, env_tracker: EnvironmentTracker) -> List[float]:
    """
    Encode global state into a vector (if include_global is True).
    """
    if not self.include_global:
      return []
    # TODO: Implement global state encoding
    return []

  def get_state_size(self) -> int:
    """
    Get the size of the encoded state vector.
    """
    size = 6  # Player features (x, y, vx, vy, sin(angle), cos(angle))
    size += 5 * self.num_nearest_asteroids  # Asteroid features (rel_x, rel_y, distance, rel_vx, rel_vy) per asteroid
    if self.include_bullets:
      size += 5 * self.num_nearest_bullets  # Bullet features (rel_x, rel_y, distance, rel_vx, rel_vy) per bullet
    if self.include_global:
      size += 2  # Global features (TODO: update when implemented)
    return size


  # Helper Methods - Used in the encoding methods

  # Normalize position to 0-1 range
  def normalize_position(self, position: float) -> float:
    return position / self.screen_width

  # Normalize velocity to -1-1 range
  def normalize_velocity(self, velocity: float) -> float:
    return velocity / self.max_player_velocity

  # Normalize distance to 0-1 range
  def normalize_distance(self, distance: float, env_tracker: EnvironmentTracker) -> float:
    return distance / env_tracker.get_player().get_max_distance(self.screen_width, self.screen_height) / 2

  # Normalize angle to -1-1 range
  def normalize_angle_sin(self, angle: float) -> float:
    return math.sin(math.radians(angle))

  # Normalize angle to -1-1 range
  def normalize_angle_cos(self, angle: float) -> float:
    return math.cos(math.radians(angle))

  def reset(self) -> None:
    """
    Reset any internal state (if needed).
    VectorEncoder has no internal state, so this is a no-op.
    """
    pass