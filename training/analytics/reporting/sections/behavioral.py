"""
Behavioral trends report section.

Generates behavioral metrics trends analysis.
"""

from typing import List, Dict, Any

from training.analytics.analysis.behavioral import calculate_behavioral_by_quarter


def write_behavioral_trends(f, generations_data: List[Dict[str, Any]]):
    """Analyze and write behavioral metrics trends.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if not generations_data or 'avg_kills' not in generations_data[-1]:
        f.write("No behavioral data available.\n\n")
        return

    quarters = calculate_behavioral_by_quarter(generations_data)
    if not quarters:
        f.write("Not enough data for behavioral trend analysis.\n\n")
        return

    f.write("| Period | Avg Kills | Avg Steps | Avg Accuracy | Max Kills |\n")
    f.write("|--------|-----------|-----------|--------------|----------|\n")

    for q in quarters:
        f.write(f"| Q{q['quarter']} | {q['avg_kills']:.2f} | {q['avg_steps']:.0f} | "
                f"{q['avg_accuracy']*100:.1f}% | {q['max_kills']} |\n")

    f.write("\n")
