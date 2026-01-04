import arcade
import math

from game.classes.bullet import Bullet

class Player(arcade.Sprite):
    def __init__(self, texture="game/sprites/Player.png", scale=0.5):
        super().__init__(texture, scale)
        # Start in the middle of the screen (hard coded leave me alone)
        self.center_x = 400
        self.center_y = 300

        # Movement
        self.change_x = 0
        self.change_y = 0
        self.acceleration = 0.15  # Reduced from 0.3 for more realistic movement
        self.rotation_speed = 3   # Reduced from 5 for smoother turning
        self.slowdown = 0.99

        # Shooting
        self.shoot_cooldown = 0.25  # Increased from 0.12 - less spammy shooting
        self.shoot_timer = 0        # timer that goes down each frame

    def update(self, delta_time: float = 1/60) -> None:
        """Update the player's movement, apply friction, and manage the shoot timer."""
        # Update position
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Reduce the time until we can shoot again
        if self.shoot_timer >= 0:
            self.shoot_timer -= delta_time

        # Apply friction (slight movement decay)
        self.change_x *= self.slowdown
        self.change_y *= self.slowdown

    def rotate_left(self):
        """
        Rotate the ship instantly to the left by a fixed step.
        """
        self.angle -= self.rotation_speed

    def rotate_right(self):
        """Rotate the ship instantly to the right by a fixed step."""
        self.angle += self.rotation_speed

    def thrust_forward(self):
        """Accelerate in the direction the ship is currently facing."""
        angle_rad = math.radians(self.angle)
        self.change_x += math.sin(angle_rad) * self.acceleration
        self.change_y += math.cos(angle_rad) * self.acceleration

    def shoot(self):
        """Fire a bullet if the cooldown is up."""
        if self.shoot_timer <= 0:
            self.shoot_timer = self.shoot_cooldown
            return Bullet(self.center_x, self.center_y, self.angle)
        return None

    def get_max_distance(self, screen_width: int, screen_height: int) -> float:
        """Get the maximum distance the player can travel in the screen."""
        return math.sqrt(screen_width**2 + screen_height**2)

    def get_distance(self, x: float, y: float) -> float:
        """Get the distance between the player and a point."""
        return math.sqrt((self.center_x - x)**2 + (self.center_y - y)**2)
