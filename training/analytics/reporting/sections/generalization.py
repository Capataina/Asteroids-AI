"""
Generalization analysis report section.

Generates fresh game generalization analysis.
"""

from typing import List, Dict, Any


def _reward_shares(breakdown: Dict[str, float]) -> Dict[str, float]:
    positive = {k: v for k, v in breakdown.items() if v > 0}
    total = sum(positive.values())
    if total <= 0:
        return {}
    return {k: v / total for k, v in positive.items()}


def _reward_share_shift(train_shares: Dict[str, float], fresh_shares: Dict[str, float]) -> float:
    keys = set(train_shares.keys()) | set(fresh_shares.keys())
    return 0.5 * sum(abs(train_shares.get(k, 0.0) - fresh_shares.get(k, 0.0)) for k in keys)


def write_generalization_analysis(f, generations_data: List[Dict[str, Any]]):
    """Write generalization analysis from fresh game data.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    fresh_games = [g for g in generations_data if 'fresh_game' in g]
    if not fresh_games:
        f.write("No fresh game data available.\n\n")
        return

    # Recent fresh game stats
    recent = fresh_games[-10:] if len(fresh_games) >= 10 else fresh_games

    f.write("### Recent Fresh Game Performance\n\n")
    f.write("| Gen | Training Fit | Fresh Fit | Accuracy | Ratio | Grade | Cause of Death |\n")
    f.write("|-----|--------------|-----------|----------|-------|-------|----------------|\n")

    for g in recent[-10:]:
        train_fit = g.get('best_fitness', 0)
        fresh = g.get('fresh_game', {})
        gen_met = g.get('generalization_metrics', {})
        f.write(f"| {g['generation']} | {train_fit:.0f} | {fresh.get('fitness', 0):.0f} | "
                f"{fresh.get('accuracy', 0)*100:.1f}% | "
                f"{gen_met.get('fitness_ratio', 0):.2f} | {gen_met.get('generalization_grade', 'N/A')} | "
                f"{fresh.get('cause_of_death', 'N/A')} |\n")

    f.write("\n")

    # Summary stats
    all_ratios = [g.get('generalization_metrics', {}).get('fitness_ratio', 0) for g in fresh_games]
    valid_ratios = [r for r in all_ratios if r > 0]
    if valid_ratios:
        avg_ratio = sum(valid_ratios) / len(valid_ratios)
        min_ratio = min(valid_ratios)
        max_ratio = max(valid_ratios)

        f.write("### Generalization Summary\n\n")
        f.write(f"- **Average Fitness Ratio:** {avg_ratio:.2f}\n")
        f.write(f"- **Best Ratio:** {max_ratio:.2f}\n")
        f.write(f"- **Worst Ratio:** {min_ratio:.2f}\n")

        # Grade distribution
        grades = [g.get('generalization_metrics', {}).get('generalization_grade', 'N/A') for g in fresh_games]
        grade_counts = {}
        for grade in grades:
            grade_counts[grade] = grade_counts.get(grade, 0) + 1

        f.write(f"\n**Grade Distribution:** ")
        for grade in ['A', 'B', 'C', 'D', 'F']:
            count = grade_counts.get(grade, 0)
            if count > 0:
                f.write(f"{grade}:{count} ")
        f.write("\n\n")

    # Reward transfer gap analysis
    recent_with_rewards = [g for g in recent if g.get('fresh_game', {}).get('reward_breakdown')]
    if not recent_with_rewards:
        return

    f.write("### Reward Transfer Gap (Fresh vs Training)\n\n")
    f.write("| Gen | Share Shift | Largest Share Deltas |\n")
    f.write("|-----|-------------|----------------------|\n")

    for g in recent_with_rewards:
        fresh_breakdown = g.get('fresh_game', {}).get('reward_breakdown', {})
        train_breakdown = g.get('avg_reward_breakdown', {})
        train_shares = _reward_shares(train_breakdown)
        fresh_shares = _reward_shares(fresh_breakdown)

        if not train_shares or not fresh_shares:
            continue

        shift = _reward_share_shift(train_shares, fresh_shares)
        deltas = {k: fresh_shares.get(k, 0.0) - train_shares.get(k, 0.0)
                  for k in set(train_shares.keys()) | set(fresh_shares.keys())}
        top_deltas = sorted(deltas.items(), key=lambda item: abs(item[1]), reverse=True)[:3]
        top_str = ", ".join([f"{k} {v*100:+.0f}%" for k, v in top_deltas]) if top_deltas else "N/A"

        f.write(f"| {g['generation']} | {shift*100:6.1f}% | {top_str} |\n")

    f.write("\n")
