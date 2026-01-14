"""
Evolution Strategies training method.

This module implements Evolution Strategies (ES) for training neural network
policies in the Asteroids environment. ES is a gradient-free optimization
method that estimates gradients through sampling.
"""

from training.methods.evolution_strategies.driver import ESDriver
from training.methods.evolution_strategies.fitness_shaping import (
    rank_transformation,
    compute_centered_ranks
)

__all__ = ['ESDriver', 'rank_transformation', 'compute_centered_ranks']
