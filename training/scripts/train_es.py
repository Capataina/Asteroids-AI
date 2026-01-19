"""
ES Training Entry Point

Runs parallel Evolution Strategies training for Asteroids AI.
"""

import sys
import os
import math
import time
import arcade
import statistics

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from game import globals
from Asteroids import AsteroidsGame
from interfaces.encoders.HybridEncoder import HybridEncoder
from interfaces.encoders.TemporalStackEncoder import TemporalStackEncoder
from interfaces.ActionInterface import ActionInterface
from ai_agents.neuroevolution.nn_agent import NNAgent
from training.config.evolution_strategies import ESConfig
from training.config.pareto import ParetoConfig
from training.config.rewards import create_reward_calculator
from training.core.episode_runner import EpisodeRunner
from training.core.population_evaluator import evaluate_population_parallel, evaluate_single_agent
from training.core.display_manager import DisplayManager
from training.methods.evolution_strategies.cmaes_driver import CMAESDriver
from training.components.pareto.objectives import compute_objective_matrix
from training.components.pareto.utility import pareto_order
from training.analytics.analytics import TrainingAnalytics


class ESTrainingScript:
    """
    Main script for Evolution Strategies training. Orchestrates components.
    """

    def __init__(self, game):
        self.game = game
        self.max_workers = os.cpu_count()

        # 1. Setup Infrastructure
        base_encoder = HybridEncoder(
            screen_width=globals.SCREEN_WIDTH,
            screen_height=globals.SCREEN_HEIGHT,
            num_rays=16,
            num_fovea_asteroids=3
        )
        if ESConfig.USE_TEMPORAL_STACK:
            self.state_encoder = TemporalStackEncoder(
                base_encoder=base_encoder,
                stack_size=ESConfig.TEMPORAL_STACK_SIZE,
                include_deltas=ESConfig.TEMPORAL_INCLUDE_DELTAS
            )
        else:
            self.state_encoder = base_encoder
        self.action_interface = ActionInterface(action_space_type="boolean")
        self.reward_calculator = create_reward_calculator(
            max_steps=ESConfig.MAX_STEPS,
            frame_delay=ESConfig.FRAME_DELAY
        )

        self.episode_runner = EpisodeRunner(
            game=game,
            state_encoder=self.state_encoder,
            action_interface=self.action_interface,
            reward_calculator=self.reward_calculator
        )

        # 2. Setup Driver (ES Logic)
        input_size = self.state_encoder.get_state_size()
        hidden_size = ESConfig.HIDDEN_LAYER_SIZE
        output_size = 3
        param_size = NNAgent.get_parameter_count(input_size, hidden_size, output_size)

        print(f"ES Parameter Size: {param_size}")

        self.pareto_config = ParetoConfig(
            ENABLED=True,
            OBJECTIVES=["hits", "time_alive", "softmin_ttc"],
            ACCURACY_MIN_SHOTS=5,
            FRAME_DELAY=ESConfig.FRAME_DELAY
        )
        self.driver = CMAESDriver(param_size=param_size, pareto_config=self.pareto_config)

        # 3. Setup Analytics
        self.analytics = TrainingAnalytics()
        self.analytics.set_config({
            'method': 'Evolution Strategies',
            'optimizer': ESConfig.OPTIMIZER,
            'population_size': ESConfig.POPULATION_SIZE,
            'num_generations': ESConfig.NUM_GENERATIONS,
            'cmaes_sigma': ESConfig.CMAES_SIGMA,
            'cmaes_mu': ESConfig.CMAES_MU if ESConfig.CMAES_MU else 'auto',
            'cmaes_cov_min': ESConfig.CMAES_COV_MIN,
            'cmaes_cov_target_rate': ESConfig.CMAES_COV_TARGET_RATE,
            'cmaes_cov_max_scale': ESConfig.CMAES_COV_MAX_SCALE,
            'sigma_min': ESConfig.SIGMA_MIN,
            'use_antithetic': ESConfig.USE_ANTITHETIC,
            'seeds_per_agent': ESConfig.SEEDS_PER_AGENT,
            'use_common_seeds': ESConfig.USE_COMMON_SEEDS,
            'noise_handling_enabled': ESConfig.NOISE_HANDLING_ENABLED,
            'noise_handling_top_k': ESConfig.NOISE_HANDLING_TOP_K,
            'noise_handling_extra_seeds': ESConfig.NOISE_HANDLING_EXTRA_SEEDS,
            'noise_handling_seed_offset': ESConfig.NOISE_HANDLING_SEED_OFFSET,
            'restart_enabled': ESConfig.RESTART_ENABLED,
            'restart_patience': ESConfig.RESTART_PATIENCE,
            'restart_min_generations': ESConfig.RESTART_MIN_GENERATIONS,
            'restart_cooldown': ESConfig.RESTART_COOLDOWN,
            'restart_sigma_multiplier': ESConfig.RESTART_SIGMA_MULTIPLIER,
            'restart_use_best_candidate': ESConfig.RESTART_USE_BEST_CANDIDATE,
            'max_workers': self.max_workers,
            'temporal_stack_enabled': ESConfig.USE_TEMPORAL_STACK,
            'temporal_stack_size': ESConfig.TEMPORAL_STACK_SIZE,
            'temporal_stack_include_deltas': ESConfig.TEMPORAL_INCLUDE_DELTAS,
            **self.pareto_config.to_dict(),
        })

        # 4. Setup Display
        self.display_manager = DisplayManager(game, self.episode_runner, self.analytics)

        # State
        self.current_generation = 0
        self.best_fitness = float('-inf')
        self.best_candidate = None  # Store actual best candidate weights (not the mean)
        self.best_generation = 0    # Track which generation produced the best
        self.best_pareto_score = float('-inf')
        self.objective_maxima = None
        self.fitness_stagnation = 0
        self.restart_pending = False
        self.restart_cooldown = 0
        self.phase = "sampling"
        self.current_candidates = []
        self.current_fitnesses = []
        self.current_per_agent_metrics = []
        self.current_objective_vectors = []
        self.current_objective_directions = []

        # Hook draw
        original_draw = self.game.on_draw

        def new_draw():
            original_draw()
            self.display_manager.draw()

        self.game.on_draw = new_draw

        print("ES Training Script Initialized")
        print(f"  Population Size: {ESConfig.POPULATION_SIZE}")
        print(f"  Optimizer: CMA-ES (diagonal)")
        print(f"  CMA-ES Sigma: {ESConfig.CMAES_SIGMA} (min={ESConfig.SIGMA_MIN})")
        print(f"  CMA-ES Mu: {ESConfig.CMAES_MU if ESConfig.CMAES_MU else 'auto'}")
        print(f"  Pareto Objectives: {', '.join(self.pareto_config.OBJECTIVES)}")
        if ESConfig.USE_TEMPORAL_STACK:
            print(
                f"  Temporal Stack: {ESConfig.TEMPORAL_STACK_SIZE} frames "
                f"(deltas={ESConfig.TEMPORAL_INCLUDE_DELTAS})"
            )
        print(f"  Antithetic Sampling: {ESConfig.USE_ANTITHETIC}")
        print(f"  Common Seeds (CRN): {ESConfig.USE_COMMON_SEEDS}")
        print(
            f"  Noise Handling: {ESConfig.NOISE_HANDLING_ENABLED} "
            f"(top_k={ESConfig.NOISE_HANDLING_TOP_K}, extra_seeds={ESConfig.NOISE_HANDLING_EXTRA_SEEDS})"
        )
        print(
            f"  Restarts: {ESConfig.RESTART_ENABLED} "
            f"(patience={ESConfig.RESTART_PATIENCE}, cooldown={ESConfig.RESTART_COOLDOWN})"
        )

    def _blend_metrics(self, base_metrics, extra_results, base_weight):
        total_weight = base_weight + len(extra_results)
        if total_weight <= 0:
            return base_metrics
        combined = dict(base_metrics)
        for key, value in base_metrics.items():
            if isinstance(value, (int, float)):
                extra_sum = sum(r.get(key, 0.0) for r in extra_results)
                combined[key] = (value * base_weight + extra_sum) / total_weight
        base_hits = float(base_metrics.get("hits", 0.0)) * base_weight
        base_shots = float(base_metrics.get("shots_fired", 0.0)) * base_weight
        extra_hits = sum(r.get("hits", 0.0) for r in extra_results)
        extra_shots = sum(r.get("shots_fired", 0.0) for r in extra_results)
        total_shots = base_shots + extra_shots
        if total_shots > 0:
            combined["accuracy"] = (base_hits + extra_hits) / total_shots
        return combined

    def _apply_noise_handling(
        self,
        generation_seed,
        fitnesses,
        per_agent_metrics,
        objective_vectors,
        objective_directions
    ):
        if not ESConfig.NOISE_HANDLING_ENABLED:
            order, _, _ = pareto_order(objective_vectors, objective_directions)
            return fitnesses, per_agent_metrics, objective_vectors, objective_directions, order
        top_k = ESConfig.NOISE_HANDLING_TOP_K
        extra_seeds = ESConfig.NOISE_HANDLING_EXTRA_SEEDS
        if top_k <= 0 or extra_seeds <= 0:
            order, _, _ = pareto_order(objective_vectors, objective_directions)
            return fitnesses, per_agent_metrics, objective_vectors, objective_directions, order

        order, _, _ = pareto_order(objective_vectors, objective_directions)
        top_indices = order[:min(top_k, len(order))]
        if generation_seed is None:
            generation_seed = 0
        seed_base = generation_seed + ESConfig.NOISE_HANDLING_SEED_OFFSET

        for idx in top_indices:
            extra_results = []
            for seed_offset in range(extra_seeds):
                seed = seed_base + idx * extra_seeds + seed_offset
                extra_results.append(
                    evaluate_single_agent(
                        self.current_candidates[idx],
                        self.state_encoder,
                        self.action_interface,
                        max_steps=ESConfig.MAX_STEPS,
                        frame_delay=ESConfig.FRAME_DELAY,
                        random_seed=seed,
                        hidden_size=ESConfig.HIDDEN_LAYER_SIZE
                    )
                )
            per_agent_metrics[idx] = self._blend_metrics(
                per_agent_metrics[idx],
                extra_results,
                ESConfig.SEEDS_PER_AGENT
            )
            fitnesses[idx] = per_agent_metrics[idx].get("fitness", fitnesses[idx])

        objective_vectors, objective_directions, _ = compute_objective_matrix(
            per_agent_metrics,
            self.pareto_config
        )
        order, _, _ = pareto_order(objective_vectors, objective_directions)
        return fitnesses, per_agent_metrics, objective_vectors, objective_directions, order

    def update(self, delta_time):
        try:
            if self.current_generation >= ESConfig.NUM_GENERATIONS:
                if not self.display_manager.showing_best_agent:
                    print("Training Complete.")
                    print(f"All-time best fitness: {self.best_fitness:.2f} (Generation {self.best_generation})")
                    self._save()
                    if self.best_candidate is not None:
                        agent = NNAgent(self.best_candidate, self.state_encoder, self.action_interface)
                        self.display_manager.start_display(agent, self.best_fitness, self.best_fitness)
                    return

            # Phase: Displaying
            if self.display_manager.showing_best_agent:
                status = self.display_manager.update(delta_time)
                if status == "done":
                    if self.current_generation >= ESConfig.NUM_GENERATIONS:
                        arcade.close_window()
                    else:
                        self.phase = "updating"
                return

            # Phase: Sampling
            if self.phase == "sampling":
                print(f"\nGeneration {self.current_generation + 1}: Sampling...")
                self.display_manager.update_info_text_training(
                    self.current_generation + 1,
                    ESConfig.NUM_GENERATIONS,
                    self.max_workers,
                    "Sampling perturbations..."
                )

                # Sample candidates from the distribution
                self.current_candidates, _ = self.driver.sample_population()
                self.phase = "evaluating"
                return

            # Phase: Evaluating
            if self.phase == "evaluating":
                print(f"Generation {self.current_generation + 1}: Evaluating {len(self.current_candidates)} candidates...")
                self.display_manager.update_info_text_training(
                    self.current_generation + 1,
                    ESConfig.NUM_GENERATIONS,
                    self.max_workers,
                    "Evaluating..."
                )

                eval_start = time.time()
                fitnesses, generation_seed, gen_metrics, per_agent_metrics = evaluate_population_parallel(
                    self.current_candidates,
                    self.state_encoder,
                    self.action_interface,
                    max_steps=ESConfig.MAX_STEPS,
                    max_workers=self.max_workers,
                    seeds_per_agent=ESConfig.SEEDS_PER_AGENT,
                    use_common_seeds=ESConfig.USE_COMMON_SEEDS
                )

                # Pareto objectives for this generation
                objective_vectors, objective_directions, _ = compute_objective_matrix(
                    per_agent_metrics,
                    self.pareto_config
                )
                fitnesses, per_agent_metrics, objective_vectors, objective_directions, order = self._apply_noise_handling(
                    generation_seed,
                    fitnesses,
                    per_agent_metrics,
                    objective_vectors,
                    objective_directions
                )

                self.current_fitnesses = fitnesses
                self.current_per_agent_metrics = per_agent_metrics
                self.current_objective_vectors = objective_vectors
                self.current_objective_directions = objective_directions
                best_idx = order[0] if order else 0
                current_best_fit = fitnesses[best_idx]
                current_best_candidate = self.current_candidates[best_idx]
                prev_best = self.best_fitness
                gen_best_fit = max(fitnesses) if fitnesses else float('-inf')
                if gen_best_fit > prev_best:
                    self.best_fitness = gen_best_fit
                    self.best_generation = self.current_generation + 1
                    self.fitness_stagnation = 0
                else:
                    self.fitness_stagnation += 1

                if ESConfig.RESTART_ENABLED:
                    if self.restart_cooldown > 0:
                        self.restart_cooldown -= 1
                    if (
                        not self.restart_pending
                        and self.restart_cooldown <= 0
                        and (self.current_generation + 1) >= ESConfig.RESTART_MIN_GENERATIONS
                        and self.fitness_stagnation >= ESConfig.RESTART_PATIENCE
                    ):
                        self.restart_pending = True

                # Track normalized Pareto score across generations for "best of run"
                if self.objective_maxima is None:
                    self.objective_maxima = [0.0 for _ in objective_vectors[0]]
                for vector in objective_vectors:
                    for i, value in enumerate(vector):
                        if value > self.objective_maxima[i]:
                            self.objective_maxima[i] = value

                def _pareto_score(vec):
                    score = 0.0
                    for i, value in enumerate(vec):
                        denom = max(self.objective_maxima[i], 1e-9)
                        score += value / denom
                    return score

                if objective_vectors:
                    best_score = _pareto_score(objective_vectors[best_idx])
                    if best_score > self.best_pareto_score:
                        self.best_pareto_score = best_score
                        self.best_candidate = current_best_candidate.copy()

                # Record Analytics
                timing_stats = {
                    'evaluation_duration': time.time() - eval_start,
                    'update_duration': self.driver.last_update_duration
                }

                # Merge ES-specific stats
                es_stats = self.driver.last_update_stats.copy()

                self.analytics.record_generation(
                    generation=self.current_generation + 1,
                    fitness_scores=fitnesses,
                    behavioral_metrics=gen_metrics,
                    timing_stats=timing_stats,
                    operator_stats=es_stats
                )
                self.analytics.record_distributions(
                    generation=self.current_generation + 1,
                    fitness_values=fitnesses,
                    per_agent_metrics=per_agent_metrics
                )

                # Calculate stats for display
                avg_fit = sum(fitnesses) / len(fitnesses)
                min_fit = min(fitnesses)
                std_fit = statistics.stdev(fitnesses) if len(fitnesses) > 1 else 0.0

                print("\n" + "=" * 60)
                print(f" GENERATION {self.current_generation + 1} SUMMARY (ES)")
                print("=" * 60)
                print(f" FITNESS")
                print(f"  Best:  {current_best_fit:8.2f}  |  Avg: {avg_fit:8.2f}")
                print(f"  Min:   {min_fit:8.2f}  |  Std: {std_fit:8.2f}")
                print(f"  All-time Best: {self.best_fitness:.2f} (Gen {self.best_generation})")
                print("-" * 60)
                print(f" ES PARAMETERS")
                sigma = es_stats.get('sigma', self.driver.sigma)
                cov_mean = es_stats.get('cov_diag_mean', 0.0)
                cov_min = es_stats.get('cov_diag_min', 0.0)
                cov_max = es_stats.get('cov_diag_max', 0.0)
                pareto_front0 = es_stats.get('pareto_front0_size', 0)
                print(f"  Sigma: {sigma:.4f}")
                print(f"  Cov Diag: mean={cov_mean:.4f} min={cov_min:.4f} max={cov_max:.4f}")
                if pareto_front0:
                    print(f"  Pareto Front0 Size: {pareto_front0}")
                print("-" * 60)
                print(f" BEHAVIOR (Avg)")
                print(f"  Kills:    {gen_metrics.get('avg_kills', 0):6.1f}  |  Accuracy: {gen_metrics.get('avg_accuracy', 0) * 100:5.1f}%")
                print(f"  Survival: {gen_metrics.get('avg_steps_survived', 0):6.0f}  |  Shots:    {gen_metrics.get('avg_shots_fired', 0):5.1f}")
                print("=" * 60 + "\n")

                # Start Display with best candidate
                display_agent = NNAgent(current_best_candidate, self.state_encoder, self.action_interface)
                self.display_manager.start_display(display_agent, current_best_fit, self.best_fitness)
                self.phase = "displaying"
                return

            # Phase: Updating
            if self.phase == "updating":
                print(f"Updating mean for generation {self.current_generation + 1}...")

                if self.restart_pending:
                    print("Restarting CMA-ES due to stagnation...")
                    restart_sigma = ESConfig.CMAES_SIGMA if ESConfig.CMAES_SIGMA is not None else ESConfig.SIGMA
                    restart_sigma = float(restart_sigma) * ESConfig.RESTART_SIGMA_MULTIPLIER
                    restart_mean = None
                    if ESConfig.RESTART_USE_BEST_CANDIDATE and self.best_candidate is not None:
                        restart_mean = self.best_candidate
                    self.driver.restart(mean=restart_mean, sigma=restart_sigma, reason="stagnation")
                    self.restart_pending = False
                    self.restart_cooldown = ESConfig.RESTART_COOLDOWN
                    self.fitness_stagnation = 0
                    self.current_generation += 1
                    self.phase = "sampling"
                    return

                # Update the mean using fitness-weighted gradient
                self.driver.update(
                    self.current_fitnesses,
                    self.current_per_agent_metrics,
                    objective_vectors=self.current_objective_vectors,
                    objective_directions=self.current_objective_directions
                )

                self.current_generation += 1
                self.phase = "sampling"
                return

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            self._save()
            arcade.close_window()

    def _save(self):
        self.analytics.generate_markdown_report("training_summary_es.md")
        self.analytics.save_json("training_data_es.json")
        print("ES training results saved.")


def main():
    window = AsteroidsGame(globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT, "Asteroids AI - Evolution Strategies Training")
    window.setup()
    trainer = ESTrainingScript(window)
    arcade.schedule(trainer.update, ESConfig.FRAME_DELAY)

    try:
        arcade.run()
    finally:
        print("\nApplication exiting, saving training results...")
        trainer._save()


if __name__ == "__main__":
    main()
