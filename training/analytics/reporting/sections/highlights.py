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


def write_best_agent_profile(f, generations_data: List[Dict[str, Any]]):
    """Write a deep profile of the all-time best agent.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if not generations_data:
        return

    # Find the generation with the highest best_fitness
    best_gen = max(generations_data, key=lambda x: x['best_fitness'])
    
    # Check if we have detailed best_agent stats (introduced in later schema versions)
    if 'best_agent_kills' not in best_gen:
        return

    f.write("## Best Agent Deep Profile\n\n")
    f.write(f"The most fit agent appeared in **Generation {best_gen['generation']}** with a fitness of **{best_gen['best_fitness']:.2f}**.\n\n")
    
    # Basic Stats
    kills = best_gen.get('best_agent_kills', 0)
    steps = best_gen.get('best_agent_steps', 0)
    accuracy = best_gen.get('best_agent_accuracy', 0)
    shots = best_gen.get('best_agent_shoot', 0) # This might be frames, not total shots. 
    # Wait, 'best_agent_shoot' is frames where space was pressed. 
    # We don't have exact shot count for best agent, but we can infer or use 'avg_shots' as proxy if needed,
    # OR we rely on accuracy * shots = hits. 
    # Actually, we rely on the collected data. 
    # In 'collectors.py', 'best_agent_shoot' stores 'shoot_frames'. 
    # We DO NOT have 'best_agent_total_shots' explicitly, but 'best_agent_accuracy' is correct.
    
    # Let's derive shots from kills and accuracy if possible
    # Accuracy = Kills / Shots => Shots = Kills / Accuracy
    derived_shots = int(kills / accuracy) if accuracy > 0 else 0
    
    # Efficiency Metrics
    shots_per_kill = (derived_shots / kills) if kills > 0 else 0
    steps_per_kill = (steps / kills) if kills > 0 else steps
    
    f.write("### Combat Efficiency\n\n")
    f.write(f"- **Total Kills:** {kills}\n")
    f.write(f"- **Survival Time:** {steps / 60:.1f} seconds ({steps} steps)\n")
    f.write(f"- **Accuracy:** {accuracy*100:.1f}%\n")
    f.write(f"- **Shots per Kill:** {shots_per_kill:.1f}\n")
    f.write(f"- **Time per Kill:** {steps_per_kill/60:.2f} seconds\n\n")
    
    # Behavioral Analysis
    # We need to import the classifier locally to avoid circular imports if any
    try:
        from training.analytics.analysis.action_classification import classify_behavior, get_action_rates
        
        # Construct metrics dict for classifier
        # The classifier expects 'avg_...' or 'best_agent_...' keys
        behavior_label = classify_behavior(best_gen)
        rates = get_action_rates(best_gen)
        
        f.write("### Behavioral Signature\n\n")
        f.write(f"**Classification:** `{behavior_label}`\n\n")
        f.write("| Action | Rate (per step) | Description |\n")
        f.write("|--------|-----------------|-------------|\n")
        f.write(f"| **Thrust** | {rates['thrust_rate']*100:.1f}% | Movement frequency |\n")
        f.write(f"| **Turn** | {rates['turn_rate']*100:.1f}% | Rotation frequency |\n")
        f.write(f"| **Shoot** | {rates['shoot_rate']*100:.1f}% | Trigger discipline |\n")
        
    except ImportError:
        f.write("*Classifier module not found.*\n")
    
    f.write("\n")
