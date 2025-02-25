import arcade
import random

ASTEROID_TEXTURES = [
    "sprites/Asteroid_Large_1.png",
    "sprites/Asteroid_Large_2.png",
    "sprites/Asteroid_Large_3.png",
    "sprites/Asteroid_Large_4.png"
]

class Asteroid(arcade.Sprite):
    def __init__(
            self,
            screen_width,
            screen_height,
            texture=None,
            scale=1.25
    ):

        if texture is None:
            texture = random.choice(ASTEROID_TEXTURES)

        super().__init__(texture, scale)

        self.this_scale = scale

        # Determine HP based on scale
        if self.this_scale > 1.0:
            self.hp = 3
        elif self.this_scale > 0.5:
            self.hp = 2
        else:
            self.hp = 1

        # Randomly choose an edge for initial position
        # (or random positions around any edge)
        self.center_x = random.choice([0, screen_width])
        self.center_y = random.choice([0, screen_height])

        # Speed based on size
        if self.this_scale >= 1.0:
            self.max_speed = 1
        elif self.this_scale > 0.5:
            self.max_speed = 2
        else:
            self.max_speed = 3

        # Random direction
        self.change_x = random.uniform(-self.max_speed, self.max_speed)
        self.change_y = random.uniform(-self.max_speed, self.max_speed)

        # Random rotation spin
        self.rotation_speed = random.uniform(-self.max_speed * 3, self.max_speed * 3)

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
        - Large (scale > 1.0) spawns 2 medium asteroids (scale=0.75).
        - Medium (scale > 0.5) spawns 3 small asteroids (scale=0.5).
        - Small (<= 0.5) spawns no further asteroids.
        """
        new_asteroids = []

        # Large => spawn children at scale=0.75
        if self.this_scale > 1.0:
            for _ in range(2):
                child = self._spawn_child(new_scale=0.75)
                new_asteroids.append(child)

        # Medium => spawn children at scale=0.5
        elif self.this_scale > 0.5:
            for _ in range(3):
                child = self._spawn_child(new_scale=0.5)
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
            scale=new_scale
        )
        # Place child at the same position
        child.center_x = self.center_x
        child.center_y = self.center_y

        # Possibly randomize children’s speed and rotation again:
        child.change_x = random.uniform(-child.max_speed, child.max_speed)
        child.change_y = random.uniform(-child.max_speed, child.max_speed)
        child.rotation_speed = random.uniform(-child.max_speed * 3, child.max_speed * 3)

        # (Optional) shorter lifetime for smaller ones, if you like
        child.lifetime = self.lifetime  # or maybe self.lifetime / 2, etc.

        return child
