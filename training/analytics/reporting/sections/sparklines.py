"""
Sparklines report section.

Generates ASCII sparklines for quick trend visualization.
"""

from typing import List, Dict, Any


def write_sparklines(f, generations_data: List[Dict[str, Any]]):
    """Generate ASCII sparklines for quick trend visualization.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if len(generations_data) < 2:
        f.write("Not enough data for sparklines.\n\n")
        return

    sparkline_chars = "▁▂▃▄▅▆▇█"

    def make_sparkline(values, width=10):
        """Create sparkline from values."""
        if not values:
            return "N/A"
        # Sample to width points
        step = max(1, len(values) // width)
        sampled = values[::step][:width]
        if len(sampled) < 2:
            return "▄" * len(sampled)

        min_val = min(sampled)
        max_val = max(sampled)
        range_val = max_val - min_val

        if range_val == 0:
            return "▄" * len(sampled)

        result = ""
        for v in sampled:
            idx = int((v - min_val) / range_val * 7)
            idx = max(0, min(7, idx))
            result += sparkline_chars[idx]
        return result

    # Gather metrics
    best_fitness = [g['best_fitness'] for g in generations_data]
    avg_fitness = [g['avg_fitness'] for g in generations_data]
    avg_kills = [g.get('avg_kills', 0) for g in generations_data]
    avg_accuracy = [g.get('avg_accuracy', 0) for g in generations_data]
    avg_steps = [g.get('avg_steps', 0) for g in generations_data]
    std_devs = [g.get('std_dev', 0) for g in generations_data]

    def pct_change(values):
        if len(values) < 2 or values[0] == 0:
            return 0
        return ((values[-1] - values[0]) / abs(values[0])) * 100

    f.write("```\n")
    f.write(f"Best Fitness: {best_fitness[0]:.0f} → {best_fitness[-1]:.0f}   [{make_sparkline(best_fitness)}] {pct_change(best_fitness):+.0f}%\n")
    f.write(f"Avg Fitness:  {avg_fitness[0]:.0f} → {avg_fitness[-1]:.0f}   [{make_sparkline(avg_fitness)}] {pct_change(avg_fitness):+.0f}%\n")
    if any(avg_kills):
        f.write(f"Avg Kills:    {avg_kills[0]:.1f} → {avg_kills[-1]:.1f}   [{make_sparkline(avg_kills)}] {pct_change(avg_kills):+.0f}%\n")
    if any(avg_accuracy):
        f.write(f"Avg Accuracy: {avg_accuracy[0]*100:.0f}% → {avg_accuracy[-1]*100:.0f}%   [{make_sparkline(avg_accuracy)}] {pct_change(avg_accuracy):+.0f}%\n")
    if any(avg_steps):
        f.write(f"Avg Steps:    {avg_steps[0]:.0f} → {avg_steps[-1]:.0f}   [{make_sparkline(avg_steps)}] {pct_change(avg_steps):+.0f}%\n")
    if any(std_devs):
        f.write(f"Diversity:    {std_devs[0]:.0f} → {std_devs[-1]:.0f}   [{make_sparkline(std_devs)}] {pct_change(std_devs):+.0f}%\n")
    f.write("```\n\n")
