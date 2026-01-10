"""
Parallel Evaluation for Genetic Algorithm

Evaluates multiple agents simultaneously using threading for massive speedup.
"""

import concurrent.futures
import random
from typing import List, Tuple, Dict
from game.headless_game import HeadlessAsteroidsGame
from ai_agents.neuroevolution.genetic_algorithm.nn_ga_agent import NeuralNetworkGAAgent
from interfaces.encoders.VectorEncoder import VectorEncoder
from interfaces.ActionInterface import ActionInterface
from interfaces.RewardCalculator import ComposableRewardCalculator
from interfaces.rewards.SurvivalBonus import SurvivalBonus
from interfaces.rewards.VelocitySurvivalBonus import VelocitySurvivalBonus
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
from interfaces.rewards.DeathPenalty import DeathPenalty
from interfaces.rewards.ProximityPenalty import ProximityPenalty
from interfaces.rewards.VelocityKillBonus import VelocityKillBonus
from interfaces.rewards.ExplorationBonus import ExplorationBonus
from interfaces.rewards.ProximityFacingBonus import ProximityFacingBonus
from interfaces.rewards.DistanceBasedKillReward import DistanceBasedKillReward


def evaluate_single_agent(
    individual: List[float],
    state_encoder: VectorEncoder,
    action_interface: ActionInterface,
    max_steps: int = 2000,
    frame_delay: float = 1.0 / 60.0,
    random_seed: int = None,
    hidden_size: int = 24
) -> float:
    """
    Evaluate a single agent in a headless game instance.

    Args:
        individual: Parameter vector for the agent (neural network weights)
        state_encoder: State encoder instance
        action_interface: Action interface instance
        max_steps: Maximum steps per episode
        frame_delay: Time delta per step
        random_seed: Random seed for reproducible asteroid spawning
        hidden_size: Number of hidden neurons in neural network

    Returns:
        Fitness score (total reward)
    """
    # Create headless game with isolated RNG for reproducible asteroid spawning
    # Each game has its own Random instance, so parallel evaluations don't interfere
    game = HeadlessAsteroidsGame(width=800, height=600, random_seed=random_seed)
    game.reset_game()
    
    # Create reward calculator
    reward_calculator = ComposableRewardCalculator()

    # === REWARD CONFIGURATION V3: Aiming & Threat Prioritization ===
    # MUST MATCH train_ga_parallel.py exactly!

    # 1. Survival baseline (Replaced with VelocitySurvivalBonus to discourage camping)
    # Reward moving while surviving. Max speed is ~5-10 usually, so cap at 15.
    reward_calculator.add_component(VelocitySurvivalBonus(reward_multiplier=3.0, max_velocity_cap=15.0))

    # 2. Kill rewards - more reward for killing close threats (teaches aiming indirectly)
    reward_calculator.add_component(DistanceBasedKillReward(
        max_reward_per_kill=15.0,
        min_distance=50.0,
        max_distance=400.0
    ))

    # 3. Accuracy incentive - reward hits, penalize misses
    reward_calculator.add_component(ConservingAmmoBonus(hit_bonus=12.0, shot_penalty=-5.0))

    # 4. Exploration - small incentive to move around
    reward_calculator.add_component(ExplorationBonus(
        screen_width=800,
        screen_height=600,
        grid_rows=3,
        grid_cols=4,
        bonus_per_cell=10.0
    ))

    # 5. Death penalty (Increased to -150 to balance risk of high speed)
    reward_calculator.add_component(DeathPenalty(penalty=-150.0))

    # Reset reward calculator to ensure clean state
    reward_calculator.reset()

    # Create neural network agent
    agent = NeuralNetworkGAAgent(individual, state_encoder, action_interface, hidden_size=hidden_size)
    agent.reset()

    # Reset state encoder for this episode (copy all config from original)
    # Note: num_nearest_asteroids should be 5 to match train_ga_parallel.py
    state_encoder_copy = VectorEncoder(
        screen_width=state_encoder.screen_width,
        screen_height=state_encoder.screen_height,
        num_nearest_asteroids=5,  # Must match train_ga_parallel.py
        include_bullets=state_encoder.include_bullets,
        include_global=state_encoder.include_global,
        max_player_velocity=state_encoder.max_player_velocity,
        max_asteroid_velocity=state_encoder.max_asteroid_velocity,
        max_asteroid_size=state_encoder.max_asteroid_size,
        max_asteroid_hp=state_encoder.max_asteroid_hp,
    )
    state_encoder_copy.reset()
    
    # Episode variables
    steps = 0
    total_reward = 0.0

    # Action counters
    thrust_frames = 0
    turn_frames = 0
    shoot_frames = 0
    
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

        # Track actions
        if game.up_pressed:
            thrust_frames += 1
        if game.left_pressed or game.right_pressed:
            turn_frames += 1
        if game.space_pressed:
            shoot_frames += 1
        
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
        'reward_breakdown': reward_calculator.get_reward_breakdown(),
        'thrust_frames': thrust_frames,
        'turn_frames': turn_frames,
        'shoot_frames': shoot_frames,
    }
    return metrics


def evaluate_population_parallel(
    population: List[List[float]],
    state_encoder: VectorEncoder,
    action_interface: ActionInterface,
    max_steps: int = 2000,
    max_workers: int = None,
    generation_seed: int = None,
    seeds_per_agent: int = 3
) -> Tuple[List[float], int, Dict, List[Dict]]:
    """
    Evaluate entire population in parallel with multiple seeds per agent.

    Each agent is evaluated on multiple different seeds and their fitness
    is averaged. This selects for generalization rather than luck on one seed.

    Args:
        population: List of parameter vectors
        state_encoder: State encoder instance
        action_interface: Action interface instance
        max_steps: Maximum steps per episode
        max_workers: Number of parallel workers (None = auto)
        generation_seed: Base seed for this generation (used to derive per-agent seeds)
        seeds_per_agent: Number of different seeds to evaluate each agent on (default: 3)

    Returns:
        Tuple of:
            - List of averaged fitness scores
            - Base seed used
            - Aggregated metrics dict (population averages)
            - List of per-agent metrics (for distribution tracking)
    """
    # Base seed for this generation - used to derive unique seeds
    if generation_seed is None:
        generation_seed = random.randint(0, 2**31 - 1)

    # Generate seeds for all evaluations: each agent gets `seeds_per_agent` different seeds
    # Agent i gets seeds: [base + i*seeds_per_agent + 0, base + i*seeds_per_agent + 1, ...]
    all_eval_tasks = []
    for agent_idx, individual in enumerate(population):
        for seed_offset in range(seeds_per_agent):
            seed = generation_seed + agent_idx * seeds_per_agent + seed_offset
            all_eval_tasks.append((agent_idx, individual, seed))

    # Use ThreadPoolExecutor for parallel evaluation
    # All 300 evaluations (100 agents × 3 seeds) run in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                evaluate_single_agent,
                individual,
                state_encoder,
                action_interface,
                max_steps,
                random_seed=seed
            )
            for agent_idx, individual, seed in all_eval_tasks
        ]

        # Collect results as they complete
        all_results = [future.result() for future in futures]

    # Group results by agent and average their fitness
    agent_results = [[] for _ in range(len(population))]
    for i, result in enumerate(all_results):
        agent_idx = i // seeds_per_agent
        agent_results[agent_idx].append(result)

    # Calculate averaged fitness for each agent
    fitnesses = []
    averaged_results = []  # Store averaged metrics per agent for aggregation
    pop_reward_breakdown = {}
    for agent_idx, results in enumerate(agent_results):
        avg_fitness = sum(r['fitness'] for r in results) / len(results)
        fitnesses.append(avg_fitness)

        # Also average the behavioral metrics for this agent
        avg_kills = sum(r['kills'] for r in results) / len(results)
        averaged_results.append({
            'fitness': avg_fitness,
            'steps_survived': sum(r['steps_survived'] for r in results) / len(results),
            'kills': avg_kills,
            'shots_fired': sum(r['shots_fired'] for r in results) / len(results),
            'accuracy': sum(r['accuracy'] for r in results) / len(results),
            'thrust_frames': sum(r.get('thrust_frames', 0) for r in results) / len(results),
            'turn_frames': sum(r.get('turn_frames', 0) for r in results) / len(results),
            'shoot_frames': sum(r.get('shoot_frames', 0) for r in results) / len(results),
        })

        # Aggregate reward breakdown
        for r in results:
            for component, score in r['reward_breakdown'].items():
                if component not in pop_reward_breakdown:
                    pop_reward_breakdown[component] = 0.0
                pop_reward_breakdown[component] += score
    
    # Average the collected reward breakdowns across all evaluations
    num_evals = len(all_results)
    avg_reward_breakdown = {k: v / num_evals for k, v in pop_reward_breakdown.items()}


    # Find best agent (by averaged fitness)
    best_idx = fitnesses.index(max(fitnesses))

    # Aggregate behavioral metrics across population (using averaged per-agent metrics)
    aggregated_metrics = {
        'avg_steps_survived': sum(r['steps_survived'] for r in averaged_results) / len(averaged_results),
        'avg_kills': sum(r['kills'] for r in averaged_results) / len(averaged_results),
        'avg_shots_fired': sum(r['shots_fired'] for r in averaged_results) / len(averaged_results),
        'avg_accuracy': sum(r['accuracy'] for r in averaged_results) / len(averaged_results),
        'avg_thrust_frames': sum(r['thrust_frames'] for r in averaged_results) / len(averaged_results),
        'avg_turn_frames': sum(r['turn_frames'] for r in averaged_results) / len(averaged_results),
        'avg_shoot_frames': sum(r['shoot_frames'] for r in averaged_results) / len(averaged_results),
        'total_kills': sum(r['kills'] for r in averaged_results),
        'total_shots': sum(r['shots_fired'] for r in averaged_results),
        'max_kills': max(r['kills'] for r in averaged_results),
        'max_steps': max(r['steps_survived'] for r in averaged_results),
        # Best agent's stats (averaged across their seeds)
        'best_agent_kills': averaged_results[best_idx]['kills'],
        'best_agent_steps': averaged_results[best_idx]['steps_survived'],
        'best_agent_accuracy': averaged_results[best_idx]['accuracy'],
        'best_agent_thrust': averaged_results[best_idx]['thrust_frames'],
        'best_agent_turn': averaged_results[best_idx]['turn_frames'],
        'best_agent_shoot': averaged_results[best_idx]['shoot_frames'],
        'avg_reward_breakdown': avg_reward_breakdown,
    }

    # Return per-agent metrics list for distribution tracking
    return fitnesses, generation_seed, aggregated_metrics, averaged_results


def evaluate_agent_visual(
    individual: List[float],
    game,
    state_encoder: VectorEncoder,
    action_interface: ActionInterface,
    reward_calculator: ComposableRewardCalculator,
    max_steps: int = 500,
    hidden_size: int = 24
) -> Tuple[float, int]:
    """
    Evaluate agent in the visual game window.
    Used to display the best agent.

    Args:
        individual: Parameter vector (neural network weights)
        game: Visual AsteroidsGame instance
        state_encoder: State encoder
        action_interface: Action interface
        reward_calculator: Reward calculator
        max_steps: Maximum steps to display
        hidden_size: Number of hidden neurons in neural network

    Returns:
        Tuple of (total_reward, steps_survived)
    """
    # Reset game
    game.reset_game()

    # Create neural network agent
    agent = NeuralNetworkGAAgent(individual, state_encoder, action_interface, hidden_size=hidden_size)
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
