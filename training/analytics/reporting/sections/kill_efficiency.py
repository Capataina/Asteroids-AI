"""
Kill efficiency report section.

Generates kill efficiency analysis.
"""

from typing import List, Dict, Any

from training.analytics.analysis.behavioral import calculate_kill_efficiency


def write_kill_efficiency(f, generations_data: List[Dict[str, Any]]):
    """Write kill efficiency analysis.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if not generations_data or 'avg_kills' not in generations_data[-1]:
        f.write("No behavioral data available for kill efficiency analysis.\n\n")
        return

    # Get final phase data (last 10%)
    n = len(generations_data)
    final_phase = generations_data[-max(1, n // 10):]
    first_phase = generations_data[:max(1, n // 10)]

    final_eff = calculate_kill_efficiency(final_phase)
    first_eff = calculate_kill_efficiency(first_phase)

    f.write("### Current Performance (Final Phase)\n\n")
    f.write(f"- **Kills per 100 Steps:** {final_eff['kills_per_100']:.2f} (up from {first_eff['kills_per_100']:.2f} in Phase 1)\n")
    f.write(f"- **Shots per Kill:** {final_eff['shots_per_kill']:.2f} (down from {first_eff['shots_per_kill']:.2f} in Phase 1)\n")
    f.write(f"- **Kill Conversion Rate:** {final_eff['conversion_rate']*100:.1f}% (up from {first_eff['conversion_rate']*100:.1f}% in Phase 1)\n")
    f.write(f"- **Average Kills per Episode:** {final_eff['avg_kills']:.1f}\n\n")

    # Efficiency trend table
    f.write("### Efficiency Trend\n\n")
    f.write("| Phase | Kills/100 Steps | Shots/Kill | Conversion Rate |\n")
    f.write("|-------|-----------------|------------|----------------|\n")

    num_phases = min(5, n)
    phase_size = max(1, n // num_phases)

    for phase in range(num_phases):
        start_idx = phase * phase_size
        end_idx = min(start_idx + phase_size, n)
        if phase == num_phases - 1:
            end_idx = n

        phase_data = generations_data[start_idx:end_idx]
        eff = calculate_kill_efficiency(phase_data)
        f.write(f"| Phase {phase + 1} | {eff['kills_per_100']:.2f} | {eff['shots_per_kill']:.2f} | {eff['conversion_rate']*100:.1f}% |\n")

    # Assessment
    spk_improvement = ((first_eff['shots_per_kill'] - final_eff['shots_per_kill']) / max(0.1, first_eff['shots_per_kill'])) * 100
    f.write(f"\n**Assessment:** ")
    if spk_improvement > 50:
        f.write(f"Agent has learned efficient killing. Shots per kill dropped {spk_improvement:.0f}%.\n\n")
    elif spk_improvement > 20:
        f.write(f"Agent has improved efficiency moderately. Shots per kill dropped {spk_improvement:.0f}%.\n\n")
    elif spk_improvement > 0:
        f.write(f"Agent shows slight efficiency improvement. Shots per kill dropped {spk_improvement:.0f}%.\n\n")
    else:
        f.write("Agent efficiency has not improved significantly.\n\n")
