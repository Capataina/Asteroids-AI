"""
Sparklines report section.

Generates ASCII sparklines for quick trend visualization.
"""

from typing import List, Dict, Any, Callable

from training.config.analytics import AnalyticsConfig
from training.analytics.reporting.insights import trend_stats
from training.analytics.reporting.sections.common import write_glossary
from training.analytics.reporting.glossary import glossary_entries


def _bin_values(values: List[float], width: int) -> List[float]:
    if not values:
        return []
    width = max(1, min(width, len(values)))
    bins = []
    n = len(values)
    for i in range(width):
        start = int(i * n / width)
        end = int((i + 1) * n / width)
        chunk = values[start:end] or [values[start]]
        bins.append(sum(chunk) / len(chunk))
    return bins


def _make_sparkline(values: List[float], width: int) -> str:
    if not values:
        return "N/A"
    samples = _bin_values(values, width)
    if len(samples) < 2:
        return "." * len(samples)

    min_val = min(samples)
    max_val = max(samples)
    range_val = max_val - min_val
    if range_val == 0:
        return "." * len(samples)

    chars = " .:-=+*#%@"
    result = ""
    for v in samples:
        idx = int((v - min_val) / range_val * (len(chars) - 1))
        idx = max(0, min(len(chars) - 1, idx))
        result += chars[idx]
    return result


def _fmt_value(value: float, fmt: Callable[[float], str]) -> str:
    return fmt(value) if fmt else f"{value:.2f}"


def write_sparklines(f, generations_data: List[Dict[str, Any]]):
    """Generate ASCII sparklines for quick trend visualization."""
    if len(generations_data) < 2:
        f.write("Not enough data for sparklines.\n\n")
        return

    width = AnalyticsConfig.SPARKLINE_WIDTH
    metrics = [
        ("Best Fitness", "best_fitness", lambda v: f"{v:.0f}", True),
        ("Avg Fitness", "avg_fitness", lambda v: f"{v:.0f}", True),
        ("Min Fitness", "min_fitness", lambda v: f"{v:.0f}", True),
        ("Fitness Spread", "std_dev", lambda v: f"{v:.0f}", False),
        ("Avg Kills", "avg_kills", lambda v: f"{v:.1f}", True),
        ("Avg Accuracy", "avg_accuracy", lambda v: f"{v*100:.0f}%", True),
        ("Avg Steps", "avg_steps", lambda v: f"{v:.0f}", True),
        ("Action Entropy", "avg_action_entropy", lambda v: f"{v:.2f}", True),
        ("Output Saturation", "avg_output_saturation", lambda v: f"{v*100:.0f}%", False),
        ("Frontness Avg", "avg_frontness", lambda v: f"{v*100:.0f}%", True),
        ("Danger Exposure", "avg_danger_exposure_rate", lambda v: f"{v*100:.0f}%", False),
        ("Softmin TTC", "avg_softmin_ttc", lambda v: f"{v:.2f}", True),
        ("Seed Fitness Std", "avg_fitness_std", lambda v: f"{v:.1f}", False),
    ]

    f.write("```\n")
    for label, key, fmt, higher_is_better in metrics:
        if key not in generations_data[-1]:
            continue
        values = [g.get(key, 0.0) for g in generations_data]
        if all(v == 0 for v in values):
            continue
        stats = trend_stats(
            generations_data,
            key,
            higher_is_better=higher_is_better,
            phase_count=AnalyticsConfig.PHASE_COUNT,
        )
        line = (
            f"{label:<16} "
            f"{_fmt_value(stats['start'], fmt)} -> {_fmt_value(stats['end'], fmt)}  "
            f"[{_make_sparkline(values, width)}]  "
            f"{stats['tag']} ({stats['confidence']})"
        )
        f.write(line + "\n")
    f.write("```\n\n")

    write_glossary(
        f,
        glossary_entries([
            "best_fitness",
            "avg_fitness",
            "min_fitness",
            "std_dev",
            "avg_kills",
            "avg_accuracy",
            "avg_steps",
            "avg_action_entropy",
            "avg_output_saturation",
            "avg_frontness",
            "avg_danger_exposure_rate",
            "avg_softmin_ttc",
            "avg_fitness_std",
        ]),
        title="Quick Trend Glossary",
    )
