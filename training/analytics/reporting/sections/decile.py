"""
Phase breakdown report section.

Generates training progress broken down by fixed phases.
"""

from typing import List, Dict, Any

from training.analytics.analysis.phases import split_generations
from training.analytics.reporting.sections.common import write_takeaways, write_warnings, write_glossary
from training.analytics.reporting.glossary import glossary_entries
from training.config.analytics import AnalyticsConfig


def write_decile_breakdown(f, generations_data: List[Dict[str, Any]]):
    """Write training progress broken down by phases."""
    phases = split_generations(generations_data, phase_count=AnalyticsConfig.PHASE_COUNT)
    if not phases:
        f.write("Not enough data for phase breakdown.\n\n")
        return

    f.write("| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |\n")
    f.write("|-------|------|----------|---------|-----------|---------|-----------|----------|\n")

    for phase in phases:
        phase_data = phase["data"]
        if not phase_data:
            continue

        best_fit = max(g['best_fitness'] for g in phase_data)
        avg_fit = sum(g['avg_fitness'] for g in phase_data) / len(phase_data)
        avg_kills = sum(g.get('avg_kills', 0) for g in phase_data) / len(phase_data)
        avg_acc = sum(g.get('avg_accuracy', 0) for g in phase_data) / len(phase_data)
        avg_steps = sum(g.get('avg_steps', 0) for g in phase_data) / len(phase_data)
        diversity = sum(g.get('std_dev', 0) for g in phase_data) / len(phase_data)

        f.write(
            f"| {phase['label']} | {phase['gen_start']}-{phase['gen_end']} | {best_fit:.0f} | "
            f"{avg_fit:.0f} | {avg_kills:.1f} | {avg_acc*100:.0f}% | {avg_steps:.0f} | {diversity:.0f} |\n"
        )

    f.write("\n")

    takeaways = [
        "Phase breakdown uses equal 25% blocks for run-normalized comparisons.",
    ]
    warnings: List[str] = []

    write_takeaways(f, takeaways)
    write_warnings(f, warnings)
    write_glossary(
        f,
        glossary_entries([
            "best_fitness",
            "avg_fitness",
            "avg_kills",
            "avg_accuracy",
            "avg_steps",
            "std_dev",
        ])
    )
