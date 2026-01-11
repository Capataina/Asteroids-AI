"""
Generation tables report section.

Generates detailed generation tables.
"""

from typing import List, Dict, Any


def write_generation_table(f, generations_data: List[Dict[str, Any]],
                           limit: int = 30, include_behavior: bool = False):
    """Write detailed generation table.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
        limit: Number of recent generations to show
        include_behavior: Whether to include behavioral metrics
    """
    recent = generations_data[-limit:]

    f.write("<details>\n<summary>Click to expand Recent Generations table</summary>\n\n")

    if include_behavior:
        f.write("| Gen   | Best   | Avg    | StdDev | Kills  | Steps  | Acc%   | Stag   |\n")
        f.write("|-------|--------|--------|--------|--------|--------|--------|--------|\n")

        for gen_data in recent:
            f.write(f"| {gen_data['generation']:<5} | ")
            f.write(f"{gen_data['best_fitness']:<6.0f} | ")
            f.write(f"{gen_data['avg_fitness']:<6.0f} | ")
            f.write(f"{gen_data['std_dev']:<6.0f} | ")
            f.write(f"{gen_data.get('avg_kills', 0):<6.1f} | ")
            f.write(f"{gen_data.get('avg_steps', 0):<6.0f} | ")
            f.write(f"{gen_data.get('avg_accuracy', 0)*100:<6.0f} | ")
            f.write(f"{gen_data.get('generations_since_improvement', 0):<6} |\n")
    else:
        f.write("| Gen   | Best   | Avg    | Min    | Median | StdDev | Best D | Avg D  |\n")
        f.write("|-------|--------|--------|--------|--------|--------|--------|--------|\n")

        for gen_data in recent:
            f.write(f"| {gen_data['generation']:<5} | ")
            f.write(f"{gen_data['best_fitness']:<6.1f} | ")
            f.write(f"{gen_data['avg_fitness']:<6.1f} | ")
            f.write(f"{gen_data['min_fitness']:<6.1f} | ")
            f.write(f"{gen_data['median_fitness']:<6.1f} | ")
            f.write(f"{gen_data['std_dev']:<6.1f} | ")
            f.write(f"{gen_data['best_improvement']:<+6.1f} | ")
            f.write(f"{gen_data['avg_improvement']:<+6.1f} |\n")

    f.write("\n</details>\n\n")


def write_best_generations(f, generations_data: List[Dict[str, Any]],
                           include_behavior: bool = False):
    """Write top performing generations.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
        include_behavior: Whether to include behavioral metrics
    """
    sorted_gens = sorted(generations_data, key=lambda x: x['best_fitness'], reverse=True)[:10]

    f.write("<details>\n<summary>Click to expand Top 10 Best Generations table</summary>\n\n")

    if include_behavior:
        f.write("| Rank | Gen   | Best   | Avg    | Kills  | Steps  | Accuracy |\n")
        f.write("|------|-------|--------|--------|--------|--------|----------|\n")

        for i, gen_data in enumerate(sorted_gens, 1):
            f.write(f"| {i:<4} | {gen_data['generation']:<5} | ")
            f.write(f"{gen_data['best_fitness']:<6.0f} | ")
            f.write(f"{gen_data['avg_fitness']:<6.0f} | ")
            f.write(f"{gen_data.get('best_agent_kills', 0):<6.1f} | ")
            f.write(f"{gen_data.get('best_agent_steps', 0):<6.0f} | ")
            f.write(f"{gen_data.get('best_agent_accuracy', 0)*100:<8.1f} |\n")
    else:
        f.write("| Rank | Gen   | Best Fitness | Avg Fitness  | Min Fitness  |\n")
        f.write("|------|-------|--------------|--------------|--------------|\n")

        for i, gen_data in enumerate(sorted_gens, 1):
            f.write(f"| {i:<4} | {gen_data['generation']:<5} | ")
            f.write(f"{gen_data['best_fitness']:<12.2f} | ")
            f.write(f"{gen_data['avg_fitness']:<12.2f} | ")
            f.write(f"{gen_data['min_fitness']:<12.2f} |\n")

    f.write("\n</details>\n\n")
