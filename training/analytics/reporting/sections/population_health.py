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
from training.analytics.reporting.sections.common import write_takeaways, write_warnings, write_glossary
from training.analytics.reporting.glossary import glossary_entries


def write_population_health(f, generations_data: List[Dict[str, Any]]):
    """Write population health dashboard."""
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

    f.write(f"### Current Status: {health_status}\n\n")

    f.write("| Metric | Value | Trend (Recent) |\n")
    f.write("|--------|-------|----------------|\n")

    div_trend = "Increasing" if avg_std_recent > avg_std_early else "Decreasing" if avg_std_recent < avg_std_early else "Stable"
    f.write(f"| Diversity Index | {diversity_index:.2f} | {div_trend} |\n")
    f.write(f"| Elite Gap | {elite_gap:.2f} | Stable |\n")

    floor_dir = "Up" if floor_trend > 0 else "Down" if floor_trend < 0 else "Flat"
    ceiling_dir = "Up" if ceiling_trend > 0 else "Down" if ceiling_trend < 0 else "Flat"
    f.write(f"| Min Fitness Trend | {floor_trend:+.1f} | {floor_dir} |\n")
    f.write(f"| Max Fitness Trend | {ceiling_trend:+.1f} | {ceiling_dir} |\n")

    iqr_change = iqr_recent - iqr_early
    iqr_dir = "Widening" if iqr_change > 0 else "Narrowing" if iqr_change < 0 else "Stable"
    f.write(f"| IQR (p75-p25) | {iqr_recent:.0f} | {iqr_dir} |\n")

    f.write("\n")

    takeaways = [
        f"Health status is {health_status}.",
        f"Diversity index at {diversity_index:.2f} with {div_trend.lower()} spread.",
        f"Fitness floor trend {floor_trend:+.1f}, ceiling trend {ceiling_trend:+.1f}.",
    ]

    write_takeaways(f, takeaways)
    write_warnings(f, warnings)
    write_glossary(
        f,
        glossary_entries([
            "std_dev",
            "avg_fitness",
            "best_fitness",
            "min_fitness",
            "p25_fitness",
            "p75_fitness",
        ])
    )
