import math
import arcade
import random

from game import globals
import game.debug.visuals

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

class AsteroidsGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Set game variables
        self.player_list = None
        self.asteroid_list = None
        self.bullet_list = None
        self.player = None

        # Score object for performance reasons
        self.score_text = None

        # Key states
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.space_pressed = False
        
        # Debug state
        self.debug_mode = globals.COLLISION_DEBUG_ENABLED

        # Track player's last position to measure travel distance
        self.last_player_x = 0
        self.last_player_y = 0

        # Distance threshold so extremely small movement doesn't count
        self.movement_threshold = 25

        # Trackers
        self.tracker = EnvironmentTracker(self)
        self.metrics_tracker = MetricsTracker(self)
        self.reward_calculator = ComposableRewardCalculator()

        # Reward components
        self.reward_calculator.add_component(SurvivalBonus())
        self.reward_calculator.add_component(KillAsteroid())
        self.reward_calculator.add_component(ChunkBonus())
        self.reward_calculator.add_component(NearMiss())
        self.reward_calculator.add_component(AccuracyBonus())
        self.reward_calculator.add_component(KPMBonus())

        # Flag to control whether game should update its own reward calculator
        # Set to False during AI training when external reward calculator is used
        self.update_internal_rewards = True
        
        # Flag to control whether game should auto-reset on collision
        # Set to False during AI training when external episode management is used
        self.auto_reset_on_collision = True

        # Manual spawning mode - matches headless game timing for display consistency
        self.manual_spawning = False
        self.time_since_last_spawn = 0.0
        self.asteroid_spawn_interval = globals.ASTEROID_SPAWN_INTERVAL

        # External control mode - when True, on_update does nothing (training loop controls updates)
        # This prevents arcade's automatic on_update from double-counting time
        self.external_control = False

    def reset_game(self):
        """Reset the entire game state to a 'fresh' start."""
        # Unschedule the asteroid spawner so we don't stack multiple timers
        arcade.unschedule(self.spawn_asteroid)

        # Initialise score object here
        self.score_text = arcade.Text(
            text=f"Score: {math.floor(self.reward_calculator.score)}",
            x=10,
            y=self.height - 30,
            color=arcade.color.WHITE,
            font_size=20
        )

        # Recreate sprite lists
        self.player_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Create a new player
        self.player = Player()
        self.player_list.append(self.player)

        # Spawn some initial asteroids
        for _ in range(8):
            self.spawn_asteroid(delta_time=0)

        # Reset manual spawn timer
        self.time_since_last_spawn = 0.0

        # Only use arcade.schedule if NOT in manual spawning mode
        if not self.manual_spawning:
            arcade.schedule(self.spawn_asteroid, self.asteroid_spawn_interval)

        # Reset last player position for distance-based reward
        self.last_player_x = self.player.center_x
        self.last_player_y = self.player.center_y

        self.metrics_tracker.reset()
        self.reward_calculator.reset()

    def setup(self):
        # Run this only once, this doesn't add much anyway tbh
        arcade.set_background_color(arcade.color.BLACK)

        self.reset_game()

    def spawn_asteroid(self, delta_time: float):
        roll = random.random()

        if roll < 0.4:
            # 40% => small
            scale = globals.ASTEROID_SCALE_SMALL
        elif roll < 0.7:
            # 30% => medium
            scale = globals.ASTEROID_SCALE_MEDIUM
        else:
            # 30% => large
            scale = globals.ASTEROID_SCALE_LARGE

        # Create a new asteroid with this chosen scale
        asteroid = Asteroid(
            screen_width=self.width,
            screen_height=self.height,
            scale=scale
        )
        self.asteroid_list.append(asteroid)

    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.asteroid_list.draw()
        self.bullet_list.draw()

        # Show score
        self.score_text.draw()
        
        # Draw debug overlays
        if self.debug_mode:
            game.debug.visuals.draw_debug_overlays(self)

    def on_update(self, delta_time):
        # Skip if under external control (training loop calls this explicitly)
        # This prevents arcade's automatic on_update from double-counting
        if self.external_control:
            return

        self.player_list.update()
        self.asteroid_list.update()
        self.bullet_list.update()

        # Wrap all sprites
        self.wrap_sprite(self.player)
        for bullet in self.bullet_list:
            self.wrap_sprite(bullet)
        for asteroid in self.asteroid_list:
            self.wrap_sprite(asteroid)

        # Bullet-asteroid collisions (Manual distance check for parity with Headless)
        bullets_to_remove = []
        asteroids_to_remove = []
        
        for bullet in self.bullet_list:
            if bullet in bullets_to_remove:
                continue
                
            hit_asteroid = False
            for asteroid in self.asteroid_list:
                if asteroid in asteroids_to_remove:
                    continue
                
                # Manual circular collision check
                dx = bullet.center_x - asteroid.center_x
                dy = bullet.center_y - asteroid.center_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                asteroid_radius = globals.ASTEROID_BASE_RADIUS * asteroid.this_scale
                collision_threshold = globals.BULLET_RADIUS + asteroid_radius
                
                if distance < collision_threshold:
                    hit_asteroid = True
                    self.metrics_tracker.total_hits += 1
                    
                    # Damage asteroid
                    asteroid.hp -= 1
                    
                    if asteroid.hp <= 0:
                        asteroids_to_remove.append(asteroid)
                        self.metrics_tracker.total_kills += 1
                        
                        # Break asteroid
                        new_asteroids = asteroid.break_asteroid()
                        for child in new_asteroids:
                            self.asteroid_list.append(child)
                    
                    # Bullet hits only one asteroid
                    break
            
            if hit_asteroid:
                bullets_to_remove.append(bullet)
        
        # Apply removals
        for bullet in bullets_to_remove:
            bullet.remove_from_sprite_lists()
        for asteroid in asteroids_to_remove:
            asteroid.remove_from_sprite_lists()

        # Player-asteroid collisions (Manual distance check)
        if self.player in self.player_list:
            player_hit = False
            for asteroid in self.asteroid_list:
                dx = self.player.center_x - asteroid.center_x
                dy = self.player.center_y - asteroid.center_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                asteroid_radius = globals.ASTEROID_BASE_RADIUS * asteroid.this_scale
                collision_threshold = globals.PLAYER_RADIUS + asteroid_radius
                
                if distance < collision_threshold:
                    player_hit = True
                    break
            
            if player_hit:
                # Only print and reset if auto-reset is enabled (manual play mode)
                if self.auto_reset_on_collision:
                    print("Player hit an asteroid! Final Score:", self.reward_calculator.current_score(self.tracker, self.metrics_tracker))
                    self.reset_game()
                else:
                    # During AI training, just remove the player and let training loop handle reset
                    self.player.remove_from_sprite_lists()

        # Handle continuous input because the library is weird and "lightweight" (lowkey bad)
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

        # Manual asteroid spawning (matches headless game timing exactly)
        if self.manual_spawning:
            self.time_since_last_spawn += delta_time
            if self.time_since_last_spawn >= self.asteroid_spawn_interval:
                self.spawn_asteroid(delta_time=0)
                self.time_since_last_spawn = 0.0

        # Only update internal reward calculator if not being controlled by external training
        if self.update_internal_rewards:
            self.reward_calculator.calculate_step_reward(self.tracker, self.metrics_tracker)

        self.score_text.text = f"Score: {math.floor(self.reward_calculator.score)}"
        self.metrics_tracker.time_alive += delta_time
        self.tracker.update(self)

    def wrap_sprite(self, sprite):
        if sprite.center_x < 0:
            sprite.center_x = self.width
        elif sprite.center_x > self.width:
            sprite.center_x = 0
        if sprite.center_y < 0:
            sprite.center_y = self.height
        elif sprite.center_y > self.height:
            sprite.center_y = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.SPACE:
            self.space_pressed = True
        elif key == arcade.key.D:
            self.debug_mode = not self.debug_mode

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.SPACE:
            self.space_pressed = False

def main():
    window = AsteroidsGame(globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT, globals.SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
