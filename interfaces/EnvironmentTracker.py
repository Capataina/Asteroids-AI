import math
from typing import TYPE_CHECKING, List, Optional, Tuple

if TYPE_CHECKING:
    from Asteroids import AsteroidsGame

from game.classes.bullet import Bullet
from game.classes.asteroid import Asteroid
from game.classes.player import Player


class EnvironmentTracker:
    def __init__(self, game: 'AsteroidsGame'):
        self.game = game

    def update(self, game: 'AsteroidsGame') -> None:
        self.game = game

    # Current state access
    def get_all_bullets(self) -> List[Bullet]:
        return self.game.bullet_list

    def get_all_asteroids(self) -> List[Asteroid]:
        return self.game.asteroid_list
    
    def get_player(self) -> Optional[Player]:
        return self.game.player

    def is_player_alive(self) -> bool:
        """Check if player is alive (in player_list)."""
        return self.game.player is not None and self.game.player in self.game.player_list
        
    def get_tick(self) -> int:
        return self.game.time
    
    # Per-tick events (reset each frame)
    # TODO: Implement this later
    #   def get_shots_fired_this_tick(self) -> int:
    #    return self.game.shots_fired_this_tick

    # TODO: Implement this later
    #   def get_asteroids_destroyed_this_tick(self) -> int:
    #    return self.game.asteroids_destroyed_this_tick
    
    # Derived state
    def get_nearest_asteroid(self) -> Optional[Asteroid]:
        """
        Get the nearest asteroid to the player.
        
        Returns:
            The nearest Asteroid, or None if no asteroids exist or no player exists.
        """
        if not self.game.player or not self.game.asteroid_list:
            return None
        
        asteroid_distances = self._get_asteroid_distances()
        if not asteroid_distances:
            return None
        
        # Sort by distance (first element of tuple)
        asteroid_distances.sort(key=lambda x: x[1])
        return asteroid_distances[0][0]  # Return the asteroid (first element of first tuple)

    def get_distance_to_nearest_asteroid(self) -> Optional[float]:
        """
        Get the distance to the nearest asteroid.
        
        Returns:
            Distance to nearest asteroid, or None if no asteroids exist or no player exists.
        """
        if not self.game.player or not self.game.asteroid_list:
            return None
        
        asteroid_distances = self._get_asteroid_distances()
        if not asteroid_distances:
            return None
        
        # Sort by distance
        asteroid_distances.sort(key=lambda x: x[1])
        return asteroid_distances[0][1]  # Return the distance (second element of first tuple)
    
    def get_asteroids_in_range(self, distance: float) -> List[Asteroid]:
        """
        Get all asteroids within a given distance of the player.
        
        Args:
            distance: Maximum distance to consider.
            
        Returns:
            List of asteroids within the specified distance.
        """
        if not self.game.player or not self.game.asteroid_list:
            return []
        
        asteroid_distances = self._get_asteroid_distances()
        # Filter by distance and return asteroids
        return [asteroid for asteroid, dist in asteroid_distances if dist < distance]
    
    def get_nearest_asteroids(self, num_asteroids: int) -> List[Asteroid]:
        """
        Get the N nearest asteroids to the player.
        
        Args:
            num_asteroids: Number of nearest asteroids to return.
            
        Returns:
            List of the nearest asteroids, sorted by distance (nearest first).
            Returns fewer than num_asteroids if there aren't enough asteroids.
        """
        if not self.game.player or not self.game.asteroid_list:
            return []
        
        asteroid_distances = self._get_asteroid_distances()
        if not asteroid_distances:
            return []
        
        # Sort by distance (nearest first)
        asteroid_distances.sort(key=lambda x: x[1])
        
        # Return the first num_asteroids asteroids
        return [asteroid for asteroid, _ in asteroid_distances[:num_asteroids]]

    # TODO: Implement this later
    # def get_near_miss_score(self, safe_distance: float = 50.0) -> float:
    #   return self.get_distance_to_nearest_asteroid() - safe_distance


    # Helper Functions
    def get_distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate Euclidean distance between two points, accounting for screen wrap."""
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        
        if dx > self.game.width / 2:
            dx = self.game.width - dx
        if dy > self.game.height / 2:
            dy = self.game.height - dy
            
        return math.sqrt(dx * dx + dy * dy)

    def all_asteroids_distance_to_player(self) -> List[float]:
        """
        Get distances from all asteroids to the player.
        
        Returns:
            List of distances (one per asteroid).
        """
        if not self.game.player:
            return []
        return [self.get_distance(asteroid.center_x, asteroid.center_y, self.game.player.center_x, self.game.player.center_y) for asteroid in self.game.asteroid_list]
    
    def _get_asteroid_distances(self) -> List[Tuple[Asteroid, float]]:
        """
        Get list of (asteroid, distance) tuples for all asteroids.
        
        Returns:
            List of tuples (asteroid, distance_to_player).
        """
        if not self.game.player or not self.game.asteroid_list:
            return []
        
        return [
            (asteroid, self.get_distance(
                asteroid.center_x, 
                asteroid.center_y, 
                self.game.player.center_x, 
                self.game.player.center_y
            ))
            for asteroid in self.game.asteroid_list
        ]