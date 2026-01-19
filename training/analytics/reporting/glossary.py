"""
Metric glossary for analytics reporting.

Centralizes metric explanations to keep report sections consistent.
"""

from typing import Dict, Tuple, List


METRIC_GLOSSARY: Dict[str, Tuple[str, str]] = {
    # Fitness and population
    "best_fitness": ("Best fitness", "Highest per-generation fitness across the population (max average reward)."),
    "avg_fitness": ("Average fitness", "Mean fitness across the population for a generation."),
    "min_fitness": ("Minimum fitness", "Lowest fitness in the population for a generation."),
    "std_dev": ("Fitness std dev", "Standard deviation of fitness across the population (diversity proxy)."),
    "p25_fitness": ("Fitness p25", "25th percentile of population fitness."),
    "p75_fitness": ("Fitness p75", "75th percentile of population fitness."),
    "median_fitness": ("Median fitness", "Median population fitness (robust central tendency)."),
    "avg_fitness_std": ("Seed fitness std", "Average per-agent fitness std dev across seeds (evaluation noise proxy)."),
    "best_improvement": ("Best improvement", "Change in best fitness compared to the previous generation."),
    "avg_improvement": ("Average improvement", "Change in average fitness compared to the previous generation."),

    # Combat and survival
    "avg_kills": ("Average kills", "Mean kills per episode across the population."),
    "max_kills": ("Max kills", "Highest kills achieved by any agent in the generation."),
    "avg_steps": ("Average steps", "Mean steps survived per episode across the population."),
    "max_steps": ("Max steps", "Highest steps survived by any agent in the generation."),
    "avg_accuracy": ("Accuracy", "Hits divided by shots fired (0 to 1)."),
    "avg_shots": ("Average shots", "Mean shots fired per episode across the population."),
    "avg_hits": ("Average hits", "Mean hits per episode across the population."),
    "avg_shots_per_kill": ("Shots per kill", "Shots fired divided by kills (lower is more efficient)."),
    "avg_shots_per_hit": ("Shots per hit", "Shots fired divided by hits (lower is more efficient)."),
    "std_dev_kills": ("Kills std dev", "Standard deviation of kills across the population."),
    "std_dev_steps": ("Steps std dev", "Standard deviation of survival steps across the population."),
    "std_dev_accuracy": ("Accuracy std dev", "Standard deviation of accuracy across the population."),

    # Reward composition
    "avg_reward_breakdown": ("Reward breakdown", "Per-component average reward contribution per episode."),
    "reward_entropy": ("Reward entropy", "Normalized entropy of positive reward components (balance proxy)."),
    "reward_dominance_index": ("Reward dominance index", "HHI-style dominance of positive rewards (higher = more concentrated)."),
    "reward_max_share": ("Reward max share", "Share of total positive reward from the largest component."),
    "reward_positive_component_count": ("Positive component count", "Number of reward components with positive contribution."),

    # Control + aim
    "avg_turn_deadzone_rate": ("Turn deadzone rate", "Fraction of frames where signed turn input is exactly zero (deadzone currently disabled)."),
    "avg_turn_balance": ("Turn balance", "Right-turn frames minus left-turn frames divided by total turning."),
    "avg_turn_switch_rate": ("Turn switch rate", "Rate of turn direction switches per signed turn."),
    "avg_turn_streak": ("Average turn streak", "Average consecutive frames turning in the same direction."),
    "avg_max_turn_streak": ("Max turn streak", "Longest consecutive turn streak per episode (averaged)."),
    "avg_frontness": ("Frontness average", "Alignment of nearest asteroid with ship heading (1 ahead, 0 behind)."),
    "avg_frontness_at_shot": ("Frontness at shot", "Frontness measured at shot times (aim alignment during firing)."),
    "avg_frontness_at_hit": ("Frontness at hit", "Frontness measured at hit times (aim alignment on hits)."),
    "avg_shot_distance": ("Shot distance", "Distance to nearest asteroid when firing (pixels)."),
    "avg_hit_distance": ("Hit distance", "Distance to nearest asteroid when hits occur (pixels)."),
    "std_dev_frontness": ("Frontness std dev", "Standard deviation of frontness across the population."),
    "std_dev_danger_exposure_rate": ("Danger exposure std dev", "Standard deviation of danger exposure across the population."),
    "std_dev_softmin_ttc": ("Soft-min TTC std dev", "Standard deviation of soft-min TTC across the population."),
    "std_dev_turn_deadzone_rate": ("Deadzone std dev", "Standard deviation of the per-agent zero-turn rate across the population (deadzone currently disabled)."),
    "std_dev_coverage_ratio": ("Coverage std dev", "Standard deviation of coverage ratio across the population."),

    # Risk and movement
    "avg_min_dist": ("Min asteroid distance", "Closest distance to an asteroid during an episode (pixels)."),
    "avg_asteroid_dist": ("Average asteroid distance", "Mean distance to nearest asteroid over time (pixels)."),
    "avg_danger_exposure_rate": ("Danger exposure rate", "Fraction of frames with a nearby asteroid inside danger radius."),
    "avg_danger_entries": ("Danger entries", "Average number of entries into the danger zone per episode."),
    "avg_danger_reaction_time": ("Danger reaction time", "Average frames to react after entering danger."),
    "avg_danger_wraps": ("Danger wraps", "Screen-wrap count while in danger zones (mobility under threat)."),
    "avg_softmin_ttc": ("Soft-min TTC", "Weighted time-to-collision proxy that emphasizes the nearest threats (seconds)."),
    "softmin_ttc": ("Soft-min TTC", "Weighted time-to-collision proxy that emphasizes the nearest threats (seconds)."),
    "avg_distance_traveled": ("Distance traveled", "Total distance traveled per episode (pixels)."),
    "avg_speed": ("Average speed", "Mean movement speed per episode."),
    "avg_speed_std": ("Speed std dev", "Standard deviation of movement speed per episode."),
    "avg_coverage_ratio": ("Coverage ratio", "Fraction of spatial grid cells visited (0 to 1)."),
    "std_dev_fitness_std": ("Seed fitness std dev", "Standard deviation of per-agent fitness std across the population."),

    # Action usage
    "avg_thrust_frames": ("Thrust frames", "Average frames with thrust active per episode."),
    "avg_turn_frames": ("Turn frames", "Average frames with turn input active per episode."),
    "avg_shoot_frames": ("Shoot frames", "Average frames with shooting active per episode."),
    "avg_thrust_duration": ("Thrust duration", "Average consecutive frames per thrust burst."),
    "avg_turn_duration": ("Turn duration", "Average consecutive frames per turning burst."),
    "avg_shoot_duration": ("Shoot duration", "Average consecutive frames per shooting burst."),
    "avg_idle_rate": ("Idle rate", "Fraction of frames with no action input."),
    "avg_screen_wraps": ("Screen wraps", "Average number of screen-edge wraps per episode."),

    # Neural behavior
    "avg_output_saturation": ("Output saturation", "Share of NN outputs near 0 or 1 (binary control tendency)."),
    "avg_action_entropy": ("Action entropy", "Entropy of action combinations (higher = more varied control)."),
    "avg_quarterly_scores": ("Quarterly scores", "Average reward earned in each episode quarter (0-25%, 25-50%, 50-75%, 75-100%)."),

    # Performance timing
    "evaluation_duration": ("Evaluation duration", "Wall time spent evaluating a generation."),
    "evolution_duration": ("Evolution duration", "Wall time spent evolving a generation."),
    "total_gen_duration": ("Total generation duration", "Combined evaluation and evolution wall time."),
    "sigma": ("Sigma", "CMA-ES global step size controlling exploration radius."),
    "cov_diag_mean": ("Cov diag mean", "Mean diagonal covariance value (per-parameter variance)."),
    "cov_diag_std": ("Cov diag std", "Standard deviation of diagonal covariance values."),
    "cov_diag_mean_abs_dev": ("Cov diag mean abs dev", "Mean absolute deviation of diagonal covariance from 1.0."),
    "cov_diag_max_abs_dev": ("Cov diag max abs dev", "Largest absolute deviation of diagonal covariance from 1.0."),
    "cov_lr_scale": ("Cov lr scale", "Scaling factor applied to CMA-ES covariance learning rates (c1/cmu)."),
    "cov_lr_effective_rate": ("Cov lr effective rate", "Effective c1 + cmu rate used for diagonal covariance update."),

    # Generalization
    "fitness_ratio": ("Fitness ratio", "Fresh-game fitness divided by training fitness for the same generation."),
    "generalization_grade": ("Generalization grade", "Letter grade derived from generalization ratios."),
}


def glossary_entries(keys: List[str]) -> List[Tuple[str, str]]:
    """Map glossary keys to (label, description) entries."""
    entries: List[Tuple[str, str]] = []
    for key in keys:
        entry = METRIC_GLOSSARY.get(key)
        if entry:
            entries.append(entry)
    return entries
