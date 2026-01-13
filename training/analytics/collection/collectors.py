"""
Data collection methods for training analytics.

Contains functions for recording generation metrics, fresh game results,
and distribution data.
"""

from typing import List, Dict, Any, Optional

from training.analytics.collection.models import AnalyticsData
from training.analytics.analysis.fitness import median, std_dev, calculate_skewness, calculate_kurtosis


def record_generation(data: AnalyticsData, generation: int, fitness_scores: List[float],
                      behavioral_metrics: Optional[Dict[str, Any]] = None,
                      best_agent_stats: Optional[Dict[str, Any]] = None,
                      timing_stats: Optional[Dict[str, float]] = None,
                      operator_stats: Optional[Dict[str, int]] = None):
    """Record metrics for a generation.

    Args:
        data: AnalyticsData instance to store results
        generation: Generation number
        fitness_scores: List of fitness scores for all agents
        behavioral_metrics: Optional aggregated behavioral metrics
        best_agent_stats: Optional stats for the best agent
        timing_stats: Optional timing metrics (duration of phases)
        operator_stats: Optional genetic operator statistics
    """
    if not fitness_scores:
        return

    sorted_scores = sorted(fitness_scores)
    n = len(sorted_scores)

    gen_data = {
        'generation': generation,
        # Fitness statistics
        'best_fitness': max(fitness_scores),
        'avg_fitness': sum(fitness_scores) / len(fitness_scores),
        'min_fitness': min(fitness_scores),
        'median_fitness': median(fitness_scores),
        'std_dev': std_dev(fitness_scores),
        'population_size': len(fitness_scores),
        # Percentiles for understanding distribution
        'p25_fitness': sorted_scores[n // 4] if n >= 4 else sorted_scores[0],
        'p75_fitness': sorted_scores[3 * n // 4] if n >= 4 else sorted_scores[-1],
        'p90_fitness': sorted_scores[int(n * 0.9)] if n >= 10 else sorted_scores[-1],
    }

    # Add timing stats if available
    if timing_stats:
        gen_data.update(timing_stats)
        
    # Add operator stats if available
    if operator_stats:
        gen_data.update(operator_stats)

    # Calculate improvement metrics
    if data.generations_data:
        prev_best = data.generations_data[-1]['best_fitness']
        prev_avg = data.generations_data[-1]['avg_fitness']
        gen_data['best_improvement'] = gen_data['best_fitness'] - prev_best
        gen_data['avg_improvement'] = gen_data['avg_fitness'] - prev_avg
    else:
        gen_data['best_improvement'] = 0.0
        gen_data['avg_improvement'] = 0.0

    # Update all-time best tracking
    data.update_best_tracking(generation, gen_data['best_fitness'])

    gen_data['all_time_best'] = data.all_time_best_fitness
    gen_data['generations_since_improvement'] = data.generations_since_improvement

    # Add behavioral metrics if available
    if behavioral_metrics:
        gen_data['avg_kills'] = behavioral_metrics.get('avg_kills', 0)
        gen_data['avg_steps'] = behavioral_metrics.get('avg_steps_survived', 0)
        gen_data['avg_accuracy'] = behavioral_metrics.get('avg_accuracy', 0)
        gen_data['avg_shots'] = behavioral_metrics.get('avg_shots_fired', 0)
        
        # Action metrics
        gen_data['avg_thrust_frames'] = behavioral_metrics.get('avg_thrust_frames', 0)
        gen_data['avg_turn_frames'] = behavioral_metrics.get('avg_turn_frames', 0)
        gen_data['avg_shoot_frames'] = behavioral_metrics.get('avg_shoot_frames', 0)
        
        # Input style metrics
        gen_data['avg_thrust_duration'] = behavioral_metrics.get('avg_thrust_duration', 0.0)
        gen_data['avg_turn_duration'] = behavioral_metrics.get('avg_turn_duration', 0.0)
        gen_data['avg_shoot_duration'] = behavioral_metrics.get('avg_shoot_duration', 0.0)
        gen_data['avg_idle_rate'] = behavioral_metrics.get('avg_idle_rate', 0.0)
        
        # Engagement metrics
        gen_data['avg_asteroid_dist'] = behavioral_metrics.get('avg_asteroid_dist', 0.0)
        gen_data['avg_screen_wraps'] = behavioral_metrics.get('avg_screen_wraps', 0.0)
        
        gen_data['total_kills'] = behavioral_metrics.get('total_kills', 0)
        gen_data['max_kills'] = behavioral_metrics.get('max_kills', 0)
        gen_data['max_steps'] = behavioral_metrics.get('max_steps', 0)
        
        # Best agent metrics
        gen_data['best_agent_kills'] = behavioral_metrics.get('best_agent_kills', 0)
        gen_data['best_agent_steps'] = behavioral_metrics.get('best_agent_steps', 0)
        gen_data['best_agent_accuracy'] = behavioral_metrics.get('best_agent_accuracy', 0)
        gen_data['best_agent_thrust'] = behavioral_metrics.get('best_agent_thrust', 0)
        gen_data['best_agent_turn'] = behavioral_metrics.get('best_agent_turn', 0)
        gen_data['best_agent_shoot'] = behavioral_metrics.get('best_agent_shoot', 0)
        
        gen_data['avg_reward_breakdown'] = behavioral_metrics.get('avg_reward_breakdown', {})
        gen_data['avg_quarterly_scores'] = behavioral_metrics.get('avg_quarterly_scores', [])
        
        # Spatial data
        gen_data['best_agent_positions'] = behavioral_metrics.get('best_agent_positions', [])
        gen_data['best_agent_kill_events'] = behavioral_metrics.get('best_agent_kill_events', [])
        gen_data['population_positions'] = behavioral_metrics.get('population_positions', [])
        gen_data['population_kill_events'] = behavioral_metrics.get('population_kill_events', [])

    # Add best agent stats if available
    if best_agent_stats:
        gen_data.update(best_agent_stats)

    data.generations_data.append(gen_data)


def record_fresh_game(data: AnalyticsData, generation: int, fresh_game_data: Dict[str, Any],
                      generalization_metrics: Dict[str, Any]):
    """Record fresh game test results for a generation.

    Args:
        data: AnalyticsData instance to store results
        generation: Generation number
        fresh_game_data: Fresh game performance metrics
        generalization_metrics: Comparison to training performance
    """
    data.fresh_game_data[generation] = {
        'fresh_game': fresh_game_data,
        'generalization_metrics': generalization_metrics
    }

    # Also attach to the generation data if it exists
    for gen_data in data.generations_data:
        if gen_data['generation'] == generation:
            gen_data['fresh_game'] = fresh_game_data
            gen_data['generalization_metrics'] = generalization_metrics
            break


def record_distributions(data: AnalyticsData, generation: int, fitness_values: List[float],
                         per_agent_metrics: List[Dict[str, Any]]):
    """Record per-agent distribution data for a generation.

    Args:
        data: AnalyticsData instance to store results
        generation: Generation number
        fitness_values: List of all fitness scores
        per_agent_metrics: List of per-agent behavioral metrics
    """
    sorted_fitness = sorted(fitness_values)
    sorted_kills = sorted([m.get('kills', 0) for m in per_agent_metrics])
    sorted_steps = sorted([m.get('steps_survived', 0) for m in per_agent_metrics])
    sorted_accuracy = sorted([m.get('accuracy', 0) for m in per_agent_metrics])
    sorted_shots = sorted([m.get('shots_fired', 0) for m in per_agent_metrics])
    sorted_thrust = sorted([m.get('thrust_frames', 0) for m in per_agent_metrics])
    sorted_turn = sorted([m.get('turn_frames', 0) for m in per_agent_metrics])
    sorted_shoot = sorted([m.get('shoot_frames', 0) for m in per_agent_metrics])

    # Calculate distribution statistics
    skewness = calculate_skewness(sorted_fitness)
    kurtosis = calculate_kurtosis(sorted_fitness)

    # Count viable (positive fitness) vs failed agents
    viable_count = sum(1 for f in sorted_fitness if f > 0)
    failed_count = len(sorted_fitness) - viable_count

    distributions = {
        'fitness_values': sorted_fitness,
        'kills_values': sorted_kills,
        'steps_values': sorted_steps,
        'accuracy_values': sorted_accuracy,
        'shots_values': sorted_shots,
        'thrust_values': sorted_thrust,
        'turn_values': sorted_turn,
        'shoot_values': sorted_shoot,
    }

    distribution_stats = {
        'fitness_skewness': skewness,
        'fitness_kurtosis': kurtosis,
        'viable_agent_count': viable_count,
        'failed_agent_count': failed_count,
    }

    data.distributions_data[generation] = {
        'distributions': distributions,
        'distribution_stats': distribution_stats
    }

    # Also attach to generation data if it exists
    for gen_data in data.generations_data:
        if gen_data['generation'] == generation:
            gen_data['distributions'] = distributions
            gen_data['distribution_stats'] = distribution_stats
            break
