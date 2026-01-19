"""
Stagnation analysis report section.

Generates stagnation pattern analysis.
"""

from typing import List, Dict, Any

from training.analytics.analysis.convergence import analyze_stagnation_periods
from training.analytics.reporting.sections.common import write_takeaways, write_warnings, write_glossary
from training.analytics.reporting.glossary import glossary_entries


def _percentile(values: List[int], pct: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    idx = int(round((pct / 100.0) * (len(values) - 1)))
    return values[max(0, min(len(values) - 1, idx))]


def write_stagnation_analysis(f, generations_data: List[Dict[str, Any]],
                               generations_since_improvement: int):
    """Analyze and write stagnation patterns."""
    if not generations_data:
        f.write("No data available.\n\n")
        return

    stag = analyze_stagnation_periods(generations_data)
    periods = stag['periods']

    if not periods:
        f.write("No stagnation periods detected - fitness improved every generation!\n\n")
        return

    avg_stagnation = stag['avg_stagnation']
    max_stagnation = stag['max_stagnation']
    num_periods = stag['num_periods']
    current = generations_since_improvement

    f.write(f"- **Current Stagnation:** {current} generations\n")
    f.write(f"- **Average Stagnation Period:** {avg_stagnation:.1f} generations\n")
    f.write(f"- **Longest Stagnation:** {max_stagnation} generations\n")
    f.write(f"- **Number of Stagnation Periods:** {num_periods}\n\n")

    warnings: List[str] = []
    takeaways: List[str] = []

    p75 = _percentile(periods, 75)
    p90 = _percentile(periods, 90)

    if current >= p90 and current > 0:
        warnings.append("Current stagnation is in the top 10% of historical plateaus.")
    elif current >= p75 and current > 0:
        warnings.append("Current stagnation is above typical plateaus.")

    takeaways.append(f"Stagnation periods average {avg_stagnation:.1f} generations.")
    takeaways.append(f"Longest plateau reached {max_stagnation} generations.")

    write_takeaways(f, takeaways)
    write_warnings(f, warnings)
    write_glossary(
        f,
        glossary_entries([
            "best_fitness",
        ])
    )
