import arcade
import random
from game import globals

ASTEROID_TEXTURES = [
    "game/sprites/Asteroid_Large_1.png",
    "game/sprites/Asteroid_Large_2.png",
    "game/sprites/Asteroid_Large_3.png",
    "game/sprites/Asteroid_Large_4.png"
]

class Asteroid(arcade.Sprite):
    def __init__(
            self,
            screen_width,
            screen_height,
            texture=None,
            scale=globals.ASTEROID_SCALE_LARGE,
            rng=None  # Optional isolated Random instance for reproducibility
    ):
        # Use provided RNG or fall back to global random module
        self._rng = rng if rng is not None else random

        if texture is None:
            texture = self._rng.choice(ASTEROID_TEXTURES)

        super().__init__(texture, scale)

        self.this_scale = scale

        # Determine HP based on scale
        if self.this_scale >= globals.ASTEROID_SCALE_LARGE:
            self.hp = globals.ASTEROID_HP_LARGE
        elif self.this_scale >= globals.ASTEROID_SCALE_MEDIUM:
            self.hp = globals.ASTEROID_HP_MEDIUM
        else:
            self.hp = globals.ASTEROID_HP_SMALL

        # Randomly choose an edge for initial position
        # (or random positions around any edge)
        self.center_x = self._rng.choice([0, screen_width])
        self.center_y = self._rng.choice([0, screen_height])

        # Speed based on size
        if self.this_scale >= globals.ASTEROID_SCALE_LARGE:
            self.max_speed = globals.ASTEROID_SPEED_LARGE
        elif self.this_scale >= globals.ASTEROID_SCALE_MEDIUM:
            self.max_speed = globals.ASTEROID_SPEED_MEDIUM
        else:
            self.max_speed = globals.ASTEROID_SPEED_SMALL

        # Random direction
        self.change_x = self._rng.uniform(-self.max_speed, self.max_speed)
        self.change_y = self._rng.uniform(-self.max_speed, self.max_speed)

        # Random rotation spin
        self.rotation_speed = self._rng.uniform(-self.max_speed * 3, self.max_speed * 3)

        # Lifetime if you want them to disappear eventually, scales with size
        self.lifetime = 1200 * self.this_scale

        # Keep track of screen bounds to pass to child asteroids if needed
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, delta_time: float = 1 / 60):
        """Move the asteroid each frame."""
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += self.rotation_speed

        # Decrement lifetime if you're using timed destruction
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.remove_from_sprite_lists()

    def break_asteroid(self) -> list:
        """
        Returns a list of new child asteroids when this asteroid is destroyed.
        - Large spawns 2 medium.
        - Medium spawns 3 small.
        - Small spawns nothing.
        """
        new_asteroids = []

        # Large => spawn children at scale=MEDIUM
        if self.this_scale >= globals.ASTEROID_SCALE_LARGE:
            for _ in range(2):
                child = self._spawn_child(new_scale=globals.ASTEROID_SCALE_MEDIUM)
                new_asteroids.append(child)

        # Medium => spawn children at scale=SMALL
        elif self.this_scale >= globals.ASTEROID_SCALE_MEDIUM:
            for _ in range(3):
                child = self._spawn_child(new_scale=globals.ASTEROID_SCALE_SMALL)
                new_asteroids.append(child)

        # Small => no children
        return new_asteroids

    def _spawn_child(self, new_scale: float) -> "Asteroid":
        """
        Internal helper to spawn a new asteroid at this asteroid's position,
        but with new random velocity & rotation.
        """
        child = Asteroid(
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            texture=self.texture,
            scale=new_scale,
            rng=self._rng  # Pass our RNG for reproducibility
        )
        # Place child at the same position
        child.center_x = self.center_x
        child.center_y = self.center_y

        # Randomize children's speed and rotation using our RNG
        child.change_x = self._rng.uniform(-child.max_speed, child.max_speed)
        child.change_y = self._rng.uniform(-child.max_speed, child.max_speed)
        child.rotation_speed = self._rng.uniform(-child.max_speed * 3, child.max_speed * 3)

        # (Optional) shorter lifetime for smaller ones, if you like
        child.lifetime = self.lifetime  # or maybe self.lifetime / 2, etc.

        return child
