"""
ES Training Entry Point

Runs parallel Evolution Strategies training for Asteroids AI using TensorFlow.
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
from interfaces.ActionInterface import ActionInterface
from ai_agents.neuroevolution.nn_agent import NNAgent
from training.config.evolution_strategies import ESConfig
from training.config.rewards import create_reward_calculator
from training.core.episode_runner import EpisodeRunner
from training.core.population_evaluator import evaluate_population_parallel
from training.core.display_manager import DisplayManager
from training.methods.evolution_strategies.driver import ESDriver
from training.analytics.analytics import TrainingAnalytics


class ESTrainingScript:
    """
    Main script for Evolution Strategies training. Orchestrates components.
    """

    def __init__(self, game):
        self.game = game
        self.max_workers = os.cpu_count()

        # 1. Setup Infrastructure
        self.state_encoder = HybridEncoder(
            screen_width=globals.SCREEN_WIDTH,
            screen_height=globals.SCREEN_HEIGHT,
            num_rays=16,
            num_fovea_asteroids=3
        )
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

        self.driver = ESDriver(param_size=param_size)

        # 3. Setup Analytics
        self.analytics = TrainingAnalytics()
        self.analytics.set_config({
            'method': 'Evolution Strategies',
            'population_size': ESConfig.POPULATION_SIZE,
            'num_generations': ESConfig.NUM_GENERATIONS,
            'sigma': ESConfig.SIGMA,
            'sigma_decay': ESConfig.SIGMA_DECAY,
            'sigma_min': ESConfig.SIGMA_MIN,
            'adaptive_sigma': ESConfig.ADAPTIVE_SIGMA_ENABLED,
            'learning_rate': ESConfig.LEARNING_RATE,
            'use_antithetic': ESConfig.USE_ANTITHETIC,
            'use_rank_transformation': ESConfig.USE_RANK_TRANSFORMATION,
            'weight_decay': ESConfig.WEIGHT_DECAY,
            'seeds_per_agent': ESConfig.SEEDS_PER_AGENT,
            'use_common_seeds': ESConfig.USE_COMMON_SEEDS,
            'enable_novelty': ESConfig.ENABLE_NOVELTY,
            'enable_diversity': ESConfig.ENABLE_DIVERSITY,
            'novelty_weight': ESConfig.NOVELTY_WEIGHT,
            'diversity_weight': ESConfig.DIVERSITY_WEIGHT,
            'use_adamw': ESConfig.USE_ADAMW,
            'adamw_beta1': ESConfig.ADAMW_BETA1,
            'adamw_beta2': ESConfig.ADAMW_BETA2,
            'enable_elitism': ESConfig.ENABLE_ELITISM,
            'elite_pull_enabled': ESConfig.ELITE_PULL_ENABLED,
            'max_workers': self.max_workers,
        })

        # 4. Setup Display
        self.display_manager = DisplayManager(game, self.episode_runner, self.analytics)

        # State
        self.current_generation = 0
        self.best_fitness = float('-inf')
        self.best_candidate = None  # Store actual best candidate weights (not the mean)
        self.best_generation = 0    # Track which generation produced the best
        self.phase = "sampling"
        self.current_candidates = []
        self.current_fitnesses = []
        self.current_per_agent_metrics = []

        # Hook draw
        original_draw = self.game.on_draw

        def new_draw():
            original_draw()
            self.display_manager.draw()

        self.game.on_draw = new_draw

        print("ES Training Script Initialized")
        print(f"  Population Size: {ESConfig.POPULATION_SIZE}")
        print(f"  Sigma: {ESConfig.SIGMA} (decay={ESConfig.SIGMA_DECAY}, min={ESConfig.SIGMA_MIN})")
        print(f"  Adaptive Sigma: {ESConfig.ADAPTIVE_SIGMA_ENABLED} (patience={ESConfig.ADAPTIVE_SIGMA_PATIENCE})")
        print(f"  Learning Rate: {ESConfig.LEARNING_RATE}")
        print(f"  Optimizer: {'AdamW' if ESConfig.USE_ADAMW else 'SGD'} (β1={ESConfig.ADAMW_BETA1}, β2={ESConfig.ADAMW_BETA2})")
        print(f"  Elitism: {ESConfig.ENABLE_ELITISM} (pull={ESConfig.ELITE_PULL_ENABLED}, strength={ESConfig.ELITE_PULL_STRENGTH})")
        print(f"  Antithetic Sampling: {ESConfig.USE_ANTITHETIC}")
        print(f"  Rank Transformation: {ESConfig.USE_RANK_TRANSFORMATION}")
        print(f"  Common Seeds (CRN): {ESConfig.USE_COMMON_SEEDS}")
        print(f"  Novelty: {ESConfig.ENABLE_NOVELTY} (weight={ESConfig.NOVELTY_WEIGHT})")
        print(f"  Diversity: {ESConfig.ENABLE_DIVERSITY} (weight={ESConfig.DIVERSITY_WEIGHT})")

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
                fitnesses, _, gen_metrics, per_agent_metrics = evaluate_population_parallel(
                    self.current_candidates,
                    self.state_encoder,
                    self.action_interface,
                    max_steps=ESConfig.MAX_STEPS,
                    max_workers=self.max_workers,
                    seeds_per_agent=ESConfig.SEEDS_PER_AGENT,
                    use_common_seeds=ESConfig.USE_COMMON_SEEDS
                )
                self.current_fitnesses = fitnesses
                self.current_per_agent_metrics = per_agent_metrics

                # Find best candidate this generation
                best_idx = fitnesses.index(max(fitnesses))
                current_best_fit = fitnesses[best_idx]
                current_best_candidate = self.current_candidates[best_idx]

                # Update all-time best - store actual candidate weights, not the mean
                if current_best_fit > self.best_fitness:
                    self.best_fitness = current_best_fit
                    self.best_candidate = current_best_candidate.copy()  # Store actual best candidate
                    self.best_generation = self.current_generation + 1

                # Record Analytics
                timing_stats = {
                    'evaluation_duration': time.time() - eval_start,
                    'update_duration': self.driver.last_update_duration
                }

                # Merge ES-specific stats
                es_stats = self.driver.last_update_stats.copy()
                es_stats.update({
                    'sigma': self.driver.sigma,
                })

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
                print(f"  Sigma: {self.driver.sigma:.4f}  |  LR: {ESConfig.LEARNING_RATE:.4f}")
                if 'gradient_norm' in es_stats:
                    print(f"  Grad Norm: {es_stats['gradient_norm']:.4f}  |  Mean Norm: {es_stats.get('mean_param_norm', 0):.2f}")
                stagnation = self.driver.generations_since_improvement
                adaptive_triggered = es_stats.get('adaptive_sigma_triggered', False)
                elite_pull = es_stats.get('elite_pull_applied', False)
                print(f"  Stagnation: {stagnation} gens  |  Adaptive σ: {'YES' if adaptive_triggered else 'no'}")
                if ESConfig.ENABLE_ELITISM:
                    print(f"  Elite Injected: {es_stats.get('elite_injected', False)}  |  Elite Pull: {'YES' if elite_pull else 'no'}")
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

                # Update the mean using fitness-weighted gradient
                self.driver.update(self.current_fitnesses, self.current_per_agent_metrics)

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
