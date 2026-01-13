"""
Combined Selection Scoring

Combines fitness, behavior novelty, and reward diversity into a single
selection score used for parent selection in evolutionary algorithms.
"""

from typing import Dict, List, Optional
from training.config.novelty import NoveltyConfig


def compute_selection_score(
    fitness: float,
    behavior_novelty: float,
    reward_diversity: float,
    config: Optional[NoveltyConfig] = None
) -> float:
    """
    Compute combined selection score for an individual.

    Balances three objectives:
    1. Fitness: How well does the agent perform?
    2. Behavior Novelty: How different is this agent from others?
    3. Reward Diversity: Does the agent use multiple reward sources?

    Args:
        fitness: Raw fitness score (can be negative)
        behavior_novelty: Novelty score from behavior comparison [0+]
        reward_diversity: Entropy-based diversity score [0, 1]
        config: Novelty configuration (uses defaults if None)

    Returns:
        Combined selection score
    """
    if config is None:
        config = NoveltyConfig()

    score = fitness

    # Behavior novelty bonus
    # Scaled by a multiplier to bring novelty into similar range as fitness
    if config.enable_behavior_novelty:
        score += config.behavior_novelty_weight * behavior_novelty * config.novelty_fitness_scale

    # Reward diversity bonus
    # Scaled by |fitness| so high-diversity low-fitness agents don't dominate
    if config.enable_reward_diversity:
        fitness_magnitude = abs(fitness) if abs(fitness) > 1.0 else 1.0
        score += config.diversity_weight * reward_diversity * fitness_magnitude

    return score


def compute_population_selection_scores(
    fitnesses: List[float],
    novelty_scores: List[float],
    diversity_scores: List[float],
    config: Optional[NoveltyConfig] = None
) -> List[float]:
    """
    Compute selection scores for an entire population.

    Args:
        fitnesses: List of fitness scores
        novelty_scores: List of behavior novelty scores
        diversity_scores: List of reward diversity scores
        config: Novelty configuration (uses defaults if None)

    Returns:
        List of combined selection scores
    """
    if config is None:
        config = NoveltyConfig()

    if len(fitnesses) != len(novelty_scores) or len(fitnesses) != len(diversity_scores):
        raise ValueError("All input lists must have the same length")

    return [
        compute_selection_score(f, n, d, config)
        for f, n, d in zip(fitnesses, novelty_scores, diversity_scores)
    ]


def get_selection_stats(
    fitnesses: List[float],
    novelty_scores: List[float],
    diversity_scores: List[float],
    selection_scores: List[float]
) -> Dict[str, float]:
    """
    Compute statistics about the selection score components.

    Useful for understanding how much each component contributes.

    Args:
        fitnesses: Raw fitness scores
        novelty_scores: Behavior novelty scores
        diversity_scores: Reward diversity scores
        selection_scores: Combined selection scores

    Returns:
        Dictionary with component statistics
    """
    n = len(fitnesses)
    if n == 0:
        return {}

    avg_fitness = sum(fitnesses) / n
    avg_novelty = sum(novelty_scores) / n
    avg_diversity = sum(diversity_scores) / n
    avg_selection = sum(selection_scores) / n

    # Calculate how much novelty and diversity contributed
    avg_bonus = avg_selection - avg_fitness

    return {
        'avg_fitness': avg_fitness,
        'avg_novelty': avg_novelty,
        'avg_diversity': avg_diversity,
        'avg_selection_score': avg_selection,
        'avg_novelty_diversity_bonus': avg_bonus,
        'max_fitness': max(fitnesses),
        'max_novelty': max(novelty_scores),
        'max_diversity': max(diversity_scores),
        'max_selection_score': max(selection_scores),
    }
