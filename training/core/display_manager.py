import arcade
import math
from game import globals
from training.config.genetic_algorithm import GAConfig

class DisplayManager:
    """
    Manages the visual display of the best agent in the game window.
    """
    def __init__(self, game, episode_runner, analytics, max_steps: int | None = None):
        self.game = game
        self.episode_runner = episode_runner
        self.analytics = analytics
        
        self.display_agent = None
        self.display_fitness = 0.0
        self.best_fitness = 0.0
        
        self.showing_best_agent = False
        self.best_agent_steps = 0
        self.best_agent_max_steps = max_steps if max_steps is not None else GAConfig.MAX_STEPS
        
        self.fresh_game_start_kills = 0
        self.fresh_game_start_shots = 0
        self.fresh_game_start_hits = 0
        
        # Create info text
        self.info_text = arcade.Text(
            text="Starting...",
            x=10,
            y=globals.SCREEN_HEIGHT - 60,
            color=arcade.color.YELLOW,
            font_size=14
        )

    def start_display(self, agent, fitness, all_time_best_fitness):
        """Start displaying the given agent in a fresh game."""
        self.display_agent = agent
        self.display_fitness = fitness
        self.best_fitness = all_time_best_fitness
        
        if self.display_agent is None:
            return

        self.showing_best_agent = True
        self.best_agent_steps = 0

        # Use manual spawning to match headless timing exactly
        self.game.manual_spawning = True

        # Reset game
        self.game.reset_game()
        self.game.metrics_tracker.time_alive = 0.0
        self.game.metrics_tracker.reset()

        # Enable external control
        self.game.external_control = True

        # Reset runners
        self.episode_runner.env_tracker.update(self.game)
        self.episode_runner.reward_calculator.reset()
        self.episode_runner.state_encoder.reset()
        self.display_agent.reset()

        # Track starting state
        self.fresh_game_start_kills = self.game.metrics_tracker.total_kills
        self.fresh_game_start_shots = self.game.metrics_tracker.total_shots_fired
        self.fresh_game_start_hits = self.game.metrics_tracker.total_hits

        print(f"Testing best agent in fresh game (training fitness={self.display_fitness:.2f}, all-time best={self.best_fitness:.2f})...")

    def update(self, delta_time):
        """Update the visual display. Returns 'continue' or 'done'."""
        if not self.showing_best_agent:
            return "done"

        # Check for death (from previous frame)
        if self.display_agent is None or self.game.player not in self.game.player_list:
            print(f"Best agent died after {self.best_agent_steps} steps")
            self._capture_metrics("asteroid_collision")
            self._stop_display()
            return "done"
        
        # Check max steps
        if self.best_agent_steps >= self.best_agent_max_steps:
            self._capture_metrics("completed_episode")
            self._stop_display()
            return "done"

        # Get and Apply Action
        state = self.episode_runner.state_encoder.encode(self.episode_runner.env_tracker)
        action = self.display_agent.get_action(state)
        
        self.episode_runner.action_interface.validate(action)
        action = self.episode_runner.action_interface.normalize(action)
        if self.episode_runner.action_interface.action_space_type == "continuous":
            game_input = self.episode_runner.action_interface.to_game_input_continuous(action)
            self.game.continuous_control_mode = True
            self.game.turn_magnitude = game_input["turn_magnitude"]
            self.game.thrust_magnitude = game_input["thrust_magnitude"]
            self.game.shoot_requested = game_input["shoot"]
            self.game.left_pressed = False
            self.game.right_pressed = False
            self.game.up_pressed = False
            self.game.space_pressed = False
        else:
            game_input = self.episode_runner.action_interface.to_game_input(action)
            self.game.continuous_control_mode = False
            self.game.left_pressed = game_input["left_pressed"]
            self.game.right_pressed = game_input["right_pressed"]
            self.game.up_pressed = game_input["up_pressed"]
            self.game.space_pressed = game_input["space_pressed"]
        
        # Step game
        self.game.external_control = False
        # FORCE fixed time step to match training simulation exactly
        # Arcade provides variable delta_time, but training assumes fixed 1/60s
        self.game.on_update(self.episode_runner.frame_delay)
        self.game.external_control = True

        # Update trackers
        self.episode_runner.env_tracker.update(self.game)

        # Calculate reward (for display/tracking only)
        self.episode_runner.reward_calculator.calculate_step_reward(
            self.episode_runner.env_tracker,
            self.game.metrics_tracker,
            debug=False
        )

        self.best_agent_steps += 1
        self._update_info_text()
        
        return "continue"

    def draw(self):
        """Draw overlay info."""
        if self.showing_best_agent:
            # Sync score to game display
            self.game.reward_calculator.score = self.episode_runner.reward_calculator.score
            display_score = max(0, math.floor(self.game.reward_calculator.score))
            self.game.score_text.text = f"Score: {display_score}"
            self.info_text.draw()
            
            # Debug Overlays
            if self.game.debug_mode:
                import game.debug.visuals
                game.debug.visuals.draw_hybrid_encoder_debug(self.episode_runner.state_encoder, self.game)
                game.debug.visuals.draw_target_lock_debug(self.game)

    def _stop_display(self):
        self.showing_best_agent = False
        self.game.manual_spawning = False
        self.game.external_control = False

    def _capture_metrics(self, cause_of_death):
        # Get metrics from the fresh game
        metrics = self.game.metrics_tracker
        reward_calc = self.episode_runner.reward_calculator

        fresh_kills = metrics.total_kills - self.fresh_game_start_kills
        fresh_shots = metrics.total_shots_fired - self.fresh_game_start_shots
        fresh_hits = metrics.total_hits - self.fresh_game_start_hits
        fresh_accuracy = fresh_hits / fresh_shots if fresh_shots > 0 else 0.0
        fresh_fitness = reward_calc.score

        fresh_game_data = {
            'fitness': fresh_fitness,
            'kills': fresh_kills,
            'steps_survived': self.best_agent_steps,
            'shots_fired': fresh_shots,
            'hits': fresh_hits,
            'accuracy': fresh_accuracy,
            'time_alive_seconds': metrics.time_alive,
            'cause_of_death': cause_of_death,
            'completed_full_episode': cause_of_death == "completed_episode",
            'reward_breakdown': reward_calc.get_reward_breakdown(),
        }

        # Calculate generalization metrics
        gen_data = self.analytics.generations_data[-1] if self.analytics.generations_data else {}
        training_fitness = self.display_fitness
        training_kills = gen_data.get('best_agent_kills', 0)
        training_steps = gen_data.get('best_agent_steps', 0)
        training_accuracy = gen_data.get('best_agent_accuracy', 0)

        # Calculate ratios
        fitness_ratio = fresh_fitness / training_fitness if training_fitness > 0 else 0.0
        kills_ratio = fresh_kills / training_kills if training_kills > 0 else 0.0
        steps_ratio = self.best_agent_steps / training_steps if training_steps > 0 else 0.0
        accuracy_delta = fresh_accuracy - training_accuracy

        # Grade
        if fitness_ratio >= 0.90: grade = "A"
        elif fitness_ratio >= 0.70: grade = "B"
        elif fitness_ratio >= 0.50: grade = "C"
        elif fitness_ratio >= 0.30: grade = "D"
        else: grade = "F"

        generalization_metrics = {
            'fitness_ratio': fitness_ratio,
            'kills_ratio': kills_ratio,
            'steps_ratio': steps_ratio,
            'accuracy_delta': accuracy_delta,
            'generalization_grade': grade,
        }

        # Record to analytics
        generation = len(self.analytics.generations_data) # Estimate current gen from data
        self.analytics.record_fresh_game(
            generation=generation,
            fresh_game_data=fresh_game_data,
            generalization_metrics=generalization_metrics
        )

        print("-" * 50)
        print(" FRESH GAME (GENERALIZATION TEST)")
        print("-" * 50)
        print(" PERFORMANCE")
        print(f"  Fitness: {fresh_fitness:8.2f}  |  Grade: {grade}")
        print(f"  Ratio:   {fitness_ratio:8.2f}  |  Steps: {self.best_agent_steps}")
        print("-" * 50)
        print(" BEHAVIOR")
        print(f"  Kills:   {fresh_kills:8d}  |  Accuracy: {fresh_accuracy*100:5.1f}%")
        print(f"  Death:   {cause_of_death:8s}  |  Shots:    {fresh_shots:5d}")
        print("=" * 50 + "\n")

    def _update_info_text(self):
        metrics = self.game.metrics_tracker.get_episode_stats()
        # We assume generation info is passed or tracked elsewhere, 
        # but for now we'll just show what we have.
        # Ideally DisplayManager should know current generation.
        generation = len(self.analytics.generations_data)
        
        self.info_text.text = (
            f"Generation {generation} | "
            f"Testing Best Agent ({self.best_agent_steps}/{self.best_agent_max_steps})\n"
            f"Training Fitness: {self.display_fitness:.2f} | All-Time Best: {self.best_fitness:.2f} | "
            f"Fresh Game Kills: {metrics.get('total_kills', 0)}"
        )
    
    def update_info_text_training(self, generation, total_generations, workers, phase_desc):
        """Helper to update text during training phase (not displaying agent)."""
        avg = 0.0 
        # We don't have easy access to fitnesses here unless passed.
        # So maybe this method belongs in the driver, or driver updates text directly.
        # For now, let's allow external text setting.
        self.info_text.text = (
            f"Generation {generation}/{total_generations} | "
            f"{phase_desc}\n"
            f"All-Time Best: {self.best_fitness:.2f} | "
            f"Workers: {workers}"
        )
