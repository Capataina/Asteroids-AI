"""
Population health report section.

Generates population health dashboard.
"""

from typing import List, Dict, Any

from training.analytics.analysis.population import (
    calculate_diversity_metrics,
    calculate_fitness_trends,
    assess_population_health
)


def write_population_health(f, generations_data: List[Dict[str, Any]]):
    """Write population health dashboard.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if len(generations_data) < 5:
        f.write("Not enough data for population health analysis.\n\n")
        return

    diversity = calculate_diversity_metrics(generations_data)
    trends = calculate_fitness_trends(generations_data)
    health_status, warnings = assess_population_health(generations_data)

    diversity_index = diversity.get('diversity_index', 0)
    elite_gap = diversity.get('elite_gap', 0)
    avg_std_recent = diversity.get('avg_std_recent', 0)
    avg_std_early = diversity.get('avg_std_early', 0)

    floor_trend = trends.get('floor_trend', 0)
    ceiling_trend = trends.get('ceiling_trend', 0)
    iqr_early = trends.get('iqr_early', 0)
    iqr_recent = trends.get('iqr_recent', 0)

    status_icon = '🟢' if health_status == 'Healthy' else '🟡' if health_status == 'Watch' else '🔴'
    f.write(f"### Current Status: {status_icon} {health_status}\n\n")

    f.write("| Metric | Value | Trend (Recent) | Status |\n")
    f.write("|--------|-------|----------------|--------|\n")

    div_status = "🟢 Good" if 0.3 <= diversity_index <= 0.7 else "🟡 Watch" if 0.2 <= diversity_index <= 1.0 else "🔴 Warning"
    div_trend = "↓ Decreasing" if avg_std_recent < avg_std_early else "↑ Increasing" if avg_std_recent > avg_std_early else "→ Stable"
    f.write(f"| Diversity Index | {diversity_index:.2f} | {div_trend} | {div_status} |\n")

    gap_status = "🟢 Good" if 0.5 <= elite_gap <= 2.0 else "🟡 Watch" if elite_gap <= 3.0 else "🔴 Warning"
    f.write(f"| Elite Gap | {elite_gap:.2f} | → | {gap_status} |\n")

    floor_status = "🟢 Good" if floor_trend >= 0 else "🟡 Watch"
    f.write(f"| Min Fitness Trend | {floor_trend:+.1f} | {'↑' if floor_trend > 0 else '↓'} | {floor_status} |\n")

    ceiling_status = "🟢 Good" if ceiling_trend > 0 else "🟡 Watch"
    f.write(f"| Max Fitness Trend | {ceiling_trend:+.1f} | {'↑' if ceiling_trend > 0 else '↓'} | {ceiling_status} |\n")

    iqr_change = iqr_recent - iqr_early
    f.write(f"| IQR (p75-p25) | {iqr_recent:.0f} | {'↓' if iqr_change < 0 else '↑'} {abs(iqr_change):.0f} | 🟢 |\n")

    f.write("\n")

    if warnings:
        f.write("### Warnings\n\n")
        for w in warnings:
            f.write(f"- ⚠️ {w}\n")
        f.write("\n")
