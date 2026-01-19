"""
Trend analysis report section.

Generates phase-based fitness trend analysis.
"""

from typing import List, Dict, Any

from training.analytics.analysis.phases import split_generations
from training.analytics.reporting.insights import trend_stats
from training.analytics.reporting.sections.common import write_takeaways, write_warnings, write_glossary
from training.analytics.reporting.glossary import glossary_entries
from training.config.analytics import AnalyticsConfig


def write_trend_analysis(f, generations_data: List[Dict[str, Any]]):
    """Analyze and write fitness trends over time."""
    if len(generations_data) < 10:
        f.write("Not enough data for trend analysis.\n\n")
        return

    phases = split_generations(generations_data, phase_count=AnalyticsConfig.PHASE_COUNT)
    if not phases:
        f.write("Not enough data for trend analysis.\n\n")
        return

    f.write("| Phase | Avg Best | Avg Mean | Avg Min | Improvement |\n")
    f.write("|-------|----------|----------|---------|-------------|\n")

    prev_avg_best = None
    for phase in phases:
        data = phase["data"]
        avg_best = sum(g['best_fitness'] for g in data) / len(data)
        avg_mean = sum(g['avg_fitness'] for g in data) / len(data)
        avg_min = sum(g['min_fitness'] for g in data) / len(data)

        improvement = ""
        if prev_avg_best is not None:
            delta = avg_best - prev_avg_best
            improvement = f"{delta:+.1f}"

        f.write(f"| {phase['label']} | {avg_best:.1f} | {avg_mean:.1f} | {avg_min:.1f} | {improvement} |\n")
        prev_avg_best = avg_best

    f.write("\n")

    best_trend = trend_stats(generations_data, 'best_fitness', higher_is_better=True, phase_count=AnalyticsConfig.PHASE_COUNT)
    avg_trend = trend_stats(generations_data, 'avg_fitness', higher_is_better=True, phase_count=AnalyticsConfig.PHASE_COUNT)
    min_trend = trend_stats(generations_data, 'min_fitness', higher_is_better=True, phase_count=AnalyticsConfig.PHASE_COUNT)

    takeaways = [
        f"Best fitness: {best_trend['tag']} ({best_trend['confidence']}).",
        f"Average fitness: {avg_trend['tag']} ({avg_trend['confidence']}).",
        f"Minimum fitness: {min_trend['tag']} ({min_trend['confidence']}).",
    ]

    warnings = []
    if "regression" in min_trend["tag"]:
        warnings.append("Fitness floor is degrading; weakest agents are worsening.")

    write_takeaways(f, takeaways)
    write_warnings(f, warnings)
    write_glossary(
        f,
        glossary_entries([
            "best_fitness",
            "avg_fitness",
            "min_fitness",
        ])
    )
