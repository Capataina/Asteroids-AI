"""
Reward balance warnings report section.

Automatically detects potential issues with reward configuration
and surfaces them as actionable warnings.
"""

from typing import List, Dict, Any, Tuple


def analyze_reward_balance(generations_data: List[Dict[str, Any]]) -> Tuple[List[str], List[str]]:
    """Analyze reward components for potential issues.

    Args:
        generations_data: List of generation data dictionaries

    Returns:
        Tuple of (warnings, confirmations) lists
    """
    warnings = []
    confirmations = []

    if not generations_data or 'avg_reward_breakdown' not in generations_data[-1]:
        return warnings, confirmations

    # Get first and last phase data
    n = len(generations_data)
    phase_size = max(1, n // 10)
    first_phase = generations_data[:phase_size]
    last_phase = generations_data[-phase_size:]

    def avg_component(data, comp):
        values = [g.get('avg_reward_breakdown', {}).get(comp, 0) for g in data]
        return sum(values) / len(values) if values else 0

    # Get all components from last generation
    components = list(generations_data[-1].get('avg_reward_breakdown', {}).keys())
    if not components:
        return warnings, confirmations

    # Calculate totals for percentage analysis
    last_breakdown = generations_data[-1].get('avg_reward_breakdown', {})
    total_positive = sum(v for v in last_breakdown.values() if v > 0)
    total_negative = sum(abs(v) for v in last_breakdown.values() if v < 0)

    # Analyze each component
    consistently_negative = []
    dominant_components = []
    declining_components = []
    learned_components = []

    for comp in components:
        first_val = avg_component(first_phase, comp)
        last_val = avg_component(last_phase, comp)

        # Check for consistently negative throughout training
        all_negative = all(
            g.get('avg_reward_breakdown', {}).get(comp, 0) < 0
            for g in generations_data
        )

        # Check for dominance (>40% of positive rewards)
        if total_positive > 0 and last_val > 0:
            pct_of_total = (last_val / total_positive) * 100
            if pct_of_total > 40:
                dominant_components.append((comp, pct_of_total))

        # Check if component was learned (negative -> positive)
        if first_val < 0 and last_val > 0:
            learned_components.append(comp)

        # Check for consistently negative
        if all_negative and last_val < -5:
            consistently_negative.append((comp, last_val))

        # Check for declining positive rewards
        if first_val > 10 and last_val < first_val * 0.5:
            declining_components.append((comp, first_val, last_val))

    # Generate warnings
    for comp, avg_val in consistently_negative:
        warnings.append(
            f"**{comp} consistently negative** - This component has been negative "
            f"throughout training, averaging {avg_val:.1f}/episode. The intended behavior "
            f"may not be incentivized strongly enough, or there may be a conflict with other rewards."
        )

    for comp, pct in dominant_components:
        if pct > 60:
            warnings.append(
                f"**{comp} dominates reward ({pct:.0f}%)** - This single component accounts for "
                f"most of all positive reward. Other behaviors may be under-incentivized."
            )
        elif pct > 40:
            warnings.append(
                f"**{comp} is dominant ({pct:.0f}%)** - This component accounts for a large portion "
                f"of positive reward. Consider if this is intentional."
            )

    for comp, first_val, last_val in declining_components:
        warnings.append(
            f"**{comp} declining** - This component dropped from {first_val:.1f} to {last_val:.1f}. "
            f"The agent may be trading off this behavior for others."
        )

    # Generate confirmations
    for comp in learned_components:
        confirmations.append(f"**{comp} learned** - Started negative, now positive")

    if not dominant_components or all(pct <= 60 for _, pct in dominant_components):
        confirmations.append("**Reward reasonably balanced** - No single component >60%")

    # Check if survival is positive
    survival_comp = next((c for c in components if 'survival' in c.lower()), None)
    if survival_comp:
        survival_val = last_breakdown.get(survival_comp, 0)
        if survival_val > 0:
            confirmations.append(f"**{survival_comp} positive** - Agents are learning to stay alive")

    # Check for healthy penalty ratio
    if total_positive > 0 and total_negative > 0:
        penalty_ratio = total_negative / total_positive
        if penalty_ratio < 0.3:
            confirmations.append("**Penalty ratio healthy** - Negative rewards are not overwhelming positive")
        elif penalty_ratio > 0.5:
            warnings.append(
                f"**High penalty ratio ({penalty_ratio:.1%})** - Negative rewards are {penalty_ratio:.0%} "
                f"of positive rewards. Agents may be struggling to achieve net positive fitness."
            )

    return warnings, confirmations


def write_reward_warnings(f, generations_data: List[Dict[str, Any]]):
    """Write reward balance warnings section.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if not generations_data or 'avg_reward_breakdown' not in generations_data[-1]:
        f.write("No reward component data available for analysis.\n\n")
        return

    warnings, confirmations = analyze_reward_balance(generations_data)

    if warnings:
        f.write("### Warnings\n\n")
        for warning in warnings:
            f.write(f"- {warning}\n\n")

    if confirmations:
        f.write("### Confirmations\n\n")
        for confirmation in confirmations:
            f.write(f"- {confirmation}\n")
        f.write("\n")

    if not warnings and not confirmations:
        f.write("No significant reward balance issues detected.\n\n")

    # Recommendations based on warnings
    if warnings:
        f.write("### Recommendations\n\n")

        has_negative_warning = any('consistently negative' in w.lower() for w in warnings)
        has_dominant_warning = any('dominates' in w.lower() or 'dominant' in w.lower() for w in warnings)

        if has_negative_warning:
            f.write("- Consider increasing the magnitude of consistently negative reward components\n")
            f.write("- Check if there are conflicting incentives preventing the behavior\n")

        if has_dominant_warning:
            f.write("- Review if other behaviors need stronger incentives\n")
            f.write("- Consider reducing the dominant component or boosting others\n")

        f.write("\n")
