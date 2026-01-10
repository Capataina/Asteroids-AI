"""
Learning velocity report section.

Generates learning velocity analysis showing how fast fitness is improving
and whether learning is accelerating or decelerating.
"""

from typing import List, Dict, Any


def calculate_velocity_by_phase(generations_data: List[Dict[str, Any]], num_phases: int = 5) -> List[Dict[str, Any]]:
    """Calculate learning velocity metrics by phase.

    Args:
        generations_data: List of generation data dictionaries
        num_phases: Number of phases to divide training into

    Returns:
        List of phase velocity data
    """
    n = len(generations_data)
    if n < 2:
        return []

    phase_size = max(1, n // num_phases)
    results = []

    for phase in range(num_phases):
        start_idx = phase * phase_size
        end_idx = min(start_idx + phase_size, n)
        if phase == num_phases - 1:
            end_idx = n

        phase_data = generations_data[start_idx:end_idx]
        if len(phase_data) < 2:
            continue

        # Calculate fitness change across phase
        start_best = phase_data[0]['best_fitness']
        end_best = phase_data[-1]['best_fitness']
        fitness_delta = end_best - start_best

        # Per-generation rate
        num_gens = len(phase_data)
        delta_per_gen = fitness_delta / num_gens if num_gens > 0 else 0

        # Classify velocity
        if delta_per_gen > 20:
            velocity_class = "Fast"
        elif delta_per_gen > 5:
            velocity_class = "Moderate"
        elif delta_per_gen > 0:
            velocity_class = "Slow"
        else:
            velocity_class = "Stalled"

        results.append({
            'phase': phase + 1,
            'fitness_delta': fitness_delta,
            'delta_per_gen': delta_per_gen,
            'velocity_class': velocity_class,
            'num_gens': num_gens,
        })

    return results


def calculate_acceleration(velocity_phases: List[Dict[str, Any]]) -> float:
    """Calculate acceleration (change in velocity over phases).

    Args:
        velocity_phases: List of phase velocity data

    Returns:
        Acceleration value (positive = speeding up, negative = slowing down)
    """
    if len(velocity_phases) < 2:
        return 0.0

    # Compare first half velocity to second half velocity
    mid = len(velocity_phases) // 2
    early_velocity = sum(p['delta_per_gen'] for p in velocity_phases[:mid]) / mid
    late_velocity = sum(p['delta_per_gen'] for p in velocity_phases[mid:]) / (len(velocity_phases) - mid)

    return late_velocity - early_velocity


def write_learning_velocity(f, generations_data: List[Dict[str, Any]]):
    """Write learning velocity analysis.

    Args:
        f: File handle to write to
        generations_data: List of generation data dictionaries
    """
    if len(generations_data) < 10:
        f.write("Not enough data for velocity analysis (need at least 10 generations).\n\n")
        return

    velocity_phases = calculate_velocity_by_phase(generations_data)
    if not velocity_phases:
        f.write("Could not calculate velocity phases.\n\n")
        return

    acceleration = calculate_acceleration(velocity_phases)

    # Current velocity (last phase)
    current_velocity = velocity_phases[-1]['delta_per_gen']

    # Project generations to reach target (if improving)
    current_best = generations_data[-1]['best_fitness']
    target_fitness = current_best * 1.5  # 50% improvement target

    if current_velocity > 0:
        gens_to_target = int((target_fitness - current_best) / current_velocity)
    else:
        gens_to_target = None

    f.write("### Velocity by Phase\n\n")
    f.write("| Phase | Fitness Delta | Delta/Gen | Velocity | Trend |\n")
    f.write("|-------|---------------|-----------|----------|-------|\n")

    prev_velocity = None
    for phase in velocity_phases:
        trend = ""
        if prev_velocity is not None:
            if phase['delta_per_gen'] > prev_velocity * 1.1:
                trend = "↑ Accelerating"
            elif phase['delta_per_gen'] < prev_velocity * 0.9:
                trend = "↓ Slowing"
            else:
                trend = "→ Stable"

        f.write(f"| Phase {phase['phase']} | {phase['fitness_delta']:+.0f} | "
                f"{phase['delta_per_gen']:+.1f} | {phase['velocity_class']} | {trend} |\n")
        prev_velocity = phase['delta_per_gen']

    f.write("\n")

    # Current velocity summary
    f.write("### Current Velocity\n\n")
    f.write(f"- **Recent Improvement Rate:** {current_velocity:+.1f} fitness/generation\n")

    if acceleration > 1:
        f.write(f"- **Acceleration:** {acceleration:+.1f} (learning speeding up)\n")
    elif acceleration < -1:
        f.write(f"- **Acceleration:** {acceleration:+.1f} (learning slowing down)\n")
    else:
        f.write(f"- **Acceleration:** {acceleration:+.1f} (relatively stable)\n")

    if gens_to_target and gens_to_target > 0 and gens_to_target < 10000:
        f.write(f"- **Projected Generations to +50% Fitness:** ~{gens_to_target} generations\n")
    elif current_velocity <= 0:
        f.write(f"- **Projected Generations to +50% Fitness:** N/A (not improving)\n")

    f.write("\n")

    # Assessment
    f.write("### Velocity Assessment\n\n")

    if current_velocity > 10 and acceleration >= 0:
        f.write("Learning is progressing well with good velocity. Continue training.\n\n")
    elif current_velocity > 5:
        f.write("Learning is progressing at a moderate pace. Consider if further training is worthwhile.\n\n")
    elif current_velocity > 0:
        f.write("Learning is slow. The population may be approaching a local optimum. Consider:\n")
        f.write("- Increasing mutation rate to escape plateau\n")
        f.write("- Adding diversity through fresh random individuals\n\n")
    else:
        f.write("Learning has stalled. Fitness is no longer improving. Consider:\n")
        f.write("- Stopping training (may have converged)\n")
        f.write("- Restarting with different hyperparameters\n")
        f.write("- Reviewing reward structure\n\n")
