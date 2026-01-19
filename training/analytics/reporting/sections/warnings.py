"""
Reward balance analysis section.

Detects reward component dominance, instability, and penalty skew.
"""

from typing import List, Dict, Any, Tuple

from training.analytics.analysis.phases import split_generations, summarize_values
from training.analytics.reporting.sections.common import write_takeaways, write_warnings, write_glossary
from training.analytics.reporting.glossary import glossary_entries


def _component_series(generations_data: List[Dict[str, Any]], component: str) -> List[float]:
    return [g.get('avg_reward_breakdown', {}).get(component, 0.0) for g in generations_data]


def analyze_reward_balance(generations_data: List[Dict[str, Any]]) -> Tuple[List[str], List[str]]:
    warnings: List[str] = []
    takeaways: List[str] = []

    if not generations_data or 'avg_reward_breakdown' not in generations_data[-1]:
        return warnings, takeaways

    last_breakdown = generations_data[-1].get('avg_reward_breakdown', {})
    components = list(last_breakdown.keys())
    if not components:
        return warnings, takeaways

    # Dominance and entropy signals (latest generation)
    dominance_index = generations_data[-1].get('reward_dominance_index', 0.0)
    entropy = generations_data[-1].get('reward_entropy', 0.0)
    max_share = generations_data[-1].get('reward_max_share', 0.0)

    # Build historical baselines for dominance
    dominance_series = [g.get('reward_dominance_index', 0.0) for g in generations_data if 'reward_dominance_index' in g]
    entropy_series = [g.get('reward_entropy', 0.0) for g in generations_data if 'reward_entropy' in g]

    dom_stats = summarize_values(dominance_series)
    ent_stats = summarize_values(entropy_series)

    if dominance_series and dominance_index > dom_stats["mean"] + dom_stats["std"]:
        warnings.append("Reward dominance is above run average (one component is likely overpowering).")
    if entropy_series and entropy < max(0.1, ent_stats["mean"] - ent_stats["std"]):
        warnings.append("Reward entropy is below run average (reward mix is narrowing).")
    if max_share > 0.6:
        warnings.append(f"Max component share is high ({max_share*100:.1f}%).")

    # Component-level stability
    phases = split_generations(generations_data, phase_count=4)
    for comp in components:
        series = _component_series(generations_data, comp)
        stats = summarize_values(series)
        if stats["std"] > max(1.0, abs(stats["mean"]) * 0.75):
            warnings.append(f"{comp} is volatile across the run (high variance vs mean).")

        if stats["mean"] < 0 and series[-1] < 0:
            warnings.append(f"{comp} remains negative on average (behavior may be over-penalized).")

        # Sign flip across phases
        if phases:
            phase_values = [sum(g.get('avg_reward_breakdown', {}).get(comp, 0.0) for g in p["data"]) / len(p["data"]) for p in phases]
            if any(v < 0 for v in phase_values) and any(v > 0 for v in phase_values):
                takeaways.append(f"{comp} flipped sign across phases (objective meaning changed during training).")

    # Penalty ratio
    total_positive = sum(v for v in last_breakdown.values() if v > 0)
    total_negative = sum(abs(v) for v in last_breakdown.values() if v < 0)
    penalty_ratio = (total_negative / total_positive) if total_positive > 0 else 0.0
    if penalty_ratio > 0.7:
        warnings.append(f"Penalty ratio is high ({penalty_ratio:.2f}), negative rewards dominate.")
    elif penalty_ratio > 0.4:
        takeaways.append(f"Penalty ratio is elevated ({penalty_ratio:.2f}); rewards are penalty-heavy.")

    if not takeaways:
        takeaways.append("Reward mix is broadly stable with no major dominance spikes.")

    return warnings, takeaways


def write_reward_warnings(f, generations_data: List[Dict[str, Any]]):
    """Write reward balance warnings section."""
    if not generations_data or 'avg_reward_breakdown' not in generations_data[-1]:
        f.write("No reward component data available for analysis.\n\n")
        return

    last_gen = generations_data[-1]
    if 'reward_dominance_index' in last_gen:
        f.write("### Balance Metrics (Latest Generation)\n\n")
        f.write(f"- Reward dominance index (HHI): {last_gen.get('reward_dominance_index', 0.0):.2f}\n")
        f.write(f"- Reward entropy (normalized): {last_gen.get('reward_entropy', 0.0):.2f}\n")
        f.write(f"- Max component share: {last_gen.get('reward_max_share', 0.0)*100:.1f}%\n")
        f.write(f"- Positive component count: {last_gen.get('reward_positive_component_count', 0)}\n\n")

    warnings, takeaways = analyze_reward_balance(generations_data)

    write_takeaways(f, takeaways)
    write_warnings(f, warnings)
    write_glossary(
        f,
        glossary_entries([
            "avg_reward_breakdown",
            "reward_dominance_index",
            "reward_entropy",
            "reward_max_share",
            "reward_positive_component_count",
        ])
    )
