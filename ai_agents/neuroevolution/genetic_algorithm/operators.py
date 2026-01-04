from typing import List, Tuple
import random

class GAGeneticOperators:
  def __init__(self, mutation_probability: float = 0.1, crossover_probability: float = 0.9, mutation_gaussian_sigma: float = 0.1, mutation_uniform_low: float = -1.0, mutation_uniform_high: float = 1.0, crossover_alpha: float = 0.5):
    self.mutation_probability = mutation_probability
    self.crossover_probability = crossover_probability
    self.mutation_gaussian_sigma = mutation_gaussian_sigma
    self.mutation_uniform_low = mutation_uniform_low
    self.mutation_uniform_high = mutation_uniform_high
    self.crossover_probability = crossover_probability

  def mutate_gaussian(self, individual: List[float]) -> Tuple[List[float]]:
    """
    Gaussian mutation: add noise to parameters.
    
    Args:
      individual: Parameter vector
    
    Returns:
      Mutated individual (tuple for DEAP)
    """
    return [individual[i] + random.gauss(0, self.mutation_gaussian_sigma) for i in range(len(individual)) if random.random() < self.mutation_probability]

  def mutate_uniform(self, individual: List[float]) -> Tuple[List[float]]:
    """
    Uniform mutation: replace parameter with random value in range.
    
    Args:
      individual: Parameter vector
    
    Returns:
      Mutated individual (tuple for DEAP)
    """
    return [individual[i] + random.uniform(self.mutation_uniform_low, self.mutation_uniform_high) for i in range(len(individual)) if random.random() < self.mutation_probability]

  def crossover_blend(self, individual1: List[float], individual2: List[float]) -> Tuple[List[float], List[float]]:
    """
    Blend crossover: create offspring between parents.

    Args:
      individual1: First parent
      individual2: Second parent
    
    Returns:
      Two offspring (tuples for DEAP)
    """
    return [(individual1[i] * self.crossover_probability + individual2[i] * (1 - self.crossover_probability)) for i in range(len(individual1))]

  def crossover_arithmetic(self, individual1: List[float], individual2: List[float]) -> Tuple[List[float], List[float]]:
    """
    Arithmetic crossover: weighted average of parents.
    
    Args:
      individual1: First parent
      individual2: Second parent
    
    Returns:
      Two offspring (tuples for DEAP)
    """
    return [(individual1[i] * self.crossover_probability + individual2[i] * (1 - self.crossover_probability)) for i in range(len(individual1))]