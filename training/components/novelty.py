"""
Behavior Novelty System

Encourages diverse action patterns across the population by rewarding agents
that behave differently from others. This prevents convergence to identical
strategies and promotes exploration of the behavior space.
"""

import math
from typing import List, Dict


def compute_behavior_vector(metrics: Dict, steps: int) -> List[float]:
    """
    Compute reward-agnostic behavior characterization from agent metrics.

    All values are normalized to [0, 1] for fair distance comparison.
    This vector describes WHAT the agent did, not how well it was rewarded.

    Args:
        metrics: Dictionary containing agent evaluation metrics
        steps: Total steps the agent survived

    Returns:
        List of 7 normalized behavior features
    """
    if steps <= 0:
        return [0.0] * 7

    return [
        # Movement tendency - how often does it thrust?
        min(metrics.get('thrust_frames', 0) / steps, 1.0),

        # Rotation tendency - how often does it turn?
        min(metrics.get('turn_frames', 0) / steps, 1.0),

        # Aggression - how often does it shoot?
        min(metrics.get('shoot_frames', 0) / steps, 1.0),

        # Precision - hits / shots (already [0, 1])
        min(metrics.get('accuracy', 0.0), 1.0),

        # Passivity - proportion of frames with no input
        min(metrics.get('idle_rate', 0.0), 1.0),

        # Engagement distance - how close does it get to asteroids?
        # Normalized by 400px (roughly half screen diagonal)
        min(metrics.get('avg_asteroid_dist', 400.0) / 400.0, 1.0),

        # Area coverage - how much does it move around the screen?
        # Normalized by 20 wraps (arbitrary reasonable max)
        min(metrics.get('screen_wraps', 0) / 20.0, 1.0),
    ]


def euclidean_distance(vec1: List[float], vec2: List[float]) -> float:
    """Calculate Euclidean distance between two behavior vectors."""
    if len(vec1) != len(vec2):
        raise ValueError(f"Vector length mismatch: {len(vec1)} vs {len(vec2)}")

    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))


def compute_behavior_novelty(
    behavior: List[float],
    population_behaviors: List[List[float]],
    archive_behaviors: List[List[float]],
    k_nearest: int = 15
) -> float:
    """
    Calculate novelty score as average distance to k-nearest neighbors.

    Higher score = more unique/novel behavior.

    Args:
        behavior: The behavior vector to evaluate
        population_behaviors: Behaviors of current population (excluding self)
        archive_behaviors: Behaviors from the historical archive
        k_nearest: Number of nearest neighbors to consider

    Returns:
        Novelty score (higher = more novel)
    """
    all_behaviors = population_behaviors + archive_behaviors

    if len(all_behaviors) == 0:
        return 1.0  # Everything is maximally novel when alone

    # Calculate distances to all other behaviors
    distances = [euclidean_distance(behavior, other) for other in all_behaviors]

    # Sort and take k nearest
    distances.sort()
    k = min(k_nearest, len(distances))

    if k == 0:
        return 1.0

    # Average distance to k nearest neighbors
    return sum(distances[:k]) / k


def compute_population_novelty(
    population_behaviors: List[List[float]],
    archive_behaviors: List[List[float]],
    k_nearest: int = 15
) -> List[float]:
    """
    Compute novelty scores for an entire population.

    Args:
        population_behaviors: List of behavior vectors for all agents
        archive_behaviors: Behaviors from the historical archive
        k_nearest: Number of nearest neighbors to consider

    Returns:
        List of novelty scores, one per agent
    """
    novelty_scores = []

    for i, behavior in enumerate(population_behaviors):
        # Exclude self from population when computing novelty
        other_population = population_behaviors[:i] + population_behaviors[i+1:]

        novelty = compute_behavior_novelty(
            behavior,
            other_population,
            archive_behaviors,
            k_nearest
        )
        novelty_scores.append(novelty)

    return novelty_scores
