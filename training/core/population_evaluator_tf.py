"""
TensorFlow-based Parallel Evaluation for Evolution Strategies.

Evaluates multiple agents simultaneously using threading and TensorFlow policies.
"""

import concurrent.futures
import random
import math
from collections import defaultdict
from typing import List, Tuple, Dict
from game.headless_game import HeadlessAsteroidsGame
from ai_agents.neuroevolution.nn_agent_tf import NNAgentTF
from interfaces.StateEncoder import StateEncoder
from interfaces.ActionInterface import ActionInterface
from training.config.rewards import create_reward_calculator
from training.config.evolution_strategies import ESConfig
from training.components.novelty import compute_behavior_vector
from training.components.diversity import compute_reward_diversity


def evaluate_single_agent_tf(
    individual: List[float],
    state_encoder: StateEncoder,
    action_interface: ActionInterface,
    max_steps: int = 2000,
    frame_delay: float = 1.0 / 60.0,
    random_seed: int = None,
    hidden_size: int = ESConfig.HIDDEN_LAYER_SIZE
) -> Dict:
    """
    Evaluate a single agent using TensorFlow policy in a headless game instance.

    Args:
        individual: Parameter vector for the agent (neural network weights)
        state_encoder: State encoder instance
        action_interface: Action interface instance
        max_steps: Maximum steps per episode
        frame_delay: Time delta per step
        random_seed: Random seed for reproducible asteroid spawning
        hidden_size: Number of hidden neurons in neural network

    Returns:
        Dictionary of metrics including fitness score
    """
    # Create headless game with isolated RNG
    game = HeadlessAsteroidsGame(width=800, height=600, random_seed=random_seed)
    game.reset_game()

    # Create reward calculator from config
    reward_calculator = create_reward_calculator()
    reward_calculator.reset()

    # Create TensorFlow neural network agent
    agent = NNAgentTF(individual, state_encoder, action_interface, hidden_size=hidden_size)
    agent.reset()

    # Reset state encoder for this episode
    state_encoder_copy = state_encoder.clone()
    state_encoder_copy.reset()

    # Episode variables
    steps = 0
    total_reward = 0.0

    # Action counters
    thrust_frames = 0
    turn_frames = 0
    shoot_frames = 0

    # Spatial tracking
    position_history = []
    kill_data = []
    prev_kills = 0
    total_asteroid_distance = 0.0
    distance_samples = 0
    min_asteroid_dist = float('inf')

    # Input analysis tracking
    input_history = []
    idle_frames = 0
    action_counts = defaultdict(int)

    # Neural health tracking
    total_outputs = 0
    saturated_outputs = 0

    # Physics tracking
    screen_wraps = 0
    last_x = game.player.center_x
    last_y = game.player.center_y

    # Episode loop
    while steps < max_steps and game.player in game.player_list:
        # Encode state
        state = state_encoder_copy.encode(game.tracker)

        # Get action from agent
        action_vector = agent.get_action(state)

        # Check output saturation
        for val in action_vector:
            total_outputs += 1
            if val > 0.9 or val < 0.1:
                saturated_outputs += 1

        # Validate and normalize
        action_interface.validate(action_vector)
        action_norm = action_interface.normalize(action_vector)

        # Convert to game input
        game_input = action_interface.to_game_input(action_norm)

        # Apply to game
        game.left_pressed = game_input["left_pressed"]
        game.right_pressed = game_input["right_pressed"]
        game.up_pressed = game_input["up_pressed"]
        game.space_pressed = game_input["space_pressed"]

        # Track actions
        current_inputs = (game.up_pressed, game.left_pressed, game.right_pressed, game.space_pressed)
        input_history.append(current_inputs)

        # Update entropy counter
        action_key = "".join(["1" if x else "0" for x in current_inputs])
        action_counts[action_key] += 1

        if not any(current_inputs):
            idle_frames += 1

        if game.up_pressed:
            thrust_frames += 1
        if game.left_pressed or game.right_pressed:
            turn_frames += 1
        if game.space_pressed:
            shoot_frames += 1

        # Step game
        game.on_update(frame_delay)

        # Track screen wraps
        curr_x = game.player.center_x
        curr_y = game.player.center_y

        if abs(curr_x - last_x) > game.width / 2:
            screen_wraps += 1
        if abs(curr_y - last_y) > game.height / 2:
            screen_wraps += 1

        last_x = curr_x
        last_y = curr_y

        # Update trackers
        game.tracker.update(game)
        game.metrics_tracker.update(game)

        # Track spatial data (subsampled every 60 frames)
        if steps % 60 == 0:
            position_history.append((int(game.player.center_x), int(game.player.center_y)))

        # Track kills
        if game.metrics_tracker.total_kills > prev_kills:
            kill_data.append((int(game.player.center_x), int(game.player.center_y)))
            prev_kills = game.metrics_tracker.total_kills

        # Track distance to nearest threat
        dist = game.tracker.get_distance_to_nearest_asteroid()
        if dist is not None:
            total_asteroid_distance += dist
            distance_samples += 1
            if dist < min_asteroid_dist:
                min_asteroid_dist = dist

        # Calculate step reward
        step_reward = reward_calculator.calculate_step_reward(
            game.tracker,
            game.metrics_tracker
        )
        total_reward += step_reward
        steps += 1

    # Calculate action durations
    def _avg_duration(history, indices):
        durations = []
        current_run = 0
        for step_inputs in history:
            is_active = any(step_inputs[i] for i in indices)
            if is_active:
                current_run += 1
            elif current_run > 0:
                durations.append(current_run)
                current_run = 0
        if current_run > 0:
            durations.append(current_run)
        return sum(durations) / len(durations) if durations else 0.0

    avg_thrust_duration = _avg_duration(input_history, [0])
    avg_turn_duration = _avg_duration(input_history, [1, 2])
    avg_shoot_duration = _avg_duration(input_history, [3])
    idle_rate = idle_frames / steps if steps > 0 else 0.0

    # Metrics: Risk
    if min_asteroid_dist == float('inf'):
        min_asteroid_dist = 0.0

    # Metrics: Neural Saturation
    saturation_rate = saturated_outputs / total_outputs if total_outputs > 0 else 0.0

    # Metrics: Action Entropy
    action_entropy = 0.0
    if steps > 0:
        for count in action_counts.values():
            p = count / steps
            if p > 0:
                action_entropy -= p * math.log2(p)

    # Calculate final episode reward
    episode_reward = reward_calculator.calculate_episode_reward(game.metrics_tracker)
    total_reward += episode_reward

    # Return detailed metrics
    metrics = {
        'fitness': total_reward,
        'steps_survived': steps,
        'kills': game.metrics_tracker.total_kills,
        'shots_fired': game.metrics_tracker.total_shots_fired,
        'hits': game.metrics_tracker.total_hits,
        'accuracy': game.metrics_tracker.get_accuracy(),
        'time_alive': game.metrics_tracker.time_alive,
        'avg_asteroid_dist': total_asteroid_distance / distance_samples if distance_samples > 0 else 0.0,
        'min_asteroid_dist': min_asteroid_dist,
        'reward_breakdown': reward_calculator.get_reward_breakdown(),
        'quarterly_scores': reward_calculator.get_quarterly_scores(),
        'thrust_frames': thrust_frames,
        'turn_frames': turn_frames,
        'shoot_frames': shoot_frames,
        'avg_thrust_duration': avg_thrust_duration,
        'avg_turn_duration': avg_turn_duration,
        'avg_shoot_duration': avg_shoot_duration,
        'idle_rate': idle_rate,
        'screen_wraps': screen_wraps,
        'position_history': position_history,
        'kill_data': kill_data,
        'output_saturation': saturation_rate,
        'action_entropy': action_entropy
    }
    return metrics


def evaluate_population_parallel_tf(
    population: List[List[float]],
    state_encoder: StateEncoder,
    action_interface: ActionInterface,
    max_steps: int = 2000,
    max_workers: int = None,
    generation_seed: int = None,
    seeds_per_agent: int = 3
) -> Tuple[List[float], int, Dict, List[Dict]]:
    """
    Evaluate entire population in parallel with TensorFlow agents.

    Args:
        population: List of parameter vectors
        state_encoder: State encoder instance
        action_interface: Action interface instance
        max_steps: Maximum steps per episode
        max_workers: Number of parallel workers (None = auto)
        generation_seed: Base seed for this generation
        seeds_per_agent: Number of different seeds to evaluate each agent on

    Returns:
        Tuple of:
            - List of averaged fitness scores
            - Base seed used
            - Aggregated metrics dict (population averages)
            - List of per-agent metrics (for distribution tracking)
    """
    # Base seed for this generation
    if generation_seed is None:
        generation_seed = random.randint(0, 2**31 - 1)

    print(f"[DEBUG] ES Evaluation Generation Seed: {generation_seed}")

    # Generate seeds for all evaluations
    all_eval_tasks = []
    for agent_idx, individual in enumerate(population):
        for seed_offset in range(seeds_per_agent):
            seed = generation_seed + agent_idx * seeds_per_agent + seed_offset
            all_eval_tasks.append((agent_idx, individual, seed))

    # Use ThreadPoolExecutor for parallel evaluation
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                evaluate_single_agent_tf,
                individual,
                state_encoder,
                action_interface,
                max_steps,
                random_seed=seed
            )
            for agent_idx, individual, seed in all_eval_tasks
        ]

        # Collect results
        all_results = [future.result() for future in futures]

    # Group results by agent and average
    agent_results = [[] for _ in range(len(population))]
    for i, result in enumerate(all_results):
        agent_idx = i // seeds_per_agent
        agent_results[agent_idx].append(result)

    # Calculate averaged fitness for each agent
    fitnesses = []
    averaged_results = []
    pop_reward_breakdown = {}

    for agent_idx, results in enumerate(agent_results):
        avg_fitness = sum(r['fitness'] for r in results) / len(results)
        fitnesses.append(avg_fitness)

        # Average behavioral metrics
        avg_kills = sum(r['kills'] for r in results) / len(results)
        avg_steps = sum(r['steps_survived'] for r in results) / len(results)
        avg_idle_rate = sum(r.get('idle_rate', 0.0) for r in results) / len(results)
        avg_asteroid_dist = sum(r.get('avg_asteroid_dist', 0.0) for r in results) / len(results)
        avg_screen_wraps = sum(r.get('screen_wraps', 0) for r in results) / len(results)
        avg_thrust = sum(r.get('thrust_frames', 0) for r in results) / len(results)
        avg_turn = sum(r.get('turn_frames', 0) for r in results) / len(results)
        avg_shoot = sum(r.get('shoot_frames', 0) for r in results) / len(results)
        avg_accuracy = sum(r['accuracy'] for r in results) / len(results)

        # New metrics averaging
        avg_min_dist = sum(r.get('min_asteroid_dist', 0.0) for r in results) / len(results)
        avg_saturation = sum(r.get('output_saturation', 0.0) for r in results) / len(results)
        avg_entropy = sum(r.get('action_entropy', 0.0) for r in results) / len(results)

        # Average reward breakdown for this agent
        agent_reward_breakdown = {}
        for r in results:
            for comp, val in r['reward_breakdown'].items():
                if comp not in agent_reward_breakdown:
                    agent_reward_breakdown[comp] = 0.0
                agent_reward_breakdown[comp] += val / len(results)

        # Compute behavior vector for novelty
        agent_metrics_for_behavior = {
            'thrust_frames': avg_thrust,
            'turn_frames': avg_turn,
            'shoot_frames': avg_shoot,
            'accuracy': avg_accuracy,
            'idle_rate': avg_idle_rate,
            'avg_asteroid_dist': avg_asteroid_dist,
            'screen_wraps': avg_screen_wraps,
        }
        behavior_vector = compute_behavior_vector(agent_metrics_for_behavior, avg_steps)

        # Compute reward diversity score
        reward_diversity = compute_reward_diversity(agent_reward_breakdown)

        averaged_results.append({
            'fitness': avg_fitness,
            'steps_survived': avg_steps,
            'kills': avg_kills,
            'shots_fired': sum(r['shots_fired'] for r in results) / len(results),
            'accuracy': avg_accuracy,
            'thrust_frames': avg_thrust,
            'turn_frames': avg_turn,
            'shoot_frames': avg_shoot,
            'idle_rate': avg_idle_rate,
            'avg_asteroid_dist': avg_asteroid_dist,
            'min_asteroid_dist': avg_min_dist,
            'screen_wraps': avg_screen_wraps,
            'reward_breakdown': agent_reward_breakdown,
            'behavior_vector': behavior_vector,
            'reward_diversity': reward_diversity,
            'output_saturation': avg_saturation,
            'action_entropy': avg_entropy,
        })

        # Aggregate reward breakdown
        for r in results:
            for component, score in r['reward_breakdown'].items():
                if component not in pop_reward_breakdown:
                    pop_reward_breakdown[component] = 0.0
                pop_reward_breakdown[component] += score

    # Average reward breakdowns
    num_evals = len(all_results)
    avg_reward_breakdown = {k: v / num_evals for k, v in pop_reward_breakdown.items()}

    # Average quarterly scores
    avg_quarterly = [0.0, 0.0, 0.0, 0.0]
    for r in all_results:
        q_scores = r.get('quarterly_scores', [0, 0, 0, 0])
        for i in range(4):
            avg_quarterly[i] += q_scores[i]
    avg_quarterly = [s / num_evals for s in avg_quarterly]

    # Find best agent
    best_idx = fitnesses.index(max(fitnesses))

    # Aggregate spatial data for best agent
    best_agent_positions = []
    best_agent_kill_events = []
    for r in agent_results[best_idx]:
        best_agent_positions.extend(r.get('position_history', []))
        best_agent_kill_events.extend(r.get('kill_data', []))

    # Collect population spatial data
    sample_size = min(30, len(agent_results))
    sample_indices = random.sample(range(len(agent_results)), sample_size)

    population_positions = []
    population_kill_events = []

    for idx in sample_indices:
        for r in agent_results[idx]:
            population_positions.extend(r.get('position_history', []))
            population_kill_events.extend(r.get('kill_data', []))

    # Aggregate behavioral metrics
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
        'best_agent_kills': averaged_results[best_idx]['kills'],
        'best_agent_steps': averaged_results[best_idx]['steps_survived'],
        'best_agent_accuracy': averaged_results[best_idx]['accuracy'],
        'best_agent_thrust': averaged_results[best_idx]['thrust_frames'],
        'best_agent_turn': averaged_results[best_idx]['turn_frames'],
        'best_agent_shoot': averaged_results[best_idx]['shoot_frames'],
        'avg_asteroid_dist': sum(r.get('avg_asteroid_dist', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_min_dist': sum(r.get('min_asteroid_dist', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_thrust_duration': sum(r.get('avg_thrust_duration', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_turn_duration': sum(r.get('avg_turn_duration', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_shoot_duration': sum(r.get('avg_shoot_duration', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_idle_rate': sum(r.get('idle_rate', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_screen_wraps': sum(r.get('screen_wraps', 0) for r in averaged_results) / len(averaged_results),
        'avg_output_saturation': sum(r.get('output_saturation', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_action_entropy': sum(r.get('action_entropy', 0.0) for r in averaged_results) / len(averaged_results),
        'best_agent_positions': best_agent_positions,
        'best_agent_kill_events': best_agent_kill_events,
        'population_positions': population_positions,
        'population_kill_events': population_kill_events,
        'avg_reward_breakdown': avg_reward_breakdown,
        'avg_quarterly_scores': avg_quarterly,
    }

    return fitnesses, generation_seed, aggregated_metrics, averaged_results
