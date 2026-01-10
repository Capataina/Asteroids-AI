"""
Headless Asteroids Game for Parallel Evaluation

This is a simplified version of AsteroidsGame that runs without rendering.
Used for fast parallel evaluation of multiple agents.
"""

import math
import random
from game import globals
from game.classes.player import Player
from game.classes.asteroid import Asteroid
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker
from interfaces.RewardCalculator import ComposableRewardCalculator

from interfaces.rewards.SurvivalBonus import SurvivalBonus
from interfaces.rewards.KillAsteroid import KillAsteroid
from interfaces.rewards.ChunkBonus import ChunkBonus
from interfaces.rewards.NearMiss import NearMiss
from interfaces.rewards.AccuracyBonus import AccuracyBonus
from interfaces.rewards.KPMBonus import KPMBonus


class HeadlessAsteroidsGame:
    """
    Headless version of AsteroidsGame for parallel evaluation.
    No rendering, no arcade.Window - just game logic.
    """

    def __init__(self, width=800, height=600, random_seed=None):
        """Initialize headless game.

        Args:
            width: Screen width
            height: Screen height
            random_seed: If provided, use isolated Random instance for reproducibility
        """
        self.width = width
        self.height = height

        # Use isolated Random instance to avoid threading issues
        # Each game instance has its own RNG that doesn't interfere with others
        if random_seed is not None:
            self.rng = random.Random(random_seed)
        else:
            self.rng = random.Random()

        # Set game variables
        self.player_list = []
        self.asteroid_list = []
        self.bullet_list = []
        self.player = None

        # Key states
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.space_pressed = False

        # Track player's last position
        self.last_player_x = 0
        self.last_player_y = 0
        self.movement_threshold = 25

        # Trackers
        self.tracker = EnvironmentTracker(self)
        self.metrics_tracker = MetricsTracker(self)
        self.reward_calculator = ComposableRewardCalculator()
        
        # Add reward components
        self.reward_calculator.add_component(SurvivalBonus())
        self.reward_calculator.add_component(KillAsteroid())
        self.reward_calculator.add_component(ChunkBonus())
        self.reward_calculator.add_component(NearMiss())
        self.reward_calculator.add_component(AccuracyBonus())
        self.reward_calculator.add_component(KPMBonus())
        
        # Control flags (same as regular game)
        self.update_internal_rewards = False  # Controlled by external training
        self.auto_reset_on_collision = False  # Controlled by external training
        
        # Asteroid spawning
        self.asteroid_spawn_interval = globals.ASTEROID_SPAWN_INTERVAL
        self.time_since_last_spawn = 0.0
        
    def reset_game(self):
        """Reset the entire game state."""
        # Recreate sprite lists
        self.player_list = []
        self.asteroid_list = []
        self.bullet_list = []
        
        # Create a new player
        self.player = Player()
        self.player_list.append(self.player)
        
        # Spawn initial asteroids
        for _ in range(8):
            self.spawn_asteroid()
        
        # Reset tracking
        self.last_player_x = self.player.center_x
        self.last_player_y = self.player.center_y
        self.time_since_last_spawn = 0.0
        
        self.metrics_tracker.reset()
        self.reward_calculator.reset()
    
    def spawn_asteroid(self):
        """Spawn a new asteroid using isolated RNG."""
        roll = self.rng.random()

        if roll < 0.4:
            scale = globals.ASTEROID_SCALE_SMALL
        elif roll < 0.7:
            scale = globals.ASTEROID_SCALE_MEDIUM
        else:
            scale = globals.ASTEROID_SCALE_LARGE

        # Create asteroid with our isolated RNG for position/velocity
        asteroid = Asteroid(
            screen_width=self.width,
            screen_height=self.height,
            scale=scale,
            rng=self.rng  # Pass our isolated RNG
        )
        self.asteroid_list.append(asteroid)
    
    def on_update(self, delta_time):
        """Update game state (no rendering)."""
        # Update sprites
        for sprite in self.player_list:
            sprite.update()
        for sprite in self.asteroid_list:
            sprite.update()
        for sprite in self.bullet_list:
            sprite.update()
        
        # Wrap all sprites
        self.wrap_sprite(self.player)
        for bullet in self.bullet_list[:]:  # Copy list for safe iteration
            self.wrap_sprite(bullet)
        for asteroid in self.asteroid_list[:]:
            self.wrap_sprite(asteroid)
        
        # Bullet-asteroid collisions
        # NOTE: We use explicit collision radii because sprite.width may be 0 in headless mode
        BULLET_COLLISION_RADIUS = globals.BULLET_RADIUS
        ASTEROID_BASE_RADIUS = globals.ASTEROID_BASE_RADIUS

        for bullet in self.bullet_list[:]:
            if bullet not in self.bullet_list:
                continue

            # Check collision with asteroids
            for asteroid in self.asteroid_list[:]:
                if asteroid not in self.asteroid_list:
                    continue

                # Simple circle collision with explicit radii
                dx = bullet.center_x - asteroid.center_x
                dy = bullet.center_y - asteroid.center_y
                distance = math.sqrt(dx*dx + dy*dy)

                asteroid_radius = ASTEROID_BASE_RADIUS * asteroid.this_scale
                if distance < (BULLET_COLLISION_RADIUS + asteroid_radius):
                    # Collision!
                    if bullet in self.bullet_list:
                        self.bullet_list.remove(bullet)
                    
                    self.metrics_tracker.total_hits += 1
                    
                    # Damage asteroid
                    asteroid.hp -= 1
                    
                    if asteroid.hp <= 0:
                        new_asteroids = asteroid.break_asteroid()
                        if asteroid in self.asteroid_list:
                            self.asteroid_list.remove(asteroid)
                        
                        self.metrics_tracker.total_kills += 1
                        
                        # Add child asteroids
                        for child in new_asteroids:
                            self.asteroid_list.append(child)
                    
                    break
        
        # Player-asteroid collisions
        # NOTE: We use explicit collision radii because sprite.width may be 0 in headless mode
        # (textures don't load properly without arcade window context)
        PLAYER_COLLISION_RADIUS = globals.PLAYER_RADIUS
        ASTEROID_BASE_RADIUS = globals.ASTEROID_BASE_RADIUS

        if self.player in self.player_list:
            for asteroid in self.asteroid_list:
                # Simple circle collision with explicit radii
                dx = self.player.center_x - asteroid.center_x
                dy = self.player.center_y - asteroid.center_y
                distance = math.sqrt(dx*dx + dy*dy)

                asteroid_radius = ASTEROID_BASE_RADIUS * asteroid.this_scale
                collision_threshold = PLAYER_COLLISION_RADIUS + asteroid_radius

                if distance < collision_threshold:
                    if self.auto_reset_on_collision:
                        self.reset_game()
                    else:
                        # Just remove player (training loop handles reset)
                        if self.player in self.player_list:
                            self.player_list.remove(self.player)
                    break
        
        # Handle continuous input
        if self.player in self.player_list:
            if self.left_pressed:
                self.player.rotate_left()
            if self.right_pressed:
                self.player.rotate_right()
            if self.up_pressed:
                self.player.thrust_forward()
            if self.space_pressed:
                bullet = self.player.shoot()
                if bullet:
                    self.bullet_list.append(bullet)
                    self.metrics_tracker.total_shots_fired += 1
        
        # Update trackers
        self.metrics_tracker.time_alive += delta_time
        self.tracker.update(self)
        
        # Spawn asteroids periodically
        self.time_since_last_spawn += delta_time
        if self.time_since_last_spawn >= self.asteroid_spawn_interval:
            self.spawn_asteroid()
            self.time_since_last_spawn = 0.0
        
        # Calculate rewards if enabled
        if self.update_internal_rewards:
            self.reward_calculator.calculate_step_reward(self.tracker, self.metrics_tracker)
    
    def wrap_sprite(self, sprite):
        """Wrap sprite around screen edges."""
        if sprite is None:
            return
            
        if sprite.center_x < 0:
            sprite.center_x = self.width
        elif sprite.center_x > self.width:
            sprite.center_x = 0
        if sprite.center_y < 0:
            sprite.center_y = self.height
        elif sprite.center_y > self.height:
            sprite.center_y = 0
