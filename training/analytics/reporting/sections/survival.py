"""
Survival distribution report section.

Generates survival distribution analysis.
"""

from typing import List, Dict, Any

from training.analytics.analysis.phases import split_generations
from training.analytics.reporting.sections.common import write_takeaways, write_warnings, write_glossary
from training.analytics.reporting.glossary import glossary_entries
from training.config.analytics import AnalyticsConfig


def write_survival_distribution(f, generations_data: List[Dict[str, Any]], config: Dict[str, Any]):
    """Write survival distribution analysis."""
    if not generations_data or 'avg_steps' not in generations_data[-1]:
        f.write("No survival data available.\n\n")
        return

    phases = split_generations(generations_data, phase_count=AnalyticsConfig.PHASE_COUNT)
    if not phases:
        f.write("No survival data available.\n\n")
        return

    max_steps_config = config.get('max_steps', 1500)
    final_phase = phases[-1]["data"]

    avg_survival = sum(g.get('avg_steps', 0) for g in final_phase) / len(final_phase)
    max_survival = max(g.get('max_steps', 0) for g in final_phase)

    f.write("### Survival Statistics (Final Phase)\n\n")
    f.write(f"- **Mean Survival:** {avg_survival:.0f} steps ({avg_survival/max_steps_config*100:.1f}% of max)\n")
    f.write(f"- **Max Survival:** {max_survival:.0f} steps\n\n")

    f.write("### Survival Progression (Phase Averages)\n\n")
    f.write("| Phase | Mean Steps | Change vs Prior |\n")
    f.write("|-------|------------|-----------------|\n")

    prev_survival = None
    for phase in phases:
        phase_survival = sum(g.get('avg_steps', 0) for g in phase["data"]) / len(phase["data"])
        change = ""
        if prev_survival is not None:
            delta = phase_survival - prev_survival
            change = f"{delta:+.0f}"
        f.write(f"| {phase['label']} | {phase_survival:.0f} | {change} |\n")
        prev_survival = phase_survival

    f.write("\n")

    takeaways = [
        f"Final-phase survival averages {avg_survival:.0f} steps.",
        f"Best survival reached {max_survival:.0f} steps.",
    ]
    warnings = []

    if avg_survival < 0.5 * max_steps_config:
        warnings.append("Average survival remains below half of max steps; survivability is still limited.")

    write_takeaways(f, takeaways)
    write_warnings(f, warnings)
    write_glossary(
        f,
        glossary_entries([
            "avg_steps",
            "max_steps",
        ])
    )
