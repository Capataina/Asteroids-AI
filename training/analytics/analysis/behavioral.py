"""
Behavioral metrics analysis.

Provides functions for analyzing kill efficiency and behavioral trends.
"""

from typing import List, Dict, Any, Tuple


def calculate_kill_efficiency(generations_data: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate kill efficiency metrics for a phase of training.

    Args:
        generations_data: List of generation data dictionaries (for a phase)

    Returns:
        Dictionary with efficiency metrics
    """
    if not generations_data:
        return {
            'kills_per_100': 0,
            'shots_per_kill': 0,
            'conversion_rate': 0,
            'avg_kills': 0,
        }

    avg_kills = sum(g.get('avg_kills', 0) for g in generations_data) / len(generations_data)
    avg_steps = sum(g.get('avg_steps', 1) for g in generations_data) / len(generations_data)
    avg_shots = sum(g.get('avg_shots', 1) for g in generations_data) / len(generations_data)

    kills_per_100 = (avg_kills / max(1, avg_steps)) * 100
    shots_per_kill = avg_shots / max(0.1, avg_kills)
    conversion_rate = avg_kills / max(1, avg_shots)

    return {
        'kills_per_100': kills_per_100,
        'shots_per_kill': shots_per_kill,
        'conversion_rate': conversion_rate,
        'avg_kills': avg_kills,
    }


def compare_efficiency_phases(generations_data: List[Dict[str, Any]]) -> Tuple[Dict, Dict]:
    """Compare kill efficiency between first and final phases.

    Args:
        generations_data: Full list of generation data

    Returns:
        Tuple of (first_phase_efficiency, final_phase_efficiency)
    """
    if not generations_data or 'avg_kills' not in generations_data[-1]:
        return {}, {}

    n = len(generations_data)
    phase_size = max(1, n // 10)

    first_phase = generations_data[:phase_size]
    final_phase = generations_data[-phase_size:]

    return (
        calculate_kill_efficiency(first_phase),
        calculate_kill_efficiency(final_phase)
    )


def calculate_behavioral_by_quarter(generations_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Calculate behavioral metrics by quarter.

    Args:
        generations_data: Full list of generation data

    Returns:
        List of dictionaries with metrics for each quarter
    """
    if not generations_data or 'avg_kills' not in generations_data[-1]:
        return []

    n = len(generations_data)
    if n < 4:
        return []

    quarter = n // 4
    quarters_data = [
        generations_data[:quarter],
        generations_data[quarter:quarter * 2],
        generations_data[quarter * 2:quarter * 3],
        generations_data[quarter * 3:]
    ]

    results = []
    for i, q in enumerate(quarters_data, 1):
        if not q:
            continue
        avg_kills = sum(g.get('avg_kills', 0) for g in q) / len(q)
        avg_steps = sum(g.get('avg_steps', 0) for g in q) / len(q)
        avg_acc = sum(g.get('avg_accuracy', 0) for g in q) / len(q)
        max_kills = max(g.get('max_kills', 0) for g in q)
        
        # New action metrics
        avg_thrust = sum(g.get('avg_thrust_frames', 0) for g in q) / len(q)
        avg_turn = sum(g.get('avg_turn_frames', 0) for g in q) / len(q)
        avg_shoot = sum(g.get('avg_shoot_frames', 0) for g in q) / len(q)
        avg_dist = sum(g.get('avg_asteroid_dist', 0) for g in q) / len(q)
        
        # Input style metrics
        thrust_dur = sum(g.get('avg_thrust_duration', 0) for g in q) / len(q)
        turn_dur = sum(g.get('avg_turn_duration', 0) for g in q) / len(q)
        shoot_dur = sum(g.get('avg_shoot_duration', 0) for g in q) / len(q)
        idle_rate = sum(g.get('avg_idle_rate', 0) for g in q) / len(q)
        screen_wraps = sum(g.get('avg_screen_wraps', 0) for g in q) / len(q)

        results.append({
            'quarter': i,
            'avg_kills': avg_kills,
            'avg_steps': avg_steps,
            'avg_accuracy': avg_acc,
            'max_kills': max_kills,
            'avg_thrust_frames': avg_thrust,
            'avg_turn_frames': avg_turn,
            'avg_shoot_frames': avg_shoot,
            'avg_asteroid_dist': avg_dist,
            'avg_thrust_duration': thrust_dur,
            'avg_turn_duration': turn_dur,
            'avg_shoot_duration': shoot_dur,
            'avg_idle_rate': idle_rate,
            'avg_screen_wraps': screen_wraps,
        })

    return results


def calculate_reward_evolution(generations_data: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    """Calculate reward component evolution across training phases.

    Args:
        generations_data: Full list of generation data

    Returns:
        Dictionary mapping component names to their phase values and trends
    """
    if not generations_data or 'avg_reward_breakdown' not in generations_data[-1]:
        return {}

    n = len(generations_data)
    num_phases = min(10, n)
    phase_size = max(1, n // num_phases)

    first_phase = generations_data[:phase_size]
    mid_idx = n // 2
    mid_phase = generations_data[mid_idx - phase_size // 2:mid_idx + phase_size // 2] or generations_data[mid_idx:mid_idx + 1]
    last_phase = generations_data[-phase_size:]

    components = list(generations_data[-1].get('avg_reward_breakdown', {}).keys())
    if not components:
        return {}

    def avg_component(data, comp):
        values = [g.get('avg_reward_breakdown', {}).get(comp, 0) for g in data]
        return sum(values) / len(values) if values else 0

    result = {}
    for comp in components:
        first_val = avg_component(first_phase, comp)
        mid_val = avg_component(mid_phase, comp)
        last_val = avg_component(last_phase, comp)

        if first_val != 0:
            pct_change = ((last_val - first_val) / abs(first_val)) * 100
        else:
            pct_change = 100 if last_val > 0 else -100 if last_val < 0 else 0

        result[comp] = {
            'first': first_val,
            'mid': mid_val,
            'last': last_val,
            'pct_change': pct_change,
        }

    return result
