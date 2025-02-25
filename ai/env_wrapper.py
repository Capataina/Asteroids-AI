import math
import arcade
import torch
import torch_geometric as pyg
from torch_geometric.data import Data
import numpy as np


class AsteroidsGraphEnv:
    def __init__(self, game):
        """
        Wraps the Asteroids game to provide a graph-based interface.

        Args:
            game: The AsteroidsGame instance
        """
        self.game = game
        self.action_space_size = 4  # left, right, thrust, shoot

    def reset(self):
        """Reset the game and return the initial graph state."""
        self.game.reset_game()
        return self._get_graph_state()

    def _wrap_sprite(self, sprite):
        """Helper function for wrapping sprites around screen edges"""
        if sprite.center_x < 0:
            sprite.center_x = self.game.width
        elif sprite.center_x > self.game.width:
            sprite.center_x = 0
        if sprite.center_y < 0:
            sprite.center_y = self.game.height
        elif sprite.center_y > self.game.height:
            sprite.center_y = 0

    def step(self, actions):
        """
        Take an action in the environment.

        Args:
            actions: Array of 4 values [left, right, thrust, shoot]
                    Each value is between 0 and 1 (continuous)

        Returns:
            next_state: Graph representation of new state
            reward: Reward for this step
            done: Whether the episode has ended
            info: Additional information
        """
        # Save current score for reward calculation
        prev_score = self.game.score

        # Save original input state
        left_pressed = self.game.left_pressed
        right_pressed = self.game.right_pressed
        up_pressed = self.game.up_pressed
        space_pressed = self.game.space_pressed

        # Set the control inputs from the AI action
        self.game.left_pressed = actions[0] > 0.5
        self.game.right_pressed = actions[1] > 0.5
        self.game.up_pressed = actions[2] > 0.5
        self.game.space_pressed = actions[3] > 0.5

        # Update player, bullets, and asteroids directly
        self.game.player_list.update()
        self.game.asteroid_list.update()
        self.game.bullet_list.update()
        self.game.score += 0.1  # Small score increment for surviving

        # Wrap all sprites
        for sprite in self.game.player_list:
            self._wrap_sprite(sprite)
        for sprite in self.game.bullet_list:
            self._wrap_sprite(sprite)
        for sprite in self.game.asteroid_list:
            self._wrap_sprite(sprite)

        # Handle bullet-asteroid collisions (copied from game's on_update)
        for bullet in self.game.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.game.asteroid_list)
            for asteroid in hit_list:
                bullet.remove_from_sprite_lists()
                asteroid.hp -= 1
                if asteroid.hp <= 0:
                    self.game.score += 10
                    new_asteroids = asteroid.break_asteroid()
                    asteroid.remove_from_sprite_lists()
                    for child in new_asteroids:
                        self.game.asteroid_list.append(child)

        # Flag to track if player died
        done = False

        # Check for player-asteroid collisions
        if self.game.player in self.game.player_list:
            if arcade.check_for_collision_with_list(self.game.player, self.game.asteroid_list):
                print(f"Player hit an asteroid! Final Score: {self.game.score}")
                done = True

        # Handle continuous input for player
        if self.game.left_pressed:
            self.game.player.rotate_left()
        if self.game.right_pressed:
            self.game.player.rotate_right()
        if self.game.up_pressed:
            self.game.player.thrust_forward()
        if self.game.space_pressed:
            bullet = self.game.player.shoot()
            if bullet:
                self.game.bullet_list.append(bullet)

        # Update score text
        self.game.score_text.text = f"Score: {math.floor(self.game.score)}"

        # Restore the original input state
        self.game.left_pressed = left_pressed
        self.game.right_pressed = right_pressed
        self.game.up_pressed = up_pressed
        self.game.space_pressed = space_pressed

        # Check if game was reset (player died)
        if self.game.score < prev_score:
            done = True

        # Calculate reward (basic version)
        reward = self.game.score - prev_score

        # Get new state as graph
        next_state = self._get_graph_state()

        return next_state, reward, done, {}

    def _get_graph_state(self):
        """
        Convert the current game state to a graph representation.

        Returns:
            torch_geometric.data.Data: The graph state
        """
        # 1. Extract node features
        nodes = []
        node_types = []  # 0=player, 1=asteroid, 2=bullet

        # Player features
        if self.game.player in self.game.player_list:
            player_features = [
                self.game.player.center_x / self.game.width,  # Normalise x position
                self.game.player.center_y / self.game.height,  # Normalise y position
                self.game.player.change_x / 10.0,  # Normalise x velocity
                self.game.player.change_y / 10.0,  # Normalise y velocity
                np.sin(np.radians(self.game.player.angle)),  # Direction as sin/cos
                np.cos(np.radians(self.game.player.angle))
            ]
            nodes.append(player_features)
            node_types.append(0)

        # Asteroid features
        for ast in self.game.asteroid_list:
            ast_features = [
                ast.center_x / self.game.width,
                ast.center_y / self.game.height,
                ast.change_x / 5.0,
                ast.change_y / 5.0,
                ast.this_scale / 1.25,  # Normalize size
                ast.hp / 3.0  # Normalize HP
            ]
            nodes.append(ast_features)
            node_types.append(1)

        # Bullet features
        for bullet in self.game.bullet_list:
            bullet_features = [
                bullet.center_x / self.game.width,
                bullet.center_y / self.game.height,
                bullet.change_x / 10.0,
                bullet.change_y / 10.0,
                bullet.lifetime / 60.0,  # Normalize lifetime
                0.0  # Padding to match feature dimension
            ]
            nodes.append(bullet_features)
            node_types.append(2)

        # 2. Create edges based on proximity
        # Bare minimum: no edges yet - we'll add this in the next iteration
        edge_index = torch.zeros((2, 0), dtype=torch.long)

        # 3. Convert to PyG Data object
        x = torch.tensor(nodes, dtype=torch.float)
        node_type = torch.tensor(node_types, dtype=torch.long)

        graph = Data(
            x=x,
            edge_index=edge_index,
            node_type=node_type,
            num_nodes=len(nodes)
        )

        return graph