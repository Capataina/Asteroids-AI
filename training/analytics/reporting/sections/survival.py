"""
Survival distribution report section.

Generates survival distribution analysis.
"""

from typing import List, Dict, Any


def write_survival_distribution(f, generations_data: List[Dict[str, Any]], config: Dict[str, Any]):
    """Write survival distribution analysis.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
        config: Training configuration dictionary
    """
    if not generations_data or 'avg_steps' not in generations_data[-1]:
        f.write("No survival data available.\n\n")
        return

    # Get survival data from last phase
    n = len(generations_data)
    final_phase = generations_data[-max(1, n // 10):]

    avg_survival = sum(g.get('avg_steps', 0) for g in final_phase) / len(final_phase)
    max_survival = max(g.get('max_steps', 0) for g in final_phase)

    # Estimate completion rate (survived to max_steps)
    max_steps_config = config.get('max_steps', 1500)

    f.write("### Survival Statistics (Final Phase)\n\n")
    f.write(f"- **Mean Survival:** {avg_survival:.0f} steps ({avg_survival/max_steps_config*100:.1f}% of max)\n")
    f.write(f"- **Max Survival:** {max_survival:.0f} steps\n")

    # Progression over training
    first_phase = generations_data[:max(1, n // 10)]
    first_avg_survival = sum(g.get('avg_steps', 0) for g in first_phase) / len(first_phase)

    f.write(f"\n### Survival Progression\n\n")
    f.write("| Phase | Mean Steps | Change |\n")
    f.write("|-------|------------|--------|\n")

    num_phases = min(5, n)
    phase_size = max(1, n // num_phases)
    prev_survival = None

    for phase in range(num_phases):
        start_idx = phase * phase_size
        end_idx = min(start_idx + phase_size, n)
        if phase == num_phases - 1:
            end_idx = n

        phase_data = generations_data[start_idx:end_idx]
        phase_survival = sum(g.get('avg_steps', 0) for g in phase_data) / len(phase_data)

        change = ""
        if prev_survival is not None:
            delta = phase_survival - prev_survival
            change = f"{delta:+.0f}"

        f.write(f"| Phase {phase + 1} | {phase_survival:.0f} | {change} |\n")
        prev_survival = phase_survival

    f.write("\n")
