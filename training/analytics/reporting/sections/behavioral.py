"""
Behavioral trends report section.

Generates behavioral metrics trends analysis.
"""

from typing import List, Dict, Any

from training.analytics.analysis.behavioral import calculate_behavioral_by_quarter
from training.analytics.analysis.action_classification import classify_behavior, get_action_rates


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

    f.write("### Performance Metrics by Quarter\n\n")
    f.write("| Period | Avg Kills | Avg Steps | Avg Accuracy | Max Kills |\n")
    f.write("|--------|-----------|-----------|--------------|----------|\n")

    for q in quarters:
        f.write(f"| Q{q['quarter']} | {q['avg_kills']:.2f} | {q['avg_steps']:.0f} | "
                f"{q['avg_accuracy']*100:.1f}% | {q['max_kills']} |\n")

    f.write("\n")

    # Check if we have action data for the latest quarter
    # (Checking the first quarter might fail if we resumed training with new code)
    has_action_data = 'avg_thrust_frames' in generations_data[-1]

    if has_action_data:
        f.write("### Action Distribution & Strategy Evolution\n\n")
        f.write("Analysis of how the population's physical behavior has changed over time.\n\n")
        f.write("| Period | Thrust % | Turn % | Shoot % | Dominant Strategy |\n")
        f.write("|--------|----------|--------|---------|-------------------|\n")

        for q in quarters:
            # Reconstruct a 'metrics' dict from the quarter averages to pass to the classifier
            # The 'quarters' list from calculate_behavioral_by_quarter aggregates keys dynamically
            # providing they exist in the source data.
            
            # Note: We need to handle cases where old data doesn't have these keys
            if 'avg_thrust_frames' not in q:
                f.write(f"| Q{q['quarter']} | N/A | N/A | N/A | *Legacy Data* |\n")
                continue

            rates = get_action_rates(q)
            label = classify_behavior(q)
            
            f.write(f"| Q{q['quarter']} | {rates['thrust_rate']*100:.1f}% | "
                    f"{rates['turn_rate']*100:.1f}% | {rates['shoot_rate']*100:.1f}% | "
                    f"**{label}** |\n")
        
        f.write("\n")
