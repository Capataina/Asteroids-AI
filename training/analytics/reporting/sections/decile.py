"""
Decile breakdown report section.

Generates training progress broken down by decile (10 equal phases).
"""

from typing import List, Dict, Any


def write_decile_breakdown(f, generations_data: List[Dict[str, Any]]):
    """Write training progress broken down by decile (10 equal phases).

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    n = len(generations_data)
    if n < 10:
        # For short runs, use fewer phases
        if n < 5:
            f.write("Not enough data for decile breakdown (need at least 5 generations).\n\n")
            return
        num_phases = n
    else:
        num_phases = 10

    phase_size = max(1, n // num_phases)

    f.write("| Phase | Gens | Best Fit | Avg Fit | Avg Kills | Avg Acc | Avg Steps | Diversity |\n")
    f.write("|-------|------|----------|---------|-----------|---------|-----------|----------|\n")

    for phase in range(num_phases):
        start_idx = phase * phase_size
        end_idx = min(start_idx + phase_size, n)
        if phase == num_phases - 1:
            end_idx = n  # Include all remaining in last phase

        phase_data = generations_data[start_idx:end_idx]
        if not phase_data:
            continue

        start_gen = phase_data[0]['generation']
        end_gen = phase_data[-1]['generation']
        best_fit = max(g['best_fitness'] for g in phase_data)
        avg_fit = sum(g['avg_fitness'] for g in phase_data) / len(phase_data)
        avg_kills = sum(g.get('avg_kills', 0) for g in phase_data) / len(phase_data)
        avg_acc = sum(g.get('avg_accuracy', 0) for g in phase_data) / len(phase_data)
        avg_steps = sum(g.get('avg_steps', 0) for g in phase_data) / len(phase_data)
        diversity = sum(g.get('std_dev', 0) for g in phase_data) / len(phase_data)

        pct_start = int((phase / num_phases) * 100)
        pct_end = int(((phase + 1) / num_phases) * 100)

        f.write(f"| {pct_start}-{pct_end}% | {start_gen}-{end_gen} | {best_fit:.0f} | {avg_fit:.0f} | "
                f"{avg_kills:.1f} | {avg_acc*100:.0f}% | {avg_steps:.0f} | {diversity:.0f} |\n")

    f.write("\n")
