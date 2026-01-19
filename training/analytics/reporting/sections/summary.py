"""
Summary report section.

Generates the overall summary and configuration sections.
"""

from typing import Dict, Any

from training.analytics.reporting.sections.common import write_takeaways, write_glossary
from training.analytics.reporting.glossary import glossary_entries


def write_config(f, config: Dict[str, Any]):
    """Write training configuration section.

    Args:
        f: File handle to write to
        config: Training configuration dictionary
    """
    f.write("## Training Configuration\n\n")
    f.write("```\n")
    for key, value in config.items():
        f.write(f"{key}: {value}\n")
    f.write("```\n\n")
    write_takeaways(
        f,
        [
            "Configuration snapshot captures the exact training parameters for reproducibility.",
        ],
        title="Config Takeaways",
    )
    write_glossary(
        f,
        [
            ("Config value", "Literal hyperparameter or run setting recorded at training start."),
        ],
        title="Config Glossary",
    )


def write_overall_summary(f, summary: Dict[str, Any], has_fresh_game: bool):
    """Write overall summary section.

    Args:
        f: File handle to write to
        summary: Summary statistics dictionary
        has_fresh_game: Whether fresh game data is available
    """
    f.write("## Overall Summary\n\n")
    f.write(f"- **Total Generations:** {summary.get('total_generations', 0)}\n")
    f.write(f"- **Training Duration:** {summary.get('training_duration', 'N/A')}\n")
    f.write(f"- **All-Time Best Fitness:** {summary.get('all_time_best_fitness', 0):.2f}\n")
    f.write(f"- **Best Generation:** {summary.get('best_generation', 0)}\n")
    f.write(f"- **Final Best Fitness:** {summary.get('final_best_fitness', 0):.2f}\n")
    f.write(f"- **Final Average Fitness:** {summary.get('final_avg_fitness', 0):.2f}\n")
    f.write(f"- **Avg Improvement (Phase 1->Phase 4):** {summary.get('avg_improvement_early_to_late', 0):.2f}\n")
    f.write(f"- **Stagnation:** {summary.get('final_stagnation', 0)} generations since improvement\n")

    # Fresh game summary (if available)
    if has_fresh_game:
        f.write(f"\n**Generalization (Fresh Game Performance):**\n")
        f.write(f"- Avg Generalization Ratio: {summary.get('avg_generalization_ratio', 0):.2f}\n")
        f.write(f"- Best Fresh Fitness: {summary.get('best_fresh_fitness', 0):.2f} (Gen {summary.get('best_fresh_generation', 0)})\n")
        f.write(f"- Episode Completion Rate: {summary.get('fresh_episode_completion_rate', 0)*100:.1f}%\n")
    f.write("\n")

    takeaways = [
        f"Best fitness achieved: {summary.get('all_time_best_fitness', 0):.2f} (Gen {summary.get('best_generation', 0)}).",
        f"Final avg fitness: {summary.get('final_avg_fitness', 0):.2f}.",
    ]
    if summary.get('final_stagnation', 0) > 0:
        takeaways.append(f"Current stagnation: {summary.get('final_stagnation', 0)} generations without improvement.")

    write_takeaways(f, takeaways)
    glossary = glossary_entries([
        "best_fitness",
        "avg_fitness",
        "min_fitness",
    ])
    glossary.append(
        ("Avg improvement (Phase 1->Phase 4)", "Difference between average fitness in the first and last 25% of training.")
    )
    if has_fresh_game:
        glossary.extend([
            ("Generalization ratio", "Fresh-game fitness divided by training fitness (averaged across fresh runs)."),
            ("Episode completion rate", "Share of fresh-game episodes that completed the full max-step window."),
        ])
    write_glossary(f, glossary)


def write_behavioral_summary(f, summary: Dict[str, Any]):
    """Write behavioral summary section.

    Args:
        f: File handle to write to
        summary: Summary statistics dictionary
    """
    if 'final_avg_kills' not in summary:
        return

    f.write("## Behavioral Summary (Last 10 Generations)\n\n")
    f.write(f"- **Avg Kills per Agent:** {summary.get('final_avg_kills', 0):.2f}\n")
    f.write(f"- **Avg Steps Survived:** {summary.get('final_avg_steps', 0):.0f}\n")
    f.write(f"- **Avg Accuracy:** {summary.get('final_avg_accuracy', 0)*100:.1f}%\n")
    f.write(f"- **Max Kills (Any Agent Ever):** {summary.get('max_kills_ever', 0)}\n")
    f.write(f"- **Max Steps (Any Agent Ever):** {summary.get('max_steps_ever', 0)}\n\n")
    write_takeaways(
        f,
        [
            f"Recent average kills: {summary.get('final_avg_kills', 0):.2f}.",
            f"Recent average accuracy: {summary.get('final_avg_accuracy', 0)*100:.1f}%.",
        ]
    )
    write_glossary(
        f,
        glossary_entries([
            "avg_kills",
            "avg_steps",
            "avg_accuracy",
        ])
    )
