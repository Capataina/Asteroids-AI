"""
Generalization analysis report section.

Generates fresh game generalization analysis.
"""

from typing import List, Dict, Any


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
    f.write("| Gen | Training Fit | Fresh Fit | Ratio | Grade | Cause of Death |\n")
    f.write("|-----|--------------|-----------|-------|-------|----------------|\n")

    for g in recent[-10:]:
        train_fit = g.get('best_fitness', 0)
        fresh = g.get('fresh_game', {})
        gen_met = g.get('generalization_metrics', {})
        f.write(f"| {g['generation']} | {train_fit:.0f} | {fresh.get('fitness', 0):.0f} | "
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
