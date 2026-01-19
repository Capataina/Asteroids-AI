"""
Population health analysis.

Provides functions for analyzing population diversity and health metrics.
"""

from typing import List, Dict, Any, Tuple, List as ListType

from training.analytics.analysis.phases import split_generations
from training.analytics.analysis.convergence import analyze_stagnation_periods


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

    phases = split_generations(generations_data, phase_count=4)
    if not phases:
        return {}
    early = phases[0]["data"]
    recent = phases[-1]["data"]

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

    phases = split_generations(generations_data, phase_count=4)
    if not phases:
        return {}
    early = phases[0]["data"]
    recent = phases[-1]["data"]

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
    floor_trend = trends.get('floor_trend', 0.0)

    # Build historical baselines for relative thresholds
    diversity_series: ListType[float] = []
    elite_gap_series: ListType[float] = []
    for g in generations_data:
        avg_fit = g.get('avg_fitness', 0.0)
        std = g.get('std_dev', 0.0)
        diversity_series.append(std / max(1.0, abs(avg_fit)))
        elite_gap_series.append((g.get('best_fitness', 0.0) - avg_fit) / max(1.0, abs(avg_fit)))

    def _percentile(values: ListType[float], pct: float) -> float:
        if not values:
            return 0.0
        values = sorted(values)
        idx = int(round((pct / 100.0) * (len(values) - 1)))
        return values[max(0, min(len(values) - 1, idx))]

    low_div = _percentile(diversity_series, 15)
    high_div = _percentile(diversity_series, 85)
    high_gap = _percentile(elite_gap_series, 85)

    # Stagnation relative to history
    stag_stats = analyze_stagnation_periods(generations_data)
    current_stag = generations_data[-1].get('generations_since_improvement', 0)
    avg_stag = stag_stats.get('avg_stagnation', 0.0)
    max_stag = stag_stats.get('max_stagnation', 0)

    health_status = 'Healthy'

    if current_stag > max(5, avg_stag * 1.5, max_stag):
        health_status = 'Warning'
        warnings.append(f"Stagnation spike ({current_stag} gens) vs historical mean {avg_stag:.1f}")
    if diversity_index < low_div:
        health_status = 'Warning'
        warnings.append("Diversity compressed vs run baseline (risk of premature convergence)")
    elif diversity_index > high_div:
        health_status = 'Warning'
        warnings.append("Diversity inflated vs run baseline (population may be too chaotic)")

    if elite_gap > high_gap:
        warnings.append("Elite gap unusually high vs run baseline (knowledge not spreading)")

    if floor_trend < 0:
        warnings.append("Fitness floor trending down (weakest agents worsening)")
        if health_status == 'Healthy':
            health_status = 'Watch'

    return health_status, warnings
