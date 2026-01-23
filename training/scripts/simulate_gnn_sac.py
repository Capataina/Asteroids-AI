"""
GNN + SAC Combined Simulation

Single-process mode that trains headless SAC while continuously rendering
the current policy in the windowed game. The display game resets instantly
when the agent dies, so there's always something to watch.
"""

import sys
import os
import time
import random
import copy
from typing import Dict, Any, List, Optional, Tuple

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
from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker
from interfaces.encoders.GraphEncoder import GraphEncoder
from interfaces.ActionInterface import ActionInterface
from training.config.sac import SACConfig
from training.config.rewards import create_reward_calculator
from training.analytics.analytics import TrainingAnalytics
from training.methods.sac.replay_buffer import ReplayBuffer, Transition
from training.methods.sac.learner import SACLearner


class SACSimulationScript:
    """
    Single-process training + continuous playback loop.

    Training runs on a headless game in the background.
    The windowed game continuously displays the current policy,
    resetting instantly when the agent dies.
    """

    def __init__(self, game: AsteroidsGame):
        self.game = game
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Reproducibility
        random.seed(SACConfig.SEED)
        np.random.seed(SACConfig.SEED)
        torch.manual_seed(SACConfig.SEED)

        # === Training (headless) ===
        self.num_collectors = max(1, int(SACConfig.NUM_COLLECTORS))
        self.collectors: List[Dict[str, Any]] = []

        self.learner = SACLearner(device=self.device, config=SACConfig)
        self.replay_buffer = ReplayBuffer(capacity=SACConfig.REPLAY_SIZE, seed=SACConfig.SEED)

        # === Display (windowed) ===
        self.game.continuous_control_mode = True
        self.game.update_internal_rewards = False
        self.game.auto_reset_on_collision = False
        self.game.external_control = True  # Prevent arcade's auto on_update, we call it manually
        self.game.manual_spawning = True   # Prevent arcade.schedule timer accumulation on reset

        # Unschedule any spawner that was set up during window.setup()
        arcade.unschedule(self.game.spawn_asteroid)

        self.display_encoder = GraphEncoder(
            screen_width=globals.SCREEN_WIDTH,
            screen_height=globals.SCREEN_HEIGHT,
            max_asteroids=SACConfig.MAX_ASTEROIDS
        )
        self.display_reward = create_reward_calculator(
            max_steps=SACConfig.VIEWER_MAX_STEPS,
            frame_delay=SACConfig.FRAME_DELAY
        )

        # Display uses a separate copy of the learner (synced periodically)
        self.display_learner = SACLearner(device=self.device, config=SACConfig)

        # Display episode state
        self.display_episode_steps = 0
        self.display_episode_return = 0.0
        self.display_episode_count = 0
        self.display_seed_rng = random.Random(SACConfig.VIEWER_SEED_START)
        self.display_prev_action: Optional[List[float]] = None

        # Analytics
        self.analytics = TrainingAnalytics()

        # Best tracking (for checkpointing)
        self.best_snapshot: Optional[Dict[str, Any]] = None
        self.best_eval_return = float("-inf")
        self.best_eval_step = 0

        # Training counters
        self.total_steps = 0
        self.episode_count = 0
        self.completed_returns: List[float] = []
        self.completed_metrics: List[Dict[str, Any]] = []
        self.update_metrics_window: List[Dict[str, float]] = []
        self.step_rewards_window: List[float] = []
        self.terminal_rewards_window: List[float] = []
        self.window_steps = 0
        self.window_done_steps = 0
        self.update_count = 0
        self.action_stats: List[Dict[str, float]] = []
        self.last_log_time = time.time()
        self.last_sync_step = 0
        self.finalized = False

        # Eval tracking for diagnostics
        self.last_eval_data: Dict[str, Any] = {}
        self.last_eval_holdout_data: Dict[str, Any] = {}
        self.eval_since_improve = 0

        # Probe metrics (policy/critic drift)
        self.probe_payloads = None
        self.probe_prev_actions = None

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
            "reward_scale": SACConfig.REWARD_SCALE,
            "obs_norm_enabled": SACConfig.OBS_NORM_ENABLED,
            "obs_norm_eps": SACConfig.OBS_NORM_EPS,
            "obs_norm_clip": SACConfig.OBS_NORM_CLIP,
            "action_smoothing_enabled": SACConfig.ACTION_SMOOTHING_ENABLED,
            "action_smoothing_alpha": SACConfig.ACTION_SMOOTHING_ALPHA,
            "num_collectors": SACConfig.NUM_COLLECTORS,
            "collector_seed_offset": SACConfig.COLLECTOR_SEED_OFFSET,
            "actor_lr": SACConfig.ACTOR_LR,
            "critic_lr": SACConfig.CRITIC_LR,
            "alpha_lr": SACConfig.ALPHA_LR,
            "critic_loss": SACConfig.CRITIC_LOSS,
            "huber_delta": SACConfig.HUBER_DELTA,
            "auto_entropy": SACConfig.AUTO_ENTROPY,
            "init_alpha": SACConfig.INIT_ALPHA,
            "target_entropy": SACConfig.TARGET_ENTROPY,
            "agc_enabled": SACConfig.AGC_ENABLED,
            "agc_clip_factor": SACConfig.AGC_CLIP_FACTOR,
            "agc_eps": SACConfig.AGC_EPS,
            "gnn_hidden_dim": SACConfig.GNN_HIDDEN_DIM,
            "gnn_num_layers": SACConfig.GNN_NUM_LAYERS,
            "gnn_heads": SACConfig.GNN_HEADS,
            "gnn_dropout": SACConfig.GNN_DROPOUT,
            "actor_hidden_dim": SACConfig.ACTOR_HIDDEN_DIM,
            "critic_hidden_dim": SACConfig.CRITIC_HIDDEN_DIM,
            "max_asteroids": SACConfig.MAX_ASTEROIDS,
            "device": str(self.device),
            "eval_seeds": SACConfig.EVAL_SEEDS,
            "holdout_eval_seeds": SACConfig.HOLDOUT_EVAL_SEEDS,
            "eval_every_episodes": SACConfig.EVAL_EVERY_EPISODES,
        })

        # Initialize collectors
        for idx in range(self.num_collectors):
            self.collectors.append(self._build_collector(idx))

        # Initialize display game
        self._reset_display_episode()

    # ===== Training (headless) =====

    def _build_collector(self, index: int) -> Dict[str, Any]:
        seed = SACConfig.SEED + SACConfig.COLLECTOR_SEED_OFFSET * index
        game = HeadlessAsteroidsGame(
            width=globals.SCREEN_WIDTH,
            height=globals.SCREEN_HEIGHT,
            random_seed=seed
        )
        game.continuous_control_mode = True
        game.update_internal_rewards = False
        game.auto_reset_on_collision = False

        encoder = GraphEncoder(
            screen_width=globals.SCREEN_WIDTH,
            screen_height=globals.SCREEN_HEIGHT,
            max_asteroids=SACConfig.MAX_ASTEROIDS
        )
        reward_calculator = create_reward_calculator(
            max_steps=SACConfig.MAX_EPISODE_STEPS,
            frame_delay=SACConfig.FRAME_DELAY
        )

        collector = {
            "game": game,
            "encoder": encoder,
            "reward_calculator": reward_calculator,
            "episode_steps": 0,
            "episode_return": 0.0,
            "prev_action": None,
        }
        self._reset_training_collector(collector)
        return collector

    def _reset_training_collector(self, collector: Dict[str, Any]) -> None:
        """Reset a headless training collector for a new episode."""
        game = collector["game"]
        game.reset_game()
        game.continuous_control_mode = True
        game.turn_magnitude = 0.0
        game.thrust_magnitude = 0.0
        game.shoot_requested = False
        game.tracker.update(game)
        game.metrics_tracker.update(game)
        collector["reward_calculator"].reset()
        collector["encoder"].reset()
        collector["episode_steps"] = 0
        collector["episode_return"] = 0.0
        collector["prev_action"] = None

    def _select_training_action(self, payload) -> List[float]:
        """Select action for training (with exploration noise during warmup)."""
        if self.total_steps < SACConfig.LEARN_START_STEPS:
            # Random actions during warmup
            turn = random.uniform(-1.0, 1.0)
            thrust = random.uniform(0.0, 1.0)
            shoot = random.uniform(0.0, 1.0)
            return [turn, thrust, shoot]

        graph_tensors = ReplayBuffer.collate_graphs([payload], self.device)
        action_tensor, _ = self.learner.select_action(graph_tensors, deterministic=False)
        action = action_tensor.squeeze(0).detach().cpu().tolist()
        return [
            max(-1.0, min(1.0, float(action[0]))),
            max(0.0, min(1.0, float(action[1]))),
            max(0.0, min(1.0, float(action[2]))),
        ]

    def _apply_action_smoothing(
        self,
        action: List[float],
        prev_action: Optional[List[float]],
    ) -> Tuple[List[float], Optional[List[float]]]:
        if not SACConfig.ACTION_SMOOTHING_ENABLED:
            return action, prev_action

        if prev_action is None:
            smoothed = action
        else:
            alpha = SACConfig.ACTION_SMOOTHING_ALPHA
            smoothed = [
                alpha * prev_action[0] + (1.0 - alpha) * action[0],
                alpha * prev_action[1] + (1.0 - alpha) * action[1],
                alpha * prev_action[2] + (1.0 - alpha) * action[2],
            ]

        smoothed = [
            max(-1.0, min(1.0, float(smoothed[0]))),
            max(0.0, min(1.0, float(smoothed[1]))),
            max(0.0, min(1.0, float(smoothed[2]))),
        ]
        return smoothed, smoothed

    @staticmethod
    def _percentile(values: List[float], pct: float) -> float:
        if not values:
            return 0.0
        return float(np.percentile(values, pct))

    def _compute_weight_stats(self, module: torch.nn.Module, prefix: str) -> Dict[str, float]:
        with torch.no_grad():
            params = [p.detach().flatten() for p in module.parameters() if p.numel() > 0]
            if not params:
                return {
                    f"{prefix}_weight_mean": 0.0,
                    f"{prefix}_weight_std": 0.0,
                    f"{prefix}_weight_norm": 0.0,
                    f"{prefix}_weight_zero_frac": 0.0,
                }
            flat = torch.cat(params)
            zero_frac = float((flat.abs() < 1e-6).float().mean().item())
            return {
                f"{prefix}_weight_mean": float(flat.mean().item()),
                f"{prefix}_weight_std": float(flat.std().item()),
                f"{prefix}_weight_norm": float(flat.norm().item()),
                f"{prefix}_weight_zero_frac": zero_frac,
            }

    def _compute_probe_metrics(self) -> Dict[str, float]:
        probe_size = 128
        if self.probe_payloads is None and len(self.replay_buffer) >= probe_size:
            self.probe_payloads = [t.obs for t in self.replay_buffer.sample(probe_size)]
        if not self.probe_payloads:
            return {}

        with torch.no_grad():
            graph_tensors = ReplayBuffer.collate_graphs(self.probe_payloads, self.device)
            player_feat, asteroid_feat, edge_index, edge_attr = graph_tensors
            player_feat, asteroid_feat, edge_attr = self.learner.normalizer.normalize(
                player_feat, asteroid_feat, edge_attr
            )
            state = self.learner.gnn(player_feat, asteroid_feat, edge_index, edge_attr)
            action, _ = self.learner.actor(state, deterministic=True)
            q1, _ = self.learner.critics(state, action)
            tq1, _ = self.learner.target_critics(state, action)
            critic_target_gap = float((q1 - tq1).abs().mean().item())

            drift = 0.0
            if self.probe_prev_actions is not None:
                drift = float((action - self.probe_prev_actions).abs().mean().item())
            self.probe_prev_actions = action.detach()

        return {
            "sac_policy_drift": drift,
            "sac_critic_target_gap": critic_target_gap,
        }

    def _training_step(self, collector: Dict[str, Any]) -> None:
        """Execute one step of training on a headless collector."""
        game = collector["game"]
        encoder = collector["encoder"]
        reward_calculator = collector["reward_calculator"]

        state = encoder.encode(game.tracker)
        action = self._select_training_action(state)
        action, collector["prev_action"] = self._apply_action_smoothing(action, collector["prev_action"])

        self.action_stats.append({
            "turn": action[0],
            "thrust": action[1],
            "shoot": action[2],
        })

        game.continuous_control_mode = True
        game.turn_magnitude = float(action[0])
        game.thrust_magnitude = float(action[1])
        game.shoot_requested = float(action[2]) > 0.5

        game.on_update(SACConfig.FRAME_DELAY)
        game.tracker.update(game)
        game.metrics_tracker.update(game)

        step_reward = reward_calculator.calculate_step_reward(
            game.tracker,
            game.metrics_tracker
        )
        step_reward *= SACConfig.REWARD_SCALE

        collector["episode_return"] += step_reward
        collector["episode_steps"] += 1
        self.total_steps += 1

        done = game.player not in game.player_list
        timeout = collector["episode_steps"] >= SACConfig.MAX_EPISODE_STEPS

        if done or timeout:
            episode_reward = reward_calculator.calculate_episode_reward(game.metrics_tracker)
            episode_reward *= SACConfig.REWARD_SCALE
            step_reward += episode_reward
            collector["episode_return"] += episode_reward
            self.terminal_rewards_window.append(episode_reward)
            self.window_done_steps += 1

        self.step_rewards_window.append(step_reward)
        self.window_steps += 1

        next_state = encoder.encode(game.tracker)
        transition = Transition(
            obs=state,
            action=action,
            reward=step_reward,
            next_obs=next_state,
            done=done or timeout
        )
        self.replay_buffer.push(transition)

        # Learning updates
        if self.total_steps >= SACConfig.LEARN_START_STEPS and len(self.replay_buffer) >= SACConfig.BATCH_SIZE:
            for _ in range(SACConfig.UPDATES_PER_STEP):
                batch = self.replay_buffer.sample_batch(SACConfig.BATCH_SIZE, self.device)
                update_metrics = self.learner.update(batch)
                self.update_metrics_window.append(update_metrics)
                self.update_count += 1

        # Episode end handling
        if done or timeout:
            metrics = game.metrics_tracker.get_episode_stats()
            metrics["steps"] = collector["episode_steps"]
            self.completed_returns.append(collector["episode_return"])
            self.completed_metrics.append(metrics)
            self.episode_count += 1

            # Periodic evaluation
            if (
                self.total_steps >= SACConfig.LEARN_START_STEPS
                and self.episode_count % SACConfig.EVAL_EVERY_EPISODES == 0
            ):
                eval_data = self._evaluate_policy(SACConfig.EVAL_SEEDS)
                self.last_eval_data = eval_data

                if SACConfig.HOLDOUT_EVAL_SEEDS:
                    self.last_eval_holdout_data = self._evaluate_policy(SACConfig.HOLDOUT_EVAL_SEEDS)
                else:
                    self.last_eval_holdout_data = {}

                prev_best = self.best_eval_return
                self._update_best(eval_data)
                if self.best_eval_return > prev_best:
                    self.eval_since_improve = 0
                else:
                    self.eval_since_improve += 1

            self._reset_training_collector(collector)

        # Periodic logging
        if self.total_steps % SACConfig.LOG_EVERY_STEPS == 0:
            self._log_interval()

    # ===== Display (windowed) =====

    def _reset_display_episode(self) -> None:
        """Reset the windowed display game for a new episode."""
        # Pick a new seed for variety
        seed = self.display_seed_rng.randint(0, 100000)
        self.game.set_seed(seed)
        self.game.reset_game()

        # Ensure continuous control mode
        self.game.continuous_control_mode = True
        self.game.turn_magnitude = 0.0
        self.game.thrust_magnitude = 0.0
        self.game.shoot_requested = False

        # Reset encoder and reward calculator
        self.display_encoder.reset()
        self.display_reward.reset()

        # Reset episode counters
        self.display_episode_steps = 0
        self.display_episode_return = 0.0
        self.display_episode_count += 1
        self.display_prev_action = None

    def _sync_display_policy(self) -> None:
        """Sync display learner with current training learner weights."""
        self.display_learner.gnn.load_state_dict(self.learner.gnn.state_dict())
        self.display_learner.actor.load_state_dict(self.learner.actor.state_dict())
        self.display_learner.normalizer.load_state_dict(self.learner.normalizer.state_dict())
        self.last_sync_step = self.total_steps

    def _select_display_action(self, payload) -> List[float]:
        """Select action for display (deterministic, no exploration)."""
        # During warmup, use random actions for display too
        if self.total_steps < SACConfig.LEARN_START_STEPS:
            turn = random.uniform(-1.0, 1.0)
            thrust = random.uniform(0.0, 1.0)
            shoot = random.uniform(0.0, 1.0)
            action = [turn, thrust, shoot]
        else:
            graph_tensors = ReplayBuffer.collate_graphs([payload], self.device)
            action_tensor, _ = self.display_learner.select_action(graph_tensors, deterministic=True)
            action = action_tensor.squeeze(0).detach().cpu().tolist()
            action = [
                max(-1.0, min(1.0, float(action[0]))),
                max(0.0, min(1.0, float(action[1]))),
                max(0.0, min(1.0, float(action[2]))),
            ]

        action, self.display_prev_action = self._apply_action_smoothing(action, self.display_prev_action)
        return action

    def _display_step(self) -> None:
        """Execute one step on the windowed display game."""
        # Check if player is still alive
        if self.game.player not in self.game.player_list:
            self._reset_display_episode()
            return

        # Check timeout
        if self.display_episode_steps >= SACConfig.VIEWER_MAX_STEPS:
            self._reset_display_episode()
            return

        # Get state and select action
        self.game.tracker.update(self.game)
        state = self.display_encoder.encode(self.game.tracker)
        action = self._select_display_action(state)

        # Apply action
        self.game.continuous_control_mode = True
        self.game.turn_magnitude = float(action[0])
        self.game.thrust_magnitude = float(action[1])
        self.game.shoot_requested = float(action[2]) > 0.5

        # Step the game (temporarily disable external_control so our call works)
        self.game.external_control = False
        self.game.on_update(SACConfig.FRAME_DELAY)
        self.game.external_control = True

        # Update our reward tracking and the score display
        self.game.tracker.update(self.game)
        self.game.metrics_tracker.update(self.game)
        step_reward = self.display_reward.calculate_step_reward(
            self.game.tracker,
            self.game.metrics_tracker
        )
        step_reward *= SACConfig.REWARD_SCALE
        self.display_episode_return += step_reward

        # Update the score text to show our reward
        if self.game.score_text:
            self.game.score_text.text = f"Score: {int(self.display_episode_return)}"

        self.display_episode_steps += 1

    # ===== Evaluation & Best Tracking =====

    def _evaluate_policy(self, seeds: List[int]) -> Dict[str, Any]:
        """Evaluate current policy on fixed seeds."""
        eval_returns = []
        for seed in seeds:
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
            prev_action = None
            while steps < SACConfig.MAX_EPISODE_STEPS and game.player in game.player_list:
                state = encoder.encode(game.tracker)
                graph_tensors = ReplayBuffer.collate_graphs([state], self.device)
                action_tensor, _ = self.learner.select_action(graph_tensors, deterministic=True)
                action = action_tensor.squeeze(0).detach().cpu().tolist()
                action, prev_action = self._apply_action_smoothing(action, prev_action)

                game.continuous_control_mode = True
                game.turn_magnitude = float(action[0])
                game.thrust_magnitude = float(action[1])
                game.shoot_requested = float(action[2]) > 0.5

                game.on_update(SACConfig.FRAME_DELAY)

                step_reward = reward_calc.calculate_step_reward(
                    game.tracker,
                    game.metrics_tracker
                )
                step_reward *= SACConfig.REWARD_SCALE
                total_reward += step_reward
                steps += 1

            total_reward += reward_calc.calculate_episode_reward(game.metrics_tracker) * SACConfig.REWARD_SCALE
            eval_returns.append(total_reward)

        avg_return = float(np.mean(eval_returns)) if eval_returns else 0.0
        return {
            "avg_return": avg_return,
            "returns": eval_returns
        }

    def _update_best(self, eval_data: Dict[str, Any]) -> None:
        """Update best snapshot if current policy is better."""
        if eval_data["avg_return"] <= self.best_eval_return:
            return
        self.best_eval_return = eval_data["avg_return"]
        self.best_eval_step = self.total_steps
        self.best_snapshot = {
            "gnn": copy.deepcopy(self.learner.gnn.state_dict()),
            "actor": copy.deepcopy(self.learner.actor.state_dict()),
            "normalizer": copy.deepcopy(self.learner.normalizer.state_dict()),
            "avg_return": self.best_eval_return,
            "step": self.best_eval_step,
        }
        print(
            f"[SAC] New best avg return {self.best_eval_return:.2f} "
            f"at step {self.best_eval_step}."
        )

    # ===== Analytics =====

    def _log_interval(self) -> None:
        """Log training metrics to analytics."""
        if not self.completed_returns:
            return

        generation = len(self.analytics.generations_data) + 1
        fitness_scores = list(self.completed_returns)

        kills = [m.get("total_kills", 0) for m in self.completed_metrics]
        accuracy = [m.get("accuracy", 0.0) for m in self.completed_metrics]
        time_alive = [m.get("time_alive", 0.0) for m in self.completed_metrics]
        steps = [m.get("steps", 0) for m in self.completed_metrics]
        shots_fired = [m.get("total_shots_fired", 0) for m in self.completed_metrics]
        hits = [m.get("total_hits", 0) for m in self.completed_metrics]

        # Aggregate action stats
        action_stats_avg = {}
        if self.action_stats:
            action_stats_avg = {
                "turn_mean": float(np.mean([s["turn"] for s in self.action_stats])),
                "turn_std": float(np.std([s["turn"] for s in self.action_stats])),
                "thrust_mean": float(np.mean([s["thrust"] for s in self.action_stats])),
                "thrust_std": float(np.std([s["thrust"] for s in self.action_stats])),
                "shoot_rate": float(np.mean([s["shoot"] for s in self.action_stats])),
            }

        # Aggregate learner metrics
        learner_stats = {}
        if self.update_metrics_window:
            keys = self.update_metrics_window[0].keys()
            for key in keys:
                values = [m[key] for m in self.update_metrics_window]
                learner_stats[f"{key}_mean"] = float(np.mean(values))

        sac_metrics: Dict[str, Any] = {
            "sac_env_steps_total": self.total_steps,
            "sac_updates_total": self.update_count,
            "sac_update_to_data_ratio": float(self.update_count) / max(1, self.total_steps),
            "sac_replay_size": len(self.replay_buffer),
        }

        if self.step_rewards_window:
            sac_metrics.update({
                "sac_step_reward_mean": float(np.mean(self.step_rewards_window)),
                "sac_step_reward_std": float(np.std(self.step_rewards_window)),
                "sac_step_reward_p90": self._percentile(self.step_rewards_window, 90),
                "sac_step_reward_p99": self._percentile(self.step_rewards_window, 99),
            })
        if self.terminal_rewards_window:
            sac_metrics.update({
                "sac_terminal_reward_mean": float(np.mean(self.terminal_rewards_window)),
                "sac_terminal_reward_std": float(np.std(self.terminal_rewards_window)),
            })
        if self.window_steps:
            sac_metrics["sac_terminal_frac"] = float(self.window_done_steps) / float(self.window_steps)

        if steps:
            sac_metrics["sac_episode_steps_mean"] = float(np.mean(steps))
            sac_metrics["sac_episode_steps_p90"] = self._percentile(steps, 90)
            sac_metrics["sac_episode_steps_p99"] = self._percentile(steps, 99)

        if action_stats_avg and self.action_stats:
            turns = np.array([s["turn"] for s in self.action_stats], dtype=np.float32)
            thrusts = np.array([s["thrust"] for s in self.action_stats], dtype=np.float32)
            shoots = np.array([s["shoot"] for s in self.action_stats], dtype=np.float32)
            sac_metrics.update({
                "sac_turn_mean": float(np.mean(turns)),
                "sac_turn_std": float(np.std(turns)),
                "sac_turn_zero_rate": float(np.mean(np.abs(turns) < 0.05)),
                "sac_turn_saturation_rate": float(np.mean(np.abs(turns) > 0.95)),
                "sac_thrust_mean": float(np.mean(thrusts)),
                "sac_thrust_std": float(np.std(thrusts)),
                "sac_thrust_zero_rate": float(np.mean(thrusts < 0.05)),
                "sac_thrust_saturation_rate": float(np.mean((thrusts < 0.05) | (thrusts > 0.95))),
                "sac_shoot_rate": float(np.mean(shoots)),
                "sac_shoot_saturation_rate": float(np.mean((shoots < 0.05) | (shoots > 0.95))),
            })

        if learner_stats:
            sac_metrics.update({
                "sac_critic_loss_mean": learner_stats.get("critic_loss_mean", 0.0),
                "sac_actor_loss_mean": learner_stats.get("actor_loss_mean", 0.0),
                "sac_alpha_mean": learner_stats.get("alpha_value_mean", 0.0),
                "sac_policy_entropy_mean": learner_stats.get("policy_entropy_mean", 0.0),
                "sac_q1_mean": learner_stats.get("q1_mean_mean", 0.0),
                "sac_q2_mean": learner_stats.get("q2_mean_mean", 0.0),
                "sac_q1_std": learner_stats.get("q1_std_mean", 0.0),
                "sac_q2_std": learner_stats.get("q2_std_mean", 0.0),
                "sac_target_q_mean": learner_stats.get("target_q_mean_mean", 0.0),
                "sac_target_q_std": learner_stats.get("target_q_std_mean", 0.0),
                "sac_td_abs_mean": learner_stats.get("td_abs_mean_mean", 0.0),
                "sac_td_abs_p90": learner_stats.get("td_abs_p90_mean", 0.0),
                "sac_td_abs_p99": learner_stats.get("td_abs_p99_mean", 0.0),
                "sac_critic_grad_norm": learner_stats.get("critic_grad_norm_mean", 0.0),
                "sac_actor_grad_norm": learner_stats.get("actor_grad_norm_mean", 0.0),
                "sac_critic_clip_rate": learner_stats.get("critic_clip_hit_mean", 0.0),
                "sac_actor_clip_rate": learner_stats.get("actor_clip_hit_mean", 0.0),
                "sac_embedding_norm": learner_stats.get("embedding_norm_mean", 0.0),
                "sac_embedding_dim_std": learner_stats.get("embedding_dim_std_mean", 0.0),
                "sac_embedding_cos_sim": learner_stats.get("embedding_cos_sim_mean", 0.0),
            })

        if self.last_eval_data:
            eval_returns = self.last_eval_data.get("returns", [])
            sac_metrics.update({
                "sac_eval_return_mean": float(self.last_eval_data.get("avg_return", 0.0)),
                "sac_eval_return_std": float(np.std(eval_returns)) if eval_returns else 0.0,
                "sac_eval_seed_min": float(np.min(eval_returns)) if eval_returns else 0.0,
                "sac_eval_seed_max": float(np.max(eval_returns)) if eval_returns else 0.0,
                "sac_eval_returns": eval_returns,
                "sac_eval_best_return": float(self.best_eval_return),
                "sac_eval_best_step": int(self.best_eval_step),
                "sac_eval_since_improve": int(self.eval_since_improve),
            })

        if self.last_eval_holdout_data:
            holdout_returns = self.last_eval_holdout_data.get("returns", [])
            sac_metrics.update({
                "sac_eval_holdout_return_mean": float(self.last_eval_holdout_data.get("avg_return", 0.0)),
                "sac_eval_holdout_return_std": float(np.std(holdout_returns)) if holdout_returns else 0.0,
                "sac_eval_holdout_seed_min": float(np.min(holdout_returns)) if holdout_returns else 0.0,
                "sac_eval_holdout_seed_max": float(np.max(holdout_returns)) if holdout_returns else 0.0,
                "sac_eval_holdout_returns": holdout_returns,
            })

        sac_metrics.update(self._compute_probe_metrics())
        sac_metrics.update(self._compute_weight_stats(self.learner.gnn, "sac_gnn"))
        sac_metrics.update(self._compute_weight_stats(self.learner.actor, "sac_actor"))
        sac_metrics.update(self._compute_weight_stats(self.learner.critics, "sac_critic"))

        behavioral_metrics = {
            "avg_kills": float(np.mean(kills)) if kills else 0.0,
            "max_kills": float(np.max(kills)) if kills else 0.0,
            "avg_accuracy": float(np.mean(accuracy)) if accuracy else 0.0,
            "avg_steps": float(np.mean(steps)) if steps else 0.0,
            "avg_steps_survived": float(np.mean(steps)) if steps else 0.0,
            "avg_time_alive": float(np.mean(time_alive)) if time_alive else 0.0,
            "avg_shots": float(np.mean(shots_fired)) if shots_fired else 0.0,
            "avg_shots_fired": float(np.mean(shots_fired)) if shots_fired else 0.0,
            "avg_hits": float(np.mean(hits)) if hits else 0.0,
            "avg_shots_per_kill": float(np.mean([
                (s / k) if k > 0 else 0.0
                for s, k in zip(shots_fired, kills)
            ])) if shots_fired and kills else 0.0,
            "avg_shots_per_hit": float(np.mean([
                (s / h) if h > 0 else 0.0
                for s, h in zip(shots_fired, hits)
            ])) if shots_fired and hits else 0.0,
            "avg_fitness_std": float(np.std(fitness_scores)) if fitness_scores else 0.0,
            "replay_size": len(self.replay_buffer),
            "total_steps": self.total_steps,
            "episode_count": self.episode_count,
            **action_stats_avg,
            **learner_stats,
            **sac_metrics,
        }

        timing_stats = {
            "evaluation_duration": time.time() - self.last_log_time
        }

        self.analytics.record_generation(
            generation=generation,
            fitness_scores=fitness_scores,
            behavioral_metrics=behavioral_metrics,
            timing_stats=timing_stats
        )

        # Print progress
        avg_return = float(np.mean(fitness_scores))
        print(
            f"[SAC] Step {self.total_steps:,} | "
            f"Episodes: {self.episode_count} | "
            f"Avg Return: {avg_return:.1f} | "
            f"Replay: {len(self.replay_buffer):,}"
        )

        self.completed_returns.clear()
        self.completed_metrics.clear()
        self.update_metrics_window.clear()
        self.action_stats.clear()
        self.step_rewards_window.clear()
        self.terminal_rewards_window.clear()
        self.window_steps = 0
        self.window_done_steps = 0
        self.last_log_time = time.time()

    # ===== Main Update Loop =====

    def update(self, delta_time: float) -> None:
        """
        Called every frame by arcade.

        - Runs training steps in the background (headless)
        - Steps the display game (windowed) with the current policy
        - Syncs display policy periodically
        """
        # Sync display policy periodically (every 1000 training steps)
        sync_interval = 1000
        if self.total_steps - self.last_sync_step >= sync_interval:
            self._sync_display_policy()

        # Run training steps (headless)
        # Before learning starts: run multiple steps per frame (just collecting, fast)
        # After learning starts: run fewer steps to keep display smooth
        if self.total_steps < SACConfig.TOTAL_STEPS:
            if self.total_steps < SACConfig.LEARN_START_STEPS:
                # Pre-learning: collect data fast
                steps_this_frame = SACConfig.TRAIN_STEPS_PER_FRAME * 5
            else:
                # Learning active: limit to 1 step per frame to keep display smooth
                steps_this_frame = 1

            for _ in range(steps_this_frame):
                for collector in self.collectors:
                    if self.total_steps >= SACConfig.TOTAL_STEPS:
                        break
                    self._training_step(collector)
                if self.total_steps >= SACConfig.TOTAL_STEPS:
                    break
        else:
            # Training complete - finalize
            if not self.finalized:
                if self.completed_returns:
                    self._log_interval()
                self.analytics.generate_markdown_report("training_summary_sac.md")
                self.analytics.save_json("training_data_sac.json")
                print("[SAC] Training complete. Reports saved.")
                self.finalized = True

        # Step the display game (always runs, even after training completes)
        self._display_step()


def main() -> None:
    window = AsteroidsGame(
        globals.SCREEN_WIDTH,
        globals.SCREEN_HEIGHT,
        "AsteroidsAI - SAC Live Training"
    )
    window.setup()

    trainer = SACSimulationScript(window)

    # Schedule updates at the configured frame rate
    arcade.schedule(trainer.update, SACConfig.FRAME_DELAY)
    arcade.run()


if __name__ == "__main__":
    main()
