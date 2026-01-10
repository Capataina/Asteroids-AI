"""
Correlation analysis report section.

Generates correlation matrix between metrics.
"""

from typing import List, Dict, Any

from training.analytics.analysis.fitness import pearson_correlation


def write_correlation_matrix(f, generations_data: List[Dict[str, Any]]):
    """Write correlation analysis between metrics.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if len(generations_data) < 10:
        f.write("Not enough data for correlation analysis.\n\n")
        return

    # Get distributions data or calculate from aggregates
    has_distributions = any('distributions' in g for g in generations_data)

    if has_distributions:
        # Use full distribution data
        all_fitness = []
        all_kills = []
        all_steps = []
        all_accuracy = []

        for g in generations_data:
            if 'distributions' in g:
                all_fitness.extend(g['distributions'].get('fitness_values', []))
                all_kills.extend(g['distributions'].get('kills_values', []))
                all_steps.extend(g['distributions'].get('steps_values', []))
                all_accuracy.extend(g['distributions'].get('accuracy_values', []))
    else:
        # Use generation-level averages as proxy
        all_fitness = [g['avg_fitness'] for g in generations_data]
        all_kills = [g.get('avg_kills', 0) for g in generations_data]
        all_steps = [g.get('avg_steps', 0) for g in generations_data]
        all_accuracy = [g.get('avg_accuracy', 0) for g in generations_data]

    # Calculate correlations
    corr_kills = pearson_correlation(all_fitness, all_kills)
    corr_steps = pearson_correlation(all_fitness, all_steps)
    corr_accuracy = pearson_correlation(all_fitness, all_accuracy)

    def strength(r):
        r = abs(r)
        if r >= 0.7:
            return "Strong"
        elif r >= 0.4:
            return "Moderate"
        else:
            return "Weak"

    f.write("### Fitness Correlations\n\n")
    f.write("| Metric | Correlation | Strength |\n")
    f.write("|--------|-------------|----------|\n")
    f.write(f"| Kills | {corr_kills:+.2f} | {strength(corr_kills)} |\n")
    f.write(f"| Steps Survived | {corr_steps:+.2f} | {strength(corr_steps)} |\n")
    f.write(f"| Accuracy | {corr_accuracy:+.2f} | {strength(corr_accuracy)} |\n")
    f.write("\n")

    # Interpretation
    f.write("### Interpretation\n\n")
    strongest = max([(abs(corr_kills), 'kills', corr_kills),
                     (abs(corr_steps), 'survival time', corr_steps),
                     (abs(corr_accuracy), 'accuracy', corr_accuracy)])
    f.write(f"Fitness is most strongly predicted by {strongest[1]} (r={strongest[2]:.2f}).\n\n")
