"""
GNN + SAC Combined Simulation

Single-process mode that trains headless SAC while continuously rendering
the best-so-far actor in the windowed game.
"""

import sys
import os
import time
import random
import copy
from typing import Dict, Any, List, Optional

import numpy as np
import torch
import arcade

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from game import globals
from Asteroids import AsteroidsGame
from game.headless_game import HeadlessAsteroidsGame
from interfaces.encoders.GraphEncoder import GraphEncoder
from interfaces.ActionInterface import ActionInterface
from training.config.sac import SACConfig
from training.config.rewards import create_reward_calculator
from training.analytics.analytics import TrainingAnalytics
from training.core.episode_runner import EpisodeRunner
from training.core.display_manager import DisplayManager
from training.methods.sac.replay_buffer import ReplayBuffer, Transition
from training.methods.sac.learner import SACLearner
from ai_agents.reinforcement_learning.sac_agent import SACAgent


class SACSimulationScript:
    """Single-process training + playback loop."""
    def __init__(self, game: AsteroidsGame):
        self.game = game
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Reproducibility
        random.seed(SACConfig.SEED)
        np.random.seed(SACConfig.SEED)
        torch.manual_seed(SACConfig.SEED)

        # Training (headless)
        self.train_game = HeadlessAsteroidsGame(
            width=globals.SCREEN_WIDTH,
            height=globals.SCREEN_HEIGHT,
            random_seed=SACConfig.SEED
        )
        self.train_game.continuous_control_mode = True
        self.train_game.update_internal_rewards = False
        self.train_game.auto_reset_on_collision = False

        self.train_encoder = GraphEncoder(
            screen_width=globals.SCREEN_WIDTH,
            screen_height=globals.SCREEN_HEIGHT,
            max_asteroids=SACConfig.MAX_ASTEROIDS
        )
        self.train_reward = create_reward_calculator(
            max_steps=SACConfig.MAX_EPISODE_STEPS,
            frame_delay=SACConfig.FRAME_DELAY
        )

        self.learner = SACLearner(device=self.device, config=SACConfig)
        self.replay_buffer = ReplayBuffer(capacity=SACConfig.REPLAY_SIZE, seed=SACConfig.SEED)

        # Playback (windowed)
        self.display_encoder = GraphEncoder(
            screen_width=globals.SCREEN_WIDTH,
            screen_height=globals.SCREEN_HEIGHT,
            max_asteroids=SACConfig.MAX_ASTEROIDS
        )
        self.display_action_interface = ActionInterface(action_space_type="continuous")
        self.display_reward = create_reward_calculator(
            max_steps=SACConfig.VIEWER_MAX_STEPS,
            frame_delay=SACConfig.FRAME_DELAY
        )
        self.episode_runner = EpisodeRunner(
            game=self.game,
            state_encoder=self.display_encoder,
            action_interface=self.display_action_interface,
            reward_calculator=self.display_reward
        )
        self.analytics = TrainingAnalytics()
        self.display_manager = DisplayManager(
            self.game,
            self.episode_runner,
            self.analytics,
            max_steps=SACConfig.VIEWER_MAX_STEPS
        )

        # Separate learner for display (frozen snapshot)
        self.display_learner = SACLearner(device=self.device, config=SACConfig)
        self.display_agent = SACAgent(self.display_learner, device=self.device)

        # Best tracking
        self.best_snapshot: Optional[Dict[str, Any]] = None
        self.best_eval_return = float("-inf")
        self.best_eval_step = 0

        # Training counters
        self.total_steps = 0
        self.episode_steps = 0
        self.episode_return = 0.0
        self.episode_count = 0
        self.completed_returns: List[float] = []
        self.completed_metrics: List[Dict[str, Any]] = []
        self.update_metrics_window: List[Dict[str, float]] = []
        self.last_log_time = time.time()
        self.finalized = False

        # Viewer seed handling
        self.viewer_seed_mode = SACConfig.VIEWER_SEED_MODE
        self.viewer_seed_rng = random.Random(SACConfig.VIEWER_SEED_START)
        self.viewer_seed_counter = SACConfig.VIEWER_SEED_START

        # Analytics config
        self.analytics.set_config({
            "method": "GNN + SAC (Simulated)",
            "total_steps": SACConfig.TOTAL_STEPS,
            "max_episode_steps": SACConfig.MAX_EPISODE_STEPS,
            "frame_delay": SACConfig.FRAME_DELAY,
            "gamma": SACConfig.GAMMA,
            "tau": SACConfig.TAU,
            "batch_size": SACConfig.BATCH_SIZE,
            "replay_size": SACConfig.REPLAY_SIZE,
            "learn_start_steps": SACConfig.LEARN_START_STEPS,
            "updates_per_step": SACConfig.UPDATES_PER_STEP,
            "actor_lr": SACConfig.ACTOR_LR,
            "critic_lr": SACConfig.CRITIC_LR,
            "alpha_lr": SACConfig.ALPHA_LR,
            "auto_entropy": SACConfig.AUTO_ENTROPY,
            "init_alpha": SACConfig.INIT_ALPHA,
            "target_entropy": SACConfig.TARGET_ENTROPY,
            "gnn_hidden_dim": SACConfig.GNN_HIDDEN_DIM,
            "gnn_num_layers": SACConfig.GNN_NUM_LAYERS,
            "gnn_heads": SACConfig.GNN_HEADS,
            "gnn_dropout": SACConfig.GNN_DROPOUT,
            "actor_hidden_dim": SACConfig.ACTOR_HIDDEN_DIM,
            "critic_hidden_dim": SACConfig.CRITIC_HIDDEN_DIM,
            "max_asteroids": SACConfig.MAX_ASTEROIDS,
            "device": str(self.device),
            "eval_seeds": SACConfig.EVAL_SEEDS,
            "eval_every_episodes": SACConfig.EVAL_EVERY_EPISODES,
        })

        # Hook draw
        original_draw = self.game.on_draw
        def new_draw():
            original_draw()
            self.display_manager.draw()
        self.game.on_draw = new_draw

        # Initialize training episode
        self._reset_training_episode()

    def _reset_training_episode(self) -> None:
        self.train_game.reset_game()
        self.train_game.continuous_control_mode = True
        self.train_game.turn_magnitude = 0.0
        self.train_game.thrust_magnitude = 0.0
        self.train_game.shoot_requested = False
        self.train_game.tracker.update(self.train_game)
        self.train_game.metrics_tracker.update(self.train_game)
        self.train_reward.reset()
        self.train_encoder.reset()
        self.episode_steps = 0
        self.episode_return = 0.0

    def _select_action(self, payload) -> List[float]:
        if self.total_steps < SACConfig.LEARN_START_STEPS:
            turn = random.uniform(-1.0, 1.0)
            thrust = random.uniform(0.0, 1.0)
            shoot = 1.0 if random.random() > 0.5 else 0.0
            return [turn, thrust, shoot]

        graph_tensors = ReplayBuffer.collate_graphs([payload], self.device)
        action_tensor, _ = self.learner.select_action(graph_tensors, deterministic=False)
        action = action_tensor.squeeze(0).detach().cpu().tolist()
        return [
            max(-1.0, min(1.0, float(action[0]))),
            max(0.0, min(1.0, float(action[1]))),
            1.0 if float(action[2]) > 0.5 else 0.0
        ]

    def _log_interval(self) -> None:
        if not self.completed_returns:
            return

        generation = len(self.analytics.generations_data) + 1
        fitness_scores = list(self.completed_returns)

        kills = [m.get("total_kills", 0) for m in self.completed_metrics]
        accuracy = [m.get("accuracy", 0.0) for m in self.completed_metrics]
        time_alive = [m.get("time_alive", 0.0) for m in self.completed_metrics]
        steps = [m.get("steps", 0) for m in self.completed_metrics]

        behavioral_metrics = {
            "avg_kills": float(np.mean(kills)) if kills else 0.0,
            "max_kills": float(np.max(kills)) if kills else 0.0,
            "avg_accuracy": float(np.mean(accuracy)) if accuracy else 0.0,
            "avg_steps": float(np.mean(steps)) if steps else 0.0,
            "avg_time_alive": float(np.mean(time_alive)) if time_alive else 0.0,
            "avg_fitness_std": float(np.std(fitness_scores)) if fitness_scores else 0.0,
            "replay_size": len(self.replay_buffer),
        }

        if self.update_metrics_window:
            behavioral_metrics.update({
                "critic_loss_mean": float(np.mean([m["critic_loss"] for m in self.update_metrics_window])),
                "actor_loss_mean": float(np.mean([m["actor_loss"] for m in self.update_metrics_window])),
                "alpha_value": float(np.mean([m["alpha_value"] for m in self.update_metrics_window])),
                "q1_mean": float(np.mean([m["q1_mean"] for m in self.update_metrics_window])),
                "q2_mean": float(np.mean([m["q2_mean"] for m in self.update_metrics_window])),
            })

        timing_stats = {
            "evaluation_duration": time.time() - self.last_log_time
        }

        self.analytics.record_generation(
            generation=generation,
            fitness_scores=fitness_scores,
            behavioral_metrics=behavioral_metrics,
            timing_stats=timing_stats
        )

        self.completed_returns.clear()
        self.completed_metrics.clear()
        self.update_metrics_window.clear()
        self.last_log_time = time.time()

    def _evaluate_policy(self) -> Dict[str, Any]:
        eval_returns = []
        for seed in SACConfig.EVAL_SEEDS:
            game = HeadlessAsteroidsGame(
                width=globals.SCREEN_WIDTH,
                height=globals.SCREEN_HEIGHT,
                random_seed=seed
            )
            game.continuous_control_mode = True
            game.update_internal_rewards = False
            game.auto_reset_on_collision = False
            game.reset_game()

            reward_calc = create_reward_calculator(
                max_steps=SACConfig.MAX_EPISODE_STEPS,
                frame_delay=SACConfig.FRAME_DELAY
            )
            reward_calc.reset()

            encoder = GraphEncoder(
                screen_width=globals.SCREEN_WIDTH,
                screen_height=globals.SCREEN_HEIGHT,
                max_asteroids=SACConfig.MAX_ASTEROIDS
            )
            encoder.reset()

            steps = 0
            total_reward = 0.0
            while steps < SACConfig.MAX_EPISODE_STEPS and game.player in game.player_list:
                state = encoder.encode(game.tracker)
                graph_tensors = ReplayBuffer.collate_graphs([state], self.device)
                action_tensor, _ = self.learner.select_action(graph_tensors, deterministic=True)
                action = action_tensor.squeeze(0).detach().cpu().tolist()

                game.continuous_control_mode = True
                game.turn_magnitude = float(action[0])
                game.thrust_magnitude = float(action[1])
                game.shoot_requested = float(action[2]) > 0.5

                game.on_update(SACConfig.FRAME_DELAY)

                step_reward = reward_calc.calculate_step_reward(
                    game.tracker,
                    game.metrics_tracker
                )
                total_reward += step_reward
                steps += 1

            total_reward += reward_calc.calculate_episode_reward(game.metrics_tracker)
            eval_returns.append(total_reward)

        avg_return = float(np.mean(eval_returns)) if eval_returns else 0.0
        return {
            "avg_return": avg_return,
            "returns": eval_returns
        }

    def _update_best(self, eval_data: Dict[str, Any]) -> None:
        if eval_data["avg_return"] <= self.best_eval_return:
            return
        self.best_eval_return = eval_data["avg_return"]
        self.best_eval_step = self.total_steps
        self.best_snapshot = {
            "gnn": copy.deepcopy(self.learner.gnn.state_dict()),
            "actor": copy.deepcopy(self.learner.actor.state_dict()),
            "avg_return": self.best_eval_return,
            "step": self.best_eval_step,
        }
        print(
            f"[SAC] New best avg return {self.best_eval_return:.2f} "
            f"at step {self.best_eval_step}."
        )

    def _apply_best_snapshot(self) -> None:
        if not self.best_snapshot:
            return
        self.display_learner.gnn.load_state_dict(self.best_snapshot["gnn"])
        self.display_learner.actor.load_state_dict(self.best_snapshot["actor"])

    def _next_viewer_seed(self) -> int:
        if self.viewer_seed_mode == "random":
            low, high = SACConfig.VIEWER_SEED_RANGE
            return self.viewer_seed_rng.randint(low, high)
        seed = self.viewer_seed_counter
        self.viewer_seed_counter += 1
        return seed

    def _start_display(self) -> None:
        if not self.best_snapshot:
            return
        self._apply_best_snapshot()
        seed = self._next_viewer_seed()
        self.game.set_seed(seed)
        self.display_manager.start_display(
            self.display_agent,
            self.best_snapshot["avg_return"],
            self.best_snapshot["avg_return"]
        )

    def _training_step(self) -> None:
        state = self.train_encoder.encode(self.train_game.tracker)
        action = self._select_action(state)

        self.train_game.continuous_control_mode = True
        self.train_game.turn_magnitude = float(action[0])
        self.train_game.thrust_magnitude = float(action[1])
        self.train_game.shoot_requested = float(action[2]) > 0.5

        self.train_game.on_update(SACConfig.FRAME_DELAY)
        self.train_game.tracker.update(self.train_game)
        self.train_game.metrics_tracker.update(self.train_game)

        step_reward = self.train_reward.calculate_step_reward(
            self.train_game.tracker,
            self.train_game.metrics_tracker
        )

        self.episode_return += step_reward
        self.episode_steps += 1
        self.total_steps += 1

        done = self.train_game.player not in self.train_game.player_list
        timeout = self.episode_steps >= SACConfig.MAX_EPISODE_STEPS

        if done or timeout:
            episode_reward = self.train_reward.calculate_episode_reward(self.train_game.metrics_tracker)
            step_reward += episode_reward
            self.episode_return += episode_reward

        next_state = self.train_encoder.encode(self.train_game.tracker)
        transition = Transition(
            obs=state,
            action=action,
            reward=step_reward,
            next_obs=next_state,
            done=done or timeout
        )
        self.replay_buffer.push(transition)

        if self.total_steps >= SACConfig.LEARN_START_STEPS and len(self.replay_buffer) >= SACConfig.BATCH_SIZE:
            for _ in range(SACConfig.UPDATES_PER_STEP):
                batch = self.replay_buffer.sample_batch(SACConfig.BATCH_SIZE, self.device)
                update_metrics = self.learner.update(batch)
                self.update_metrics_window.append(update_metrics)

        if done or timeout:
            metrics = self.train_game.metrics_tracker.get_episode_stats()
            metrics["steps"] = self.episode_steps
            self.completed_returns.append(self.episode_return)
            self.completed_metrics.append(metrics)
            self.episode_count += 1

            if (
                self.total_steps >= SACConfig.LEARN_START_STEPS
                and self.episode_count % SACConfig.EVAL_EVERY_EPISODES == 0
            ):
                eval_data = self._evaluate_policy()
                self._update_best(eval_data)

            self._reset_training_episode()

        if self.total_steps % SACConfig.LOG_EVERY_STEPS == 0:
            self._log_interval()

    def update(self, delta_time: float) -> None:
        # Update display
        if self.display_manager.showing_best_agent:
            status = self.display_manager.update(delta_time)
            if status == "done":
                self._start_display()
        else:
            if self.best_snapshot:
                self._start_display()

        # Train in the background (headless)
        if self.total_steps < SACConfig.TOTAL_STEPS:
            for _ in range(SACConfig.TRAIN_STEPS_PER_FRAME):
                self._training_step()
        else:
            # Final flush + save once
            if not self.finalized:
                if self.completed_returns:
                    self._log_interval()
                self.analytics.generate_markdown_report("training_summary_sac.md")
                self.analytics.save_json("training_data_sac.json")
                self.finalized = True


def main() -> None:
    window = AsteroidsGame(
        globals.SCREEN_WIDTH,
        globals.SCREEN_HEIGHT,
        "AsteroidsAI - SAC Simulated"
    )
    window.setup()
    trainer = SACSimulationScript(window)
    arcade.schedule(trainer.update, SACConfig.FRAME_DELAY)
    arcade.run()


if __name__ == "__main__":
    main()
