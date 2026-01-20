"""
Graph-based state encoder for GNN-SAC.

Encodes the game state as a graph with:
- Player node: velocity, heading, cooldown
- Asteroid nodes: scale, velocity
- Edges (asteroid -> player): wrapped distance, bearing, relative velocity
"""

from dataclasses import dataclass
from typing import List, Optional, Any
import math

from interfaces.StateEncoder import StateEncoder
from interfaces.EnvironmentTracker import EnvironmentTracker
from game import globals


@dataclass
class GraphPayload:
    """
    Framework-agnostic graph representation.

    This structure can be converted to PyTorch Geometric Data objects
    at training time without coupling the encoder to PyTorch.
    """
    player_features: List[float]           # [5]: vel_x, vel_y, heading_sin, heading_cos, cooldown
    asteroid_features: List[List[float]]   # [N, 3]: scale, vel_x, vel_y per asteroid
    edge_attr: List[List[float]]           # [N, 7]: dx, dy, dist, bearing_sin, bearing_cos, rel_vx, rel_vy
    num_asteroids: int

    # Feature dimensions (for network construction)
    PLAYER_DIM = 5
    ASTEROID_DIM = 3
    EDGE_DIM = 7


class GraphEncoder(StateEncoder):
    """
    Encodes the game state as a graph for GNN processing.

    Graph structure:
    - 1 player node with proprioceptive features
    - N asteroid nodes with physics features
    - N directed edges from each asteroid to the player

    All spatial features use toroidal (wrapped) coordinates.
    """

    def __init__(
        self,
        screen_width: int = globals.SCREEN_WIDTH,
        screen_height: int = globals.SCREEN_HEIGHT,
        max_asteroids: Optional[int] = None,
        max_player_velocity: Optional[float] = None,
        max_asteroid_velocity: Optional[float] = None,
    ):
        """
        Initialize the graph encoder.

        Args:
            screen_width: Width of the game screen (for wrapping).
            screen_height: Height of the game screen (for wrapping).
            max_asteroids: Maximum number of asteroids to include (None = all).
                          If exceeded, nearest asteroids by wrapped distance are kept.
            max_player_velocity: Normalization bound for player velocity.
                                Defaults to terminal velocity.
            max_asteroid_velocity: Normalization bound for asteroid velocity.
                                  Defaults to small asteroid speed.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_asteroids = max_asteroids

        # Compute normalization bounds
        # Terminal velocity = acceleration / (1 - friction)
        default_player_max = globals.PLAYER_ACCELERATION / (1 - globals.PLAYER_FRICTION)
        self.max_player_velocity = max_player_velocity if max_player_velocity else default_player_max
        self.max_asteroid_velocity = max_asteroid_velocity if max_asteroid_velocity else globals.ASTEROID_SPEED_SMALL
        self.max_relative_velocity = self.max_player_velocity + self.max_asteroid_velocity

        # Diagonal for distance normalization
        self.diag_distance = math.sqrt(screen_width**2 + screen_height**2)

    def _wrapped_delta(self, ax: float, ay: float, px: float, py: float) -> tuple:
        """
        Compute wrapped (dx, dy) for toroidal geometry.

        This ensures that objects near opposite screen edges are
        represented as being close to each other.

        Args:
            ax, ay: Asteroid position
            px, py: Player position

        Returns:
            (dx, dy): Signed offset from player to asteroid, wrapped
        """
        dx = ((ax - px + self.screen_width / 2) % self.screen_width) - self.screen_width / 2
        dy = ((ay - py + self.screen_height / 2) % self.screen_height) - self.screen_height / 2
        return dx, dy

    def encode(self, env_tracker: EnvironmentTracker) -> GraphPayload:
        """
        Encode the current game state as a graph.

        Args:
            env_tracker: Environment tracker with access to game entities.

        Returns:
            GraphPayload with player features, asteroid features, and edge attributes.
        """
        player = env_tracker.get_player()

        if player is None or not env_tracker.is_player_alive():
            # Dead state - return empty graph with zeroed player features
            return GraphPayload(
                player_features=[0.0] * GraphPayload.PLAYER_DIM,
                asteroid_features=[],
                edge_attr=[],
                num_asteroids=0
            )

        # === Player features (5D) ===
        heading_rad = math.radians(player.angle)
        cooldown_frac = max(0.0, player.shoot_timer) / player.shoot_cooldown if player.shoot_cooldown > 0 else 0.0

        player_features = [
            self._clamp(player.change_x / self.max_player_velocity, -1.0, 1.0),  # vel_x normalized
            self._clamp(player.change_y / self.max_player_velocity, -1.0, 1.0),  # vel_y normalized
            math.sin(heading_rad),                                                 # heading_sin
            math.cos(heading_rad),                                                 # heading_cos
            min(1.0, max(0.0, cooldown_frac)),                                     # cooldown [0,1]
        ]

        # === Get asteroids ===
        asteroids = list(env_tracker.get_all_asteroids())

        # Cap asteroids if needed (keep nearest by wrapped distance)
        if self.max_asteroids is not None and len(asteroids) > self.max_asteroids:
            def wrapped_distance(ast):
                dx, dy = self._wrapped_delta(ast.center_x, ast.center_y, player.center_x, player.center_y)
                return math.sqrt(dx**2 + dy**2)
            asteroids = sorted(asteroids, key=wrapped_distance)[:self.max_asteroids]

        asteroid_features = []
        edge_attr = []

        for ast in asteroids:
            # === Asteroid features (3D) ===
            ast_feat = [
                ast.this_scale,  # scale (roughly 0.25 to 1.25)
                self._clamp(ast.change_x / self.max_asteroid_velocity, -1.0, 1.0),  # vel_x normalized
                self._clamp(ast.change_y / self.max_asteroid_velocity, -1.0, 1.0),  # vel_y normalized
            ]
            asteroid_features.append(ast_feat)

            # === Edge features (7D): asteroid -> player relationship ===
            dx, dy = self._wrapped_delta(ast.center_x, ast.center_y, player.center_x, player.center_y)
            dist = math.sqrt(dx**2 + dy**2)

            # Bearing: angle from player to asteroid
            # atan2(dx, dy) gives angle with 0 = up, increasing clockwise
            bearing = math.atan2(dx, dy)

            # Relative velocity: asteroid velocity - player velocity
            rel_vx = ast.change_x - player.change_x
            rel_vy = ast.change_y - player.change_y

            edge_feat = [
                dx / (self.screen_width / 2),                                     # normalized dx [-1, 1]
                dy / (self.screen_height / 2),                                    # normalized dy [-1, 1]
                min(1.0, dist / self.diag_distance),                              # normalized distance [0, 1]
                math.sin(bearing),                                                 # bearing sin
                math.cos(bearing),                                                 # bearing cos
                self._clamp(rel_vx / self.max_relative_velocity, -1.0, 1.0),      # rel vel x normalized
                self._clamp(rel_vy / self.max_relative_velocity, -1.0, 1.0),      # rel vel y normalized
            ]
            edge_attr.append(edge_feat)

        return GraphPayload(
            player_features=player_features,
            asteroid_features=asteroid_features,
            edge_attr=edge_attr,
            num_asteroids=len(asteroids)
        )

    def get_state_size(self) -> int:
        """
        Return the player feature dimension for compatibility.

        Note: For graph encoders, this returns the player node dimension.
        The full graph size varies with asteroid count.
        """
        return GraphPayload.PLAYER_DIM

    def reset(self) -> None:
        """Reset the encoder state. GraphEncoder is stateless, so this is a no-op."""
        pass

    def clone(self) -> 'GraphEncoder':
        """Create a deep copy of the encoder with the same configuration."""
        return GraphEncoder(
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            max_asteroids=self.max_asteroids,
            max_player_velocity=self.max_player_velocity,
            max_asteroid_velocity=self.max_asteroid_velocity,
        )

    @staticmethod
    def _clamp(value: float, min_val: float, max_val: float) -> float:
        """Clamp a value to a range."""
        return max(min_val, min(max_val, value))
