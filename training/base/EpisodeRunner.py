from typing import Optional
from Asteroids import AsteroidsGame
from interfaces.StateEncoder import StateEncoder
from interfaces.ActionInterface import ActionInterface
from interfaces.RewardCalculator import ComposableRewardCalculator
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker
from training.base.BaseAgent import BaseAgent
from training.base.EpisodeResult import EpisodeResult

class EpisodeRunner:
  """
  Class for running episodes.

  Args:
    game: AsteroidsGame instance
    state_encoder: StateEncoder instance (e.g., VectorEncoder for GA)
    action_interface: ActionInterface instance
    reward_calculator: ComposableRewardCalculator instance
    env_tracker: EnvironmentTracker instance (defaults to game.tracker)
    metrics_tracker: MetricsTracker instance (defaults to game.metrics_tracker)
  """

  def __init__(
    self,
    game: AsteroidsGame,
    state_encoder: StateEncoder,
    action_interface: ActionInterface,
    reward_calculator: ComposableRewardCalculator,
    env_tracker: Optional[EnvironmentTracker] = None,
    metrics_tracker: Optional[MetricsTracker] = None
  ):
    """
    Initialize EpisodeRunner with game and infrastructure components.
    
    Args:
      game: AsteroidsGame instance
      state_encoder: StateEncoder instance (e.g., VectorEncoder for GA)
      action_interface: ActionInterface instance
      reward_calculator: ComposableRewardCalculator instance
      env_tracker: EnvironmentTracker instance (defaults to game.tracker)
      metrics_tracker: MetricsTracker instance (defaults to game.metrics_tracker)
    """
    self.game = game
    self.state_encoder = state_encoder
    self.action_interface = action_interface
    self.reward_calculator = reward_calculator
    self.env_tracker = env_tracker or game.tracker
    self.metrics_tracker = metrics_tracker or game.metrics_tracker

    # Frame rate for manual stepping (default 60 FPS)
    self.frame_delay = 1.0 / 60.0
    
    # Disable game's internal systems during episode running
    self.game.update_internal_rewards = False
    self.game.auto_reset_on_collision = False

  def run_episode(self, agent: BaseAgent, max_steps: int = 1000) -> EpisodeResult:
    """
    Run a single episode with the given agent.

    Args:
      agent: BaseAgent instance to run episode with
      max_steps: Maximum number of steps before timeout

    Returns:
      EpisodeResult with episode statistics
    """
    # Reset the game and trackers
    self.game.reset_game()
    self.env_tracker.update(self.game)
    self.metrics_tracker.update(self.game)
    self.reward_calculator.reset()
    self.state_encoder.reset()
    agent.reset()

    # Initialize episode variables
    done = False
    steps = 0
    total_reward = 0.0
    done_reason = "timeout"
    metrics = {}

    # Episode loop:
    while not done and steps < max_steps:

      # Encode state using state_encoder
      state = self.state_encoder.encode(self.env_tracker)

      # Get action from agent
      action = agent.get_action(state)

      # Validate and normalize action
      self.action_interface.validate(action)
      action = self.action_interface.normalize(action)

      # Convert to game input
      game_input = self.action_interface.to_game_input(action)

      # Apply to game (set left_pressed, etc.)
      self.game.left_pressed = game_input["left_pressed"]
      self.game.right_pressed = game_input["right_pressed"]
      self.game.up_pressed = game_input["up_pressed"]
      self.game.space_pressed = game_input["space_pressed"]

      # Step game (call game.on_update())
      self.game.on_update(self.frame_delay)

      # Update trackers
      self.env_tracker.update(self.game)
      self.metrics_tracker.update(self.game)

      # Calculate step reward
      step_reward = self.reward_calculator.calculate_step_reward(self.env_tracker, self.metrics_tracker)
      total_reward += step_reward
      steps += 1

      # Check done conditions (collision, timeout)
      if self.game.player not in self.game.player_list:
        # Player was removed (collision detected in on_update)
        done = True
        done_reason = "collision"

      # Calculate episode reward
      episode_reward = self.reward_calculator.calculate_episode_reward(self.metrics_tracker)
      total_reward += episode_reward

      # Collect metrics
      metrics = self.metrics_tracker.get_episode_stats()

    return EpisodeResult(total_reward=total_reward, steps=steps, metrics=metrics, done_reason=done_reason)