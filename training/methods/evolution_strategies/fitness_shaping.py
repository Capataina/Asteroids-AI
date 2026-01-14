"""
Fitness Shaping for Evolution Strategies.

This module provides rank-based fitness transformation functions that
reduce sensitivity to outlier fitness values and provide consistent
gradient scales across generations.
"""

import math
from typing import List
import numpy as np


def compute_centered_ranks(fitnesses: List[float]) -> np.ndarray:
    """
    Compute centered ranks for fitness values.

    Transforms raw fitness values to ranks centered around 0,
    with values in the range [-0.5, 0.5].

    Args:
        fitnesses: List of raw fitness values.

    Returns:
        NumPy array of centered ranks.
    """
    n = len(fitnesses)
    if n == 0:
        return np.array([])

    # Get ranks (0 to n-1, where higher fitness = higher rank)
    ranks = np.zeros(n)
    sorted_indices = np.argsort(fitnesses)
    for rank, idx in enumerate(sorted_indices):
        ranks[idx] = rank

    # Center ranks to [-0.5, 0.5]
    centered_ranks = (ranks / (n - 1)) - 0.5 if n > 1 else np.zeros(n)

    return centered_ranks


def rank_transformation(fitnesses: List[float]) -> np.ndarray:
    """
    Apply rank-based fitness transformation (OpenAI ES style).

    Transforms raw fitness values using the formula:
        u_i = max(0, log(n/2 + 1) - log(rank_i))

    Then normalizes so utilities sum to 1 and are centered around 0.

    This transformation:
    - Is invariant to monotonic transformations of fitness
    - Reduces sensitivity to outlier fitness values
    - Provides consistent gradient scale across generations

    Args:
        fitnesses: List of raw fitness values.

    Returns:
        NumPy array of transformed utility values (sum to ~0, roughly in [-1, 1]).
    """
    n = len(fitnesses)
    if n == 0:
        return np.array([])

    if n == 1:
        return np.array([0.0])

    # Sort indices by fitness (descending - best first)
    sorted_indices = np.argsort(fitnesses)[::-1]

    # Compute utilities using log formula
    utilities = np.zeros(n)
    for rank, idx in enumerate(sorted_indices):
        # rank is 0-indexed, so rank 0 is the best
        # u_i = max(0, log(n/2 + 1) - log(rank + 1))
        u = max(0.0, math.log(n / 2 + 1) - math.log(rank + 1))
        utilities[idx] = u

    # Normalize: make utilities sum to 1, then subtract 1/n to center
    utility_sum = utilities.sum()
    if utility_sum > 0:
        utilities = utilities / utility_sum
    utilities = utilities - (1.0 / n)

    return utilities


def normalize_fitness(fitnesses: List[float]) -> np.ndarray:
    """
    Normalize fitness values to zero mean and unit variance.

    Simple alternative to rank transformation that preserves
    relative fitness differences.

    Args:
        fitnesses: List of raw fitness values.

    Returns:
        NumPy array of normalized fitness values.
    """
    fitnesses_array = np.array(fitnesses)
    mean = fitnesses_array.mean()
    std = fitnesses_array.std()

    if std < 1e-8:
        return np.zeros_like(fitnesses_array)

    return (fitnesses_array - mean) / std
