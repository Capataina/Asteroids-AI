"""
NEAT Training Entry Point

Runs parallel NEAT training for Asteroids AI.
"""

import json
import os
import sys
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
from ai_agents.neuroevolution.neat.agent import NEATAgent
from training.config.neat import NEATConfig
from training.config.rewards import create_reward_calculator
from training.core.episode_runner import EpisodeRunner
from training.core.population_evaluator import evaluate_population_parallel
from training.core.display_manager import DisplayManager
from training.methods.neat.driver import NEATDriver
from training.analytics.analytics import TrainingAnalytics


class NEATTrainingScript:
    """
    Main script for NEAT training. Orchestrates components.
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
        # Small deadzone (0.03) allows AI to express "don't turn" without perfect 0.5 output
        # This is easier to learn than no deadzone (always turning) while still being easy to escape
        self.action_interface = ActionInterface(action_space_type="boolean", turn_deadzone=0.03)
        self.reward_calculator = create_reward_calculator(
            max_steps=NEATConfig.MAX_STEPS,
            frame_delay=NEATConfig.FRAME_DELAY
        )

        self.episode_runner = EpisodeRunner(
            game=game,
            state_encoder=self.state_encoder,
            action_interface=self.action_interface,
            reward_calculator=self.reward_calculator
        )

        # 2. Setup Driver (NEAT Logic)
        input_size = self.state_encoder.get_state_size()
        output_size = NEATConfig.OUTPUT_SIZE
        self.driver = NEATDriver(input_size=input_size, output_size=output_size)

        # 3. Setup Analytics
        self.analytics = TrainingAnalytics()
        self.analytics.set_config({
            "method": "NEAT",
            "population_size": NEATConfig.POPULATION_SIZE,
            "num_generations": NEATConfig.NUM_GENERATIONS,
            "seeds_per_agent": NEATConfig.SEEDS_PER_AGENT,
            "use_common_seeds": NEATConfig.USE_COMMON_SEEDS,
            "compatibility_threshold": NEATConfig.COMPATIBILITY_THRESHOLD,
            "c1": NEATConfig.C1,
            "c2": NEATConfig.C2,
            "c3": NEATConfig.C3,
            "weight_mutation_prob": NEATConfig.WEIGHT_MUTATION_PROB,
            "weight_mutation_sigma": NEATConfig.WEIGHT_MUTATION_SIGMA,
            "add_connection_prob": NEATConfig.ADD_CONNECTION_PROB,
            "add_node_prob": NEATConfig.ADD_NODE_PROB,
            "crossover_prob": NEATConfig.CROSSOVER_PROB,
            "inherit_disabled_prob": NEATConfig.INHERIT_DISABLED_PROB,
            "elitism_per_species": NEATConfig.ELITISM_PER_SPECIES,
            "species_stagnation": NEATConfig.SPECIES_STAGNATION,
            "max_nodes": NEATConfig.MAX_NODES,
            "max_connections": NEATConfig.MAX_CONNECTIONS,
            "novelty_enabled": NEATConfig.ENABLE_NOVELTY,
            "diversity_enabled": NEATConfig.ENABLE_DIVERSITY,
            "turn_deadzone": self.action_interface.turn_deadzone,
            "max_workers": self.max_workers
        })

        # 4. Setup Display
        self.display_manager = DisplayManager(game, self.episode_runner, self.analytics)
        self.display_manager.best_agent_max_steps = NEATConfig.MAX_STEPS

        # Artifacts
        self.artifacts_dir = os.path.join(project_root, "training", "neat_artifacts")
        os.makedirs(self.artifacts_dir, exist_ok=True)

        # State
        self.current_generation = 0
        self.best_fitness = float("-inf")
        self.last_improvement_gen = 0
        self.best_genome = None
        self.phase = "evaluating"
        self.current_fitnesses = []
        self.current_adjusted_fitnesses = []
        self.current_per_agent_metrics = []

        # Hook draw
        original_draw = self.game.on_draw
        def new_draw():
            original_draw()
            self.display_manager.draw()
        self.game.on_draw = new_draw

        print("NEAT Training Script Initialized.")

    def _agent_factory(self, genome, state_encoder, action_interface):
        return NEATAgent(genome)

    def _save_genome_artifacts(self, genome, label: str):
        if genome is None:
            return
        json_path = os.path.join(self.artifacts_dir, f"{label}.json")
        dot_path = os.path.join(self.artifacts_dir, f"{label}.dot")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(genome.to_dict(), f, indent=2)

        lines = ["digraph NEAT {"]
        for node_id, node in genome.nodes.items():
            lines.append(f'  {node_id} [label="{node.node_type}:{node_id}"];')
        for conn in genome.connections.values():
            if not conn.enabled:
                continue
            lines.append(f'  {conn.in_node} -> {conn.out_node} [label="{conn.weight:.3f}"];')
        lines.append("}")
        with open(dot_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def update(self, delta_time):
        try:
            if self.current_generation >= NEATConfig.NUM_GENERATIONS:
                if not self.display_manager.showing_best_agent:
                    print("Training Complete.")
                    self._save()
                    if self.best_genome is not None:
                        agent = NEATAgent(self.best_genome)
                        self.display_manager.start_display(agent, self.best_fitness, self.best_fitness)
                    return

            # Phase: Displaying
            if self.display_manager.showing_best_agent:
                status = self.display_manager.update(delta_time)
                if status == "done":
                    if self.current_generation >= NEATConfig.NUM_GENERATIONS:
                        arcade.close_window()
                    else:
                        self.phase = "evolving"
                return

            # Phase: Evaluating
            if self.phase == "evaluating":
                print(f"Generation {self.current_generation + 1}: Evaluating...")
                self.display_manager.update_info_text_training(
                    self.current_generation + 1,
                    NEATConfig.NUM_GENERATIONS,
                    self.max_workers,
                    "Evaluating..."
                )

                eval_start = time.time()
                fitnesses, _, gen_metrics, per_agent_metrics = evaluate_population_parallel(
                    self.driver.population,
                    self.state_encoder,
                    self.action_interface,
                    max_steps=NEATConfig.MAX_STEPS,
                    max_workers=self.max_workers,
                    seeds_per_agent=NEATConfig.SEEDS_PER_AGENT,
                    use_common_seeds=NEATConfig.USE_COMMON_SEEDS,
                    agent_factory=self._agent_factory
                )
                self.current_fitnesses = fitnesses
                self.current_per_agent_metrics = per_agent_metrics

                # Calculate Reliability-Based Fitness (penalize std dev)
                # This filters out "lucky" agents that only succeed on specific seeds
                self.current_adjusted_fitnesses = []
                for i, metrics in enumerate(per_agent_metrics):
                    std_dev = metrics.get('fitness_std', 0.0)
                    penalty = std_dev * NEATConfig.FITNESS_STD_PENALTY_RATIO
                    adjusted_fit = fitnesses[i] - penalty
                    self.current_adjusted_fitnesses.append(adjusted_fit)

                # Use best fitness agent for both tracking and display
                # (NEAT uses fitness-based selection, not Pareto)
                best_idx = fitnesses.index(max(fitnesses)) if fitnesses else 0
                current_best_fit = fitnesses[best_idx] if fitnesses else float("-inf")
                current_best_genome = self.driver.population[best_idx].copy()
                display_genome = current_best_genome

                if current_best_fit > self.best_fitness:
                    self.best_fitness = current_best_fit
                    self.best_genome = current_best_genome.copy()
                    self.last_improvement_gen = self.current_generation
                    self._save_genome_artifacts(self.best_genome, "best_overall")

                # Early Stopping Check
                gens_since_improvement = self.current_generation - self.last_improvement_gen
                if gens_since_improvement >= NEATConfig.EARLY_STOPPING_GENERATIONS:
                    print(f"\nEarly Stopping triggered: No improvement for {gens_since_improvement} generations.")
                    self._save()
                    arcade.close_window()
                    return

                # Record Analytics
                timing_stats = {
                    "evaluation_duration": time.time() - eval_start,
                    "evolution_duration": self.driver.last_evolution_duration
                }
                operator_stats = self.driver.last_evolution_stats.copy()

                self.analytics.record_generation(
                    generation=self.current_generation + 1,
                    fitness_scores=fitnesses,
                    behavioral_metrics=gen_metrics,
                    timing_stats=timing_stats,
                    operator_stats=operator_stats
                )
                self.analytics.record_distributions(
                    generation=self.current_generation + 1,
                    fitness_values=fitnesses,
                    per_agent_metrics=per_agent_metrics
                )

                # Save artifacts for this generation
                self._save_genome_artifacts(display_genome, f"gen_{self.current_generation + 1:04d}_best")

                # Calculate stats for display
                avg_fit = sum(fitnesses) / len(fitnesses) if fitnesses else 0.0
                min_fit = min(fitnesses) if fitnesses else 0.0
                std_fit = statistics.stdev(fitnesses) if len(fitnesses) > 1 else 0.0

                print("\n" + "=" * 60)
                print(f" GENERATION {self.current_generation + 1} SUMMARY (NEAT)")
                print("=" * 60)
                print(" FITNESS (Raw)")
                print(f"  Best:  {current_best_fit:8.2f}  |  Avg: {avg_fit:8.2f}")
                print(f"  Min:   {min_fit:8.2f}  |  Std: {std_fit:8.2f}")
                print(f"  Last Impr: Gen {self.last_improvement_gen + 1} ({gens_since_improvement} ago)")
                print("-" * 60)

                # Start Display (showing best fitness agent)
                display_agent = NEATAgent(display_genome)
                self.display_manager.start_display(display_agent, current_best_fit, self.best_fitness)
                self.phase = "displaying"
                return

            # Phase: Evolving
            if self.phase == "evolving":
                print(f"Evolving generation {self.current_generation + 1}...")
                # Pass adjusted fitnesses to driver to penalize luck
                self.driver.evolve(self.current_adjusted_fitnesses, self.current_per_agent_metrics)
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
        self.analytics.generate_markdown_report("training_summary_neat.md")
        self.analytics.save_json("training_data_neat.json")
        print("NEAT training results saved.")


def main():
    window = AsteroidsGame(globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT, "Asteroids AI - NEAT Training")
    window.setup()
    trainer = NEATTrainingScript(window)
    arcade.schedule(trainer.update, NEATConfig.FRAME_DELAY)

    try:
        arcade.run()
    finally:
        print("\nApplication exiting, saving training results...")
        trainer._save()


if __name__ == "__main__":
    main()
