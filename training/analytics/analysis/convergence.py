"""
Convergence and stagnation analysis.

Provides functions for analyzing training convergence and stagnation patterns.
"""

from typing import List, Dict, Any, Tuple


def analyze_stagnation_periods(generations_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze stagnation periods throughout training.

    Args:
        generations_data: Full list of generation data

    Returns:
        Dictionary with stagnation analysis results
    """
    if not generations_data:
        return {
            'periods': [],
            'avg_stagnation': 0,
            'max_stagnation': 0,
            'num_periods': 0,
        }

    stagnation_periods = []
    current_stagnation = 0
    best_so_far = float('-inf')

    for g in generations_data:
        if g['best_fitness'] > best_so_far:
            if current_stagnation > 0:
                stagnation_periods.append(current_stagnation)
            current_stagnation = 0
            best_so_far = g['best_fitness']
        else:
            current_stagnation += 1

    if current_stagnation > 0:
        stagnation_periods.append(current_stagnation)

    if not stagnation_periods:
        return {
            'periods': [],
            'avg_stagnation': 0,
            'max_stagnation': 0,
            'num_periods': 0,
        }

    return {
        'periods': stagnation_periods,
        'avg_stagnation': sum(stagnation_periods) / len(stagnation_periods),
        'max_stagnation': max(stagnation_periods),
        'num_periods': len(stagnation_periods),
    }


def analyze_convergence(generations_data: List[Dict[str, Any]],
                        recent_count: int = 20) -> Dict[str, Any]:
    """Analyze population convergence.

    Args:
        generations_data: Full list of generation data
        recent_count: Number of recent generations to analyze

    Returns:
        Dictionary with convergence analysis results
    """
    if not generations_data:
        return {}

    recent_gens = generations_data[-recent_count:]
    avg_std_dev = sum(g['std_dev'] for g in recent_gens) / len(recent_gens)
    avg_range = sum(g['best_fitness'] - g['min_fitness'] for g in recent_gens) / len(recent_gens)

    # Calculate diversity trend
    if len(generations_data) >= 20:
        early_std = sum(g['std_dev'] for g in generations_data[:10]) / 10
        late_std = sum(g['std_dev'] for g in generations_data[-10:]) / 10
        diversity_change = ((late_std - early_std) / max(1, early_std)) * 100
    else:
        diversity_change = 0

    # Determine status
    if avg_std_dev < 300:
        status = 'converging'
    elif avg_std_dev < 800:
        status = 'moderate'
    else:
        status = 'exploring'

    return {
        'avg_std_dev': avg_std_dev,
        'avg_range': avg_range,
        'diversity_change': diversity_change,
        'status': status,
    }


def analyze_learning_progress(generations_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze learning progress between early and late training.

    Args:
        generations_data: Full list of generation data

    Returns:
        Dictionary with learning progress analysis
    """
    if len(generations_data) < 5:
        return {}

    n = len(generations_data)
    early_n = max(1, n // 10)
    early = generations_data[:early_n]
    late = generations_data[-early_n:]

    early_best_avg = sum(g['best_fitness'] for g in early) / len(early)
    late_best_avg = sum(g['best_fitness'] for g in late) / len(late)
    early_avg_avg = sum(g['avg_fitness'] for g in early) / len(early)
    late_avg_avg = sum(g['avg_fitness'] for g in late) / len(late)

    best_improvement = ((late_best_avg - early_best_avg) / max(1, abs(early_best_avg))) * 100
    avg_improvement = ((late_avg_avg - early_avg_avg) / max(1, abs(early_avg_avg))) * 100

    # Determine verdict
    if best_improvement > 50 and avg_improvement > 30:
        verdict = 'strong'
    elif best_improvement > 20 or avg_improvement > 20:
        verdict = 'moderate'
    elif best_improvement > 0 or avg_improvement > 0:
        verdict = 'weak'
    else:
        verdict = 'none'

    return {
        'early_n': early_n,
        'early_best_avg': early_best_avg,
        'late_best_avg': late_best_avg,
        'early_avg_avg': early_avg_avg,
        'late_avg_avg': late_avg_avg,
        'best_improvement': best_improvement,
        'avg_improvement': avg_improvement,
        'verdict': verdict,
    }
