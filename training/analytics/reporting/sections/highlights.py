"""
Generation highlights report section.

Identifies and reports notable moments during training such as
best improvements, worst regressions, and record achievements.
"""

from typing import List, Dict, Any, Optional, Tuple


def find_best_improvement(generations_data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Find the generation with the best fitness improvement.

    Args:
        generations_data: List of generation data dictionaries

    Returns:
        Dictionary with highlight data or None
    """
    if len(generations_data) < 2:
        return None

    best_improvement = 0
    best_gen = None

    for i, gen in enumerate(generations_data):
        improvement = gen.get('best_improvement', 0)
        if improvement > best_improvement:
            best_improvement = improvement
            best_gen = gen

    if best_gen and best_improvement > 0:
        prev_fitness = best_gen['best_fitness'] - best_improvement
        pct_improvement = (best_improvement / abs(prev_fitness) * 100) if prev_fitness != 0 else 0
        return {
            'generation': best_gen['generation'],
            'improvement': best_improvement,
            'new_fitness': best_gen['best_fitness'],
            'pct_improvement': pct_improvement,
        }
    return None


def find_worst_regression(generations_data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Find the generation with the worst fitness regression.

    Args:
        generations_data: List of generation data dictionaries

    Returns:
        Dictionary with highlight data or None
    """
    if len(generations_data) < 2:
        return None

    worst_regression = 0
    worst_gen = None

    for gen in generations_data:
        improvement = gen.get('best_improvement', 0)
        if improvement < worst_regression:
            worst_regression = improvement
            worst_gen = gen

    if worst_gen and worst_regression < 0:
        prev_fitness = worst_gen['best_fitness'] - worst_regression
        pct_regression = (abs(worst_regression) / prev_fitness * 100) if prev_fitness != 0 else 0
        return {
            'generation': worst_gen['generation'],
            'regression': abs(worst_regression),
            'new_fitness': worst_gen['best_fitness'],
            'pct_regression': pct_regression,
        }
    return None


def find_record_generation(generations_data: List[Dict[str, Any]], metric: str,
                           maximize: bool = True) -> Optional[Dict[str, Any]]:
    """Find the generation with the record value for a metric.

    Args:
        generations_data: List of generation data dictionaries
        metric: Name of the metric to find record for
        maximize: Whether to find max (True) or min (False)

    Returns:
        Dictionary with highlight data or None
    """
    if not generations_data:
        return None

    record_value = None
    record_gen = None

    for gen in generations_data:
        value = gen.get(metric)
        if value is None:
            continue

        if record_value is None:
            record_value = value
            record_gen = gen
        elif maximize and value > record_value:
            record_value = value
            record_gen = gen
        elif not maximize and value < record_value:
            record_value = value
            record_gen = gen

    if record_gen:
        return {
            'generation': record_gen['generation'],
            'value': record_value,
        }
    return None


def find_first_positive_avg(generations_data: List[Dict[str, Any]]) -> Optional[int]:
    """Find the first generation where average fitness became positive.

    Args:
        generations_data: List of generation data dictionaries

    Returns:
        Generation number or None
    """
    for gen in generations_data:
        if gen['avg_fitness'] > 0:
            return gen['generation']
    return None


def find_diversity_extremes(generations_data: List[Dict[str, Any]]) -> Tuple[Optional[Dict], Optional[Dict]]:
    """Find generations with highest and lowest diversity.

    Args:
        generations_data: List of generation data dictionaries

    Returns:
        Tuple of (most_diverse, most_converged) dictionaries
    """
    if not generations_data:
        return None, None

    most_diverse = None
    most_converged = None
    max_std = 0
    min_std = float('inf')

    for gen in generations_data:
        std = gen.get('std_dev', 0)
        avg = gen.get('avg_fitness', 1)
        # Use coefficient of variation for fair comparison
        cv = std / abs(avg) if avg != 0 else std

        if cv > max_std:
            max_std = cv
            most_diverse = {'generation': gen['generation'], 'diversity_index': cv}
        if cv < min_std and cv > 0:
            min_std = cv
            most_converged = {'generation': gen['generation'], 'diversity_index': cv}

    return most_diverse, most_converged


def write_generation_highlights(f, generations_data: List[Dict[str, Any]]):
    """Write generation highlights section.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if len(generations_data) < 5:
        f.write("Not enough data for generation highlights.\n\n")
        return

    highlights_written = False

    # Best Improvement
    best_imp = find_best_improvement(generations_data)
    if best_imp:
        f.write(f"### Best Improvement\n\n")
        f.write(f"**Generation {best_imp['generation']}**: Best fitness jumped "
                f"+{best_imp['improvement']:.1f} ({best_imp['pct_improvement']:+.1f}%)\n")
        f.write(f"- New best fitness: {best_imp['new_fitness']:.1f}\n\n")
        highlights_written = True

    # Worst Regression
    worst_reg = find_worst_regression(generations_data)
    if worst_reg:
        f.write(f"### Worst Regression\n\n")
        f.write(f"**Generation {worst_reg['generation']}**: Best fitness dropped "
                f"-{worst_reg['regression']:.1f} (-{worst_reg['pct_regression']:.1f}%)\n")
        f.write(f"- New best fitness: {worst_reg['new_fitness']:.1f}\n")
        f.write(f"- *Note: This may be normal variation after a lucky outlier*\n\n")
        highlights_written = True

    # Record Accuracy
    has_behavior = 'avg_accuracy' in generations_data[-1]
    if has_behavior:
        best_acc = find_record_generation(generations_data, 'avg_accuracy', maximize=True)
        if best_acc:
            f.write(f"### Most Accurate Generation\n\n")
            f.write(f"**Generation {best_acc['generation']}**: Population accuracy reached "
                    f"{best_acc['value']*100:.1f}%\n\n")
            highlights_written = True

        # Record Kills
        best_kills = find_record_generation(generations_data, 'max_kills', maximize=True)
        if best_kills:
            f.write(f"### Most Kills (Single Agent)\n\n")
            f.write(f"**Generation {best_kills['generation']}**: An agent achieved "
                    f"{best_kills['value']:.0f} kills\n\n")
            highlights_written = True

    # First Positive Average
    first_pos = find_first_positive_avg(generations_data)
    if first_pos:
        f.write(f"### First Viable Population\n\n")
        f.write(f"**Generation {first_pos}**: Average fitness first became positive\n\n")
        highlights_written = True

    # Diversity Extremes
    most_diverse, most_converged = find_diversity_extremes(generations_data)
    if most_diverse:
        f.write(f"### Most Diverse Generation\n\n")
        f.write(f"**Generation {most_diverse['generation']}**: Diversity index {most_diverse['diversity_index']:.2f}\n\n")
        highlights_written = True

    if most_converged and most_converged['generation'] != 1:
        f.write(f"### Most Converged Generation\n\n")
        f.write(f"**Generation {most_converged['generation']}**: Diversity index {most_converged['diversity_index']:.2f}\n\n")
        highlights_written = True

    if not highlights_written:
        f.write("No notable highlights detected.\n\n")
