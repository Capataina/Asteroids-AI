"""
Distribution analysis report section.

Generates ASCII Mean +/- StdDev charts for key metrics over recent generations.
"""

from typing import List, Dict, Any

from training.config.analytics import AnalyticsConfig
from training.analytics.reporting.insights import trend_stats
from training.analytics.reporting.sections.common import write_takeaways, write_warnings, write_glossary
from training.analytics.reporting.glossary import glossary_entries


def _draw_distribution_bar(mean: float, std: float, min_val: float, max_val: float, width: int = 40) -> str:
    """Draw a single ASCII bar representing Mean +/- StdDev."""
    if max_val == min_val:
        return " " * width + " (single value)"

    range_val = max_val - min_val
    if range_val == 0:
        range_val = 1.0

    def pos(val):
        p = int((val - min_val) / range_val * width)
        return max(0, min(width - 1, p))

    left_std = mean - std
    right_std = mean + std

    p_mean = pos(mean)
    p_left = pos(left_std)
    p_right = pos(right_std)

    chars = [' '] * width

    for i in range(p_left, p_right + 1):
        chars[i] = '-'

    chars[p_left] = '|'
    chars[p_right] = '|'
    chars[p_mean] = 'O'

    return "".join(chars)


def write_distribution_charts(f, generations_data: List[Dict[str, Any]]):
    """Write distribution charts for key metrics."""
    if not generations_data:
        return

    window = AnalyticsConfig.DISTRIBUTION_WINDOW
    recent = generations_data[-window:]

    if not recent:
        return

    f.write("## Distribution Analysis\n\n")
    f.write(f"### Metric Distributions (Last {len(recent)} Generations)\n\n")
    f.write("Visualizing population consistency: `|---O---|` represents Mean +/- 1 StdDev.\n")
    f.write("- **Narrow bar**: Consistent population (convergence)\n")
    f.write("- **Wide bar**: Diverse or noisy population\n\n")

    metrics = [
        ('avg_accuracy', 'std_dev_accuracy', 'Accuracy', True),
        ('avg_steps', 'std_dev_steps', 'Survival Steps', False),
        ('avg_kills', 'std_dev_kills', 'Kills', False),
        ('avg_fitness', 'std_dev', 'Fitness', False),
        ('avg_frontness', 'std_dev_frontness', 'Aim Frontness', True),
        ('avg_danger_exposure_rate', 'std_dev_danger_exposure_rate', 'Danger Exposure', True),
        ('avg_softmin_ttc', 'std_dev_softmin_ttc', 'Softmin TTC', False),
        ('avg_turn_deadzone_rate', 'std_dev_turn_deadzone_rate', 'Turn Deadzone', True),
        ('avg_coverage_ratio', 'std_dev_coverage_ratio', 'Coverage Ratio', True),
        ('avg_fitness_std', 'std_dev_fitness_std', 'Seed Fitness Std', False),
    ]

    for mean_key, std_key, label, is_pct in metrics:
        if mean_key not in recent[-1] or std_key not in recent[-1]:
            continue

        f.write(f"**{label} Distribution**\n")
        f.write("```\n")

        vals_low = [g.get(mean_key, 0) - g.get(std_key, 0) for g in recent]
        vals_high = [g.get(mean_key, 0) + g.get(std_key, 0) for g in recent]

        if not vals_low:
            continue

        global_min = min(vals_low)
        global_max = max(vals_high)

        if is_pct:
            global_min = max(0.0, global_min)
            global_max = min(1.0, global_max)
            if global_max < 0.1:
                global_max = 0.1
        else:
            global_min = min(0.0, global_min)
            if global_max == 0:
                global_max = 1.0
            global_max *= 1.1

        for g in recent:
            mean = g.get(mean_key, 0)
            std = g.get(std_key, 0)
            bar = _draw_distribution_bar(mean, std, global_min, global_max, AnalyticsConfig.CHART_WIDTH)

            if is_pct:
                f.write(f"Gen {g['generation']:3d}: {bar} {mean*100:5.1f}% +/- {std*100:4.1f}%\n")
            else:
                f.write(f"Gen {g['generation']:3d}: {bar} {mean:6.1f} +/- {std:5.1f}\n")

        f.write("```\n\n")

    # Takeaways and warnings
    takeaways: List[str] = []
    warnings: List[str] = []

    if 'std_dev' in generations_data[-1]:
        fitness_spread = trend_stats(generations_data, 'std_dev', higher_is_better=False, phase_count=AnalyticsConfig.PHASE_COUNT)
        takeaways.append(f"Fitness spread trend: {fitness_spread['tag']} ({fitness_spread['confidence']}).")
        if "regression" in fitness_spread['tag'] or "volatile" in fitness_spread['tag']:
            warnings.append("Fitness spread is widening or volatile; convergence is weak.")

    if 'avg_fitness_std' in generations_data[-1]:
        seed_noise = trend_stats(generations_data, 'avg_fitness_std', higher_is_better=False, phase_count=AnalyticsConfig.PHASE_COUNT)
        takeaways.append(f"Seed variance trend: {seed_noise['tag']} ({seed_noise['confidence']}).")
        if "regression" in seed_noise['tag']:
            warnings.append("Seed-to-seed variance is rising; evaluation noise may mask true improvements.")

    write_takeaways(f, takeaways)
    write_warnings(f, warnings)
    write_glossary(
        f,
        glossary_entries([
            "std_dev",
            "avg_fitness_std",
            "avg_accuracy",
            "std_dev_accuracy",
            "avg_steps",
            "std_dev_steps",
            "avg_kills",
            "std_dev_kills",
            "avg_frontness",
            "std_dev_frontness",
            "avg_danger_exposure_rate",
            "std_dev_danger_exposure_rate",
            "avg_softmin_ttc",
            "std_dev_softmin_ttc",
            "avg_turn_deadzone_rate",
            "std_dev_turn_deadzone_rate",
            "avg_coverage_ratio",
            "std_dev_coverage_ratio",
        ])
    )
