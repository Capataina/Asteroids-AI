"""
Debug visualizer for the Asteroids game.
Draws hitboxes, vectors, and other debug information.
"""

import arcade
import math
from game import globals

def draw_debug_overlays(game):
    """
    Draw debug overlays for the game entities.
    
    Args:
        game: The AsteroidsGame instance.
    """
    # Draw Player Debug
    if game.player and game.player in game.player_list:
        player = game.player
        
        # 1. Collision Circle
        arcade.draw_circle_outline(
            player.center_x,
            player.center_y,
            globals.PLAYER_RADIUS,
            arcade.color.RED,
            2
        )
        
        # 2. Facing Vector (Blue Line)
        angle_rad = math.radians(player.angle)
        end_x = player.center_x + math.sin(angle_rad) * 50
        end_y = player.center_y + math.cos(angle_rad) * 50
        arcade.draw_line(
            player.center_x, player.center_y,
            end_x, end_y,
            arcade.color.CYAN,
            2
        )
        
        # 3. Velocity Vector (Green Line)
        # Scale up slightly to make small movements visible
        vel_end_x = player.center_x + player.change_x * 10
        vel_end_y = player.center_y + player.change_y * 10
        arcade.draw_line(
            player.center_x, player.center_y,
            vel_end_x, vel_end_y,
            arcade.color.GREEN,
            2
        )

    # Draw Asteroid Debug
    if game.asteroid_list:
        for asteroid in game.asteroid_list:
            # Calculate radius based on scale
            radius = globals.ASTEROID_BASE_RADIUS * asteroid.this_scale
            
            # Collision Circle
            arcade.draw_circle_outline(
                asteroid.center_x,
                asteroid.center_y,
                radius,
                arcade.color.RED,
                2
            )
            
            # Velocity Vector
            vel_end_x = asteroid.center_x + asteroid.change_x * 10
            vel_end_y = asteroid.center_y + asteroid.change_y * 10
            arcade.draw_line(
                asteroid.center_x, asteroid.center_y,
                vel_end_x, vel_end_y,
                arcade.color.YELLOW,
                1
            )

    # Draw Bullet Debug
    if game.bullet_list:
        for bullet in game.bullet_list:
            arcade.draw_circle_outline(
                bullet.center_x,
                bullet.center_y,
                globals.BULLET_RADIUS,
                arcade.color.RED,
                1
            )
