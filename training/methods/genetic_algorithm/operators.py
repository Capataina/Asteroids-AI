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
    BLX-alpha crossover: create offspring by sampling from extended range.

    For each gene, samples from [min - alpha*d, max + alpha*d] where d is the
    distance between parents. This creates genetic diversity even when parents
    are similar.

    Args:
      individual1: First parent
      individual2: Second parent

    Returns:
      Two distinct offspring
    """
    alpha = self.crossover_alpha
    child1 = []
    child2 = []

    for i in range(len(individual1)):
      p1 = individual1[i]
      p2 = individual2[i]

      # Calculate range for BLX-alpha
      d = abs(p1 - p2)
      low = min(p1, p2) - alpha * d
      high = max(p1, p2) + alpha * d

      # Sample two different children from the range
      child1.append(random.uniform(low, high))
      child2.append(random.uniform(low, high))

    return (child1, child2)

  def crossover_arithmetic(self, individual1: List[float], individual2: List[float]) -> Tuple[List[float], List[float]]:
    """
    Arithmetic crossover: weighted average of parents with random alpha.

    Uses a random alpha for each crossover to create diverse offspring.

    Args:
      individual1: First parent
      individual2: Second parent

    Returns:
      Two complementary offspring
    """
    # Use random alpha for diversity
    alpha = random.uniform(0.3, 0.7)

    child1 = [
      individual1[i] * alpha + individual2[i] * (1 - alpha)
      for i in range(len(individual1))
    ]
    child2 = [
      individual1[i] * (1 - alpha) + individual2[i] * alpha
      for i in range(len(individual2))
    ]
    return (child1, child2)
