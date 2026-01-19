"""
Reward component report sections.

Generates reward component evolution and analysis.
"""

from typing import List, Dict, Any

from training.analytics.analysis.behavioral import calculate_reward_evolution
from training.analytics.reporting.sections.common import write_takeaways, write_warnings, write_glossary
from training.analytics.reporting.glossary import glossary_entries
from training.config.analytics import AnalyticsConfig


def write_reward_evolution(f, generations_data: List[Dict[str, Any]]):
    """Write reward component evolution across training phases."""
    if not generations_data or 'avg_reward_breakdown' not in generations_data[-1]:
        f.write("No reward component data available.\n\n")
        return

    evolution = calculate_reward_evolution(generations_data)
    if not evolution:
        f.write("No reward breakdown data available.\n\n")
        return

    f.write("| Component | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Trend | Status |\n")
    f.write("|-----------|---------|---------|---------|---------|-------|--------|\n")

    # Sort by absolute final value
    sorted_components = sorted(evolution.items(), key=lambda x: abs(x[1]['last']), reverse=True)
    takeaways: List[str] = []
    warnings: List[str] = []

    for comp, values in sorted_components:
        phase_values = values.get("phases", [])
        while len(phase_values) < AnalyticsConfig.PHASE_COUNT:
            phase_values.append(0.0)
        first_val = phase_values[0]
        last_val = phase_values[-1]
        pct_change = values['pct_change']

        delta = last_val - first_val
        direction = "up" if delta > 0 else "down" if delta < 0 else "flat"

        if pct_change >= 120:
            trend = "+++"
        elif pct_change >= 60:
            trend = "++"
        elif pct_change >= 20:
            trend = "+"
        elif pct_change <= -120:
            trend = "---"
        elif pct_change <= -60:
            trend = "--"
        elif pct_change <= -20:
            trend = "-"
        else:
            trend = "~"

        if last_val > 0 and pct_change > 20:
            status = "Learned"
        elif last_val > 0 and abs(pct_change) <= 20:
            status = "Stable"
        elif last_val < 0 and delta > 0:
            status = "Improving penalty"
        elif last_val < 0 and delta < 0:
            status = "Worsening penalty"
        else:
            status = "Neutral"

        f.write(
            f"| {comp} | {phase_values[0]:+.1f} | {phase_values[1]:+.1f} | "
            f"{phase_values[2]:+.1f} | {phase_values[3]:+.1f} | "
            f"{trend} {pct_change:+.0f}% | {status} |\n"
        )

        if abs(pct_change) >= 60 and len(takeaways) < 3:
            takeaways.append(
                f"{comp} shifted {direction} by {pct_change:+.0f}% from Phase 1 to Phase 4."
            )
        if last_val < 0 and delta < 0:
            warnings.append(f"{comp} penalty deepened (more negative over time).")

    f.write("\n")

    # Exploration Efficiency Analysis
    if 'ExplorationBonus' in [c for c, _ in sorted_components]:
        n = len(generations_data)
        final_phase = generations_data[-max(1, n // 10):]

        avg_expl_score = sum(g.get('avg_reward_breakdown', {}).get('ExplorationBonus', 0) for g in final_phase) / len(final_phase)
        avg_steps = sum(g.get('avg_steps', 1) for g in final_phase) / len(final_phase)

        expl_rate = avg_expl_score / max(1, avg_steps)

        f.write(f"**Exploration Efficiency (Final Phase):** {expl_rate:.4f} score/step\n")
        f.write("- *A higher rate indicates faster map traversal, independent of survival time.*\n\n")

    if not takeaways:
        takeaways.append("Reward component shifts are modest or mixed across phases.")

    write_takeaways(f, takeaways)
    write_warnings(f, warnings)
    write_glossary(f, glossary_entries(["avg_reward_breakdown"]))


def write_reward_analysis(f, generations_data: List[Dict[str, Any]]):
    """Analyze and write reward component contributions from the last generation."""
    if not generations_data or 'avg_reward_breakdown' not in generations_data[-1]:
        f.write("No reward component data available for analysis.\n\n")
        return

    last_gen_breakdown = generations_data[-1].get('avg_reward_breakdown', {})
    if not last_gen_breakdown:
        f.write("Reward breakdown for the last generation is empty.\n\n")
        return

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
