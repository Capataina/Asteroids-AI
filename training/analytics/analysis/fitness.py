"""
Fitness statistics utilities.

Provides statistical functions for analyzing fitness scores.
"""

import math
from typing import List


def median(values: List[float]) -> float:
    """Calculate median value.

    Args:
        values: List of numeric values

    Returns:
        Median value
    """
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n % 2 == 0:
        return (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2
    return sorted_vals[n // 2]


def std_dev(values: List[float]) -> float:
    """Calculate standard deviation.

    Args:
        values: List of numeric values

    Returns:
        Standard deviation
    """
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return math.sqrt(variance)


def percentile(values: List[float], p: float) -> float:
    """Calculate percentile.

    Args:
        values: List of numeric values
        p: Percentile (0-100)

    Returns:
        Value at the given percentile
    """
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    idx = int(len(sorted_vals) * p / 100)
    return sorted_vals[min(idx, len(sorted_vals) - 1)]


def pearson_correlation(x: List[float], y: List[float]) -> float:
    """Calculate Pearson correlation coefficient.

    Args:
        x: First list of values
        y: Second list of values

    Returns:
        Correlation coefficient (-1 to 1)
    """
    if len(x) != len(y) or len(x) < 2:
        return 0.0
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / n)
    std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / n)
    if std_x == 0 or std_y == 0:
        return 0.0
    cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
    return cov / (std_x * std_y)


def calculate_skewness(values: List[float]) -> float:
    """Calculate Fisher's skewness.

    Args:
        values: List of numeric values

    Returns:
        Skewness value
    """
    n = len(values)
    if n < 3:
        return 0.0

    mean = sum(values) / n
    std = std_dev(values)

    if std == 0:
        return 0.0

    skewness = (n / ((n - 1) * (n - 2))) * sum(((x - mean) / std) ** 3 for x in values)
    return skewness


def calculate_kurtosis(values: List[float]) -> float:
    """Calculate Fisher's excess kurtosis.

    Args:
        values: List of numeric values

    Returns:
        Excess kurtosis value
    """
    n = len(values)
    if n < 4:
        return 0.0

    mean = sum(values) / n
    std = std_dev(values)

    if std == 0:
        return 0.0

    m4 = sum((x - mean) ** 4 for x in values) / n
    kurtosis = (m4 / (std ** 4)) - 3
    return kurtosis
