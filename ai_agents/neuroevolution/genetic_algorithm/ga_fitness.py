from training.base.EpisodeRunner import EpisodeRunner
from interfaces.RewardCalculator import ComposableRewardCalculator
from typing import List
from ai_agents.neuroevolution.genetic_algorithm.ga_agent import GAAgent

class GAFitness:
  def __init__(self, episode_runner: EpisodeRunner, reward_calculator: ComposableRewardCalculator):
    self.episode_runner = episode_runner
    self.reward_calculator = reward_calculator

  def evaluate_ga_fitness(self, parameter_vector: List[float]) -> float:
    """
    Evaluate fitness of GA agent with parameter vector.
    
    Args:
      parameter_vector: List of floats encoding control policy
    
    Returns:
      Fitness score
    """
    # Create GAAgent from parameter vector
    agent = GAAgent(parameter_vector, self.state_encoder, self.action_interface)

    # Run episode using EpisodeRunner
    episode_result = self.episode_runner.run_episode(agent)

    # Return fitness score
    return episode_result.total_reward