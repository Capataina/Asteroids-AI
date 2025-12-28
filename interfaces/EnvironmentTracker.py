import math
from typing import TYPE_CHECKING, List, Optional

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
        distances = self.all_asteroids_distance_to_player()
        distances.sort()
        return self.game.asteroid_list[distances.index(min(distances))]

    def get_distance_to_nearest_asteroid(self) -> Optional[float]:
        distances = self.all_asteroids_distance_to_player()
        distances.sort()
        return distances[0]
    
    def get_asteroids_in_range(self, distance: float) -> List[Asteroid]:
        distances = self.all_asteroids_distance_to_player()
        distances.sort()
        return [self.game.asteroid_list[i] for i in range(len(distances)) if distances[i] < distance]
    
    # TODO: Implement this later
    # def get_near_miss_score(self, safe_distance: float = 50.0) -> float:
    #   return self.get_distance_to_nearest_asteroid() - safe_distance


    # Helper Functions
    def get_distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def all_asteroids_distance_to_player(self) -> List[float]:
        return [self.get_distance(asteroid.center_x, asteroid.center_y, self.game.player.center_x, self.game.player.center_y) for asteroid in self.game.asteroid_list]
