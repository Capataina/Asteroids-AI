"""
Risk profile analysis.

Reports on agent risk-taking behavior (proximity to asteroids).
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


def write_risk_analysis(f, generations_data: List[Dict[str, Any]]):
    """Write risk analysis section."""
    if not generations_data:
        return

    window = AnalyticsConfig.RECENT_TABLE_WINDOW
    recent = generations_data[-window:]
    if not recent:
        return

    if 'avg_min_dist' not in recent[-1]:
        return

    f.write("## Risk Profile Analysis\n\n")
    f.write("Analysis of how close agents let asteroids get before reacting or killing them.\n\n")

    fitness_series = [g.get('avg_fitness', 0.0) for g in recent]
    dist_series = [g.get('avg_min_dist', 0.0) for g in recent]

    fit_q25 = _percentile(fitness_series, 25)
    fit_q75 = _percentile(fitness_series, 75)
    dist_q25 = _percentile(dist_series, 25)
    dist_q75 = _percentile(dist_series, 75)

    f.write("| Gen | Avg Min Dist | Fitness | Kills | Archetype |\n")
    f.write("|-----|--------------|---------|-------|-----------|\n")

    for gen in recent:
        min_dist = gen.get('avg_min_dist', 0.0)
        fit = gen.get('avg_fitness', 0.0)
        kills = gen.get('avg_kills', 0.0)

        archetype = "Balanced"
        if fit >= fit_q75 and min_dist <= dist_q25:
            archetype = "Daredevil"
        elif fit >= fit_q75 and min_dist >= dist_q75:
            archetype = "Sniper"
        elif fit <= fit_q25 and min_dist <= dist_q25:
            archetype = "Overexposed"
        elif fit <= fit_q25 and min_dist >= dist_q75:
            archetype = "Cautious Underperformer"

        f.write(f"| {gen['generation']} | {min_dist:6.1f}px | {fit:6.1f} | {kills:4.1f} | {archetype} |\n")

    f.write("\n")

    takeaways: List[str] = []
    warnings: List[str] = []

    dist_trend = trend_stats(generations_data, 'avg_min_dist', higher_is_better=True, phase_count=AnalyticsConfig.PHASE_COUNT)
    takeaways.append(f"Min-distance trend: {dist_trend['tag']} ({dist_trend['confidence']}).")

    if 'avg_danger_exposure_rate' in generations_data[-1]:
        danger_trend = trend_stats(generations_data, 'avg_danger_exposure_rate', higher_is_better=False, phase_count=AnalyticsConfig.PHASE_COUNT)
        takeaways.append(f"Danger exposure trend: {danger_trend['tag']} ({danger_trend['confidence']}).")
        if "regression" in danger_trend["tag"]:
            warnings.append("Danger exposure is increasing; agents spend more time in threat zones.")
    if 'avg_softmin_ttc' in generations_data[-1]:
        ttc_trend = trend_stats(generations_data, 'avg_softmin_ttc', higher_is_better=True, phase_count=AnalyticsConfig.PHASE_COUNT)
        takeaways.append(f"Soft-min TTC trend: {ttc_trend['tag']} ({ttc_trend['confidence']}).")
        if "regression" in ttc_trend["tag"]:
            warnings.append("Soft-min TTC is declining; imminent threats are worsening.")

    if "regression" in dist_trend["tag"]:
        warnings.append("Agents are getting closer to asteroids over time (risk rising).")

    write_takeaways(f, takeaways)
    write_warnings(f, warnings)
    write_glossary(
        f,
        glossary_entries([
            "avg_min_dist",
            "avg_asteroid_dist",
            "avg_danger_exposure_rate",
            "avg_softmin_ttc",
        ])
    )
