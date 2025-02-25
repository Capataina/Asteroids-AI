import arcade
import math

class Bullet(arcade.Sprite):
    def __init__(self, x, y, angle, texture="sprites/Bullet.png", scale=0.8):
        super().__init__(texture, scale)
        self.center_x = x
        self.center_y = y
        self.angle = angle
        self.bullet_speed = 10

        # Convert angle to radians for velocity calculations
        angle_rad = math.radians(angle)
        self.change_x = math.sin(angle_rad) * self.bullet_speed
        self.change_y = math.cos(angle_rad) * self.bullet_speed

        # Disappear after ~1 second at 60FPS
        self.lifetime = 60

    def update(self, delta_time: float = 1/60):
        """Move the bullet and remove it if lifetime runs out."""
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.lifetime -= 1

        if self.lifetime <= 0:
            self.remove_from_sprite_lists()
