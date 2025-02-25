import arcade
import math

from classes.bullet import Bullet

class Player(arcade.Sprite):
    def __init__(self, texture="sprites/Player.png", scale=0.5):
        super().__init__(texture, scale)
        # Start in the middle of the screen
        self.center_x = 400
        self.center_y = 300

        # Movement
        self.change_x = 0
        self.change_y = 0
        self.acceleration = 0.3
        self.rotation_speed = 5
        self.slowdown = 0.99

        # Shooting
        self.shoot_cooldown = 0.12  # seconds between shots
        self.shoot_timer = 0       # timer that goes down each frame

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
        This is simpler than setting a rotation_speed and integrating it over time.
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
        """Fire a bullet if the cooldown has expired."""
        if self.shoot_timer <= 0:
            self.shoot_timer = self.shoot_cooldown
            return Bullet(self.center_x, self.center_y, self.angle)
        return None
