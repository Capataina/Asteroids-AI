"""
Learning progress report section.

Generates learning progress analysis.
"""

from typing import List, Dict, Any

from training.analytics.analysis.convergence import analyze_learning_progress


def write_learning_progress(f, generations_data: List[Dict[str, Any]]):
    """Analyze and write learning progress.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if len(generations_data) < 5:
        f.write("Not enough data for learning analysis.\n\n")
        return

    progress = analyze_learning_progress(generations_data)
    if not progress:
        f.write("Not enough data for learning analysis.\n\n")
        return

    early_n = progress['early_n']
    early_best_avg = progress['early_best_avg']
    late_best_avg = progress['late_best_avg']
    early_avg_avg = progress['early_avg_avg']
    late_avg_avg = progress['late_avg_avg']
    best_improvement = progress['best_improvement']
    avg_improvement = progress['avg_improvement']
    verdict = progress['verdict']

    f.write(f"**Comparing First {early_n} vs Last {early_n} Generations:**\n\n")
    f.write(f"| Metric | Early | Late | Change |\n")
    f.write(f"|--------|-------|------|--------|\n")
    f.write(f"| Best Fitness | {early_best_avg:.1f} | {late_best_avg:.1f} | {best_improvement:+.1f}% |\n")
    f.write(f"| Avg Fitness | {early_avg_avg:.1f} | {late_avg_avg:.1f} | {avg_improvement:+.1f}% |\n\n")

    # Learning verdict
    if verdict == 'strong':
        f.write("**Verdict:** Strong learning - both best and average fitness improved significantly.\n\n")
    elif verdict == 'moderate':
        f.write("**Verdict:** Moderate learning - some improvement but room for more training.\n\n")
    elif verdict == 'weak':
        f.write("**Verdict:** Weak learning - minimal improvement, consider tuning parameters.\n\n")
    else:
        f.write("**Verdict:** No learning detected - fitness may have decreased. Check for issues.\n\n")
