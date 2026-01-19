"""
Pareto ranking utilities (front assignment and crowding distance).
"""

from typing import Dict, List, Tuple


def _dominates(a: List[float], b: List[float], directions: List[str]) -> bool:
    better_or_equal = True
    strictly_better = False
    for idx, direction in enumerate(directions):
        av = a[idx]
        bv = b[idx]
        if direction == "max":
            if av < bv:
                better_or_equal = False
                break
            if av > bv:
                strictly_better = True
        else:
            if av > bv:
                better_or_equal = False
                break
            if av < bv:
                strictly_better = True
    return better_or_equal and strictly_better


def pareto_fronts(values: List[List[float]], directions: List[str]) -> List[List[int]]:
    """
    Compute Pareto fronts using a fast non-dominated sort.
    """
    n = len(values)
    if n == 0:
        return []

    dominates_list = [[] for _ in range(n)]
    dominated_count = [0 for _ in range(n)]
    fronts: List[List[int]] = []

    for p in range(n):
        for q in range(n):
            if p == q:
                continue
            if _dominates(values[p], values[q], directions):
                dominates_list[p].append(q)
            elif _dominates(values[q], values[p], directions):
                dominated_count[p] += 1

    current_front = [i for i in range(n) if dominated_count[i] == 0]
    fronts.append(current_front)

    i = 0
    while i < len(fronts) and fronts[i]:
        next_front = []
        for p in fronts[i]:
            for q in dominates_list[p]:
                dominated_count[q] -= 1
                if dominated_count[q] == 0:
                    next_front.append(q)
        if next_front:
            fronts.append(next_front)
        i += 1

    return fronts


def crowding_distance(
    front: List[int],
    values: List[List[float]],
    directions: List[str]
) -> Dict[int, float]:
    """
    Compute crowding distance for a single Pareto front.
    """
    distances = {idx: 0.0 for idx in front}
    if len(front) <= 2:
        for idx in front:
            distances[idx] = float("inf")
        return distances

    num_obj = len(values[0])
    for obj_idx in range(num_obj):
        sorted_front = sorted(front, key=lambda i: values[i][obj_idx])

        distances[sorted_front[0]] = float("inf")
        distances[sorted_front[-1]] = float("inf")

        min_val = values[sorted_front[0]][obj_idx]
        max_val = values[sorted_front[-1]][obj_idx]
        denom = max(1e-12, max_val - min_val)

        for i in range(1, len(sorted_front) - 1):
            prev_idx = sorted_front[i - 1]
            next_idx = sorted_front[i + 1]
            prev_val = values[prev_idx][obj_idx]
            next_val = values[next_idx][obj_idx]
            distances[sorted_front[i]] += (next_val - prev_val) / denom

    return distances
