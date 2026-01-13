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

def draw_hybrid_encoder_debug(encoder, game):
    """
    Draw debug visuals for the HybridEncoder (Raycasts).
    
    Args:
        encoder: The HybridEncoder instance.
        game: The AsteroidsGame instance.
    """
    # Check if we have a player
    if not game.player or game.player not in game.player_list:
        return

    player = game.player
    
    # Check type (lazy import to avoid circular dependency issues at module level)
    # We assume 'encoder' has the attributes of HybridEncoder
    if not hasattr(encoder, 'num_rays'):
        return

    # Replicate Raycast Logic from HybridEncoder to draw what the agent "sees"
    angle_step = 360.0 / encoder.num_rays
    start_angle = player.angle
    
    # Max range
    max_dist = encoder.ray_max_distance
    
    # Pre-calculate relative asteroid positions (wrapped)
    targets = []
    if game.asteroid_list:
        for ast in game.asteroid_list:
            rel_x = ast.center_x - player.center_x
            rel_y = ast.center_y - player.center_y
            if abs(rel_x) > encoder.screen_width / 2:
                rel_x = -1 * math.copysign(encoder.screen_width - abs(rel_x), rel_x)
            if abs(rel_y) > encoder.screen_height / 2:
                rel_y = -1 * math.copysign(encoder.screen_height - abs(rel_y), rel_y)
            
            radius = globals.ASTEROID_BASE_RADIUS * ast.this_scale
            targets.append((rel_x, rel_y, radius))

    # Draw Rays
    for i in range(encoder.num_rays):
        ray_angle_deg = start_angle - (i * angle_step)
        ray_rad = math.radians(ray_angle_deg)
        ray_dx = math.sin(ray_rad)
        ray_dy = math.cos(ray_rad)
        
        hit_dist = max_dist
        
        # Check intersection
        for tx, ty, rad in targets:
            t = tx * ray_dx + ty * ray_dy
            if t < 0 or t > max_dist + rad: continue
            
            closest_x = t * ray_dx
            closest_y = t * ray_dy
            dist_sq = (closest_x - tx)**2 + (closest_y - ty)**2
            
            if dist_sq < rad * rad:
                dt = math.sqrt(rad * rad - dist_sq)
                curr_hit = t - dt
                if curr_hit < 0: curr_hit = 0
                if curr_hit < hit_dist:
                    hit_dist = curr_hit
        
        # Draw Line
        # Convert relative (wrapped) endpoint back to screen coordinates?
        # No, for drawing we want to show the "Sensor View". 
        # If we draw a line to a wrapped asteroid, it might streak across the screen.
        # So we draw the ray from player center out to 'hit_dist'.
        
        end_x = player.center_x + ray_dx * hit_dist
        end_y = player.center_y + ray_dy * hit_dist
        
        # Color: Yellow if hit something, Gray if max range
        color = arcade.color.YELLOW if hit_dist < max_dist else (100, 100, 100, 100)
        
        arcade.draw_line(
            player.center_x, player.center_y,
            end_x, end_y,
            color,
            1
        )

