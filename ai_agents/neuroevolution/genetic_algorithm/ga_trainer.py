import random
from ai_agents.neuroevolution.genetic_algorithm.operators import GAGeneticOperators
from ai_agents.neuroevolution.genetic_algorithm.ga_agent import GAAgent
from interfaces.StateEncoder import StateEncoder
from interfaces.ActionInterface import ActionInterface
from training.base.EpisodeRunner import EpisodeRunner
from typing import List

class GATrainer:
  def __init__(self, population_size: int, num_generations: int, mutation_probability: float, crossover_probability: float, mutation_gaussian_sigma: float, mutation_uniform_low: float, mutation_uniform_high: float, crossover_alpha: float, state_encoder: StateEncoder, action_interface: ActionInterface, episode_runner: EpisodeRunner):
    self.population_size = population_size
    self.num_generations = num_generations
    self.mutation_probability = mutation_probability
    self.crossover_probability = crossover_probability
    self.mutation_gaussian_sigma = mutation_gaussian_sigma
    self.mutation_uniform_low = mutation_uniform_low
    self.mutation_uniform_high = mutation_uniform_high
    self.crossover_alpha = crossover_alpha
    self.state_encoder = state_encoder
    self.action_interface = action_interface
    self.episode_runner = episode_runner
    self.operators = GAGeneticOperators(mutation_probability, crossover_probability, mutation_gaussian_sigma, mutation_uniform_low, mutation_uniform_high, crossover_alpha)

  def evaluate_individual(self, individual: List[float]) -> float:
    """
    Evaluate fitness of an individual parameter vector.
    
    Args:
      individual: Parameter vector
    
    Returns:
      Fitness score
    """
    return self.episode_runner.run_episode(individual)

  def train(self) -> GAAgent:
    """
    Train the GA agent.
    
    Returns:
      Best agent from final generation
    """
    # Initialize population (random parameter vectors)
    population = self.random_population()
    
    best_agent = None
    best_fitness = float('inf')
    # For each generation:
    for generation in range(self.num_generations):
      # Evaluate population
      fitnesses = [self.evaluate_individual(individual) for individual in population]

      # Select parents (tournament selection)
      parents = [population[i] for i in self.tournament_selection(fitnesses, self.population_size)]

      # Apply crossover and mutation
      offspring = [self.operators.crossover(parents[0], parents[1]) for _ in range(self.population_size - len(parents))]
      # Replace population (elitism)
      population = self.elitism(parents + offspring, fitnesses)
      # Update best agent
      if fitnesses[0] < best_fitness:
        best_fitness = fitnesses[0]
        best_agent = population[0]

    # Return best agent
    return GAAgent(best_agent, self.state_encoder, self.action_interface)


  # Helper methods

  def random_population(self) -> List[List[float]]:
    """
    Generate a random population of parameter vectors.
    
    Returns:
      List of parameter vectors
    """
    # Calculate correct parameter size: state_size * action_size
    # Each action (4 total: left, right, thrust, shoot) needs a weight for each state feature
    state_size = self.state_encoder.get_state_size()
    action_size = 4
    param_size = state_size * action_size
    
    return [
      [random.uniform(self.mutation_uniform_low, self.mutation_uniform_high) for _ in range(param_size)]
      for _ in range(self.population_size)
    ]

  def elitism(self, population: List[List[float]], fitnesses: List[float]) -> List[List[float]]:
    """
    Select the best individuals from population using elitism.
    
    Args:
      population: List of parameter vectors
      fitnesses: List of fitness scores
    
    Returns:
      List of selected parameter vectors
    """
    return [population[i] for i in range(len(population)) if fitnesses[i] == min(fitnesses)]

  def tournament_selection(self, fitnesses: List[float], tournament_size: int) -> List[int]:
    """
    Select parents from population using tournament selection.
    
    Args:
      fitnesses: List of fitness scores
      tournament_size: Size of tournament
    
    Returns:
      List of indices of selected parents
    """
    selected = []
    for _ in range(len(fitnesses)):
      # Randomly select tournament_size individuals
      tournament_indices = random.sample(range(len(fitnesses)), min(tournament_size, len(fitnesses)))
      # Find the best individual in the tournament
      winner_idx = max(tournament_indices, key=lambda idx: fitnesses[idx])
      selected.append(winner_idx)
    return selected