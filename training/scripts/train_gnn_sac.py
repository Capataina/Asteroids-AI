"""
GNN + SAC Training Entry Point

Runs a minimal, step-based SAC loop using the graph encoder and continuous control path.
Includes comprehensive logging and analytics for monitoring training health.
"""

import sys
import os
import time
import random
import signal
from typing import Dict, Any, List, Optional, Tuple

import numpy as np
import torch

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from game import globals
from game.headless_game import HeadlessAsteroidsGame
from interfaces.encoders.GraphEncoder import GraphEncoder
from training.config.sac import SACConfig
from training.config.rewards import create_reward_calculator
from training.analytics.analytics import TrainingAnalytics
from training.methods.sac.replay_buffer import ReplayBuffer, Transition
from training.methods.sac.learner import SACLearner


class SACTrainingScript:
    """SAC training loop with comprehensive logging and analytics."""

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Reproducibility
        random.seed(SACConfig.SEED)
        np.random.seed(SACConfig.SEED)
        torch.manual_seed(SACConfig.SEED)

        # Environment + interfaces (parallel collectors)
        self.num_collectors = max(1, int(SACConfig.NUM_COLLECTORS))
        self.collectors: List[Dict[str, Any]] = []

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
            "best_checkpoint_path": SACConfig.BEST_CHECKPOINT_PATH,
        })

        # Initialize collectors
        for idx in range(self.num_collectors):
            self.collectors.append(self._build_collector(idx))

        # Episode tracking
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

        # Per-episode reward breakdown tracking
        self.episode_reward_breakdowns: List[Dict[str, float]] = []

        # Action health tracking (per logging window)
        self.action_stats: List[Dict[str, float]] = []

        # Best tracking
        self.best_return = float("-inf")
        self.best_eval_return = float("-inf")
        self.best_eval_step = 0
        self.eval_since_improve = 0
        self.last_eval_data: Dict[str, Any] = {}
        self.last_eval_holdout_data: Dict[str, Any] = {}
        self.last_log_time = time.time()

        # Probe metrics (policy/critic drift)
        self.probe_payloads = None
        self.probe_prev_actions = None

        # Interrupted flag for signal handler
        self.interrupted = False

        checkpoint_dir = os.path.dirname(SACConfig.BEST_CHECKPOINT_PATH)
        if checkpoint_dir:
            os.makedirs(checkpoint_dir, exist_ok=True)

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

        state_encoder = GraphEncoder(
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
            "state_encoder": state_encoder,
            "reward_calculator": reward_calculator,
            "episode_steps": 0,
            "episode_return": 0.0,
            "prev_action": None,
        }
        self._reset_collector(collector)
        return collector

    def _reset_collector(self, collector: Dict[str, Any]) -> None:
        game = collector["game"]
        game.reset_game()
        game.continuous_control_mode = True
        game.turn_magnitude = 0.0
        game.thrust_magnitude = 0.0
        game.shoot_requested = False
        game.tracker.update(game)
        game.metrics_tracker.update(game)

        collector["reward_calculator"].reset()
        collector["state_encoder"].reset()
        collector["episode_steps"] = 0
        collector["episode_return"] = 0.0
        collector["prev_action"] = None

    def _select_action(self, payload) -> List[float]:
        if self.total_steps < SACConfig.LEARN_START_STEPS:
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

    def _step_collector(self, collector: Dict[str, Any]) -> None:
        game = collector["game"]
        state_encoder = collector["state_encoder"]
        reward_calculator = collector["reward_calculator"]

        state = state_encoder.encode(game.tracker)
        action = self._select_action(state)
        action, collector["prev_action"] = self._apply_action_smoothing(action, collector["prev_action"])

        # Track action stats
        self.action_stats.append({
            "turn": action[0],
            "thrust": action[1],
            "shoot": action[2],
        })

        # Apply continuous controls
        game.continuous_control_mode = True
        game.turn_magnitude = float(action[0])
        game.thrust_magnitude = float(action[1])
        game.shoot_requested = float(action[2]) > 0.5

        # Step the game
        game.on_update(SACConfig.FRAME_DELAY)
        game.tracker.update(game)
        game.metrics_tracker.update(game)

        # Compute reward (scaled)
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

        # Terminal reward
        if done or timeout:
            episode_reward = reward_calculator.calculate_episode_reward(game.metrics_tracker)
            episode_reward *= SACConfig.REWARD_SCALE
            step_reward += episode_reward
            collector["episode_return"] += episode_reward
            self.terminal_rewards_window.append(episode_reward)
            self.window_done_steps += 1

        self.step_rewards_window.append(step_reward)
        self.window_steps += 1

        next_state = state_encoder.encode(game.tracker)
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
                self.update_count += 1

        # Episode done handling
        if done or timeout:
            metrics = game.metrics_tracker.get_episode_stats()
            metrics["steps"] = collector["episode_steps"]

            # Get reward breakdown for this episode (scaled)
            reward_breakdown = reward_calculator.get_reward_breakdown()
            if SACConfig.REWARD_SCALE != 1.0:
                reward_breakdown = {k: v * SACConfig.REWARD_SCALE for k, v in reward_breakdown.items()}
            self.episode_reward_breakdowns.append(reward_breakdown)

            self.completed_returns.append(collector["episode_return"])
            self.completed_metrics.append(metrics)

            if collector["episode_return"] > self.best_return:
                self.best_return = collector["episode_return"]

            self.episode_count += 1
            if (
                self.total_steps >= SACConfig.LEARN_START_STEPS
                and self.episode_count % SACConfig.EVAL_EVERY_EPISODES == 0
            ):
                eval_data = self._evaluate_policy(SACConfig.EVAL_SEEDS)
                prev_best = self.best_eval_return
                is_new_best = eval_data["avg_return"] > self.best_eval_return
                self.last_eval_data = eval_data

                holdout_data = None
                if SACConfig.HOLDOUT_EVAL_SEEDS:
                    holdout_data = self._evaluate_policy(SACConfig.HOLDOUT_EVAL_SEEDS)
                    self.last_eval_holdout_data = holdout_data
                else:
                    self.last_eval_holdout_data = {}

                if is_new_best:
                    self.best_eval_return = eval_data["avg_return"]
                    self.best_eval_step = self.total_steps
                    self._save_best_checkpoint(eval_data)
                    self.eval_since_improve = 0
                else:
                    self.eval_since_improve += 1

                self._log_evaluation(eval_data, is_new_best, prev_best, holdout_data)

            self._reset_collector(collector)

        # Logging interval
        if self.total_steps % SACConfig.LOG_EVERY_STEPS == 0:
            self._log_interval()

    def _log_interval(self) -> None:
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

        # Aggregate reward breakdowns
        reward_breakdown_avg = {}
        if self.episode_reward_breakdowns:
            all_keys = set()
            for bd in self.episode_reward_breakdowns:
                all_keys.update(bd.keys())
            for key in all_keys:
                values = [bd.get(key, 0.0) for bd in self.episode_reward_breakdowns]
                reward_breakdown_avg[key] = float(np.mean(values))

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

        # SAC diagnostics (action saturation, replay/returns, eval, drift, weights)
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
            # Analytics schema compatibility (collectors expect *_survived / *_fired naming).
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
            **reward_breakdown_avg,
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

        # === Print formatted output ===
        avg_return = float(np.mean(fitness_scores))
        avg_kills = behavioral_metrics.get("avg_kills", 0.0)
        avg_time = behavioral_metrics.get("avg_time_alive", 0.0)

        print("=" * 75)
        print(f"[SAC] TRAINING LOG - Step {self.total_steps:,}")
        print("=" * 75)
        print(f"  Episodes:    {self.episode_count:<12} Replay Size: {len(self.replay_buffer):,}")
        print("-" * 75)
        print(f"  PERFORMANCE (last {len(fitness_scores)} episodes):")
        print(f"    Avg Return:    {avg_return:>+10.1f}    (higher = better)")
        print(f"    Avg Kills:     {avg_kills:>10.1f}    (higher = better)")
        print(f"    Avg Time:      {avg_time:>10.1f}s   (higher = survived longer)")

        # Reward breakdown
        if reward_breakdown_avg:
            print("-" * 75)
            print(f"  REWARD BREAKDOWN (avg contribution per episode):")
            # Sort by absolute value to show most impactful first
            sorted_rewards = sorted(reward_breakdown_avg.items(), key=lambda x: abs(x[1]), reverse=True)
            for name, value in sorted_rewards:
                direction = "(+good)" if value > 0 else "(-bad)" if value < 0 else ""
                print(f"    {name:<30} {value:>+10.1f}  {direction}")

        # Action health
        if action_stats_avg:
            print("-" * 75)
            print(f"  ACTION HEALTH (want variety, not extremes):")
            turn_m = action_stats_avg.get('turn_mean', 0)
            turn_s = action_stats_avg.get('turn_std', 0)
            thrust_m = action_stats_avg.get('thrust_mean', 0)
            thrust_s = action_stats_avg.get('thrust_std', 0)
            shoot_r = action_stats_avg.get('shoot_rate', 0)

            # Assess health
            turn_status = "OK" if abs(turn_m) < 0.5 and turn_s > 0.3 else "WARN" if turn_s < 0.1 else "OK"
            thrust_status = "OK" if 0.2 < thrust_m < 0.8 and thrust_s > 0.2 else "WARN" if thrust_s < 0.1 else "OK"
            shoot_status = "OK" if 0.1 < shoot_r < 0.9 else "WARN"

            print(f"    Turn:     mean={turn_m:>+6.2f}  std={turn_s:>5.2f}  [{turn_status}] (std>0.3 = exploring)")
            print(f"    Thrust:   mean={thrust_m:>+6.2f}  std={thrust_s:>5.2f}  [{thrust_status}] (want 0.3-0.7 mean)")
            print(f"    Shoot:    rate={shoot_r:>6.1%}           [{shoot_status}] (want 10-50%)")

        # Learner health (only if learning has started)
        if learner_stats:
            print("-" * 75)
            print(f"  LEARNER HEALTH:")
            critic_loss = learner_stats.get("critic_loss_mean", 0)
            actor_loss = learner_stats.get("actor_loss_mean", 0)
            alpha = learner_stats.get("alpha_value_mean", 0)
            q1 = learner_stats.get("q1_mean_mean", 0)

            # Assess critic loss (lower is generally better, but not 0)
            critic_status = "OK" if 0.01 < critic_loss < 10 else "WARN"
            print(f"    Critic Loss:   {critic_loss:>10.3f}  [{critic_status}] (lower=better, 0.01-1.0 typical)")
            print(f"    Actor Loss:    {actor_loss:>10.3f}         (negative=good, means Q is high)")
            print(f"    Alpha:         {alpha:>10.4f}         (entropy weight, auto-tuned)")
            print(f"    Q1 Mean:       {q1:>10.1f}         (expected future reward)")

            # Gradient norms
            critic_grad = learner_stats.get("critic_grad_norm_mean", 0)
            actor_grad = learner_stats.get("actor_grad_norm_mean", 0)
            grad_status = "OK" if critic_grad < 50 and actor_grad < 50 else "WARN"
            print(f"    Grad Norms:    critic={critic_grad:>5.1f}  actor={actor_grad:>5.1f}  [{grad_status}] (<50 = stable)")

            # Embedding health
            emb_norm = learner_stats.get("embedding_norm_mean", 0)
            emb_std = learner_stats.get("embedding_dim_std_mean", 0)
            emb_cos = learner_stats.get("embedding_cos_sim_mean", 0)
            entropy = learner_stats.get("policy_entropy_mean", 0)

            emb_status = "OK" if emb_std > 0.1 and emb_cos < 0.8 else "WARN"
            print(f"    Embedding:     norm={emb_norm:>5.1f}  std={emb_std:>.3f}  cos={emb_cos:>.2f}  [{emb_status}]")
            print(f"                   (std>0.1 = diverse states, cos<0.8 = not collapsed)")
            print(f"    Policy Entropy: {entropy:>9.2f}         (higher=more exploration)")

        print("=" * 75)
        print()

        # Clear window accumulators
        self.completed_returns.clear()
        self.completed_metrics.clear()
        self.update_metrics_window.clear()
        self.episode_reward_breakdowns.clear()
        self.action_stats.clear()
        self.step_rewards_window.clear()
        self.terminal_rewards_window.clear()
        self.window_steps = 0
        self.window_done_steps = 0
        self.last_log_time = time.time()

    def _log_evaluation(
        self,
        eval_data: Dict[str, Any],
        is_new_best: bool,
        prev_best: float,
        holdout_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Print formatted evaluation results."""
        print()
        print("=" * 75)
        print(f"[SAC] EVALUATION - Step {self.total_steps:,}")
        print("=" * 75)
        print(f"  Eval Return:     {eval_data['avg_return']:>+10.2f}", end="")
        if is_new_best:
            print(f"   *** NEW BEST! ***")
            print(f"  Previous Best:   {prev_best:>+10.2f}")
            print(f"  Improvement:     {eval_data['avg_return'] - prev_best:>+10.2f}")
        else:
            print(f"   (Best: {self.best_eval_return:+.2f} @ step {self.best_eval_step:,})")
        print(f"  Seeds Tested:    {SACConfig.EVAL_SEEDS}")
        print(f"  Per-seed:        [{', '.join(f'{r:+.1f}' for r in eval_data['returns'])}]")
        if holdout_data:
            print(f"  Holdout Return:  {holdout_data['avg_return']:>+10.2f}")
            print(f"  Holdout Seeds:   {SACConfig.HOLDOUT_EVAL_SEEDS}")
            print(f"  Holdout Per-seed:[{', '.join(f'{r:+.1f}' for r in holdout_data['returns'])}]")
        print("-" * 75)
        print(f"  (Eval uses deterministic actions on fixed seeds - the TRUE score)")
        print("=" * 75)
        print()

    def _evaluate_policy(self, seeds: List[int]) -> Dict[str, Any]:
        """Evaluate the current policy on fixed seeds."""
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
            prev_action = None

            while steps < SACConfig.MAX_EPISODE_STEPS and game.player in game.player_list:
                state = state_encoder.encode(game.tracker)
                graph_tensors = ReplayBuffer.collate_graphs([state], self.device)
                action_tensor, _ = self.learner.select_action(graph_tensors, deterministic=True)
                action = action_tensor.squeeze(0).detach().cpu().tolist()
                action, prev_action = self._apply_action_smoothing(action, prev_action)

                game.continuous_control_mode = True
                game.turn_magnitude = float(action[0])
                game.thrust_magnitude = float(action[1])
                game.shoot_requested = float(action[2]) > 0.5

                game.on_update(SACConfig.FRAME_DELAY)

                step_reward = reward_calculator.calculate_step_reward(
                    game.tracker,
                    game.metrics_tracker
                )
                step_reward *= SACConfig.REWARD_SCALE
                total_reward += step_reward
                steps += 1

            total_reward += reward_calculator.calculate_episode_reward(game.metrics_tracker) * SACConfig.REWARD_SCALE
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
            "normalizer": self.learner.normalizer.state_dict(),
        }
        tmp_path = SACConfig.BEST_CHECKPOINT_PATH + ".tmp"
        torch.save(payload, tmp_path)
        os.replace(tmp_path, SACConfig.BEST_CHECKPOINT_PATH)

    def _save_analytics(self) -> None:
        """Save analytics reports."""
        if self.completed_returns:
            self._log_interval()
        self.analytics.generate_markdown_report("training_summary_sac.md")
        self.analytics.save_json("training_data_sac.json")

    def _handle_interrupt(self, signum, frame) -> None:
        """Handle Ctrl+C gracefully."""
        print("\n")
        print("!" * 75)
        print("[SAC] Interrupted! Saving analytics...")
        print("!" * 75)
        self.interrupted = True

    def run(self) -> None:
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._handle_interrupt)

        print()
        print("=" * 75)
        print("[SAC] GNN-SAC TRAINING")
        print("=" * 75)
        print(f"  Device:          {self.device}")
        print(f"  Total Steps:     {SACConfig.TOTAL_STEPS:,}")
        print(f"  Learn Start:     {SACConfig.LEARN_START_STEPS:,} (random actions until then)")
        print(f"  Log Interval:    every {SACConfig.LOG_EVERY_STEPS:,} steps")
        print(f"  Eval Interval:   every {SACConfig.EVAL_EVERY_EPISODES} episodes")
        print("=" * 75)
        print()

        try:
            while self.total_steps < SACConfig.TOTAL_STEPS and not self.interrupted:
                for collector in self.collectors:
                    if self.total_steps >= SACConfig.TOTAL_STEPS or self.interrupted:
                        break
                    self._step_collector(collector)

        finally:
            # Always save analytics on exit (normal or interrupted)
            self._save_analytics()
            print()
            print("=" * 75)
            print(f"[SAC] Training {'INTERRUPTED' if self.interrupted else 'COMPLETE'}")
            print("=" * 75)
            print(f"  Final Step:      {self.total_steps:,}")
            print(f"  Episodes:        {self.episode_count}")
            print(f"  Best Eval:       {self.best_eval_return:+.2f} (at step {self.best_eval_step:,})")
            print("-" * 75)
            print(f"  Reports saved:   training_summary_sac.md")
            print(f"                   training_data_sac.json")
            print("=" * 75)


if __name__ == "__main__":
    SACTrainingScript().run()
