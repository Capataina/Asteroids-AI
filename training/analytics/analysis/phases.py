"""
Phase utilities for analytics.

Provides consistent phase splitting and summary statistics across the report.
"""

from typing import List, Dict, Any, Iterable


def split_generations(generations_data: List[Dict[str, Any]], phase_count: int = 4) -> List[Dict[str, Any]]:
    """Split generations into evenly sized phases.

    Args:
        generations_data: Full generation history.
        phase_count: Number of phases to create.

    Returns:
        List of phase dictionaries with labels and data slices.
    """
    n = len(generations_data)
    if n == 0:
        return []

    phase_count = max(1, min(phase_count, n))
    base = n // phase_count
    remainder = n % phase_count

    phases = []
    start = 0
    for idx in range(phase_count):
        size = base + (1 if idx < remainder else 0)
        end = min(n, start + size)
        if end <= start:
            continue

        phase_data = generations_data[start:end]
        pct_start = int(round((start / n) * 100))
        pct_end = int(round((end / n) * 100))
        phases.append({
            "index": idx + 1,
            "start_index": start,
            "end_index": end,
            "pct_start": pct_start,
            "pct_end": pct_end,
            "gen_start": phase_data[0].get("generation", start + 1),
            "gen_end": phase_data[-1].get("generation", end),
            "label": f"Phase {idx + 1} ({pct_start}-{pct_end}%)",
            "data": phase_data,
        })
        start = end

    return phases


def _median(values: List[float]) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    mid = len(values) // 2
    if len(values) % 2 == 0:
        return (values[mid - 1] + values[mid]) / 2.0
    return values[mid]


def summarize_values(values: Iterable[float]) -> Dict[str, float]:
    """Summarize a list of numeric values."""
    values = list(values)
    if not values:
        return {
            "count": 0,
            "mean": 0.0,
            "median": 0.0,
            "min": 0.0,
            "max": 0.0,
            "std": 0.0,
        }

    count = len(values)
    mean = sum(values) / count
    var = sum((v - mean) ** 2 for v in values) / count
    std = var ** 0.5

    return {
        "count": count,
        "mean": mean,
        "median": _median(values),
        "min": min(values),
        "max": max(values),
        "std": std,
    }


def extract_series(generations_data: List[Dict[str, Any]], key: str, default: float = 0.0) -> List[float]:
    """Extract a metric series from generations."""
    return [g.get(key, default) for g in generations_data]


def phase_metric_stats(
    generations_data: List[Dict[str, Any]],
    key: str,
    phase_count: int = 4,
    default: float = 0.0
) -> List[Dict[str, Any]]:
    """Compute phase summaries for a metric."""
    phases = split_generations(generations_data, phase_count=phase_count)
    results = []
    for phase in phases:
        values = extract_series(phase["data"], key, default=default)
        summary = summarize_values(values)
        summary.update({
            "label": phase["label"],
            "gen_start": phase["gen_start"],
            "gen_end": phase["gen_end"],
        })
        results.append(summary)
    return results
