"""
Control diagnostics report section.

Adds diagnostics for turning, aiming, danger exposure, traversal, and shooting quality.
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


def write_control_diagnostics(f, generations_data: List[Dict[str, Any]]):
    """Write control diagnostics section."""
    if not generations_data:
        return

    latest = generations_data[-1]
    if 'avg_turn_deadzone_rate' not in latest:
        f.write("No control diagnostics available.\n\n")
        return

    f.write("## Control Diagnostics\n\n")
    f.write("### Control Snapshot (Latest Generation)\n\n")
    f.write("| Category | Metric | Value |\n")
    f.write("|----------|--------|-------|\n")
    f.write(f"| Turn | Deadzone Rate | {latest.get('avg_turn_deadzone_rate', 0.0)*100:.1f}% |\n")
    f.write(f"| Turn | Turn Balance (R-L) | {latest.get('avg_turn_balance', 0.0):+.2f} |\n")
    f.write(f"| Turn | Switch Rate | {latest.get('avg_turn_switch_rate', 0.0)*100:.1f}% |\n")
    f.write(f"| Turn | Avg Streak | {latest.get('avg_turn_streak', 0.0):.1f}f |\n")
    f.write(f"| Turn | Max Streak | {latest.get('avg_max_turn_streak', 0.0):.0f}f |\n")
    f.write(f"| Aim | Frontness Avg | {latest.get('avg_frontness', 0.0)*100:.1f}% |\n")
    f.write(f"| Aim | Frontness at Shot | {latest.get('avg_frontness_at_shot', 0.0)*100:.1f}% |\n")
    f.write(f"| Aim | Frontness at Hit | {latest.get('avg_frontness_at_hit', 0.0)*100:.1f}% |\n")
    f.write(f"| Aim | Shot Distance | {latest.get('avg_shot_distance', 0.0):.1f}px |\n")
    f.write(f"| Aim | Hit Distance | {latest.get('avg_hit_distance', 0.0):.1f}px |\n")
    f.write(f"| Danger | Exposure Rate | {latest.get('avg_danger_exposure_rate', 0.0)*100:.1f}% |\n")
    f.write(f"| Danger | Entries | {latest.get('avg_danger_entries', 0.0):.1f} |\n")
    f.write(f"| Danger | Reaction Time | {latest.get('avg_danger_reaction_time', 0.0):.1f}f |\n")
    f.write(f"| Danger | Wraps in Danger | {latest.get('avg_danger_wraps', 0.0):.1f} |\n")
    f.write(f"| Movement | Distance Traveled | {latest.get('avg_distance_traveled', 0.0):.1f}px |\n")
    f.write(f"| Movement | Avg Speed | {latest.get('avg_speed', 0.0):.2f} |\n")
    f.write(f"| Movement | Speed Std | {latest.get('avg_speed_std', 0.0):.2f} |\n")
    f.write(f"| Movement | Coverage Ratio | {latest.get('avg_coverage_ratio', 0.0)*100:.1f}% |\n")
    f.write(f"| Shooting | Shots per Kill | {latest.get('avg_shots_per_kill', 0.0):.2f} |\n")
    f.write(f"| Shooting | Shots per Hit | {latest.get('avg_shots_per_hit', 0.0):.2f} |\n")
    f.write(f"| Shooting | Cooldown Usage | {latest.get('avg_cooldown_usage_rate', 0.0)*100:.1f}% |\n")
    f.write(f"| Shooting | Cooldown Ready | {latest.get('avg_cooldown_ready_rate', 0.0)*100:.1f}% |\n")
    f.write(f"| Stability | Fitness Std (Seeds) | {latest.get('avg_fitness_std', 0.0):.1f} |\n")
    f.write("\n")

    window = min(10, AnalyticsConfig.RECENT_TABLE_WINDOW, len(generations_data))
    recent = generations_data[-window:]

    f.write(f"### Recent Control Trends (Last {len(recent)})\n\n")
    f.write("| Gen | Deadzone | Turn Bias | Switch | Frontness | Danger | Coverage |\n")
    f.write("|-----|----------|-----------|--------|-----------|--------|----------|\n")
    for gen in recent:
        f.write(
            f"| {gen['generation']} | "
            f"{gen.get('avg_turn_deadzone_rate', 0.0)*100:6.1f}% | "
            f"{gen.get('avg_turn_balance', 0.0):+6.2f} | "
            f"{gen.get('avg_turn_switch_rate', 0.0)*100:6.1f}% | "
            f"{gen.get('avg_frontness', 0.0)*100:6.1f}% | "
            f"{gen.get('avg_danger_exposure_rate', 0.0)*100:6.1f}% | "
            f"{gen.get('avg_coverage_ratio', 0.0)*100:6.1f}% |\n"
        )
    f.write("\n")

    takeaways: List[str] = []
    warnings: List[str] = []

    turn_bias = trend_stats(generations_data, 'avg_turn_balance', higher_is_better=False, phase_count=AnalyticsConfig.PHASE_COUNT)
    frontness = trend_stats(generations_data, 'avg_frontness', higher_is_better=True, phase_count=AnalyticsConfig.PHASE_COUNT)
    danger = trend_stats(generations_data, 'avg_danger_exposure_rate', higher_is_better=False, phase_count=AnalyticsConfig.PHASE_COUNT)

    takeaways.append(f"Turn balance trend: {turn_bias['tag']} ({turn_bias['confidence']}).")
    takeaways.append(f"Aim alignment trend: {frontness['tag']} ({frontness['confidence']}).")
    takeaways.append(f"Danger exposure trend: {danger['tag']} ({danger['confidence']}).")

    turn_balance_series = [g.get('avg_turn_balance', 0.0) for g in generations_data]
    bias_p75 = _percentile([abs(v) for v in turn_balance_series], 75)
    if abs(latest.get('avg_turn_balance', 0.0)) > bias_p75 and bias_p75 > 0:
        warnings.append("Turn bias is high vs run baseline (one-direction dominance).")

    if latest.get('avg_frontness_at_shot', 0.0) < max(0.05, latest.get('avg_frontness', 0.0) * 0.6):
        warnings.append("Frontness at shot lags overall frontness (aiming during shots is weak).")

    if latest.get('avg_turn_deadzone_rate', 0.0) > _percentile([g.get('avg_turn_deadzone_rate', 0.0) for g in generations_data], 75):
        warnings.append("Turn deadzone rate is high; turning inputs are often too small to actuate.")

    if "regression" in danger["tag"]:
        warnings.append("Agents are spending more time in danger zones over training.")

    write_takeaways(f, takeaways)
    write_warnings(f, warnings)
    write_glossary(
        f,
        glossary_entries([
            "avg_turn_deadzone_rate",
            "avg_turn_balance",
            "avg_turn_switch_rate",
            "avg_turn_streak",
            "avg_max_turn_streak",
            "avg_frontness",
            "avg_frontness_at_shot",
            "avg_frontness_at_hit",
            "avg_shot_distance",
            "avg_hit_distance",
            "avg_danger_exposure_rate",
            "avg_danger_entries",
            "avg_danger_reaction_time",
            "avg_danger_wraps",
            "avg_distance_traveled",
            "avg_speed",
            "avg_speed_std",
            "avg_coverage_ratio",
            "avg_shots_per_kill",
            "avg_shots_per_hit",
            "avg_cooldown_usage_rate",
            "avg_cooldown_ready_rate",
            "avg_fitness_std",
        ])
    )
