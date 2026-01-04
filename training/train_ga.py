"""
Visual GA Training Entry Point

Runs Genetic Algorithm training with real-time visualization.
Watch the AI learn and improve generation by generation.
"""

import sys
import os
import math
# Add project root to Python path so we can import Asteroids
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import arcade
import random
from typing import Optional, List
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
from training.base.EpisodeRunner import EpisodeRunner
from ai_agents.neuroevolution.genetic_algorithm.ga_trainer import GATrainer
from ai_agents.neuroevolution.genetic_algorithm.ga_agent import GAAgent


class GATrainingDriver:
    """
    Handles GA training with real-time visualization.
    Similar to AIDriver in train_agent.py but for GA training.
    """

    def __init__(
        self,
        game: AsteroidsGame,
        ga_trainer: GATrainer,
        frame_delay: float = 1.0 / 60.0,
        show_best_agent: bool = False  # Set to False for faster training
    ):
        """
        Initialize GA training driver.

        Args:
            game: AsteroidsGame instance
            ga_trainer: GATrainer instance
            frame_delay: Time between updates (default 60 FPS)
            show_best_agent: Whether to show best agent playing between generations
        """
        self.game = game
        self.ga_trainer = ga_trainer
        self.frame_delay = frame_delay
        self.enable_best_agent_display = show_best_agent

        # Disable game's internal reward calculator since we're using our own
        self.game.update_internal_rewards = False
        
        # Disable game's auto-reset on collision since we manage episodes ourselves
        self.game.auto_reset_on_collision = False

        # Training state
        self.current_generation = 0
        self.population = []
        self.fitnesses = []
        self.best_agent: Optional[GAAgent] = None
        self.best_fitness = float('-inf')
        self.current_individual_index = 0
        self.evaluating_individual = False
        
        # For incremental episode evaluation (runs one step per update)
        self.current_evaluation_agent: Optional[GAAgent] = None
        self.current_episode_steps = 0
        self.current_episode_reward = 0.0
        self.current_episode_done = False
        self.current_episode_max_steps = 400  # Reduced for faster training (was 1000)

        # For displaying best agent
        self.showing_best_agent = False
        self.best_agent_episode_steps = 0
        self.best_agent_episode_reward = 0.0

        # Initialize population
        self._initialize_population()

        # Register update function with arcade
        arcade.schedule(self.update, frame_delay)

        # Create info text overlay
        self.info_text = arcade.Text(
            text="Initializing GA training...",
            x=10,
            y=SCREEN_HEIGHT - 60,
            color=arcade.color.YELLOW,
            font_size=14
        )

        # Hook into the game's draw method to add our metrics
        original_draw = self.game.on_draw

        def new_draw():
            original_draw()
            # Sync training reward to game display score
            self.game.reward_calculator.score = self.ga_trainer.episode_runner.reward_calculator.score
            # Display score (guard against displaying negative scores due to edge cases)
            display_score = max(0, math.floor(self.game.reward_calculator.score))
            self.game.score_text.text = f"Score: {display_score}"
            self.info_text.draw()

        self.game.on_draw = new_draw

    def _initialize_population(self):
        """Initialize random population."""
        state_size = self.ga_trainer.state_encoder.get_state_size()
        action_size = 4  # left, right, thrust, shoot
        param_size = state_size * action_size  # Linear policy: each action has weights for each state feature

        self.population = [
            [random.uniform(
                self.ga_trainer.mutation_uniform_low,
                self.ga_trainer.mutation_uniform_high
            ) for _ in range(param_size)]
            for _ in range(self.ga_trainer.population_size)
        ]

    def _start_evaluating_individual(self, individual: List[float]):
        """
        Start evaluating an individual by creating a GAAgent and resetting episode state.
        The episode will run incrementally in update().

        Args:
            individual: Parameter vector
        """
        # Create GAAgent from parameter vector
        self.current_evaluation_agent = GAAgent(
            individual,
            self.ga_trainer.state_encoder,
            self.ga_trainer.action_interface
        )
        
        # Reset game and episode state
        self.game.reset_game()
        self.ga_trainer.episode_runner.env_tracker.update(self.game)
        self.ga_trainer.episode_runner.metrics_tracker.update(self.game)
        self.ga_trainer.episode_runner.reward_calculator.reset()
        self.ga_trainer.episode_runner.state_encoder.reset()
        self.current_evaluation_agent.reset()
        
        # Debug: Verify reward calculator was reset
        print(f"[DEBUG] Starting individual {self.current_individual_index+1}, reward calculator score after reset: {self.ga_trainer.episode_runner.reward_calculator.score}")
        
        # Reset episode tracking
        self.current_episode_steps = 0
        self.current_episode_reward = 0.0
        self.current_episode_done = False

    def _step_evaluation_episode(self) -> Optional[float]:
        """
        Run one step of the current evaluation episode.
        Returns fitness score if episode is done, None otherwise.
        
        Returns:
            Fitness score if episode complete, None if still running
        """
        if self.current_evaluation_agent is None or self.current_episode_done:
            return None
            
        # Check if done
        if self.game.player not in self.game.player_list:
            self.current_episode_done = True
            # Calculate final episode reward
            episode_reward = self.ga_trainer.episode_runner.reward_calculator.calculate_episode_reward(
                self.ga_trainer.episode_runner.metrics_tracker
            )
            self.current_episode_reward += episode_reward
            return self.current_episode_reward
        
        if self.current_episode_steps >= self.current_episode_max_steps:
            self.current_episode_done = True
            # Calculate final episode reward
            episode_reward = self.ga_trainer.episode_runner.reward_calculator.calculate_episode_reward(
                self.ga_trainer.episode_runner.metrics_tracker
            )
            self.current_episode_reward += episode_reward
            return self.current_episode_reward
        
        # Encode state
        state = self.ga_trainer.episode_runner.state_encoder.encode(
            self.ga_trainer.episode_runner.env_tracker
        )
        
        # Get action from agent
        action = self.current_evaluation_agent.get_action(state)
        
        # Debug: Print first action of first episode to verify it's not all zeros
        if self.current_episode_steps == 0 and self.current_individual_index == 0 and self.current_generation == 0:
            print(f"[DEBUG] First action: {action[:4]}")
            print(f"[DEBUG] State size: {len(state)}, Param vector size: {len(self.current_evaluation_agent.parameter_vector)}")
        
        # Validate and normalize
        self.ga_trainer.action_interface.validate(action)
        action = self.ga_trainer.action_interface.normalize(action)
        
        # Convert to game input
        game_input = self.ga_trainer.action_interface.to_game_input(action)
        
        # Debug: Print first game input to verify actions are being applied
        if self.current_episode_steps == 0 and self.current_individual_index == 0 and self.current_generation == 0:
            print(f"[DEBUG] First game input: {game_input}")

        # Apply to game
        self.game.left_pressed = game_input["left_pressed"]
        self.game.right_pressed = game_input["right_pressed"]
        self.game.up_pressed = game_input["up_pressed"]
        self.game.space_pressed = game_input["space_pressed"]
        
        # Step game
        self.game.on_update(self.frame_delay)
        
        # Update trackers
        self.ga_trainer.episode_runner.env_tracker.update(self.game)
        self.ga_trainer.episode_runner.metrics_tracker.update(self.game)
        
        # Calculate step reward
        step_reward = self.ga_trainer.episode_runner.reward_calculator.calculate_step_reward(
            self.ga_trainer.episode_runner.env_tracker,
            self.ga_trainer.episode_runner.metrics_tracker
        )
        self.current_episode_reward += step_reward
        self.current_episode_steps += 1
        
        return None  # Episode still running

    def update(self, delta_time):
        """
        Called by arcade scheduler to update training.

        This runs the GA training loop incrementally, one step at a time,
        so the game can render between updates.
        """
        try:
            # If we've completed all generations, show final best agent then close
            if self.current_generation >= self.ga_trainer.num_generations:
                if not self.showing_best_agent and self.best_agent is not None:
                    # Start showing final best agent
                    print(f"\n=== Training Complete! ===")
                    print(f"Final Best Fitness: {self.best_fitness:.2f}")
                    print(f"Now playing best agent for 5000 steps...")
                    self.showing_best_agent = True
                    self.best_agent_episode_steps = 0
                    self.best_agent_episode_reward = 0.0
                    self.game.reset_game()
                    self.ga_trainer.episode_runner.env_tracker.update(self.game)
                    self.ga_trainer.episode_runner.metrics_tracker.update(self.game)
                    self.ga_trainer.episode_runner.reward_calculator.reset()
                    self.ga_trainer.episode_runner.state_encoder.reset()
                    self.best_agent.reset()
                    return
                elif self.showing_best_agent and self.best_agent_episode_steps >= 5000:
                    # Done showing best agent, close window
                    arcade.close_window()
                    return
                else:
                    # Continue showing best agent
                    self._update_best_agent_display(delta_time)
                    return

            # If showing best agent, let it play
            if self.showing_best_agent and self.best_agent is not None:
                self._update_best_agent_display(delta_time)
                return

            # Evaluate current generation incrementally
            if self.evaluating_individual:
                # Continue evaluating current individual (one step per update)
                fitness = self._step_evaluation_episode()
                
                if fitness is not None:
                    # Episode complete, record fitness
                    print(f"[DEBUG] Individual {self.current_individual_index} finished with fitness: {fitness}, reward calc score: {self.ga_trainer.episode_runner.reward_calculator.score}")
                    self.fitnesses.append(fitness)
                    self.current_individual_index += 1
                    self.evaluating_individual = False
                    self.current_evaluation_agent = None

                    # Update best agent if this is better
                    if fitness > self.best_fitness:
                        self.best_fitness = fitness
                        self.best_agent = GAAgent(
                            self.population[self.current_individual_index - 1],
                            self.ga_trainer.state_encoder,
                            self.ga_trainer.action_interface
                        )

                    # Update display
                    self._update_info_text()
            else:
                # Start evaluating next individual
                if self.current_individual_index < len(self.population):
                    self.evaluating_individual = True
                    self._start_evaluating_individual(self.population[self.current_individual_index])
                    # Update display
                    self._update_info_text()
                else:
                    # All individuals evaluated, evolve to next generation
                    self._evolve_generation()

        except Exception as e:
            print(f"Error in GA training update: {e}")
            import traceback
            traceback.print_exc()

    def _evolve_generation(self):
        """Evolve to next generation using GA operators."""
        # Select parents (tournament selection)
        parents = self._tournament_selection()

        # Create offspring (crossover + mutation)
        offspring = []
        while len(offspring) < self.ga_trainer.population_size - len(parents):
            if len(parents) >= 2:
                parent1 = random.choice(parents).copy()
                parent2 = random.choice(parents).copy()
                if random.random() < self.ga_trainer.crossover_probability:
                    # Use blend crossover
                    result = self.ga_trainer.operators.crossover_blend(parent1, parent2)
                    # Handle return value (may be tuple of tuples or tuple of lists)
                    if isinstance(result, tuple) and len(result) == 2:
                        child1 = list(result[0]) if isinstance(result[0], (tuple, list)) else result[0]
                        child2 = list(result[1]) if isinstance(result[1], (tuple, list)) else result[1]
                        offspring.extend([child1, child2])
                    else:
                        # Fallback: just copy parents
                        offspring.extend([parent1, parent2])
                else:
                    offspring.extend([parent1, parent2])
            else:
                # Not enough parents, just copy
                offspring.append(random.choice(parents).copy())

        # Apply mutation (use Gaussian mutation)
        for i, child in enumerate(offspring):
            if random.random() < self.ga_trainer.mutation_probability:
                mutated = self.ga_trainer.operators.mutate_gaussian(child)
                # Handle return value (may be list or tuple)
                if isinstance(mutated, tuple):
                    offspring[i] = list(mutated[0]) if len(mutated) > 0 else child
                else:
                    offspring[i] = mutated if mutated else child

        # Elitism: keep best individuals
        sorted_pop = sorted(zip(self.population, self.fitnesses), key=lambda x: x[1], reverse=True)
        elite_count = max(1, self.ga_trainer.population_size // 10)  # Keep top 10%
        elite = [ind for ind, fit in sorted_pop[:elite_count]]

        # New population = elite + offspring
        self.population = elite + offspring[:self.ga_trainer.population_size - len(elite)]
        self.population = self.population[:self.ga_trainer.population_size]  # Ensure correct size

        # Reset for next generation
        self.current_generation += 1
        self.current_individual_index = 0
        self.fitnesses = []

        # Show best agent for a bit before next generation (if enabled)
        if self.enable_best_agent_display and self.best_agent is not None:
            self.showing_best_agent = True
            self.best_agent_episode_steps = 0
            self.best_agent_episode_reward = 0.0
            self.game.reset_game()
            self.ga_trainer.episode_runner.env_tracker.update(self.game)
            self.ga_trainer.episode_runner.metrics_tracker.update(self.game)
            self.ga_trainer.episode_runner.reward_calculator.reset()
            self.ga_trainer.episode_runner.state_encoder.reset()
            self.best_agent.reset()

        print(f"Generation {self.current_generation}: Best fitness = {self.best_fitness:.2f}")

    def _tournament_selection(self, tournament_size: int = 3) -> List[List[float]]:
        """Select parents using tournament selection."""
        parents = []
        for _ in range(self.ga_trainer.population_size):
            # Random tournament
            tournament_indices = random.sample(range(len(self.population)), min(tournament_size, len(self.population)))
            tournament_fitnesses = [self.fitnesses[i] for i in tournament_indices]
            winner_idx = tournament_indices[tournament_fitnesses.index(max(tournament_fitnesses))]
            parents.append(self.population[winner_idx].copy())
        return parents

    def _update_best_agent_display(self, delta_time):
        """Update best agent playing display."""
        if self.best_agent is None:
            self.showing_best_agent = False
            return

        # Run one step of best agent
        if self.game.player in self.game.player_list:
            # Encode state
            state = self.ga_trainer.episode_runner.state_encoder.encode(
                self.ga_trainer.episode_runner.env_tracker
            )

            # Get action from best agent
            action = self.best_agent.get_action(state)

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

            # Step game
            self.game.on_update(self.frame_delay)

            # Update trackers
            self.ga_trainer.episode_runner.env_tracker.update(self.game)
            self.ga_trainer.episode_runner.metrics_tracker.update(self.game)

            # Calculate reward
            step_reward = self.ga_trainer.episode_runner.reward_calculator.calculate_step_reward(
                self.ga_trainer.episode_runner.env_tracker,
                self.ga_trainer.episode_runner.metrics_tracker
            )
            self.best_agent_episode_reward += step_reward
            self.best_agent_episode_steps += 1

            # Check if done
            if self.game.player not in self.game.player_list or self.best_agent_episode_steps >= 5000:
                # Done showing best agent, continue to next generation or end training
                self.showing_best_agent = False
        else:
            self.showing_best_agent = False

        self._update_info_text()

    def _update_info_text(self):
        """Update the info text overlay with current training metrics."""
        if self.showing_best_agent and self.best_agent is not None:
            metrics = self.ga_trainer.episode_runner.metrics_tracker.get_episode_stats()
            self.info_text.text = (
                f"Generation {self.current_generation}/{self.ga_trainer.num_generations} | "
                f"Best Fitness: {self.best_fitness:.2f} | "
                f"Best Agent Playing | "
                f"Steps: {self.best_agent_episode_steps} | "
                f"Reward: {self.best_agent_episode_reward:.2f} | "
                f"Kills: {metrics.get('total_kills', 0)} | "
                f"Accuracy: {metrics.get('accuracy', 0.0):.1%}"
            )
        else:
            avg_fitness = sum(self.fitnesses) / len(self.fitnesses) if self.fitnesses else 0.0
            if self.evaluating_individual:
                # Show current episode progress
                self.info_text.text = (
                    f"Generation {self.current_generation + 1}/{self.ga_trainer.num_generations} | "
                    f"Evaluating: {self.current_individual_index + 1}/{self.ga_trainer.population_size} | "
                    f"Steps: {self.current_episode_steps}/{self.current_episode_max_steps} | "
                    f"Reward: {self.current_episode_reward:.2f} | "
                    f"Best Fitness: {self.best_fitness:.2f}"
                )
            else:
                self.info_text.text = (
                    f"Generation {self.current_generation + 1}/{self.ga_trainer.num_generations} | "
                    f"Evaluating: {self.current_individual_index}/{self.ga_trainer.population_size} | "
                    f"Best Fitness: {self.best_fitness:.2f} | "
                    f"Avg Fitness: {avg_fitness:.2f}"
                )


def create_ga_trainer(
    game: AsteroidsGame,
    population_size: int = 50,
    num_generations: int = 100,
    mutation_probability: float = 0.1,
    crossover_probability: float = 0.7,
    mutation_gaussian_sigma: float = 0.1,
    mutation_uniform_low: float = -1.0,
    mutation_uniform_high: float = 1.0,
    crossover_alpha: float = 0.5
) -> GATrainer:
    """
    Create and configure GATrainer with all required components.

    Args:
        game: AsteroidsGame instance
        population_size: Size of GA population
        num_generations: Number of generations to evolve
        mutation_probability: Probability of mutating an individual
        crossover_probability: Probability of crossover
        mutation_gaussian_sigma: Standard deviation for Gaussian mutation
        mutation_uniform_low: Lower bound for uniform mutation
        mutation_uniform_high: Upper bound for uniform mutation
        crossover_alpha: Alpha parameter for blend crossover

    Returns:
        Configured GATrainer instance
    """
    # Create state encoder
    state_encoder = VectorEncoder(
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
        num_nearest_asteroids=2,
        include_bullets=False,
        include_global=False
    )

    # Create action interface
    action_interface = ActionInterface(action_space_type="boolean")

    # Create reward calculator with all components
    reward_calculator = ComposableRewardCalculator()
    reward_calculator.add_component(SurvivalBonus())
    reward_calculator.add_component(KillAsteroid())
    reward_calculator.add_component(ChunkBonus())
    reward_calculator.add_component(NearMiss())
    reward_calculator.add_component(AccuracyBonus())
    reward_calculator.add_component(KPMBonus())

    # Create episode runner
    episode_runner = EpisodeRunner(
        game=game,
        state_encoder=state_encoder,
        action_interface=action_interface,
        reward_calculator=reward_calculator
    )

    # Create GA trainer
    ga_trainer = GATrainer(
        population_size=population_size,
        num_generations=num_generations,
        mutation_probability=mutation_probability,
        crossover_probability=crossover_probability,
        mutation_gaussian_sigma=mutation_gaussian_sigma,
        mutation_uniform_low=mutation_uniform_low,
        mutation_uniform_high=mutation_uniform_high,
        crossover_alpha=crossover_alpha,
        state_encoder=state_encoder,
        action_interface=action_interface,
        episode_runner=episode_runner
    )

    return ga_trainer


def main():
    """Main entry point for visual GA training."""
    # Create game window
    window = AsteroidsGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()

    # Create GA trainer with default parameters
    # You can adjust these parameters here
    ga_trainer = create_ga_trainer(
        game=window,
        population_size=50,  # Increased for better diversity (was 30)
        num_generations=100,   # Increased to see more improvement
        mutation_probability=0.25,  # Increased for faster exploration (was 0.1)
        crossover_probability=0.7,
        mutation_gaussian_sigma=0.2,  # Increased for larger jumps (was 0.1)
        mutation_uniform_low=-1.0,
        mutation_uniform_high=1.0,
        crossover_alpha=0.5
    )

    # Create training driver
    driver = GATrainingDriver(
        game=window,
        ga_trainer=ga_trainer,
        frame_delay=1.0 / 60.0,  # 60 FPS
        show_best_agent=False  # Set to True to watch best agent between generations (slower)
    )

    print("Starting GA training with visualization...")
    print("Watch the AI learn and improve generation by generation!")
    print("Close the window to stop training.")

    # Run the game (this starts the arcade loop)
    arcade.run()


if __name__ == "__main__":
    main()
