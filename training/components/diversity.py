"""
Reward Diversity System

Encourages agents to earn rewards from multiple components rather than
specializing in one easy source. This prevents degenerate strategies
like "just fly around" or "camp in corner" that exploit single reward sources.
"""

import math
from typing import Dict, List


def compute_reward_diversity(reward_breakdown: Dict[str, float]) -> float:
    """
    Calculate entropy-based diversity of reward distribution.

    Measures how evenly the agent's rewards are distributed across
    different reward components. Uses Shannon entropy normalized to [0, 1].

    Args:
        reward_breakdown: Dictionary mapping reward component names to their totals

    Returns:
        Diversity score:
        - 0.0 = All reward from single source (specialist/degenerate)
        - 1.0 = Equal reward from all sources (balanced/human-like)
    """
    if not reward_breakdown:
        return 0.0

    # Only consider positive rewards (achievements, not penalties)
    positive_rewards = {k: v for k, v in reward_breakdown.items() if v > 0}
    total = sum(positive_rewards.values())

    # Need at least 2 positive sources and some total reward
    if total <= 0 or len(positive_rewards) <= 1:
        return 0.0

    # Calculate Shannon entropy
    entropy = 0.0
    for value in positive_rewards.values():
        proportion = value / total
        if proportion > 0:
            entropy -= proportion * math.log(proportion)

    # Normalize by maximum possible entropy (uniform distribution)
    max_entropy = math.log(len(positive_rewards))

    if max_entropy <= 0:
        return 0.0

    return entropy / max_entropy


def compute_population_diversity_stats(
    reward_breakdowns: List[Dict[str, float]]
) -> Dict[str, float]:
    """
    Compute diversity statistics across a population.

    Args:
        reward_breakdowns: List of reward breakdown dicts, one per agent

    Returns:
        Dictionary with population diversity statistics
    """
    if not reward_breakdowns:
        return {
            'avg_diversity': 0.0,
            'min_diversity': 0.0,
            'max_diversity': 0.0,
            'std_diversity': 0.0,
        }

    diversities = [compute_reward_diversity(rb) for rb in reward_breakdowns]

    avg = sum(diversities) / len(diversities)
    min_div = min(diversities)
    max_div = max(diversities)

    # Standard deviation
    if len(diversities) > 1:
        variance = sum((d - avg) ** 2 for d in diversities) / len(diversities)
        std = math.sqrt(variance)
    else:
        std = 0.0

    return {
        'avg_diversity': avg,
        'min_diversity': min_div,
        'max_diversity': max_div,
        'std_diversity': std,
    }


def get_reward_balance_warnings(reward_breakdown: Dict[str, float]) -> List[str]:
    """
    Analyze reward breakdown and return warnings about imbalances.

    Args:
        reward_breakdown: Dictionary mapping reward component names to their totals

    Returns:
        List of warning strings describing potential issues
    """
    warnings = []

    if not reward_breakdown:
        return warnings

    positive_rewards = {k: v for k, v in reward_breakdown.items() if v > 0}
    negative_rewards = {k: v for k, v in reward_breakdown.items() if v < 0}

    total_positive = sum(positive_rewards.values()) if positive_rewards else 0
    total_negative = abs(sum(negative_rewards.values())) if negative_rewards else 0

    # Check for dominant components (>60% of positive reward)
    for name, value in positive_rewards.items():
        if total_positive > 0:
            proportion = value / total_positive
            if proportion > 0.6:
                warnings.append(f"{name} is dominant ({proportion*100:.0f}% of positive reward)")

    # Check for unused components (positive rewards with <5% share)
    for name, value in positive_rewards.items():
        if total_positive > 0:
            proportion = value / total_positive
            if proportion < 0.05:
                warnings.append(f"{name} is underutilized ({proportion*100:.1f}% of positive reward)")

    # Check penalty ratio
    if total_positive > 0:
        penalty_ratio = total_negative / total_positive
        if penalty_ratio > 0.8:
            warnings.append(f"High penalty ratio ({penalty_ratio*100:.0f}% of positive rewards)")

    return warnings
