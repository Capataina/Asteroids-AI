"""
Parallel GA Training Driver

Runs GA training with parallel evaluation for massive speedup.
All agents are evaluated simultaneously in headless game instances.
The best agent is displayed visually in the game window.
"""

import sys
import os
import math
import random
from typing import Optional, List

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import arcade
from Asteroids import AsteroidsGame, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from interfaces.encoders.VectorEncoder import VectorEncoder
from interfaces.ActionInterface import ActionInterface
from interfaces.RewardCalculator import ComposableRewardCalculator
from interfaces.rewards.SurvivalBonus import SurvivalBonus
from interfaces.rewards.KillAsteroid import KillAsteroid
from interfaces.rewards.ChunkBonus import ChunkBonus
from interfaces.rewards.NearMiss import NearMiss
from interfaces.rewards.AccuracyBonus import AccuracyBonus
from interfaces.rewards.KPMBonus import KPMBonus
from interfaces.rewards.ShootingPenalty import ShootingPenalty
from ai_agents.neuroevolution.genetic_algorithm.ga_trainer import GATrainer
from ai_agents.neuroevolution.genetic_algorithm.nn_ga_agent import NeuralNetworkGAAgent
from training.parallel_evaluator import evaluate_population_parallel
from training.analytics import TrainingAnalytics


class ParallelGATrainingDriver:
    """
    Handles GA training with parallel evaluation and visual feedback.
    """
    
    def __init__(
        self,
        game: AsteroidsGame,
        ga_trainer: GATrainer,
        frame_delay: float = 1.0 / 60.0,
        max_workers: int = None
    ):
        """
        Initialize parallel GA training driver.
        
        Args:
            game: Visual AsteroidsGame instance
            ga_trainer: GATrainer instance
            frame_delay: Time between visual updates
            max_workers: Number of parallel workers (None = auto)
        """
        self.game = game
        self.ga_trainer = ga_trainer
        self.frame_delay = frame_delay
        self.max_workers = max_workers or os.cpu_count()
        
        # Disable game's internal systems
        self.game.update_internal_rewards = False
        self.game.auto_reset_on_collision = False
        
        # Training state
        self.current_generation = 0
        self.population = []
        self.fitnesses = []
        self.best_agent: Optional[NeuralNetworkGAAgent] = None  # All-time best (for saving)
        self.best_fitness = float('-inf')
        self.best_individual = None
        self.display_agent: Optional[NeuralNetworkGAAgent] = None  # Current generation's best (for display)
        self.display_fitness = 0.0

        # Neural network configuration
        self.hidden_size = 24  # Hidden layer neurons

        # Display state
        self.showing_best_agent = False
        self.best_agent_steps = 0
        self.best_agent_max_steps = 1500

        # Phase tracking
        self.phase = "evaluating"  # "evaluating", "displaying_best", "evolving"
        
        # Analytics tracking
        self.analytics = TrainingAnalytics()
        self.analytics.set_config({
            'population_size': ga_trainer.population_size,
            'num_generations': ga_trainer.num_generations,
            'mutation_probability': ga_trainer.mutation_probability,
            'mutation_gaussian_sigma': ga_trainer.mutation_gaussian_sigma,
            'crossover_probability': ga_trainer.crossover_probability,
            'max_workers': self.max_workers,
            'frame_delay': frame_delay,
        })
        
        # Initialize population
        self._initialize_population()
        
        # Register update function
        arcade.schedule(self.update, frame_delay)
        
        # Create info text
        self.info_text = arcade.Text(
            text="Starting parallel GA training...",
            x=10,
            y=SCREEN_HEIGHT - 60,
            color=arcade.color.YELLOW,
            font_size=14
        )
        
        # Hook into draw
        original_draw = self.game.on_draw
        
        def new_draw():
            original_draw()
            # Sync training reward to display
            self.game.reward_calculator.score = self.ga_trainer.episode_runner.reward_calculator.score
            display_score = max(0, math.floor(self.game.reward_calculator.score))
            self.game.score_text.text = f"Score: {display_score}"
            self.info_text.draw()
        
        self.game.on_draw = new_draw
    
    def _initialize_population(self):
        """Initialize random population with neural network parameter vectors."""
        state_size = self.ga_trainer.state_encoder.get_state_size()
        action_size = 4

        # Neural network parameter count: W1 + b1 + W2 + b2
        # W1: state_size x hidden_size, b1: hidden_size
        # W2: hidden_size x action_size, b2: action_size
        param_size = NeuralNetworkGAAgent.get_parameter_count(
            input_size=state_size,
            hidden_size=self.hidden_size,
            output_size=action_size
        )

        print(f"Neural network architecture: {state_size} -> {self.hidden_size} -> {action_size}")
        print(f"Total parameters per agent: {param_size}")

        self.population = [
            [random.uniform(
                self.ga_trainer.mutation_uniform_low,
                self.ga_trainer.mutation_uniform_high
            ) for _ in range(param_size)]
            for _ in range(self.ga_trainer.population_size)
        ]
    
    def update(self, delta_time):
        """Called each frame to update training."""
        try:
            # Check if training complete
            if self.current_generation >= self.ga_trainer.num_generations:
                if not self.showing_best_agent:
                    print(f"\n=== Training Complete! ===")
                    print(f"Final Best Fitness: {self.best_fitness:.2f}")
                    self._save_training_results()
                    print(f"Now displaying ALL-TIME best agent...")
                    # For the final demo, show the all-time best agent
                    if self.best_individual is not None:
                        self.display_agent = NeuralNetworkGAAgent(
                            self.best_individual,
                            self.ga_trainer.state_encoder,
                            self.ga_trainer.action_interface,
                            hidden_size=self.hidden_size
                        )
                        self.display_fitness = self.best_fitness
                    self._start_best_agent_display()
                    return
                elif self.best_agent_steps >= 5000 or self.game.player not in self.game.player_list:
                    arcade.close_window()
                    return
                else:
                    self._update_best_agent_display(delta_time)
                    return
            
            # Phase: Displaying best agent
            if self.showing_best_agent:
                self._update_best_agent_display(delta_time)
                
                # Check if done displaying (max steps reached OR player died)
                if self.best_agent_steps >= self.best_agent_max_steps or self.game.player not in self.game.player_list:
                    self.showing_best_agent = False
                    self.game.manual_spawning = False  # Restore normal spawning
                    self.game.external_control = False  # Allow arcade to control again
                    self.phase = "evolving"
                return
            
            # Phase: Evaluating (happens once per generation, in parallel)
            if self.phase == "evaluating":
                print(f"\nGeneration {self.current_generation + 1}: Evaluating {len(self.population)} agents in parallel...")
                self._update_info_text("Evaluating population in parallel...")
                
                # PARALLEL EVALUATION - ALL AGENTS AT ONCE
                # All agents use the SAME random seed for fair comparison within a generation
                # (seed is used internally but not stored - display uses fresh game)
                self.fitnesses, _, gen_metrics = evaluate_population_parallel(
                    self.population,
                    self.ga_trainer.state_encoder,
                    self.ga_trainer.action_interface,
                    max_steps=1500,  # Increased to give agents more time to learn
                    max_workers=self.max_workers
                )

                # Find best in current generation
                best_idx = self.fitnesses.index(max(self.fitnesses))
                current_gen_best_fitness = self.fitnesses[best_idx]
                current_gen_best_individual = self.population[best_idx].copy()

                # Update all-time best if this generation's best beats it
                if current_gen_best_fitness > self.best_fitness:
                    self.best_fitness = current_gen_best_fitness
                    self.best_individual = current_gen_best_individual

                # Always display the CURRENT generation's best agent (not all-time best)
                # This lets users see what the current population is doing
                self.display_agent = NeuralNetworkGAAgent(
                    current_gen_best_individual,
                    self.ga_trainer.state_encoder,
                    self.ga_trainer.action_interface,
                    hidden_size=self.hidden_size
                )
                self.display_fitness = current_gen_best_fitness
                
                # Print statistics
                avg_fitness = sum(self.fitnesses) / len(self.fitnesses)
                min_fitness = min(self.fitnesses)
                max_fitness = max(self.fitnesses)
                
                # Record analytics with behavioral metrics
                self.analytics.record_generation(
                    generation=self.current_generation + 1,
                    fitness_scores=self.fitnesses,
                    behavioral_metrics=gen_metrics
                )

                # Print stats with behavioral info
                print(f"Generation {self.current_generation + 1}: "
                      f"Best={max_fitness:.2f}, Avg={avg_fitness:.2f}, "
                      f"Min={min_fitness:.2f}, StdDev={self.analytics.generations_data[-1]['std_dev']:.2f}, "
                      f"All-time Best={self.best_fitness:.2f}")
                print(f"  Behavior: AvgKills={gen_metrics['avg_kills']:.1f}, "
                      f"AvgSteps={gen_metrics['avg_steps_survived']:.0f}, "
                      f"AvgAccuracy={gen_metrics['avg_accuracy']*100:.1f}%, "
                      f"BestKills={gen_metrics['best_agent_kills']}")
                
                # Move to displaying best
                self.phase = "displaying_best"
                self._start_best_agent_display()
                return
            
            # Phase: Evolving
            if self.phase == "evolving":
                print(f"Evolving generation {self.current_generation + 1}...")
                self._evolve_generation()
                self.current_generation += 1
                self.phase = "evaluating"
                self._update_info_text("Starting next generation...")
                return
                
        except Exception as e:
            print(f"Error in parallel GA training: {e}")
            import traceback
            traceback.print_exc()
    
    def _start_best_agent_display(self):
        """Start displaying the current generation's best agent in a FRESH game.

        This tests the agent's ability to generalize to new asteroid configurations,
        rather than attempting to replay the exact evaluation scenario.
        """
        if self.display_agent is None:
            return

        self.showing_best_agent = True
        self.best_agent_steps = 0

        # Use normal arcade.schedule spawning (fresh random game, not seeded replay)
        # This tests generalization - can the agent handle NEW asteroid configurations?
        self.game.manual_spawning = False

        # Reset game with fresh random asteroids
        self.game.reset_game()

        # CRITICAL: Reset game's metrics_tracker
        self.game.metrics_tracker.time_alive = 0.0
        self.game.metrics_tracker.reset()

        # Enable external control - we'll call on_update explicitly
        # This prevents arcade's automatic on_update from double-counting
        self.game.external_control = True

        self.ga_trainer.episode_runner.env_tracker.update(self.game)
        self.ga_trainer.episode_runner.reward_calculator.reset()
        self.ga_trainer.episode_runner.state_encoder.reset()
        self.display_agent.reset()

        print(f"Testing best agent in fresh game (training fitness={self.display_fitness:.2f}, all-time best={self.best_fitness:.2f})...")
    
    def _update_best_agent_display(self, delta_time):
        """Update best agent playing visually."""
        # Check if agent died
        if self.display_agent is None or self.game.player not in self.game.player_list:
            # Player died, end display early
            print(f"Best agent died after {self.best_agent_steps} steps")
            self.showing_best_agent = False
            self.game.external_control = False  # Allow arcade to control again
            self.phase = "evolving"
            return
        
        # Get action from current generation's best agent
        state = self.ga_trainer.episode_runner.state_encoder.encode(
            self.ga_trainer.episode_runner.env_tracker
        )
        action = self.display_agent.get_action(state)
        
        # Validate and normalize
        self.ga_trainer.action_interface.validate(action)
        action = self.ga_trainer.action_interface.normalize(action)
        
        # Convert to game input
        game_input = self.ga_trainer.action_interface.to_game_input(action)
        
        # Apply to game
        self.game.left_pressed = game_input["left_pressed"]
        self.game.right_pressed = game_input["right_pressed"]
        self.game.up_pressed = game_input["up_pressed"]
        self.game.space_pressed = game_input["space_pressed"]
        
        # Step game - temporarily allow on_update to run
        self.game.external_control = False
        self.game.on_update(self.frame_delay)
        self.game.external_control = True

        # Update trackers - use the GAME's own trackers, not episode_runner's!
        # The visual game updates its own metrics_tracker with kills/shots
        self.ga_trainer.episode_runner.env_tracker.update(self.game)

        # Calculate reward using the GAME's metrics tracker (which has actual kill/shot data)
        # Enable debug on every 100th step to see per-component rewards
        debug_this_step = (self.best_agent_steps % 100 == 99)
        step_reward = self.ga_trainer.episode_runner.reward_calculator.calculate_step_reward(
            self.ga_trainer.episode_runner.env_tracker,
            self.game.metrics_tracker,
            debug=debug_this_step
        )

        self.best_agent_steps += 1

        # Debug: Print running score and actions every 100 steps
        if self.best_agent_steps % 100 == 0:
            current_score = self.ga_trainer.episode_runner.reward_calculator.score
            kills = self.game.metrics_tracker.total_kills
            shots = self.game.metrics_tracker.total_shots_fired
            time_alive = self.game.metrics_tracker.time_alive
            print(f"  Step {self.best_agent_steps}: Score={current_score:.1f}, Kills={kills}, Shots={shots}, Time={time_alive:.2f}s, StepReward={step_reward:.2f}")

        self._update_info_text("Displaying best agent")

    def _evolve_generation(self):
        """Evolve to next generation using GA operators."""
        # Tournament selection
        parents = self._tournament_selection()
        
        # Create offspring through crossover
        offspring = []
        while len(offspring) < self.ga_trainer.population_size:
            if len(parents) >= 2:
                parent1 = random.choice(parents).copy()
                parent2 = random.choice(parents).copy()
                
                if random.random() < self.ga_trainer.crossover_probability:
                    result = self.ga_trainer.operators.crossover_blend(parent1, parent2)
                    if isinstance(result, tuple) and len(result) == 2:
                        child1 = list(result[0]) if isinstance(result[0], (tuple, list)) else result[0]
                        child2 = list(result[1]) if isinstance(result[1], (tuple, list)) else result[1]
                        offspring.extend([child1, child2])
                    else:
                        offspring.extend([parent1, parent2])
                else:
                    offspring.extend([parent1, parent2])
            else:
                offspring.append(random.choice(parents).copy())
        
        # Trim offspring to correct size
        offspring = offspring[:self.ga_trainer.population_size]
        
        # Apply mutation to ALL offspring (not probabilistically per-offspring)
        for i, child in enumerate(offspring):
            mutated = self.ga_trainer.operators.mutate_gaussian(child)
            if isinstance(mutated, tuple) and len(mutated) > 0:
                offspring[i] = list(mutated[0]) if isinstance(mutated[0], list) else mutated[0]
        
        # Elitism: keep best individuals from previous generation
        # TUNED: Increased from 10% to 20% for more stability
        sorted_pop = sorted(zip(self.population, self.fitnesses), key=lambda x: x[1], reverse=True)
        elite_count = max(2, self.ga_trainer.population_size // 5)  # 20% elitism (was 10%)
        elite = [ind for ind, fit in sorted_pop[:elite_count]]

        # New population: elite + best offspring
        self.population = elite + offspring[:self.ga_trainer.population_size - len(elite)]
        self.population = self.population[:self.ga_trainer.population_size]
        self.fitnesses = []
    
    def _tournament_selection(self, tournament_size: int = 3) -> List[List[float]]:
        """Select parents using tournament selection."""
        parents = []
        for _ in range(self.ga_trainer.population_size):
            tournament_indices = random.sample(range(len(self.population)), min(tournament_size, len(self.population)))
            tournament_fitnesses = [self.fitnesses[i] for i in tournament_indices]
            winner_idx = tournament_indices[tournament_fitnesses.index(max(tournament_fitnesses))]
            parents.append(self.population[winner_idx].copy())
        return parents
    
    def _save_training_results(self):
        """Save training analytics and summary reports."""
        try:
            print("\n" + "="*60)
            print("Generating training reports...")
            print("="*60)
            
            # Generate markdown summary
            markdown_path = self.analytics.generate_markdown_report("training_summary.md")
            
            # Save raw JSON data
            json_path = self.analytics.save_json("training_data.json")
            
            print("\n" + "="*60)
            print("Training reports saved successfully!")
            print(f"  - Summary: {markdown_path}")
            print(f"  - Raw Data: {json_path}")
            print("="*60 + "\n")
        except Exception as e:
            print(f"\n⚠️  Error saving training results: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_info_text(self, phase_description: str = ""):
        """Update info text overlay."""
        if self.showing_best_agent:
            # Use the GAME's metrics tracker which has actual kill/shot data
            metrics = self.game.metrics_tracker.get_episode_stats()
            self.info_text.text = (
                f"Generation {self.current_generation + 1}/{self.ga_trainer.num_generations} | "
                f"Testing Best Agent ({self.best_agent_steps}/{self.best_agent_max_steps})\n"
                f"Training Fitness: {self.display_fitness:.2f} | All-Time Best: {self.best_fitness:.2f} | "
                f"Fresh Game Kills: {metrics.get('total_kills', 0)}"
            )
        else:
            avg = sum(self.fitnesses) / len(self.fitnesses) if self.fitnesses else 0
            self.info_text.text = (
                f"Generation {self.current_generation + 1}/{self.ga_trainer.num_generations} | "
                f"{phase_description}\n"
                f"All-Time Best: {self.best_fitness:.2f} | "
                f"Avg: {avg:.2f} | "
                f"Workers: {self.max_workers}"
            )


def create_ga_trainer(game, **kwargs):
    """Create GA trainer with all components."""
    state_encoder = VectorEncoder(
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
        num_nearest_asteroids=2,
        include_bullets=False,
        include_global=False
    )
    
    action_interface = ActionInterface(action_space_type="boolean")
    
    # Create reward calculator - MUST MATCH parallel_evaluator.py exactly!
    reward_calculator = ComposableRewardCalculator()

    # === CORE REWARDS (synced with parallel_evaluator.py) ===
    reward_calculator.add_component(KillAsteroid(reward_per_asteroid=100.0))
    reward_calculator.add_component(SurvivalBonus(reward_multiplier=2.0))

    # === SHOOTING DISCIPLINE ===
    from interfaces.rewards.ConservingAmmoBonus import ConservingAmmoBonus
    reward_calculator.add_component(ConservingAmmoBonus(good_shot_bonus=5.0, bad_shot_penalty=-5.0, alignment_threshold=0.7))

    # === BEHAVIORAL SHAPING ===
    from interfaces.rewards.FacingAsteroidBonus import FacingAsteroidBonus
    from interfaces.rewards.MaintainingMomentumBonus import MaintainingMomentumBonus
    reward_calculator.add_component(FacingAsteroidBonus(bonus_per_second=2.0))
    reward_calculator.add_component(MaintainingMomentumBonus(bonus_per_second=1.0, penalty_per_second=-0.5))

    from training.base.EpisodeRunner import EpisodeRunner
    episode_runner = EpisodeRunner(
        game=game,
        state_encoder=state_encoder,
        action_interface=action_interface,
        reward_calculator=reward_calculator
    )
    
    ga_trainer = GATrainer(
        state_encoder=state_encoder,
        action_interface=action_interface,
        episode_runner=episode_runner,
        **kwargs
    )
    
    return ga_trainer


def main():
    """Main entry point for parallel GA training."""
    window = AsteroidsGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    
    # Create GA trainer with TUNED parameters for stable learning
    ga_trainer = create_ga_trainer(
        game=window,
        population_size=100,
        num_generations=500,
        # TUNED: Reduced mutation for more stable convergence
        mutation_probability=0.20,  # Was 0.35 - less frequent mutation preserves good solutions
        crossover_probability=0.7,
        mutation_gaussian_sigma=0.15,  # Was 0.3 - smaller mutations for fine-tuning
        mutation_uniform_low=-1.0,
        mutation_uniform_high=1.0,
        crossover_alpha=0.5
    )
    
    # Create parallel training driver
    driver = ParallelGATrainingDriver(
        game=window,
        ga_trainer=ga_trainer,
        frame_delay=1.0 / 60.0,
        max_workers=None  # Auto-detect CPU cores
    )
    
    print("="*60)
    print("PARALLEL GA TRAINING")
    print("="*60)
    print(f"Population size: {ga_trainer.population_size}")
    print(f"Generations: {ga_trainer.num_generations}")
    print(f"Parallel workers: {driver.max_workers}")
    print(f"Expected speedup: ~{driver.max_workers}x")
    print("="*60)
    print("\nStarting parallel GA training...")
    print("All agents evaluate simultaneously in the background.")
    print("Watch the best agent play after each generation!")
    print("Close the window or press Ctrl+C to stop training and save results.\n")
    
    try:
        arcade.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user!")
        driver._save_training_results()
    except Exception as e:
        print(f"\n\n⚠️  Training stopped due to error: {e}")
        driver._save_training_results()
        raise
    finally:
        # Always try to save on exit
        if driver.analytics.generations_data:
            print("\nCleaning up and saving final results...")
            driver._save_training_results()


if __name__ == "__main__":
    main()
