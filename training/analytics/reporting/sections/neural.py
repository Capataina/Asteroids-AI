"""
Neural and behavioral complexity analysis.

Reports on neural network health (saturation) and behavioral entropy.
"""

from typing import List, Dict, Any

from training.config.analytics import AnalyticsConfig
from training.analytics.reporting.sections.common import write_takeaways, write_warnings, write_glossary
from training.analytics.reporting.glossary import glossary_entries
from training.analytics.reporting.insights import trend_stats


def _percentile(values: List[float], pct: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    idx = int(round((pct / 100.0) * (len(values) - 1)))
    return values[max(0, min(len(values) - 1, idx))]


def write_neural_analysis(f, generations_data: List[Dict[str, Any]]):
    """Write neural and behavioral complexity analysis."""
    if not generations_data:
        return

    window = AnalyticsConfig.RECENT_TABLE_WINDOW
    recent = generations_data[-window:]
    if not recent:
        return

    if 'avg_output_saturation' not in recent[-1]:
        return

    f.write("## Neural & Behavioral Complexity\n\n")
    f.write("| Gen | Saturation | Entropy | Control Style |\n")
    f.write("|-----|------------|---------|---------------|\n")

    sat_series = [g.get('avg_output_saturation', 0.0) for g in generations_data]
    ent_series = [g.get('avg_action_entropy', 0.0) for g in generations_data]

    sat_p25 = _percentile(sat_series, 25)
    sat_p75 = _percentile(sat_series, 75)
    ent_p25 = _percentile(ent_series, 25)
    ent_p75 = _percentile(ent_series, 75)

    for gen in recent:
        sat = gen.get('avg_output_saturation', 0.0)
        ent = gen.get('avg_action_entropy', 0.0)

        style = "Balanced"
        if sat >= sat_p75:
            style = "Binary-leaning"
        elif sat <= sat_p25:
            style = "Analog-leaning"

        if ent <= ent_p25:
            style += " / Repetitive"
        elif ent >= ent_p75:
            style += " / Exploratory"

        f.write(f"| {gen['generation']} | {sat*100:5.1f}% | {ent:5.2f} | {style} |\n")

    f.write("\n")

    takeaways = []
    warnings = []

    sat_trend = trend_stats(generations_data, 'avg_output_saturation', higher_is_better=False, phase_count=AnalyticsConfig.PHASE_COUNT)
    ent_trend = trend_stats(generations_data, 'avg_action_entropy', higher_is_better=True, phase_count=AnalyticsConfig.PHASE_COUNT)

    takeaways.append(f"Output saturation trend: {sat_trend['tag']} ({sat_trend['confidence']}).")
    takeaways.append(f"Action entropy trend: {ent_trend['tag']} ({ent_trend['confidence']}).")

    latest_sat = generations_data[-1].get('avg_output_saturation', 0.0)
    latest_ent = generations_data[-1].get('avg_action_entropy', 0.0)

    if latest_sat > sat_p75 and latest_ent < ent_p25:
        warnings.append("High saturation with low entropy suggests rigid, repetitive control.")
    if latest_sat < sat_p25 and latest_ent < ent_p25:
        warnings.append("Low saturation but low entropy suggests smooth but overly repetitive control.")

    write_takeaways(f, takeaways)
    write_warnings(f, warnings)
    write_glossary(
        f,
        glossary_entries([
            "avg_output_saturation",
            "avg_action_entropy",
        ])
    )
