"""
Generation highlights report section.

Identifies and reports notable moments during training such as
best improvements, worst regressions, and record achievements.
"""

from typing import List, Dict, Any, Optional, Tuple

from training.analytics.reporting.sections.common import write_takeaways, write_glossary
from training.analytics.reporting.glossary import glossary_entries


def find_best_improvement(generations_data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if len(generations_data) < 2:
        return None

    best_improvement = 0
    best_gen = None

    for gen in generations_data:
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
    for gen in generations_data:
        if gen['avg_fitness'] > 0:
            return gen['generation']
    return None


def find_diversity_extremes(generations_data: List[Dict[str, Any]]) -> Tuple[Optional[Dict], Optional[Dict]]:
    if not generations_data:
        return None, None

    most_diverse = None
    most_converged = None
    max_std = 0
    min_std = float('inf')

    for gen in generations_data:
        std = gen.get('std_dev', 0)
        avg = gen.get('avg_fitness', 1)
        cv = std / abs(avg) if avg != 0 else std

        if cv > max_std:
            max_std = cv
            most_diverse = {'generation': gen['generation'], 'diversity_index': cv}
        if cv < min_std and cv > 0:
            min_std = cv
            most_converged = {'generation': gen['generation'], 'diversity_index': cv}

    return most_diverse, most_converged


def write_generation_highlights(f, generations_data: List[Dict[str, Any]]):
    if len(generations_data) < 5:
        f.write("Not enough data for generation highlights.\n\n")
        return

    highlights_written = False

    best_imp = find_best_improvement(generations_data)
    if best_imp:
        f.write("### Best Improvement\n\n")
        f.write(f"**Generation {best_imp['generation']}**: Best fitness jumped "
                f"+{best_imp['improvement']:.1f} ({best_imp['pct_improvement']:+.1f}%)\n")
        f.write(f"- New best fitness: {best_imp['new_fitness']:.1f}\n\n")
        highlights_written = True

    worst_reg = find_worst_regression(generations_data)
    if worst_reg:
        f.write("### Worst Regression\n\n")
        f.write(f"**Generation {worst_reg['generation']}**: Best fitness dropped "
                f"-{worst_reg['regression']:.1f} (-{worst_reg['pct_regression']:.1f}%)\n")
        f.write(f"- New best fitness: {worst_reg['new_fitness']:.1f}\n")
        f.write("- Note: this can be normal variation after a lucky outlier\n\n")
        highlights_written = True

    has_behavior = 'avg_accuracy' in generations_data[-1]
    if has_behavior:
        best_acc = find_record_generation(generations_data, 'avg_accuracy', maximize=True)
        if best_acc:
            f.write("### Most Accurate Generation\n\n")
            f.write(f"**Generation {best_acc['generation']}**: Population accuracy reached "
                    f"{best_acc['value']*100:.1f}%\n\n")
            highlights_written = True

        best_kills = find_record_generation(generations_data, 'max_kills', maximize=True)
        if best_kills:
            f.write("### Most Kills (Single Agent)\n\n")
            f.write(f"**Generation {best_kills['generation']}**: An agent achieved "
                    f"{best_kills['value']:.0f} kills\n\n")
            highlights_written = True

    first_pos = find_first_positive_avg(generations_data)
    if first_pos:
        f.write("### First Viable Population\n\n")
        f.write(f"**Generation {first_pos}**: Average fitness first became positive\n\n")
        highlights_written = True

    most_diverse, most_converged = find_diversity_extremes(generations_data)
    if most_diverse:
        f.write("### Most Diverse Generation\n\n")
        f.write(f"**Generation {most_diverse['generation']}**: Diversity index {most_diverse['diversity_index']:.2f}\n\n")
        highlights_written = True

    if most_converged and most_converged['generation'] != 1:
        f.write("### Most Converged Generation\n\n")
        f.write(f"**Generation {most_converged['generation']}**: Diversity index {most_converged['diversity_index']:.2f}\n\n")
        highlights_written = True

    if not highlights_written:
        f.write("No notable highlights detected.\n\n")

    takeaways = []
    if best_imp:
        takeaways.append(f"Best improvement at Gen {best_imp['generation']} (+{best_imp['improvement']:.1f}).")
    if worst_reg:
        takeaways.append(f"Worst regression at Gen {worst_reg['generation']} (-{worst_reg['regression']:.1f}).")
    if not takeaways:
        takeaways.append("No standout improvement or regression events flagged.")

    write_takeaways(f, takeaways)
    write_glossary(
        f,
        glossary_entries([
            "best_fitness",
            "avg_fitness",
            "avg_accuracy",
            "max_kills",
            "std_dev",
        ])
    )


def write_best_agent_profile(f, generations_data: List[Dict[str, Any]]):
    if not generations_data:
        return

    best_gen = max(generations_data, key=lambda x: x['best_fitness'])
    if 'best_agent_kills' not in best_gen:
        return

    f.write("## Best Agent Deep Profile\n\n")
    f.write(f"The most fit agent appeared in **Generation {best_gen['generation']}** with a fitness of **{best_gen['best_fitness']:.2f}**.\n\n")

    kills = best_gen.get('best_agent_kills', 0)
    steps = best_gen.get('best_agent_steps', 0)
    accuracy = best_gen.get('best_agent_accuracy', 0)

    derived_shots = int(kills / accuracy) if accuracy > 0 else 0
    shots_per_kill = (derived_shots / kills) if kills > 0 else 0
    steps_per_kill = (steps / kills) if kills > 0 else steps

    f.write("### Combat Efficiency\n\n")
    f.write(f"- **Total Kills:** {kills}\n")
    f.write(f"- **Survival Time:** {steps / 60:.1f} seconds ({steps} steps)\n")
    f.write(f"- **Accuracy:** {accuracy*100:.1f}%\n")
    f.write(f"- **Shots per Kill:** {shots_per_kill:.1f}\n")
    f.write(f"- **Time per Kill:** {steps_per_kill/60:.2f} seconds\n\n")

    try:
        from training.analytics.analysis.action_classification import classify_behavior, get_action_rates

        baseline_rates = None
        if generations_data:
            baseline = [get_action_rates(g) for g in generations_data if 'avg_steps' in g]
            if baseline:
                baseline_rates = {
                    'thrust_rate': sum(r['thrust_rate'] for r in baseline) / len(baseline),
                    'turn_rate': sum(r['turn_rate'] for r in baseline) / len(baseline),
                    'shoot_rate': sum(r['shoot_rate'] for r in baseline) / len(baseline),
                }

        behavior_label = classify_behavior(best_gen, baseline_rates=baseline_rates)
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

    write_takeaways(
        f,
        [
            f"Best agent achieved {kills} kills with {accuracy*100:.1f}% accuracy.",
            f"Behavioral classification: {behavior_label if 'behavior_label' in locals() else 'N/A'}.",
        ]
    )
    write_glossary(
        f,
        glossary_entries([
            "best_fitness",
            "avg_accuracy",
            "avg_steps",
            "avg_shots_per_kill",
        ])
    )
