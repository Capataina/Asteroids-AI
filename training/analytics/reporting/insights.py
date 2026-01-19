"""
Reporting insight helpers.

Provides phase-based trend classification and confidence tagging.
"""

from typing import List, Dict, Any

from training.analytics.analysis.phases import (
    split_generations,
    extract_series,
    summarize_values,
    phase_metric_stats,
)


def _pct_change(start: float, end: float) -> float:
    if start == 0:
        if end == 0:
            return 0.0
        return 100.0 if end > 0 else -100.0
    return ((end - start) / abs(start)) * 100.0


def _direction_switches(values: List[float]) -> int:
    if len(values) < 3:
        return 0
    switches = 0
    prev_sign = 0
    for i in range(1, len(values)):
        delta = values[i] - values[i - 1]
        sign = 1 if delta > 0 else -1 if delta < 0 else 0
        if sign != 0 and prev_sign != 0 and sign != prev_sign:
            switches += 1
        if sign != 0:
            prev_sign = sign
    return switches


def trend_stats(
    generations_data: List[Dict[str, Any]],
    key: str,
    higher_is_better: bool = True,
    phase_count: int = 4,
    default: float = 0.0
) -> Dict[str, Any]:
    """Compute phase-based trend stats for a metric."""
    values = extract_series(generations_data, key, default=default)
    if len(values) < 2:
        return {
            "key": key,
            "start": 0.0,
            "end": 0.0,
            "delta": 0.0,
            "pct_change": 0.0,
            "directional_pct": 0.0,
            "effect_size": 0.0,
            "noise_ratio": 0.0,
            "switches": 0,
            "tag": "insufficient data",
            "confidence": "insufficient data",
            "phase_means": [],
        }

    phase_stats = phase_metric_stats(generations_data, key, phase_count=phase_count, default=default)
    phase_means = [p["mean"] for p in phase_stats] if phase_stats else []
    start = phase_means[0] if phase_means else values[0]
    end = phase_means[-1] if phase_means else values[-1]
    delta = end - start
    pct_change = _pct_change(start, end)

    directional_delta = delta if higher_is_better else -delta
    directional_pct = pct_change if higher_is_better else -pct_change

    series_summary = summarize_values(values)
    series_std = series_summary["std"]
    series_mean = series_summary["mean"]
    effect_size = directional_delta / max(series_std, 1.0)
    noise_ratio = series_std / max(abs(series_mean), 1.0)
    switches = _direction_switches(phase_means) if phase_means else 0

    tag = classify_trend_tag(directional_pct, effect_size, noise_ratio, switches)
    confidence = classify_confidence(effect_size, noise_ratio, switches, len(values))

    return {
        "key": key,
        "start": start,
        "end": end,
        "delta": delta,
        "pct_change": pct_change,
        "directional_pct": directional_pct,
        "effect_size": effect_size,
        "noise_ratio": noise_ratio,
        "switches": switches,
        "tag": tag,
        "confidence": confidence,
        "phase_means": phase_means,
    }


def classify_trend_tag(
    directional_pct: float,
    effect_size: float,
    noise_ratio: float,
    switches: int
) -> str:
    """Classify trend into human-readable tags."""
    if switches >= 2 and abs(directional_pct) < 20:
        return "volatile"

    if abs(effect_size) < 0.25:
        if noise_ratio > 1.0:
            return "inconclusive (noisy)"
        return "stagnation"

    if directional_pct >= 120 or effect_size >= 1.5:
        return "breakout improvement"
    if directional_pct >= 60 or effect_size >= 1.0:
        return "great improvement"
    if directional_pct >= 25 or effect_size >= 0.6:
        return "steady improvement"
    if directional_pct >= 8 or effect_size >= 0.3:
        return "slight improvement"

    if directional_pct <= -120 or effect_size <= -1.5:
        return "sharp regression"
    if directional_pct <= -60 or effect_size <= -1.0:
        return "regression"
    if directional_pct <= -25 or effect_size <= -0.6:
        return "slight regression"

    return "stagnation"


def classify_confidence(effect_size: float, noise_ratio: float, switches: int, count: int) -> str:
    """Classify confidence in a trend."""
    if count < 4:
        return "insufficient data"
    if noise_ratio > 1.0 or switches >= 2:
        return "low confidence (noisy)"
    if abs(effect_size) >= 1.0 and switches == 0:
        return "high confidence"
    if abs(effect_size) >= 0.5:
        return "moderate confidence"
    return "low confidence"


def phase_labels(generations_data: List[Dict[str, Any]], phase_count: int = 4) -> List[str]:
    """Return phase labels for the report."""
    phases = split_generations(generations_data, phase_count=phase_count)
    return [p["label"] for p in phases]
