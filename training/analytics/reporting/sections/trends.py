"""
Trend analysis report section.

Generates fitness trend analysis.
"""

from typing import List, Dict, Any


def write_trend_analysis(f, generations_data: List[Dict[str, Any]]):
    """Analyze and write fitness trends over time.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if len(generations_data) < 10:
        f.write("Not enough data for trend analysis.\n\n")
        return

    # Split into quarters
    total = len(generations_data)
    quarter = total // 4

    quarters = [
        generations_data[:quarter],
        generations_data[quarter:quarter * 2],
        generations_data[quarter * 2:quarter * 3],
        generations_data[quarter * 3:]
    ]

    f.write("| Period | Avg Best | Avg Mean | Avg Min | Improvement |\n")
    f.write("|--------|----------|----------|---------|-------------|\n")

    prev_avg_best = None
    for i, q in enumerate(quarters, 1):
        if not q:
            continue
        avg_best = sum(g['best_fitness'] for g in q) / len(q)
        avg_mean = sum(g['avg_fitness'] for g in q) / len(q)
        avg_min = sum(g['min_fitness'] for g in q) / len(q)

        improvement = ""
        if prev_avg_best is not None:
            delta = avg_best - prev_avg_best
            improvement = f"{delta:+.1f}"

        f.write(f"| Q{i} | {avg_best:.1f} | {avg_mean:.1f} | {avg_min:.1f} | {improvement} |\n")
        prev_avg_best = avg_best

    f.write("\n")
