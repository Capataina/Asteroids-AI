"""
Stagnation analysis report section.

Generates stagnation pattern analysis.
"""

from typing import List, Dict, Any

from training.analytics.analysis.convergence import analyze_stagnation_periods


def write_stagnation_analysis(f, generations_data: List[Dict[str, Any]],
                               generations_since_improvement: int):
    """Analyze and write stagnation patterns.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
        generations_since_improvement: Current stagnation counter
    """
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

    if current > max_stagnation:
        f.write("**Warning:** Current stagnation exceeds previous maximum. Consider:\n")
        f.write("- Increasing mutation rate\n")
        f.write("- Reducing elitism\n")
        f.write("- Adding fresh random individuals\n\n")
