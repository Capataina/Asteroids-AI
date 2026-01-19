"""
Kill efficiency report section.

Generates kill efficiency analysis.
"""

from typing import List, Dict, Any

from training.analytics.analysis.behavioral import calculate_kill_efficiency
from training.analytics.analysis.phases import split_generations
from training.analytics.reporting.sections.common import write_takeaways, write_warnings, write_glossary
from training.analytics.reporting.glossary import glossary_entries
from training.config.analytics import AnalyticsConfig


def write_kill_efficiency(f, generations_data: List[Dict[str, Any]]):
    """Write kill efficiency analysis."""
    if not generations_data or 'avg_kills' not in generations_data[-1]:
        f.write("No behavioral data available for kill efficiency analysis.\n\n")
        return

    phases = split_generations(generations_data, phase_count=AnalyticsConfig.PHASE_COUNT)
    if not phases:
        f.write("No behavioral data available for kill efficiency analysis.\n\n")
        return

    first_eff = calculate_kill_efficiency(phases[0]["data"])
    last_eff = calculate_kill_efficiency(phases[-1]["data"])

    f.write("### Current Performance (Final Phase)\n\n")
    f.write(f"- **Kills per 100 Steps:** {last_eff['kills_per_100']:.2f} (Phase 1: {first_eff['kills_per_100']:.2f})\n")
    f.write(f"- **Shots per Kill:** {last_eff['shots_per_kill']:.2f} (Phase 1: {first_eff['shots_per_kill']:.2f})\n")
    f.write(f"- **Kill Conversion Rate:** {last_eff['conversion_rate']*100:.1f}% (Phase 1: {first_eff['conversion_rate']*100:.1f}%)\n")
    f.write(f"- **Average Kills per Episode:** {last_eff['avg_kills']:.1f}\n\n")

    f.write("### Efficiency Trend (Phase Averages)\n\n")
    f.write("| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |\n")
    f.write("|-------|-----------------|------------|----------------|\n")

    for phase in phases:
        eff = calculate_kill_efficiency(phase["data"])
        f.write(
            f"| {phase['label']} | {eff['kills_per_100']:.2f} | "
            f"{eff['shots_per_kill']:.2f} | {eff['conversion_rate']*100:.1f}% |\n"
        )

    f.write("\n")

    takeaways = [
        f"Kill rate changed from {first_eff['kills_per_100']:.2f} to {last_eff['kills_per_100']:.2f} kills/100 steps.",
        f"Shots per kill moved from {first_eff['shots_per_kill']:.2f} to {last_eff['shots_per_kill']:.2f}.",
    ]
    warnings: List[str] = []

    if last_eff['shots_per_kill'] > first_eff['shots_per_kill'] * 1.2:
        warnings.append("Shots per kill increased, indicating lower shooting efficiency.")

    write_takeaways(f, takeaways)
    write_warnings(f, warnings)
    write_glossary(
        f,
        glossary_entries([
            "avg_kills",
            "avg_steps",
            "avg_shots",
            "avg_accuracy",
            "avg_shots_per_kill",
        ])
    )
