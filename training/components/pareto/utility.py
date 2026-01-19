"""
Pareto ordering and utility helpers.
"""

from typing import Dict, List, Tuple
from training.components.pareto.ranking import pareto_fronts, crowding_distance


def pareto_order(
    values: List[List[float]],
    directions: List[str]
) -> Tuple[List[int], List[int], List[float]]:
    """
    Return (order, front_ranks, crowding) for a population.

    Order is sorted by (front_rank asc, crowding desc).
    """
    n = len(values)
    if n == 0:
        return [], [], []

    fronts = pareto_fronts(values, directions)
    front_rank = [0 for _ in range(n)]
    crowding = [0.0 for _ in range(n)]

    for rank, front in enumerate(fronts):
        for idx in front:
            front_rank[idx] = rank
        distances = crowding_distance(front, values, directions)
        for idx, dist in distances.items():
            crowding[idx] = dist

    order = sorted(range(n), key=lambda i: (front_rank[i], -crowding[i]))
    return order, front_rank, crowding
