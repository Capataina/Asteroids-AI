"""
Parallel Evaluation for Genetic Algorithm

Evaluates multiple agents simultaneously using threading for massive speedup.
"""

import concurrent.futures
import random
import math
from collections import defaultdict
from typing import List, Tuple, Dict, Optional
from game.headless_game import HeadlessAsteroidsGame
from game import globals
from ai_agents.neuroevolution.nn_agent import NNAgent
from interfaces.StateEncoder import StateEncoder
from interfaces.encoders.VectorEncoder import VectorEncoder
from interfaces.ActionInterface import ActionInterface
from training.config.rewards import create_reward_calculator
from training.config.genetic_algorithm import GAConfig
from training.config.pareto import ParetoConfig
from training.components.novelty import compute_behavior_vector
from training.components.diversity import compute_reward_diversity


def evaluate_single_agent(
    individual: List[float],
    state_encoder: VectorEncoder,
    action_interface: ActionInterface,
    max_steps: int = 2000,
    frame_delay: float = 1.0 / 60.0,
    random_seed: int = None,
    hidden_size: int = GAConfig.HIDDEN_LAYER_SIZE
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
    
    # Create reward calculator from config
    reward_calculator = create_reward_calculator(
        max_steps=max_steps,
        frame_delay=frame_delay
    )
    reward_calculator.reset()

    # Create neural network agent
    agent = NNAgent(individual, state_encoder, action_interface, hidden_size=hidden_size)
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

    # Detailed turn tracking (for diagnosing spin behavior)
    left_only_frames = 0   # Left pressed, right not pressed
    right_only_frames = 0  # Right pressed, left not pressed
    both_turn_frames = 0   # Both left and right pressed (cancel out)
    
    # Spatial tracking
    position_history = []
    kill_data = []
    prev_kills = 0
    total_asteroid_distance = 0.0
    distance_samples = 0
    min_asteroid_dist = float('inf') # Risk profiling
    
    # Input analysis tracking
    input_history = []  # List of (up, left, right, space) tuples
    idle_frames = 0
    action_counts = defaultdict(int) # For entropy
    
    # Neural health tracking
    total_outputs = 0
    saturated_outputs = 0

    # Signed turn tracking
    turn_value_sum = 0.0
    turn_value_sq_sum = 0.0
    turn_value_abs_sum = 0.0
    turn_deadzone_frames = 0
    turn_left_frames = 0
    turn_right_frames = 0
    turn_switches = 0
    current_turn_streak = 0
    longest_turn_streak = 0
    total_turn_streak = 0
    turn_streak_count = 0
    last_turn_sign = 0
    turn_deadzone = 0.0

    # Aim alignment tracking
    frontness_sum = 0.0
    frontness_samples = 0
    frontness_at_shot_sum = 0.0
    frontness_at_hit_sum = 0.0
    shot_alignment_samples = 0
    hit_alignment_samples = 0
    shot_distance_sum = 0.0
    hit_distance_sum = 0.0

    # Danger exposure tracking
    danger_distance = globals.ASTEROID_BASE_RADIUS * globals.ASTEROID_SCALE_LARGE * 3.0
    danger_frames = 0
    danger_entries = 0
    danger_wraps = 0
    danger_active = False

    # Soft-min TTC risk proxy (seconds)
    softmin_ttc_sum = 0.0
    softmin_ttc_samples = 0
    reaction_pending = False
    reaction_timer = 0
    reaction_times = []

    # Movement tracking
    distance_traveled = 0.0
    speed_sum = 0.0
    speed_sq_sum = 0.0
    speed_samples = 0
    grid_rows = 3
    grid_cols = 4
    visited_cells = set()

    # Shooting cooldown tracking
    cooldown_ready_frames = 0
    cooldown_used_frames = 0

    # Physics tracking
    screen_wraps = 0
    last_x = game.player.center_x
    last_y = game.player.center_y

    prev_shots = game.metrics_tracker.total_shots_fired
    prev_hits = game.metrics_tracker.total_hits

    def _compute_frontness() -> Tuple[Optional[float], Optional[float]]:
        """Return (frontness, distance) to nearest asteroid, or (None, None)."""
        player = game.player
        nearest = game.tracker.get_nearest_asteroid()
        if player is None or nearest is None:
            return None, None

        rel_x = nearest.center_x - player.center_x
        rel_y = nearest.center_y - player.center_y

        if abs(rel_x) > game.width / 2:
            rel_x = -1 * math.copysign(game.width - abs(rel_x), rel_x)
        if abs(rel_y) > game.height / 2:
            rel_y = -1 * math.copysign(game.height - abs(rel_y), rel_y)

        dist = math.sqrt(rel_x**2 + rel_y**2)
        ast_angle = math.degrees(math.atan2(rel_x, rel_y))
        angle_diff = ast_angle - player.angle
        while angle_diff > 180:
            angle_diff -= 360
        while angle_diff < -180:
            angle_diff += 360

        frontness = 1.0 - (abs(angle_diff) / 180.0)
        frontness = max(0.0, min(1.0, frontness))
        return frontness, dist
    
    # Episode loop
    while steps < max_steps and game.player in game.player_list:
        # Encode state
        state = state_encoder_copy.encode(game.tracker)
        
        # Get action from agent
        action_vector = agent.get_action(state)
        
        # Check output saturation (values >0.9 or <0.1)
        # NNAgent returns raw sigmoid outputs (0-1)
        for val in action_vector:
            total_outputs += 1
            if val > 0.9 or val < 0.1:
                saturated_outputs += 1
        
        # Validate and normalize
        action_interface.validate(action_vector)
        action_norm = action_interface.normalize(action_vector)

        # Track signed turn behavior before thresholding to inputs
        if len(action_norm) == 3:
            turn_value = (action_norm[0] * 2.0) - 1.0
        else:
            turn_value = action_norm[1] - action_norm[0]

        turn_value_sum += turn_value
        turn_value_sq_sum += turn_value * turn_value
        turn_value_abs_sum += abs(turn_value)

        turn_sign = 0
        if abs(turn_value) <= turn_deadzone:
            turn_deadzone_frames += 1
        elif turn_value > 0:
            turn_right_frames += 1
            turn_sign = 1
        else:
            turn_left_frames += 1
            turn_sign = -1

        if turn_sign != 0:
            if last_turn_sign == 0:
                current_turn_streak = 1
            elif turn_sign == last_turn_sign:
                current_turn_streak += 1
            else:
                turn_switches += 1
                total_turn_streak += current_turn_streak
                turn_streak_count += 1
                if current_turn_streak > longest_turn_streak:
                    longest_turn_streak = current_turn_streak
                current_turn_streak = 1
            last_turn_sign = turn_sign
        else:
            if last_turn_sign != 0:
                total_turn_streak += current_turn_streak
                turn_streak_count += 1
                if current_turn_streak > longest_turn_streak:
                    longest_turn_streak = current_turn_streak
                current_turn_streak = 0
                last_turn_sign = 0
        
        # Convert to game input
        game_input = action_interface.to_game_input(action_norm)

        # Apply to game
        game.left_pressed = game_input["left_pressed"]
        game.right_pressed = game_input["right_pressed"]
        game.up_pressed = game_input["up_pressed"]
        game.space_pressed = game_input["space_pressed"]

        # Aim alignment (pre-step, same state as the action)
        step_frontness, step_nearest_dist = _compute_frontness()
        if step_frontness is not None:
            frontness_sum += step_frontness
            frontness_samples += 1

        # Shooting cooldown usage (pre-step)
        if game.player.shoot_timer <= 0:
            cooldown_ready_frames += 1
            if game.space_pressed:
                cooldown_used_frames += 1

        # Track actions
        current_inputs = (game.up_pressed, game.left_pressed, game.right_pressed, game.space_pressed)
        input_history.append(current_inputs)
        
        # Update entropy counter
        # Use a string key for the action combination: "0101" -> Up:False, Left:True, Right:False, Space:True
        action_key = "".join(["1" if x else "0" for x in current_inputs])
        action_counts[action_key] += 1
        
        if not any(current_inputs):
            idle_frames += 1

        if game.up_pressed:
            thrust_frames += 1
        if game.left_pressed or game.right_pressed:
            turn_frames += 1
            # Detailed turn tracking
            if game.left_pressed and game.right_pressed:
                both_turn_frames += 1
            elif game.left_pressed:
                left_only_frames += 1
            else:  # right_pressed only
                right_only_frames += 1
        if game.space_pressed:
            shoot_frames += 1
        
        # Step game
        game.on_update(frame_delay)

        # Track screen wraps
        # If position jumped by more than half screen, it wrapped
        curr_x = game.player.center_x
        curr_y = game.player.center_y
        wrap_count = 0
        if abs(curr_x - last_x) > game.width / 2:
            screen_wraps += 1
            wrap_count += 1
        if abs(curr_y - last_y) > game.height / 2:
            screen_wraps += 1
            wrap_count += 1

        distance_traveled += game.tracker.get_distance(last_x, last_y, curr_x, curr_y)
        speed = math.sqrt(game.player.change_x**2 + game.player.change_y**2)
        speed_sum += speed
        speed_sq_sum += speed * speed
        speed_samples += 1

        cell_x = int(curr_x / (game.width / grid_cols))
        cell_y = int(curr_y / (game.height / grid_rows))
        cell_x = max(0, min(grid_cols - 1, cell_x))
        cell_y = max(0, min(grid_rows - 1, cell_y))
        visited_cells.add((cell_x, cell_y))
            
        last_x = curr_x
        last_y = curr_y
        
        # Update trackers
        game.tracker.update(game)
        game.metrics_tracker.update(game)
        
        # Track spatial data (subsampled every 60 frames / 1s)
        if steps % 60 == 0:
            position_history.append((int(game.player.center_x), int(game.player.center_y)))
            
        # Track kills
        if game.metrics_tracker.total_kills > prev_kills:
            # Record kill event (approximate location is player's location since we lack target ID)
            # ideally we'd want target location but this is a good proxy for "where the action is"
            kill_data.append((int(game.player.center_x), int(game.player.center_y)))
            prev_kills = game.metrics_tracker.total_kills
            
        # Track distance to nearest threat (for Safe Space analysis)
        dist = game.tracker.get_distance_to_nearest_asteroid()
        if dist is not None:
            total_asteroid_distance += dist
            distance_samples += 1
            if dist < min_asteroid_dist:
                min_asteroid_dist = dist

            in_danger = dist <= danger_distance
            if in_danger:
                danger_frames += 1
                if wrap_count > 0:
                    danger_wraps += wrap_count

                if not danger_active:
                    danger_entries += 1
                    danger_active = True
                    if game.up_pressed or game.left_pressed or game.right_pressed:
                        reaction_times.append(0)
                        reaction_pending = False
                    else:
                        reaction_pending = True
                        reaction_timer = 0

                if reaction_pending:
                    reaction_timer += 1
                    if game.up_pressed or game.left_pressed or game.right_pressed:
                        reaction_times.append(reaction_timer)
                        reaction_pending = False
            else:
                danger_active = False
            reaction_pending = False
            reaction_timer = 0
        else:
            danger_active = False
            reaction_pending = False
            reaction_timer = 0

        # Soft-min TTC across all asteroids (closest matters, others still count)
        if game.player:
            asteroids = game.asteroid_list
            if asteroids:
                ttc_values = []
                player_x = game.player.center_x
                player_y = game.player.center_y
                player_vx = game.player.change_x
                player_vy = game.player.change_y
                ttc_max = ParetoConfig.RISK_TTC_MAX
                tau = ParetoConfig.RISK_TAU
                for ast in asteroids:
                    dx = ast.center_x - player_x
                    dy = ast.center_y - player_y
                    if abs(dx) > game.width / 2:
                        dx = -1 * math.copysign(game.width - abs(dx), dx)
                    if abs(dy) > game.height / 2:
                        dy = -1 * math.copysign(game.height - abs(dy), dy)

                    dist = math.sqrt(dx * dx + dy * dy)
                    radius = globals.ASTEROID_BASE_RADIUS * ast.this_scale
                    if dist <= 1e-6:
                        ttc = 0.0
                    else:
                        rel_vx = ast.change_x - player_vx
                        rel_vy = ast.change_y - player_vy
                        closing_speed = -(dx * rel_vx + dy * rel_vy) / dist
                        if closing_speed <= 1e-6:
                            ttc = ttc_max
                        else:
                            ttc_frames = max(0.0, (dist - radius) / closing_speed)
                            ttc = ttc_frames * frame_delay
                            ttc = min(ttc, ttc_max)
                    ttc_values.append(ttc)

                if ttc_values:
                    if tau <= 1e-6:
                        softmin_ttc = min(ttc_values)
                    else:
                        weights = [math.exp(-ttc / tau) for ttc in ttc_values]
                        weight_sum = sum(weights)
                        if weight_sum <= 0.0:
                            softmin_ttc = ttc_max
                        else:
                            softmin_ttc = sum(w * ttc for w, ttc in zip(weights, ttc_values)) / weight_sum
                    softmin_ttc_sum += softmin_ttc
                    softmin_ttc_samples += 1
            else:
                softmin_ttc_sum += ParetoConfig.RISK_TTC_MAX
                softmin_ttc_samples += 1
        
        # Calculate step reward
        step_reward = reward_calculator.calculate_step_reward(
            game.tracker,
            game.metrics_tracker
        )
        total_reward += step_reward
        steps += 1

        shots_now = game.metrics_tracker.total_shots_fired
        if shots_now > prev_shots:
            shot_count = shots_now - prev_shots
            if step_frontness is not None:
                frontness_at_shot_sum += step_frontness * shot_count
                shot_distance_sum += step_nearest_dist * shot_count
                shot_alignment_samples += shot_count
            prev_shots = shots_now

        hits_now = game.metrics_tracker.total_hits
        if hits_now > prev_hits:
            hit_count = hits_now - prev_hits
            if step_frontness is not None:
                frontness_at_hit_sum += step_frontness * hit_count
                hit_distance_sum += step_nearest_dist * hit_count
                hit_alignment_samples += hit_count
            prev_hits = hits_now
    
    # Calculate action durations
    def _avg_duration(history, indices):
        durations = []
        current_run = 0
        for step_inputs in history:
            # Check if ANY of the tracked indices are active (e.g. left OR right for turn)
            is_active = any(step_inputs[i] for i in indices)
            if is_active:
                current_run += 1
            elif current_run > 0:
                durations.append(current_run)
                current_run = 0
        if current_run > 0: durations.append(current_run)
        
        # DEBUG: Trace why this might be 0.0 if thrust_frames > 0
        if not durations and indices == [0] and thrust_frames > 0:
             # Just checking the first few items to see what's wrong
             # print(f"[DEBUG] Thrust frames: {thrust_frames}, History len: {len(history)}, First 10: {history[:10]}")
             pass
             
        return sum(durations) / len(durations) if durations else 0.0

    avg_thrust_duration = _avg_duration(input_history, [0]) # Up
    avg_turn_duration = _avg_duration(input_history, [1, 2]) # Left or Right
    avg_shoot_duration = _avg_duration(input_history, [3]) # Space
    idle_rate = idle_frames / steps if steps > 0 else 0.0
    
    # Metrics: Risk
    if min_asteroid_dist == float('inf'): min_asteroid_dist = 0.0

    if current_turn_streak > 0:
        total_turn_streak += current_turn_streak
        turn_streak_count += 1
        if current_turn_streak > longest_turn_streak:
            longest_turn_streak = current_turn_streak

    turn_value_mean = turn_value_sum / steps if steps > 0 else 0.0
    turn_value_var = (turn_value_sq_sum / steps) - (turn_value_mean * turn_value_mean) if steps > 0 else 0.0
    turn_value_std = math.sqrt(max(0.0, turn_value_var))
    turn_abs_mean = turn_value_abs_sum / steps if steps > 0 else 0.0
    turn_deadzone_rate = turn_deadzone_frames / steps if steps > 0 else 0.0
    total_turn_signed = turn_left_frames + turn_right_frames
    turn_switch_rate = turn_switches / max(1, total_turn_signed)
    turn_balance = (turn_right_frames - turn_left_frames) / max(1, total_turn_signed)
    avg_turn_streak = total_turn_streak / max(1, turn_streak_count)

    frontness_avg = frontness_sum / frontness_samples if frontness_samples > 0 else 0.0
    frontness_at_shot = frontness_at_shot_sum / shot_alignment_samples if shot_alignment_samples > 0 else 0.0
    frontness_at_hit = frontness_at_hit_sum / hit_alignment_samples if hit_alignment_samples > 0 else 0.0
    shot_distance_avg = shot_distance_sum / shot_alignment_samples if shot_alignment_samples > 0 else 0.0
    hit_distance_avg = hit_distance_sum / hit_alignment_samples if hit_alignment_samples > 0 else 0.0

    danger_exposure_rate = danger_frames / steps if steps > 0 else 0.0
    avg_reaction_time = sum(reaction_times) / len(reaction_times) if reaction_times else 0.0
    avg_softmin_ttc = softmin_ttc_sum / softmin_ttc_samples if softmin_ttc_samples > 0 else ParetoConfig.RISK_TTC_MAX

    avg_speed = speed_sum / speed_samples if speed_samples > 0 else 0.0
    speed_var = (speed_sq_sum / speed_samples) - (avg_speed * avg_speed) if speed_samples > 0 else 0.0
    std_speed = math.sqrt(max(0.0, speed_var))
    coverage_ratio = len(visited_cells) / (grid_rows * grid_cols) if grid_rows * grid_cols > 0 else 0.0

    cooldown_ready_rate = cooldown_ready_frames / steps if steps > 0 else 0.0
    cooldown_usage_rate = cooldown_used_frames / max(1, cooldown_ready_frames)
    
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

    # Return detailed metrics for analytics
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
        # Detailed turn metrics for diagnosing spin behavior
        'left_only_frames': left_only_frames,
        'right_only_frames': right_only_frames,
        'both_turn_frames': both_turn_frames,
        'avg_thrust_duration': avg_thrust_duration,
        'avg_turn_duration': avg_turn_duration,
        'avg_shoot_duration': avg_shoot_duration,
        'idle_rate': idle_rate,
        'screen_wraps': screen_wraps,
        'turn_value_mean': turn_value_mean,
        'turn_value_std': turn_value_std,
        'turn_abs_mean': turn_abs_mean,
        'turn_deadzone_rate': turn_deadzone_rate,
        'turn_switch_rate': turn_switch_rate,
        'turn_balance': turn_balance,
        'turn_left_rate': turn_left_frames / steps if steps > 0 else 0.0,
        'turn_right_rate': turn_right_frames / steps if steps > 0 else 0.0,
        'avg_turn_streak': avg_turn_streak,
        'max_turn_streak': longest_turn_streak,
        'frontness_avg': frontness_avg,
        'frontness_at_shot': frontness_at_shot,
        'frontness_at_hit': frontness_at_hit,
        'shot_distance_avg': shot_distance_avg,
        'hit_distance_avg': hit_distance_avg,
        'danger_exposure_rate': danger_exposure_rate,
        'danger_entries': danger_entries,
        'avg_reaction_time': avg_reaction_time,
        'danger_wraps': danger_wraps,
        'softmin_ttc': avg_softmin_ttc,
        'distance_traveled': distance_traveled,
        'avg_speed': avg_speed,
        'std_speed': std_speed,
        'coverage_ratio': coverage_ratio,
        'cooldown_ready_rate': cooldown_ready_rate,
        'cooldown_usage_rate': cooldown_usage_rate,
        'position_history': position_history,
        'kill_data': kill_data,
        'output_saturation': saturation_rate,
        'action_entropy': action_entropy
    }
    return metrics


def evaluate_population_parallel(
    population: List[List[float]],
    state_encoder: StateEncoder,
    action_interface: ActionInterface,
    max_steps: int = 2000,
    max_workers: int = None,
    generation_seed: int = None,
    seeds_per_agent: int = 3,
    use_common_seeds: bool = False
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
        use_common_seeds: If True, all agents use the same seed set (CRN for ES).
                          If False, each agent gets unique seeds (default, GA-style).

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

    print(f"[DEBUG] Evaluation Generation Seed: {generation_seed} (CRN: {use_common_seeds})")

    def _std(values: List[float]) -> float:
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        var = sum((v - mean) ** 2 for v in values) / len(values)
        return math.sqrt(var)

    # Generate seeds for all evaluations
    all_eval_tasks = []
    for agent_idx, individual in enumerate(population):
        for seed_offset in range(seeds_per_agent):
            if use_common_seeds:
                # CRN mode: All agents use the same seed set within a generation
                # This ensures fitness differences reflect parameter differences, not seed luck
                # Seed set changes across generations to maintain generalization pressure
                seed = generation_seed + seed_offset
            else:
                # Default mode: Each agent gets unique seeds
                # Agent i gets seeds: [base + i*seeds_per_agent + 0, base + i*seeds_per_agent + 1, ...]
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
        avg_steps = sum(r['steps_survived'] for r in results) / len(results)
        avg_idle_rate = sum(r.get('idle_rate', 0.0) for r in results) / len(results)
        avg_asteroid_dist = sum(r.get('avg_asteroid_dist', 0.0) for r in results) / len(results)
        avg_screen_wraps = sum(r.get('screen_wraps', 0) for r in results) / len(results)
        avg_thrust = sum(r.get('thrust_frames', 0) for r in results) / len(results)
        avg_turn = sum(r.get('turn_frames', 0) for r in results) / len(results)
        avg_shoot = sum(r.get('shoot_frames', 0) for r in results) / len(results)
        avg_accuracy = sum(r['accuracy'] for r in results) / len(results)
        avg_hits = sum(r.get('hits', 0) for r in results) / len(results)
        avg_thrust_duration = sum(r.get('avg_thrust_duration', 0.0) for r in results) / len(results)
        avg_turn_duration = sum(r.get('avg_turn_duration', 0.0) for r in results) / len(results)
        avg_shoot_duration = sum(r.get('avg_shoot_duration', 0.0) for r in results) / len(results)
        avg_time_alive = sum(r.get('time_alive', 0.0) for r in results) / len(results)
        
        # New metrics averaging
        avg_min_dist = sum(r.get('min_asteroid_dist', 0.0) for r in results) / len(results)
        avg_saturation = sum(r.get('output_saturation', 0.0) for r in results) / len(results)
        avg_entropy = sum(r.get('action_entropy', 0.0) for r in results) / len(results)
        avg_turn_value_mean = sum(r.get('turn_value_mean', 0.0) for r in results) / len(results)
        avg_turn_value_std = sum(r.get('turn_value_std', 0.0) for r in results) / len(results)
        avg_turn_abs_mean = sum(r.get('turn_abs_mean', 0.0) for r in results) / len(results)
        avg_turn_deadzone_rate = sum(r.get('turn_deadzone_rate', 0.0) for r in results) / len(results)
        avg_turn_switch_rate = sum(r.get('turn_switch_rate', 0.0) for r in results) / len(results)
        avg_turn_balance = sum(r.get('turn_balance', 0.0) for r in results) / len(results)
        avg_turn_left_rate = sum(r.get('turn_left_rate', 0.0) for r in results) / len(results)
        avg_turn_right_rate = sum(r.get('turn_right_rate', 0.0) for r in results) / len(results)
        avg_turn_streak = sum(r.get('avg_turn_streak', 0.0) for r in results) / len(results)
        avg_max_turn_streak = sum(r.get('max_turn_streak', 0.0) for r in results) / len(results)
        avg_frontness = sum(r.get('frontness_avg', 0.0) for r in results) / len(results)
        avg_frontness_shot = sum(r.get('frontness_at_shot', 0.0) for r in results) / len(results)
        avg_frontness_hit = sum(r.get('frontness_at_hit', 0.0) for r in results) / len(results)
        avg_shot_distance = sum(r.get('shot_distance_avg', 0.0) for r in results) / len(results)
        avg_hit_distance = sum(r.get('hit_distance_avg', 0.0) for r in results) / len(results)
        avg_danger_exposure = sum(r.get('danger_exposure_rate', 0.0) for r in results) / len(results)
        avg_danger_entries = sum(r.get('danger_entries', 0.0) for r in results) / len(results)
        avg_reaction_time = sum(r.get('avg_reaction_time', 0.0) for r in results) / len(results)
        avg_danger_wraps = sum(r.get('danger_wraps', 0.0) for r in results) / len(results)
        avg_softmin_ttc = sum(r.get('softmin_ttc', 0.0) for r in results) / len(results)
        avg_distance_traveled = sum(r.get('distance_traveled', 0.0) for r in results) / len(results)
        avg_speed = sum(r.get('avg_speed', 0.0) for r in results) / len(results)
        avg_speed_std = sum(r.get('std_speed', 0.0) for r in results) / len(results)
        avg_coverage_ratio = sum(r.get('coverage_ratio', 0.0) for r in results) / len(results)
        avg_cooldown_ready_rate = sum(r.get('cooldown_ready_rate', 0.0) for r in results) / len(results)
        avg_cooldown_usage_rate = sum(r.get('cooldown_usage_rate', 0.0) for r in results) / len(results)

        fitness_std = _std([r['fitness'] for r in results])
        shots_per_kill = (sum(r.get('shots_fired', 0) for r in results) / len(results)) / max(0.1, avg_kills)
        shots_per_hit = (sum(r.get('shots_fired', 0) for r in results) / len(results)) / max(0.1, avg_hits)

        # Detailed turn metrics averaging
        avg_left_only = sum(r.get('left_only_frames', 0) for r in results) / len(results)
        avg_right_only = sum(r.get('right_only_frames', 0) for r in results) / len(results)
        avg_both_turn = sum(r.get('both_turn_frames', 0) for r in results) / len(results)

        # Average reward breakdown for this agent
        agent_reward_breakdown = {}
        for r in results:
            for comp, val in r['reward_breakdown'].items():
                if comp not in agent_reward_breakdown:
                    agent_reward_breakdown[comp] = 0.0
                agent_reward_breakdown[comp] += val / len(results)

        # Compute behavior vector for novelty calculation
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
            'time_alive': avg_time_alive,
            'kills': avg_kills,
            'shots_fired': sum(r['shots_fired'] for r in results) / len(results),
            'accuracy': avg_accuracy,
            'hits': avg_hits,
            'thrust_frames': avg_thrust,
            'turn_frames': avg_turn,
            'shoot_frames': avg_shoot,
            # Detailed turn metrics
            'left_only_frames': avg_left_only,
            'right_only_frames': avg_right_only,
            'both_turn_frames': avg_both_turn,
            'avg_thrust_duration': avg_thrust_duration,
            'avg_turn_duration': avg_turn_duration,
            'avg_shoot_duration': avg_shoot_duration,
            'idle_rate': avg_idle_rate,
            'avg_asteroid_dist': avg_asteroid_dist,
            'min_asteroid_dist': avg_min_dist,
            'screen_wraps': avg_screen_wraps,
            'turn_value_mean': avg_turn_value_mean,
            'turn_value_std': avg_turn_value_std,
            'turn_abs_mean': avg_turn_abs_mean,
            'turn_deadzone_rate': avg_turn_deadzone_rate,
            'turn_switch_rate': avg_turn_switch_rate,
            'turn_balance': avg_turn_balance,
            'turn_left_rate': avg_turn_left_rate,
            'turn_right_rate': avg_turn_right_rate,
            'avg_turn_streak': avg_turn_streak,
            'max_turn_streak': avg_max_turn_streak,
            'frontness_avg': avg_frontness,
            'frontness_at_shot': avg_frontness_shot,
            'frontness_at_hit': avg_frontness_hit,
            'shot_distance_avg': avg_shot_distance,
            'hit_distance_avg': avg_hit_distance,
            'danger_exposure_rate': avg_danger_exposure,
            'danger_entries': avg_danger_entries,
            'avg_reaction_time': avg_reaction_time,
            'danger_wraps': avg_danger_wraps,
            'softmin_ttc': avg_softmin_ttc,
            'distance_traveled': avg_distance_traveled,
            'avg_speed': avg_speed,
            'std_speed': avg_speed_std,
            'coverage_ratio': avg_coverage_ratio,
            'cooldown_ready_rate': avg_cooldown_ready_rate,
            'cooldown_usage_rate': avg_cooldown_usage_rate,
            'shots_per_kill': shots_per_kill,
            'shots_per_hit': shots_per_hit,
            'fitness_std': fitness_std,
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
    
    # Average the collected reward breakdowns across all evaluations
    num_evals = len(all_results)
    avg_reward_breakdown = {k: v / num_evals for k, v in pop_reward_breakdown.items()}
    
    # Average quarterly scores across all evaluations
    # Each result has [q1, q2, q3, q4]
    avg_quarterly = [0.0, 0.0, 0.0, 0.0]
    for r in all_results:
        q_scores = r.get('quarterly_scores', [0,0,0,0])
        for i in range(4):
            avg_quarterly[i] += q_scores[i]
            
    avg_quarterly = [s / num_evals for s in avg_quarterly]


    # Find best agent (by averaged fitness)
    best_idx = fitnesses.index(max(fitnesses))
    
    # Aggregate spatial data for the best agent across all their seeds
    best_agent_positions = []
    best_agent_kill_events = []
    for r in agent_results[best_idx]:
        best_agent_positions.extend(r.get('position_history', []))
        best_agent_kill_events.extend(r.get('kill_data', []))

    # Collect population spatial data (sample of up to 30 agents)
    # This represents the "average" behavior of the generation
    sample_size = min(30, len(agent_results))
    sample_indices = random.sample(range(len(agent_results)), sample_size)
    
    population_positions = []
    population_kill_events = []
    
    for idx in sample_indices:
        for r in agent_results[idx]:
            population_positions.extend(r.get('position_history', []))
            population_kill_events.extend(r.get('kill_data', []))

    # Aggregate behavioral metrics across population (using averaged per-agent metrics)
    aggregated_metrics = {
        'avg_steps_survived': sum(r['steps_survived'] for r in averaged_results) / len(averaged_results),
        'avg_time_alive': sum(r.get('time_alive', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_kills': sum(r['kills'] for r in averaged_results) / len(averaged_results),
        'avg_shots_fired': sum(r['shots_fired'] for r in averaged_results) / len(averaged_results),
        'avg_accuracy': sum(r['accuracy'] for r in averaged_results) / len(averaged_results),
        'avg_hits': sum(r['hits'] for r in averaged_results) / len(averaged_results),
        'avg_thrust_frames': sum(r['thrust_frames'] for r in averaged_results) / len(averaged_results),
        'avg_turn_frames': sum(r['turn_frames'] for r in averaged_results) / len(averaged_results),
        'avg_shoot_frames': sum(r['shoot_frames'] for r in averaged_results) / len(averaged_results),
        'avg_shots_per_kill': sum(r['shots_per_kill'] for r in averaged_results) / len(averaged_results),
        'avg_shots_per_hit': sum(r['shots_per_hit'] for r in averaged_results) / len(averaged_results),
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
        'avg_asteroid_dist': sum(r.get('avg_asteroid_dist', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_min_dist': sum(r.get('min_asteroid_dist', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_thrust_duration': sum(r.get('avg_thrust_duration', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_turn_duration': sum(r.get('avg_turn_duration', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_shoot_duration': sum(r.get('avg_shoot_duration', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_idle_rate': sum(r.get('idle_rate', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_screen_wraps': sum(r.get('screen_wraps', 0) for r in averaged_results) / len(averaged_results),
        'avg_output_saturation': sum(r.get('output_saturation', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_action_entropy': sum(r.get('action_entropy', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_turn_value_mean': sum(r.get('turn_value_mean', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_turn_value_std': sum(r.get('turn_value_std', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_turn_abs_mean': sum(r.get('turn_abs_mean', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_turn_deadzone_rate': sum(r.get('turn_deadzone_rate', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_turn_switch_rate': sum(r.get('turn_switch_rate', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_turn_balance': sum(r.get('turn_balance', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_turn_left_rate': sum(r.get('turn_left_rate', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_turn_right_rate': sum(r.get('turn_right_rate', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_turn_streak': sum(r.get('avg_turn_streak', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_max_turn_streak': sum(r.get('max_turn_streak', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_frontness': sum(r.get('frontness_avg', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_frontness_at_shot': sum(r.get('frontness_at_shot', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_frontness_at_hit': sum(r.get('frontness_at_hit', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_shot_distance': sum(r.get('shot_distance_avg', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_hit_distance': sum(r.get('hit_distance_avg', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_danger_exposure_rate': sum(r.get('danger_exposure_rate', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_danger_entries': sum(r.get('danger_entries', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_danger_reaction_time': sum(r.get('avg_reaction_time', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_danger_wraps': sum(r.get('danger_wraps', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_softmin_ttc': sum(r.get('softmin_ttc', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_distance_traveled': sum(r.get('distance_traveled', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_speed': sum(r.get('avg_speed', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_speed_std': sum(r.get('std_speed', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_coverage_ratio': sum(r.get('coverage_ratio', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_cooldown_ready_rate': sum(r.get('cooldown_ready_rate', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_cooldown_usage_rate': sum(r.get('cooldown_usage_rate', 0.0) for r in averaged_results) / len(averaged_results),
        'avg_fitness_std': sum(r.get('fitness_std', 0.0) for r in averaged_results) / len(averaged_results),
        # Detailed turn metrics for diagnosing spin behavior
        'avg_left_only_frames': sum(r.get('left_only_frames', 0) for r in averaged_results) / len(averaged_results),
        'avg_right_only_frames': sum(r.get('right_only_frames', 0) for r in averaged_results) / len(averaged_results),
        'avg_both_turn_frames': sum(r.get('both_turn_frames', 0) for r in averaged_results) / len(averaged_results),
        'best_agent_positions': best_agent_positions,
        'best_agent_kill_events': best_agent_kill_events,
        'population_positions': population_positions,
        'population_kill_events': population_kill_events,
        'avg_reward_breakdown': avg_reward_breakdown,
        'avg_quarterly_scores': avg_quarterly,
    }

    # Return per-agent metrics list for distribution tracking
    return fitnesses, generation_seed, aggregated_metrics, averaged_results
