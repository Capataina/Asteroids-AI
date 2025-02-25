# train_agent.py
import numpy as np
import arcade
from Asteroids import AsteroidsGame, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from ai.env_wrapper import AsteroidsGraphEnv


class AIDriver:
    """
    Handles the AI training without inheriting from the game class
    """

    def __init__(self, game, num_episodes=100, frame_delay=1 / 30):  # Accept an existing game
        # Use the provided game instance
        self.game = game

        # Create environment wrapper
        self.env = AsteroidsGraphEnv(self.game)

        # Training parameters
        self.num_episodes = num_episodes
        self.current_episode = 0
        self.frame_delay = frame_delay
        self.done = True
        self.state = None
        self.current_step = 0
        self.total_reward = 0

        # Register update function with arcade
        arcade.schedule(self.update, frame_delay)

        # Additional display for metrics
        self.info_text = arcade.Text(
            text="Starting training...",
            x=10,
            y=SCREEN_HEIGHT - 60,  # Positioned below the game's score display
            color=arcade.color.YELLOW,
            font_size=14
        )

        # Hook into the game's draw method to add our metrics
        original_draw = self.game.on_draw

        def new_draw():
            original_draw()
            self.info_text.draw()

        self.game.on_draw = new_draw

    def update(self, delta_time):
        """Called by the arcade scheduler"""
        try:
            if self.done:
                # Start a new episode
                self.state = self.env.reset()
                self.done = False
                self.current_step = 0
                self.total_reward = 0
                self.current_episode += 1
                if self.current_episode > self.num_episodes:
                    arcade.close_window()
                    return
                print(f"Starting Episode {self.current_episode}")

            # Use random actions for now
            action = np.random.rand(4)

            # Step the environment
            next_state, reward, self.done, _ = self.env.step(action)
            self.state = next_state
            self.total_reward += reward
            self.current_step += 1

            # Update info display
            self.info_text.text = f"Episode: {self.current_episode}/{self.num_episodes}, Steps: {self.current_step}, Reward: {self.total_reward:.2f}"

            # End episode after too many steps
            if self.current_step >= 1000:
                self.done = True

            if self.done:
                print(f"Episode {self.current_episode}: Steps = {self.current_step}, Reward = {self.total_reward:.2f}")

        except Exception as e:
            print(f"Error in AI update: {e}")
            self.done = True  # Force end of episode if there's an error


def main():
    # Create ONLY ONE game window
    window = AsteroidsGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()

    # Create AI driver with the existing window
    driver = AIDriver(window, num_episodes=10)

    # Run the game
    arcade.run()


if __name__ == "__main__":
    main()