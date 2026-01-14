"""
Control diagnostics report section.

Adds diagnostics for turning, aiming, danger exposure, traversal, and shooting quality.
"""

from typing import List, Dict, Any

from training.config.analytics import AnalyticsConfig


def write_control_diagnostics(f, generations_data: List[Dict[str, Any]]):
    """Write control diagnostics section."""
    if not generations_data:
        return

    latest = generations_data[-1]
    if 'avg_turn_deadzone_rate' not in latest:
        f.write("No control diagnostics available.\n\n")
        return

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
