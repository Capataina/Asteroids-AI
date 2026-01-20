"""
GNN + SAC Training Entry Point

Runs a minimal, step-based SAC loop using the graph encoder and continuous control path.
"""

import sys
import os
import time
import random
from typing import Dict, Any, List

import numpy as np
import torch

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from game import globals
from game.headless_game import HeadlessAsteroidsGame
from interfaces.encoders.GraphEncoder import GraphEncoder
from interfaces.ActionInterface import ActionInterface
from training.config.sac import SACConfig
from training.config.rewards import create_reward_calculator
from training.analytics.analytics import TrainingAnalytics
from training.methods.sac.replay_buffer import ReplayBuffer, Transition
from training.methods.sac.learner import SACLearner


class SACTrainingScript:
    """Minimal SAC training loop for GNN-based state."""
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Reproducibility
        random.seed(SACConfig.SEED)
        np.random.seed(SACConfig.SEED)
        torch.manual_seed(SACConfig.SEED)

        # Environment + interfaces
        self.game = HeadlessAsteroidsGame(
            width=globals.SCREEN_WIDTH,
            height=globals.SCREEN_HEIGHT,
            random_seed=SACConfig.SEED
        )
        self.game.continuous_control_mode = True
        self.game.update_internal_rewards = False
        self.game.auto_reset_on_collision = False

        self.state_encoder = GraphEncoder(
            screen_width=globals.SCREEN_WIDTH,
            screen_height=globals.SCREEN_HEIGHT,
            max_asteroids=SACConfig.MAX_ASTEROIDS
        )
        self.action_interface = ActionInterface(action_space_type="continuous")
        self.reward_calculator = create_reward_calculator(
            max_steps=SACConfig.MAX_EPISODE_STEPS,
            frame_delay=SACConfig.FRAME_DELAY
        )

        # SAC learner + replay
        self.learner = SACLearner(device=self.device, config=SACConfig)
        self.replay_buffer = ReplayBuffer(capacity=SACConfig.REPLAY_SIZE, seed=SACConfig.SEED)

        # Analytics
        self.analytics = TrainingAnalytics()
        self.analytics.set_config({
            "method": "GNN + SAC",
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
            "best_checkpoint_path": SACConfig.BEST_CHECKPOINT_PATH,
        })

        # Episode tracking
        self.total_steps = 0
        self.episode_steps = 0
        self.episode_return = 0.0
        self.episode_count = 0
        self.completed_returns: List[float] = []
        self.completed_metrics: List[Dict[str, Any]] = []
        self.update_metrics_window: List[Dict[str, float]] = []

        self.best_return = float("-inf")
        self.best_eval_return = float("-inf")
        self.best_eval_step = 0
        self.last_log_time = time.time()

        checkpoint_dir = os.path.dirname(SACConfig.BEST_CHECKPOINT_PATH)
        if checkpoint_dir:
            os.makedirs(checkpoint_dir, exist_ok=True)

    def _reset_episode(self) -> None:
        self.game.reset_game()
        self.game.continuous_control_mode = True
        self.game.turn_magnitude = 0.0
        self.game.thrust_magnitude = 0.0
        self.game.shoot_requested = False
        self.game.tracker.update(self.game)
        self.game.metrics_tracker.update(self.game)
        self.reward_calculator.reset()
        self.state_encoder.reset()
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
        """Evaluate the current policy on fixed seeds."""
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

            reward_calculator = create_reward_calculator(
                max_steps=SACConfig.MAX_EPISODE_STEPS,
                frame_delay=SACConfig.FRAME_DELAY
            )
            reward_calculator.reset()

            state_encoder = GraphEncoder(
                screen_width=globals.SCREEN_WIDTH,
                screen_height=globals.SCREEN_HEIGHT,
                max_asteroids=SACConfig.MAX_ASTEROIDS
            )
            state_encoder.reset()

            steps = 0
            total_reward = 0.0

            while steps < SACConfig.MAX_EPISODE_STEPS and game.player in game.player_list:
                state = state_encoder.encode(game.tracker)
                graph_tensors = ReplayBuffer.collate_graphs([state], self.device)
                action_tensor, _ = self.learner.select_action(graph_tensors, deterministic=True)
                action = action_tensor.squeeze(0).detach().cpu().tolist()

                game.continuous_control_mode = True
                game.turn_magnitude = float(action[0])
                game.thrust_magnitude = float(action[1])
                game.shoot_requested = float(action[2]) > 0.5

                game.on_update(SACConfig.FRAME_DELAY)

                step_reward = reward_calculator.calculate_step_reward(
                    game.tracker,
                    game.metrics_tracker
                )
                total_reward += step_reward
                steps += 1

            total_reward += reward_calculator.calculate_episode_reward(game.metrics_tracker)
            eval_returns.append(total_reward)

        avg_return = float(np.mean(eval_returns)) if eval_returns else 0.0
        return {
            "avg_return": avg_return,
            "returns": eval_returns
        }

    def _save_best_checkpoint(self, eval_data: Dict[str, Any]) -> None:
        payload = {
            "step": self.total_steps,
            "avg_return": eval_data["avg_return"],
            "eval_returns": eval_data["returns"],
            "gnn": self.learner.gnn.state_dict(),
            "actor": self.learner.actor.state_dict(),
        }
        tmp_path = SACConfig.BEST_CHECKPOINT_PATH + ".tmp"
        torch.save(payload, tmp_path)
        os.replace(tmp_path, SACConfig.BEST_CHECKPOINT_PATH)

    def run(self) -> None:
        self._reset_episode()

        while self.total_steps < SACConfig.TOTAL_STEPS:
            state = self.state_encoder.encode(self.game.tracker)
            action = self._select_action(state)

            # Apply continuous controls
            self.game.continuous_control_mode = True
            self.game.turn_magnitude = float(action[0])
            self.game.thrust_magnitude = float(action[1])
            self.game.shoot_requested = float(action[2]) > 0.5

            # Step the game
            self.game.on_update(SACConfig.FRAME_DELAY)
            self.game.tracker.update(self.game)
            self.game.metrics_tracker.update(self.game)

            # Compute reward
            step_reward = self.reward_calculator.calculate_step_reward(
                self.game.tracker,
                self.game.metrics_tracker
            )

            self.episode_return += step_reward
            self.episode_steps += 1
            self.total_steps += 1

            done = self.game.player not in self.game.player_list
            timeout = self.episode_steps >= SACConfig.MAX_EPISODE_STEPS

            # Terminal reward
            if done or timeout:
                episode_reward = self.reward_calculator.calculate_episode_reward(self.game.metrics_tracker)
                step_reward += episode_reward
                self.episode_return += episode_reward

            next_state = self.state_encoder.encode(self.game.tracker)
            transition = Transition(
                obs=state,
                action=action,
                reward=step_reward,
                next_obs=next_state,
                done=done or timeout
            )
            self.replay_buffer.push(transition)

            # Updates
            if self.total_steps >= SACConfig.LEARN_START_STEPS and len(self.replay_buffer) >= SACConfig.BATCH_SIZE:
                for _ in range(SACConfig.UPDATES_PER_STEP):
                    batch = self.replay_buffer.sample_batch(SACConfig.BATCH_SIZE, self.device)
                    update_metrics = self.learner.update(batch)
                    self.update_metrics_window.append(update_metrics)

            # Episode done handling
            if done or timeout:
                metrics = self.game.metrics_tracker.get_episode_stats()
                metrics["steps"] = self.episode_steps

                self.completed_returns.append(self.episode_return)
                self.completed_metrics.append(metrics)

                if self.episode_return > self.best_return:
                    self.best_return = self.episode_return

                self.episode_count += 1
                if (
                    self.total_steps >= SACConfig.LEARN_START_STEPS
                    and self.episode_count % SACConfig.EVAL_EVERY_EPISODES == 0
                ):
                    eval_data = self._evaluate_policy()
                    if eval_data["avg_return"] > self.best_eval_return:
                        self.best_eval_return = eval_data["avg_return"]
                        self.best_eval_step = self.total_steps
                        self._save_best_checkpoint(eval_data)
                        print(
                            f"[SAC] New best avg return {self.best_eval_return:.2f} "
                            f"at step {self.best_eval_step}."
                        )

                self._reset_episode()

            # Logging interval
            if self.total_steps % SACConfig.LOG_EVERY_STEPS == 0:
                self._log_interval()

        # Final logging + reports
        self._log_interval()
        self.analytics.generate_markdown_report("training_summary_sac.md")
        self.analytics.save_json("training_data_sac.json")


if __name__ == "__main__":
    SACTrainingScript().run()
