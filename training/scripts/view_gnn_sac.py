"""
GNN + SAC Viewer (Best-So-Far Playback)

Runs a continuous windowed playback that reloads the best checkpoint
after each episode ends.
"""

import sys
import os
import time
import random

import torch
import arcade

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from game import globals
from Asteroids import AsteroidsGame
from interfaces.encoders.GraphEncoder import GraphEncoder
from interfaces.ActionInterface import ActionInterface
from training.config.sac import SACConfig
from training.config.rewards import create_reward_calculator
from training.analytics.analytics import TrainingAnalytics
from training.core.episode_runner import EpisodeRunner
from training.core.display_manager import DisplayManager
from training.methods.sac.learner import SACLearner
from ai_agents.reinforcement_learning.sac_agent import SACAgent


class SACViewer:
    """Continuous playback of best-so-far SAC agent."""
    def __init__(self, game: AsteroidsGame):
        self.game = game
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.state_encoder = GraphEncoder(
            screen_width=globals.SCREEN_WIDTH,
            screen_height=globals.SCREEN_HEIGHT,
            max_asteroids=SACConfig.MAX_ASTEROIDS
        )
        self.action_interface = ActionInterface(action_space_type="continuous")
        self.reward_calculator = create_reward_calculator(
            max_steps=SACConfig.VIEWER_MAX_STEPS,
            frame_delay=SACConfig.FRAME_DELAY
        )
        self.episode_runner = EpisodeRunner(
            game=game,
            state_encoder=self.state_encoder,
            action_interface=self.action_interface,
            reward_calculator=self.reward_calculator
        )

        self.analytics = TrainingAnalytics()
        self.display_manager = DisplayManager(
            game,
            self.episode_runner,
            self.analytics,
            max_steps=SACConfig.VIEWER_MAX_STEPS
        )

        self.learner = SACLearner(device=self.device, config=SACConfig)
        self.agent = SACAgent(self.learner, device=self.device)

        self.best_checkpoint_mtime = None
        self.best_avg_return = 0.0
        self.best_step = 0

        self.seed_mode = SACConfig.VIEWER_SEED_MODE
        self.seed_rng = random.Random(SACConfig.VIEWER_SEED_START)
        self.seed_counter = SACConfig.VIEWER_SEED_START

        # Hook draw
        original_draw = self.game.on_draw
        def new_draw():
            original_draw()
            self.display_manager.draw()
        self.game.on_draw = new_draw

    def _next_seed(self) -> int:
        if self.seed_mode == "random":
            low, high = SACConfig.VIEWER_SEED_RANGE
            return self.seed_rng.randint(low, high)
        seed = self.seed_counter
        self.seed_counter += 1
        return seed

    def _load_best_checkpoint(self) -> bool:
        path = SACConfig.BEST_CHECKPOINT_PATH
        if not os.path.exists(path):
            return False

        mtime = os.path.getmtime(path)
        if self.best_checkpoint_mtime is not None and mtime <= self.best_checkpoint_mtime:
            return False

        checkpoint = torch.load(path, map_location=self.device)
        try:
            self.learner.gnn.load_state_dict(checkpoint["gnn"])
            self.learner.actor.load_state_dict(checkpoint["actor"])
            if "normalizer" in checkpoint:
                self.learner.normalizer.load_state_dict(checkpoint["normalizer"])
        except Exception as e:
            print(f"[SAC] Failed to load checkpoint weights from {path}: {e}")
            self.best_checkpoint_mtime = mtime
            return False
        self.best_avg_return = float(checkpoint.get("avg_return", 0.0))
        self.best_step = int(checkpoint.get("step", 0))
        self.best_checkpoint_mtime = mtime
        return True

    def _start_episode(self) -> None:
        seed = self._next_seed()
        self.game.set_seed(seed)
        self.display_manager.start_display(self.agent, self.best_avg_return, self.best_avg_return)

    def update(self, delta_time: float) -> None:
        if self.display_manager.showing_best_agent:
            status = self.display_manager.update(delta_time)
            if status == "done":
                self._load_best_checkpoint()
                if self.best_checkpoint_mtime is not None:
                    self._start_episode()
            return

        # Not currently displaying; attempt to load and start.
        if self._load_best_checkpoint():
            self._start_episode()


def main() -> None:
    window = AsteroidsGame(
        globals.SCREEN_WIDTH,
        globals.SCREEN_HEIGHT,
        "AsteroidsAI - SAC Viewer"
    )
    window.setup()
    viewer = SACViewer(window)
    arcade.schedule(viewer.update, SACConfig.FRAME_DELAY)

    try:
        arcade.run()
    finally:
        print("Viewer exiting.")


if __name__ == "__main__":
    main()
