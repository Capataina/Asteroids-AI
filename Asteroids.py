import math

import arcade
import random

from classes.player import Player
from classes.asteroid import Asteroid

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
        self.score = 0

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

    def reset_game(self):
        """Reset the entire game state to a 'fresh' start."""
        # Unschedule the asteroid spawner so we don't stack multiple timers
        arcade.unschedule(self.spawn_asteroid)

        # Reset score and other game variables
        self.score = 0

        # Initialise score object here
        self.score_text = arcade.Text(
            text=f"Score: {math.floor(self.score)}",
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

        # Schedule asteroid spawns exactly once
        arcade.schedule(self.spawn_asteroid, 0.75)

        # Reset last player position for distance-based reward
        self.last_player_x = self.player.center_x
        self.last_player_y = self.player.center_y

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
        self.score += math.ceil(delta_time) / 10

        # Wrap all sprites
        self.wrap_sprite(self.player)
        for bullet in self.bullet_list:
            self.wrap_sprite(bullet)
        for asteroid in self.asteroid_list:
            self.wrap_sprite(asteroid)

        # Compute how far the player traveled each frame
        dx = self.player.center_x - self.last_player_x
        dy = self.player.center_y - self.last_player_y
        dist = math.sqrt(dx * dx + dy * dy)

        # If the movement is bigger than our threshold, give points
        if dist > self.movement_threshold:
            # Award 1 point for each threshold chunk the player traveled, for instance.
            reward_chunks = int(dist // self.movement_threshold)  # number of threshold chunks
            self.score += reward_chunks  # 1 point per chunk

            # Update the "last position" to start measuring from here
            self.last_player_x = self.player.center_x
            self.last_player_y = self.player.center_y

            print("Player moved") #for debug ofc
        else:
            # If below threshold, do no reward,
            # but optionally keep partial distance (maybe later idk yet, might make it harder for ai).
            self.last_player_x = self.player.center_x
            self.last_player_y = self.player.center_y
            pass

        # Bullet-asteroid collisions
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.asteroid_list)
            for asteroid in hit_list:
                # Remove the bullet
                bullet.remove_from_sprite_lists()

                # Decrement asteroid HP
                asteroid.hp -= 1

                # If the asteroid is now destroyed, break it
                if asteroid.hp <= 0:
                    self.score += 10  # Or scale score to asteroid size if you like
                    new_asteroids = asteroid.break_asteroid()
                    asteroid.remove_from_sprite_lists()

                    # Add any child asteroids
                    for child in new_asteroids:
                        self.asteroid_list.append(child)

        # Player-asteroid collisions
        if self.player in self.player_list:
            if arcade.check_for_collision_with_list(self.player, self.asteroid_list):
                print("Player hit an asteroid! Final Score:", self.score)
                self.reset_game()

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

        self.score_text.text = f"Score: {math.floor(self.score)}"

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
