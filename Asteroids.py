import math

import arcade
import random

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

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE  = "Asteroids Basic"

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
        self.asteroid_spawn_interval = 0.75

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
            arcade.schedule(self.spawn_asteroid, 0.75)

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
            scale = 0.5
        elif roll < 0.7:
            # 30% => medium
            scale = 0.75
        else:
            # 30% => large
            scale = 1.25

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

    def on_update(self, delta_time):
        self.player_list.update()
        self.asteroid_list.update()
        self.bullet_list.update()

        # Wrap all sprites
        self.wrap_sprite(self.player)
        for bullet in self.bullet_list:
            self.wrap_sprite(bullet)
        for asteroid in self.asteroid_list:
            self.wrap_sprite(asteroid)

        # Bullet-asteroid collisions
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.asteroid_list)
            for asteroid in hit_list:
                # Remove the bullet
                bullet.remove_from_sprite_lists()

                self.metrics_tracker.total_hits += 1

                # Decrement asteroid HP
                asteroid.hp -= 1

                # If the asteroid is now destroyed, break it
                if asteroid.hp <= 0:
                    new_asteroids = asteroid.break_asteroid()
                    asteroid.remove_from_sprite_lists()

                    self.metrics_tracker.total_kills += 1

                    # Add any child asteroids
                    for child in new_asteroids:
                        self.asteroid_list.append(child)

        # Player-asteroid collisions
        if self.player in self.player_list:
            if arcade.check_for_collision_with_list(self.player, self.asteroid_list):
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
    window = AsteroidsGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
