"""
Reward component report sections.

Generates reward component evolution and analysis.
"""

from typing import List, Dict, Any

from training.analytics.analysis.behavioral import calculate_reward_evolution


def write_reward_evolution(f, generations_data: List[Dict[str, Any]]):
    """Write reward component evolution across training phases.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if not generations_data or 'avg_reward_breakdown' not in generations_data[-1]:
        f.write("No reward component data available.\n\n")
        return

    evolution = calculate_reward_evolution(generations_data)
    if not evolution:
        f.write("No reward breakdown data available.\n\n")
        return

    f.write("| Component | Phase 1 | Mid | Final | Trend | Status |\n")
    f.write("|-----------|---------|-----|-------|-------|--------|\n")

    # Sort by absolute final value
    sorted_components = sorted(evolution.items(), key=lambda x: abs(x[1]['last']), reverse=True)

    for comp, values in sorted_components:
        first_val = values['first']
        mid_val = values['mid']
        last_val = values['last']
        pct_change = values['pct_change']

        # Trend indicator
        if pct_change > 100:
            trend = "↑↑↑"
        elif pct_change > 50:
            trend = "↑↑"
        elif pct_change > 10:
            trend = "↑"
        elif pct_change < -100:
            trend = "↓↓↓"
        elif pct_change < -50:
            trend = "↓↓"
        elif pct_change < -10:
            trend = "↓"
        else:
            trend = "→"

        # Status
        if last_val > 0 and pct_change > 10:
            status = "Learned"
        elif last_val > 0:
            status = "Stable"
        elif last_val < 0 and first_val < last_val:
            status = "Improving"
        elif last_val < 0:
            status = "Not learned"
        else:
            status = "Negligible"

        f.write(f"| {comp} | {first_val:+.1f} | {mid_val:+.1f} | {last_val:+.1f} | {trend} {pct_change:+.0f}% | {status} |\n")

    f.write("\n")


def write_reward_analysis(f, generations_data: List[Dict[str, Any]]):
    """Analyze and write reward component contributions from the last generation.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if not generations_data or 'avg_reward_breakdown' not in generations_data[-1]:
        f.write("No reward component data available for analysis.\n\n")
        return

    # Analyze the last generation for the most relevant snapshot
    last_gen_breakdown = generations_data[-1].get('avg_reward_breakdown', {})

    if not last_gen_breakdown:
        f.write("Reward breakdown for the last generation is empty.\n\n")
        return

    # Calculate total positive rewards to use as a base for percentages
    total_positive_rewards = sum(v for v in last_gen_breakdown.values() if v > 0)

    sorted_components = sorted(last_gen_breakdown.items(), key=lambda item: abs(item[1]), reverse=True)

    f.write("Based on the average scores from the final generation:\n\n")
    f.write("| Reward Component | Avg. Score per Episode | Pct of Positive Rewards |\n")
    f.write("|------------------|------------------------|-------------------------|\n")

    for component, avg_score in sorted_components:
        percentage = (avg_score / total_positive_rewards) * 100 if total_positive_rewards > 0 else 0
        f.write(f"| {component} | {avg_score:,.2f} | {percentage:+.1f}% |\n")

    f.write("\n")
    f.write("*Note: Percentages are relative to the sum of all positive rewards in the final generation.*\n\n")
