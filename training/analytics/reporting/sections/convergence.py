"""
Convergence analysis report section.

Generates population convergence analysis.
"""

from typing import List, Dict, Any

from training.analytics.analysis.convergence import analyze_convergence


def write_convergence_analysis(f, generations_data: List[Dict[str, Any]]):
    """Analyze and write population convergence.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if not generations_data:
        f.write("No data available.\n\n")
        return

    conv = analyze_convergence(generations_data)
    if not conv:
        f.write("Not enough data for convergence analysis.\n\n")
        return

    avg_std_dev = conv['avg_std_dev']
    avg_range = conv['avg_range']
    diversity_change = conv['diversity_change']
    status = conv['status']

    f.write(f"**Recent 20 Generations Analysis:**\n\n")
    f.write(f"- Average Standard Deviation: {avg_std_dev:.2f}\n")
    f.write(f"- Average Range (Best-Min): {avg_range:.2f}\n")
    f.write(f"- Diversity Change: {diversity_change:+.1f}%\n")

    if status == 'converging':
        f.write(f"- **Status:** Population is converging (low diversity)\n")
    elif status == 'moderate':
        f.write(f"- **Status:** Population has moderate diversity (healthy)\n")
    else:
        f.write(f"- **Status:** High diversity - population is still exploring\n")

    f.write("\n")
