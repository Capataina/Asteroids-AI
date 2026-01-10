"""
ASCII charts report section.

Generates ASCII fitness progression chart.
"""

from typing import List, Dict, Any


def write_ascii_chart(f, generations_data: List[Dict[str, Any]]):
    """Generate ASCII chart of fitness progression.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if not generations_data:
        f.write("No data available.\n\n")
        return

    # Sample data points (every Nth generation for readability)
    step = max(1, len(generations_data) // 50)
    sampled = generations_data[::step]

    all_best = [g['best_fitness'] for g in sampled]
    all_avg = [g['avg_fitness'] for g in sampled]

    max_val = max(all_best)
    min_val = min(min(all_avg), 0)
    range_val = max_val - min_val

    if range_val == 0:
        f.write("Not enough variance to chart.\n\n")
        return

    f.write("```\n")
    f.write("Best Fitness (*) vs Avg Fitness (o) Over Generations\n\n")

    # Create chart (15 rows for compactness)
    chart_height = 15
    for row in range(chart_height, -1, -1):
        threshold = min_val + (range_val * row / chart_height)

        # Y-axis label
        f.write(f"{threshold:8.0f} |")

        # Plot points
        for i in range(len(sampled)):
            best = all_best[i]
            avg = all_avg[i]

            if best >= threshold and (row == chart_height or best < min_val + (range_val * (row + 1) / chart_height)):
                f.write("*")
            elif avg >= threshold and (row == chart_height or avg < min_val + (range_val * (row + 1) / chart_height)):
                f.write("o")
            else:
                f.write(" ")

        f.write("\n")

    # X-axis
    f.write("         " + "-" * len(sampled) + "\n")
    f.write(f"         Gen 1{' ' * (len(sampled) - 15)}Gen {generations_data[-1]['generation']}\n")
    f.write("```\n\n")
