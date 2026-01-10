"""
Population health analysis.

Provides functions for analyzing population diversity and health metrics.
"""

from typing import List, Dict, Any, Tuple


def calculate_diversity_metrics(generations_data: List[Dict[str, Any]],
                                 recent_count: int = 10) -> Dict[str, float]:
    """Calculate population diversity metrics.

    Args:
        generations_data: List of generation data dictionaries
        recent_count: Number of recent generations to analyze

    Returns:
        Dictionary with diversity metrics
    """
    if len(generations_data) < 5:
        return {}

    recent = generations_data[-recent_count:]
    early = generations_data[:recent_count]

    avg_std_recent = sum(g['std_dev'] for g in recent) / len(recent)
    avg_std_early = sum(g['std_dev'] for g in early) / len(early)
    avg_mean_recent = sum(g['avg_fitness'] for g in recent) / len(recent)

    # Diversity index (coefficient of variation)
    diversity_index = avg_std_recent / max(1, abs(avg_mean_recent))

    # Elite gap
    avg_best_recent = sum(g['best_fitness'] for g in recent) / len(recent)
    elite_gap = (avg_best_recent - avg_mean_recent) / max(1, abs(avg_mean_recent))

    return {
        'diversity_index': diversity_index,
        'elite_gap': elite_gap,
        'avg_std_recent': avg_std_recent,
        'avg_std_early': avg_std_early,
    }


def calculate_fitness_trends(generations_data: List[Dict[str, Any]],
                              recent_count: int = 10) -> Dict[str, float]:
    """Calculate fitness floor and ceiling trends.

    Args:
        generations_data: List of generation data dictionaries
        recent_count: Number of recent generations to analyze

    Returns:
        Dictionary with trend metrics
    """
    if len(generations_data) < 5:
        return {}

    recent = generations_data[-recent_count:]
    early = generations_data[:recent_count]

    # Floor trend (min fitness improvement)
    min_first = sum(g['min_fitness'] for g in early) / len(early)
    min_last = sum(g['min_fitness'] for g in recent) / len(recent)
    floor_trend = min_last - min_first

    # Ceiling trend
    best_first = sum(g['best_fitness'] for g in early) / len(early)
    best_last = sum(g['best_fitness'] for g in recent) / len(recent)
    ceiling_trend = best_last - best_first

    # IQR trend
    iqr_early = sum(g['p75_fitness'] - g['p25_fitness'] for g in early) / len(early)
    iqr_recent = sum(g['p75_fitness'] - g['p25_fitness'] for g in recent) / len(recent)

    return {
        'floor_trend': floor_trend,
        'ceiling_trend': ceiling_trend,
        'iqr_early': iqr_early,
        'iqr_recent': iqr_recent,
        'min_first': min_first,
        'min_last': min_last,
        'best_first': best_first,
        'best_last': best_last,
    }


def assess_population_health(generations_data: List[Dict[str, Any]]) -> Tuple[str, List[str]]:
    """Assess overall population health status.

    Args:
        generations_data: List of generation data dictionaries

    Returns:
        Tuple of (status, warnings) where status is 'Healthy', 'Watch', or 'Warning'
    """
    if len(generations_data) < 5:
        return 'Unknown', ['Not enough data']

    diversity = calculate_diversity_metrics(generations_data)
    trends = calculate_fitness_trends(generations_data)

    warnings = []
    diversity_index = diversity.get('diversity_index', 0.5)
    elite_gap = diversity.get('elite_gap', 1.0)
    floor_trend = trends.get('floor_trend', 0)

    if diversity_index < 0.2:
        health_status = 'Warning'
        warnings.append('Low diversity - population may be prematurely converged')
    elif diversity_index > 1.0:
        health_status = 'Warning'
        warnings.append('High diversity - population may be too chaotic')
    elif elite_gap > 3.0:
        health_status = 'Warning'
        warnings.append('High elite gap - knowledge not spreading to population')
    elif floor_trend < 0:
        health_status = 'Watch'
        warnings.append('Floor declining - worst agents getting worse')
    else:
        health_status = 'Healthy'

    return health_status, warnings
