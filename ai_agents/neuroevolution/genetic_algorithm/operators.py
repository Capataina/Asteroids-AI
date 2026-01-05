from typing import List, Tuple
import random

class GAGeneticOperators:
  def __init__(self, mutation_probability: float = 0.1, crossover_probability: float = 0.9, mutation_gaussian_sigma: float = 0.1, mutation_uniform_low: float = -1.0, mutation_uniform_high: float = 1.0, crossover_alpha: float = 0.5):
    self.mutation_probability = mutation_probability
    self.crossover_probability = crossover_probability
    self.mutation_gaussian_sigma = mutation_gaussian_sigma
    self.mutation_uniform_low = mutation_uniform_low
    self.mutation_uniform_high = mutation_uniform_high
    self.crossover_alpha = crossover_alpha  # Blend factor for crossover (0.5 = equal mix)

  def mutate_gaussian(self, individual: List[float]) -> Tuple[List[float]]:
    """
    Gaussian mutation: add noise to parameters.
    
    Args:
      individual: Parameter vector
    
    Returns:
      Mutated individual (tuple for DEAP)
    """
    # Mutate each gene probabilistically, but always return ALL genes
    mutated = [
      individual[i] + random.gauss(0, self.mutation_gaussian_sigma) 
      if random.random() < self.mutation_probability 
      else individual[i]
      for i in range(len(individual))
    ]
    return (mutated,)

  def mutate_uniform(self, individual: List[float]) -> Tuple[List[float]]:
    """
    Uniform mutation: replace parameter with random value in range.
    
    Args:
      individual: Parameter vector
    
    Returns:
      Mutated individual (tuple for DEAP)
    """
    # Mutate each gene probabilistically, but always return ALL genes
    mutated = [
      random.uniform(self.mutation_uniform_low, self.mutation_uniform_high)
      if random.random() < self.mutation_probability 
      else individual[i]
      for i in range(len(individual))
    ]
    return (mutated,)

  def crossover_blend(self, individual1: List[float], individual2: List[float]) -> Tuple[List[float], List[float]]:
    """
    Blend crossover: create offspring between parents.

    Args:
      individual1: First parent
      individual2: Second parent

    Returns:
      Two offspring (tuples for DEAP)
    """
    # Create two complementary offspring using crossover_alpha as blend factor
    # alpha=0.5 means equal mix, alpha=0.7 means 70% from first parent
    alpha = self.crossover_alpha
    child1 = [
      individual1[i] * alpha + individual2[i] * (1 - alpha)
      for i in range(len(individual1))
    ]
    child2 = [
      individual2[i] * alpha + individual1[i] * (1 - alpha)
      for i in range(len(individual2))
    ]
    return (child1, child2)

  def crossover_arithmetic(self, individual1: List[float], individual2: List[float]) -> Tuple[List[float], List[float]]:
    """
    Arithmetic crossover: weighted average of parents.

    Args:
      individual1: First parent
      individual2: Second parent

    Returns:
      Two offspring (tuples for DEAP)
    """
    # Create two complementary offspring using crossover_alpha as blend factor
    alpha = self.crossover_alpha
    child1 = [
      individual1[i] * alpha + individual2[i] * (1 - alpha)
      for i in range(len(individual1))
    ]
    child2 = [
      individual2[i] * alpha + individual1[i] * (1 - alpha)
      for i in range(len(individual2))
    ]
    return (child1, child2)