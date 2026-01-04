"""
Parallel Evaluation for Genetic Algorithm

Evaluates multiple agents simultaneously using threading for massive speedup.
"""

import concurrent.futures
import random
from typing import List, Tuple, Dict
from game.headless_game import HeadlessAsteroidsGame
from ai_agents.neuroevolution.genetic_algorithm.ga_agent import GAAgent
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
from interfaces.rewards.FacingAsteroidBonus import FacingAsteroidBonus
from interfaces.rewards.ConservingAmmoBonus import ConservingAmmoBonus
from interfaces.rewards.LeadingTargetBonus import LeadingTargetBonus
from interfaces.rewards.MovingTowardDangerBonus import MovingTowardDangerBonus
from interfaces.rewards.SpacingFromWallsBonus import SpacingFromWallsBonus
from interfaces.rewards.MaintainingMomentumBonus import MaintainingMomentumBonus


def evaluate_single_agent(
    individual: List[float],
    state_encoder: VectorEncoder,
    action_interface: ActionInterface,
    max_steps: int = 2000,
    frame_delay: float = 1.0 / 60.0,
    random_seed: int = None
) -> float:
    """
    Evaluate a single agent in a headless game instance.

    Args:
        individual: Parameter vector for the agent
        state_encoder: State encoder instance
        action_interface: Action interface instance
        max_steps: Maximum steps per episode
        frame_delay: Time delta per step
        random_seed: Random seed for reproducible asteroid spawning

    Returns:
        Fitness score (total reward)
    """
    # Create headless game with isolated RNG for reproducible asteroid spawning
    # Each game has its own Random instance, so parallel evaluations don't interfere
    game = HeadlessAsteroidsGame(width=800, height=600, random_seed=random_seed)
    game.reset_game()
    
    # Create reward calculator
    reward_calculator = ComposableRewardCalculator()
    
    # Active rewards (currently enabled) - REBALANCED for 1500-step episodes!
    reward_calculator.add_component(KillAsteroid(reward_per_asteroid=100.0))  # 100 points per kill (most important!)
    reward_calculator.add_component(AccuracyBonus(bonus_per_second=2.0))  # 2 pts/sec (was 15) - 50 points for full episode at 100% accuracy
    
    # Behavioral shaping rewards (NEW - active) - REBALANCED!
    reward_calculator.add_component(FacingAsteroidBonus(bonus_per_second=2.0))  # 2 pts/sec (was 15) - ~50 points for full episode
    reward_calculator.add_component(MaintainingMomentumBonus(bonus_per_second=0.5, penalty_per_second=-1.0))  # 0.5 pts/sec (was 3) - ~12 points for full episode
    
    # Reset reward calculator to ensure clean state
    reward_calculator.reset()
    
    # Available but disabled rewards (can be uncommented to test)
    # reward_calculator.add_component(SurvivalBonus())  # Time alive bonus
    # reward_calculator.add_component(ShootingPenalty())  # -0.5 points per shot (too punishing with ConservingAmmo)
    # reward_calculator.add_component(ChunkBonus())  # Kill multiple asteroids near simultaneously
    # reward_calculator.add_component(NearMiss())  # Reward for close calls
    # reward_calculator.add_component(KPMBonus())  # Kills per minute bonus
    
    # Additional behavioral shaping (implemented but not yet tested)
    # reward_calculator.add_component(ConservingAmmoBonus())  # +5 good shots, -5 bad shots (conflicts with ShootingPenalty)
    # reward_calculator.add_component(LeadingTargetBonus())  # Predictive aiming
    # reward_calculator.add_component(MovingTowardDangerBonus())  # Aggressive play
    # reward_calculator.add_component(SpacingFromWallsBonus())  # Stay away from edges
    
    # Create agent
    agent = GAAgent(individual, state_encoder, action_interface)
    agent.reset()
    
    # Reset state encoder for this episode
    state_encoder_copy = VectorEncoder(
        screen_width=800,
        screen_height=600,
        num_nearest_asteroids=state_encoder.num_nearest_asteroids,
        include_bullets=state_encoder.include_bullets,
        include_global=state_encoder.include_global
    )
    state_encoder_copy.reset()
    
    # Episode variables
    steps = 0
    total_reward = 0.0
    
    # Episode loop
    while steps < max_steps and game.player in game.player_list:
        # Encode state
        state = state_encoder_copy.encode(game.tracker)
        
        # Get action from agent
        action = agent.get_action(state)
        
        # Validate and normalize
        action_interface.validate(action)
        action = action_interface.normalize(action)
        
        # Convert to game input
        game_input = action_interface.to_game_input(action)
        
        # Apply to game
        game.left_pressed = game_input["left_pressed"]
        game.right_pressed = game_input["right_pressed"]
        game.up_pressed = game_input["up_pressed"]
        game.space_pressed = game_input["space_pressed"]
        
        # Step game
        game.on_update(frame_delay)
        
        # Update trackers
        game.tracker.update(game)
        game.metrics_tracker.update(game)
        
        # Calculate step reward
        step_reward = reward_calculator.calculate_step_reward(
            game.tracker,
            game.metrics_tracker
        )
        total_reward += step_reward
        steps += 1
    
    # Calculate final episode reward
    episode_reward = reward_calculator.calculate_episode_reward(game.metrics_tracker)
    total_reward += episode_reward

    # Return detailed metrics for analytics
    metrics = {
        'fitness': total_reward,
        'steps_survived': steps,
        'kills': game.metrics_tracker.total_kills,
        'shots_fired': game.metrics_tracker.total_shots_fired,
        'hits': game.metrics_tracker.total_hits,
        'accuracy': game.metrics_tracker.get_accuracy(),
        'time_alive': game.metrics_tracker.time_alive,
    }
    return metrics


def evaluate_population_parallel(
    population: List[List[float]],
    state_encoder: VectorEncoder,
    action_interface: ActionInterface,
    max_steps: int = 2000,
    max_workers: int = None,
    generation_seed: int = None
) -> Tuple[List[float], int, Dict]:
    """
    Evaluate entire population in parallel.

    Args:
        population: List of parameter vectors
        state_encoder: State encoder instance
        action_interface: Action interface instance
        max_steps: Maximum steps per episode
        max_workers: Number of parallel workers (None = auto)
        generation_seed: Random seed for this generation (all agents face same asteroids)

    Returns:
        Tuple of (List of fitness scores, seed used, aggregated metrics dict)
    """
    # Use a consistent seed for all agents in this generation
    # This ensures fair comparison - all agents face the SAME asteroid configuration
    if generation_seed is None:
        generation_seed = random.randint(0, 2**31 - 1)

    # Use ThreadPoolExecutor for parallel evaluation
    # Threading works well here since game logic is Python-heavy
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all evaluation tasks - ALL use the SAME seed for fair comparison
        futures = [
            executor.submit(
                evaluate_single_agent,
                individual,
                state_encoder,
                action_interface,
                max_steps,
                random_seed=generation_seed  # Same seed for all agents!
            )
            for individual in population
        ]

        # Collect results as they complete
        results = [future.result() for future in futures]

    # Extract fitness scores and aggregate metrics
    fitnesses = [r['fitness'] for r in results]

    # Aggregate behavioral metrics across population
    aggregated_metrics = {
        'avg_steps_survived': sum(r['steps_survived'] for r in results) / len(results),
        'avg_kills': sum(r['kills'] for r in results) / len(results),
        'avg_shots_fired': sum(r['shots_fired'] for r in results) / len(results),
        'avg_accuracy': sum(r['accuracy'] for r in results) / len(results),
        'total_kills': sum(r['kills'] for r in results),
        'total_shots': sum(r['shots_fired'] for r in results),
        'max_kills': max(r['kills'] for r in results),
        'max_steps': max(r['steps_survived'] for r in results),
        # Best agent's detailed stats
        'best_agent_kills': results[fitnesses.index(max(fitnesses))]['kills'],
        'best_agent_steps': results[fitnesses.index(max(fitnesses))]['steps_survived'],
        'best_agent_accuracy': results[fitnesses.index(max(fitnesses))]['accuracy'],
    }

    return fitnesses, generation_seed, aggregated_metrics


def evaluate_agent_visual(
    individual: List[float],
    game,
    state_encoder: VectorEncoder,
    action_interface: ActionInterface,
    reward_calculator: ComposableRewardCalculator,
    max_steps: int = 500
) -> Tuple[float, int]:
    """
    Evaluate agent in the visual game window.
    Used to display the best agent.
    
    Args:
        individual: Parameter vector
        game: Visual AsteroidsGame instance
        state_encoder: State encoder
        action_interface: Action interface
        reward_calculator: Reward calculator
        max_steps: Maximum steps to display
    
    Returns:
        Tuple of (total_reward, steps_survived)
    """
    # Reset game
    game.reset_game()
    
    # Create agent
    agent = GAAgent(individual, state_encoder, action_interface)
    agent.reset()
    
    # Reset everything
    game.tracker.update(game)
    game.metrics_tracker.update(game)
    reward_calculator.reset()
    state_encoder.reset()
    
    # Episode variables
    steps = 0
    total_reward = 0.0
    frame_delay = 1.0 / 60.0
    
    # Episode loop (this will be called incrementally from the training driver)
    # For now, just return - actual stepping happens in the driver
    return total_reward, steps
