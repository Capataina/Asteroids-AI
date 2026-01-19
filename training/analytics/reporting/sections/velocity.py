"""
Learning velocity report section.

Generates learning velocity analysis showing how fast fitness is improving
and whether learning is accelerating or decelerating.
"""

from typing import List, Dict, Any

from training.analytics.analysis.phases import split_generations, summarize_values
from training.analytics.reporting.sections.common import write_takeaways, write_warnings, write_glossary
from training.analytics.reporting.glossary import glossary_entries
from training.config.analytics import AnalyticsConfig


def calculate_velocity_by_phase(generations_data: List[Dict[str, Any]], phase_count: int = 4) -> List[Dict[str, Any]]:
    """Calculate learning velocity metrics by phase."""
    phases = split_generations(generations_data, phase_count=phase_count)
    if not phases:
        return []

    results = []
    for phase in phases:
        phase_data = phase["data"]
        if len(phase_data) < 2:
            continue

        start_best = phase_data[0]['best_fitness']
        end_best = phase_data[-1]['best_fitness']
        fitness_delta = end_best - start_best
        num_gens = len(phase_data)
        delta_per_gen = fitness_delta / num_gens if num_gens > 0 else 0

        results.append({
            'phase': phase["label"],
            'fitness_delta': fitness_delta,
            'delta_per_gen': delta_per_gen,
            'num_gens': num_gens,
        })

    return results


def calculate_acceleration(velocity_phases: List[Dict[str, Any]]) -> float:
    if len(velocity_phases) < 2:
        return 0.0

    mid = len(velocity_phases) // 2
    early_velocity = sum(p['delta_per_gen'] for p in velocity_phases[:mid]) / max(1, mid)
    late_velocity = sum(p['delta_per_gen'] for p in velocity_phases[mid:]) / max(1, len(velocity_phases) - mid)

    return late_velocity - early_velocity


def _percentile(values: List[float], pct: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    idx = int(round((pct / 100.0) * (len(values) - 1)))
    return values[max(0, min(len(values) - 1, idx))]


def write_learning_velocity(f, generations_data: List[Dict[str, Any]]):
    """Write learning velocity analysis."""
    if len(generations_data) < 10:
        f.write("Not enough data for velocity analysis (need at least 10 generations).\n\n")
        return

    velocity_phases = calculate_velocity_by_phase(generations_data, phase_count=AnalyticsConfig.PHASE_COUNT)
    if not velocity_phases:
        f.write("Could not calculate velocity phases.\n\n")
        return

    acceleration = calculate_acceleration(velocity_phases)
    current_velocity = velocity_phases[-1]['delta_per_gen']

    velocities = [v['delta_per_gen'] for v in velocity_phases]
    p25 = _percentile(velocities, 25)
    p75 = _percentile(velocities, 75)

    f.write("### Velocity by Phase\n\n")
    f.write("| Phase | Fitness Delta | Delta/Gen | Velocity Band |\n")
    f.write("|-------|---------------|-----------|---------------|\n")

    for phase in velocity_phases:
        band = "Balanced"
        if phase['delta_per_gen'] >= p75:
            band = "Fast"
        elif phase['delta_per_gen'] <= p25:
            band = "Slow"

        f.write(
            f"| {phase['phase']} | {phase['fitness_delta']:+.0f} | "
            f"{phase['delta_per_gen']:+.1f} | {band} |\n"
        )

    f.write("\n")

    f.write("### Current Velocity\n\n")
    f.write(f"- **Recent Improvement Rate:** {current_velocity:+.1f} fitness/generation\n")
    f.write(f"- **Acceleration:** {acceleration:+.1f} (positive = speeding up)\n\n")

    takeaways: List[str] = []
    warnings: List[str] = []

    trend = summarize_values(velocities)
    takeaways.append(f"Velocity mean {trend['mean']:+.1f} with std {trend['std']:.1f} across phases.")

    if current_velocity <= p25:
        warnings.append("Recent learning velocity is in the slowest quartile of the run.")
    if acceleration < 0 and abs(acceleration) > trend['std']:
        warnings.append("Learning is decelerating faster than typical phase-to-phase variation.")

    write_takeaways(f, takeaways)
    write_warnings(f, warnings)
    write_glossary(
        f,
        glossary_entries([
            "best_fitness",
        ])
    )
