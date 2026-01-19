"""
Learning progress report section.

Generates phase-based learning progress analysis.
"""

from typing import List, Dict, Any

from training.analytics.analysis.phases import split_generations
from training.analytics.reporting.insights import trend_stats
from training.analytics.reporting.sections.common import write_takeaways, write_warnings, write_glossary
from training.analytics.reporting.glossary import glossary_entries
from training.config.analytics import AnalyticsConfig


def write_learning_progress(f, generations_data: List[Dict[str, Any]]):
    """Analyze and write learning progress."""
    if len(generations_data) < 5:
        f.write("Not enough data for learning analysis.\n\n")
        return

    phases = split_generations(generations_data, phase_count=AnalyticsConfig.PHASE_COUNT)
    if not phases:
        f.write("Not enough data for learning analysis.\n\n")
        return

    f.write("| Phase | Gens | Avg Best | Avg Mean | Avg Min |\n")
    f.write("|-------|------|----------|----------|---------|\n")

    for phase in phases:
        data = phase["data"]
        avg_best = sum(g['best_fitness'] for g in data) / len(data)
        avg_mean = sum(g['avg_fitness'] for g in data) / len(data)
        avg_min = sum(g['min_fitness'] for g in data) / len(data)
        f.write(
            f"| {phase['label']} | {phase['gen_start']}-{phase['gen_end']} | "
            f"{avg_best:.1f} | {avg_mean:.1f} | {avg_min:.1f} |\n"
        )

    f.write("\n")

    best_trend = trend_stats(generations_data, 'best_fitness', higher_is_better=True, phase_count=AnalyticsConfig.PHASE_COUNT)
    avg_trend = trend_stats(generations_data, 'avg_fitness', higher_is_better=True, phase_count=AnalyticsConfig.PHASE_COUNT)

    takeaways = [
        f"Best fitness trend: {best_trend['tag']} ({best_trend['confidence']}).",
        f"Average fitness trend: {avg_trend['tag']} ({avg_trend['confidence']}).",
    ]

    warnings: List[str] = []
    if "regression" in best_trend["tag"] and "regression" in avg_trend["tag"]:
        warnings.append("Both best and average fitness are regressing across phases.")
    if "stagnation" in best_trend["tag"] and "stagnation" in avg_trend["tag"]:
        warnings.append("Learning appears stalled across phases.")

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
