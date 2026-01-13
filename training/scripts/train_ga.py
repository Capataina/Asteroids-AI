"""
GA Training Entry Point

Runs parallel Genetic Algorithm training for Asteroids AI.
"""

import sys
import os
import math
import time
import arcade

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from game import globals
from Asteroids import AsteroidsGame
from interfaces.encoders.VectorEncoder import VectorEncoder
from interfaces.ActionInterface import ActionInterface
from ai_agents.neuroevolution.nn_agent import NNAgent
from training.config.genetic_algorithm import GAConfig
from training.config.rewards import create_reward_calculator
from training.core.episode_runner import EpisodeRunner
from training.core.population_evaluator import evaluate_population_parallel
from training.core.display_manager import DisplayManager
from training.methods.genetic_algorithm.driver import GADriver
from training.analytics.analytics import TrainingAnalytics


class GATrainingScript:
    """
    Main script for GA training. Orchestrates components.
    """
    def __init__(self, game):
        self.game = game
        self.max_workers = os.cpu_count()
        
        # 1. Setup Infrastructure
        self.state_encoder = VectorEncoder(
            screen_width=globals.SCREEN_WIDTH,
            screen_height=globals.SCREEN_HEIGHT,
            num_nearest_asteroids=GAConfig.NUM_NEAREST_ASTEROIDS,
            include_bullets=False,
            include_global=False
        )
        self.action_interface = ActionInterface(action_space_type="boolean")
        self.reward_calculator = create_reward_calculator()
        
        self.episode_runner = EpisodeRunner(
            game=game,
            state_encoder=self.state_encoder,
            action_interface=self.action_interface,
            reward_calculator=self.reward_calculator
        )
        
        # 2. Setup Driver (GA Logic)
        input_size = self.state_encoder.get_state_size()
        hidden_size = GAConfig.HIDDEN_LAYER_SIZE
        output_size = 4
        param_size = NNAgent.get_parameter_count(input_size, hidden_size, output_size)
        
        self.driver = GADriver(param_size=param_size)
        
        # 3. Setup Analytics
        self.analytics = TrainingAnalytics()
        self.analytics.set_config({
            'population_size': GAConfig.POPULATION_SIZE,
            'num_generations': GAConfig.NUM_GENERATIONS,
            'mutation_probability': GAConfig.MUTATION_PROBABILITY,
            'max_workers': self.max_workers,
        })

        # 4. Setup Display
        self.display_manager = DisplayManager(game, self.episode_runner, self.analytics)
        
        # State
        self.current_generation = 0
        self.best_fitness = float('-inf')
        self.best_individual = None
        self.phase = "evaluating"
        self.current_fitnesses = []
        
        # Hook draw
        original_draw = self.game.on_draw
        def new_draw():
            original_draw()
            self.display_manager.draw()
        self.game.on_draw = new_draw
        
        print("GA Training Script Initialized.")

    def update(self, delta_time):
        try:
            if self.current_generation >= GAConfig.NUM_GENERATIONS:
                if not self.display_manager.showing_best_agent:
                    print("Training Complete.")
                    self._save()
                    if self.best_individual:
                        agent = NNAgent(self.best_individual, self.state_encoder, self.action_interface)
                        self.display_manager.start_display(agent, self.best_fitness, self.best_fitness)
                    return
            
            # Phase: Displaying
            if self.display_manager.showing_best_agent:
                status = self.display_manager.update(delta_time)
                if status == "done":
                    if self.current_generation >= GAConfig.NUM_GENERATIONS:
                        arcade.close_window()
                    else:
                        self.phase = "evolving"
                return

            # Phase: Evaluating
            if self.phase == "evaluating":
                print(f"Generation {self.current_generation + 1}: Evaluating...")
                self.display_manager.update_info_text_training(self.current_generation + 1, GAConfig.NUM_GENERATIONS, self.max_workers, "Evaluating...")
                
                eval_start = time.time()
                fitnesses, _, gen_metrics, per_agent_metrics = evaluate_population_parallel(
                    self.driver.population,
                    self.state_encoder,
                    self.action_interface,
                    max_steps=GAConfig.MAX_STEPS,
                    max_workers=self.max_workers,
                    seeds_per_agent=GAConfig.SEEDS_PER_AGENT
                )
                self.current_fitnesses = fitnesses
                
                # Update best
                best_idx = fitnesses.index(max(fitnesses))
                current_best_fit = fitnesses[best_idx]
                current_best_ind = self.driver.population[best_idx].copy()
                
                if current_best_fit > self.best_fitness:
                    self.best_fitness = current_best_fit
                    self.best_individual = current_best_ind
                
                # Record Analytics
                timing_stats = {
                    'evaluation_duration': time.time() - eval_start,
                    'evolution_duration': self.driver.last_evolution_duration
                }
                self.analytics.record_generation(
                    generation=self.current_generation + 1,
                    fitness_scores=fitnesses,
                    behavioral_metrics=gen_metrics,
                    timing_stats=timing_stats,
                    operator_stats=self.driver.last_evolution_stats
                )
                self.analytics.record_distributions(
                    generation=self.current_generation + 1,
                    fitness_values=fitnesses,
                    per_agent_metrics=per_agent_metrics
                )
                
                print(f"Gen {self.current_generation + 1} Best: {current_best_fit:.2f}")

                # Start Display
                display_agent = NNAgent(current_best_ind, self.state_encoder, self.action_interface)
                self.display_manager.start_display(display_agent, current_best_fit, self.best_fitness)
                self.phase = "displaying"
                return

            # Phase: Evolving
            if self.phase == "evolving":
                print(f"Evolving generation {self.current_generation + 1}...")
                stagnation = 0
                if self.analytics.generations_data:
                    stagnation = self.analytics.generations_data[-1].get('generations_since_improvement', 0)
                
                self.driver.evolve(self.current_fitnesses, self.best_individual, stagnation)
                self.current_generation += 1
                self.phase = "evaluating"
                return

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            self._save()
            arcade.close_window()

    def _save(self):
        self.analytics.generate_markdown_report("training_summary.md")
        self.analytics.save_json("training_data.json")

def main():
    window = AsteroidsGame(globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT, globals.SCREEN_TITLE)
    window.setup()
    trainer = GATrainingScript(window)
    arcade.schedule(trainer.update, GAConfig.FRAME_DELAY)
    
    try:
        arcade.run()
    finally:
        print("\nApplication exiting, saving training results...")
        trainer._save()

if __name__ == "__main__":
    main()
