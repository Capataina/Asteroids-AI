from EnvironmentTracker import EnvironmentTracker
from MetricsTracker import MetricsTracker

class RewardComponent:
  def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
    pass

  def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
    pass

  def reset(self) -> None:
    pass

class ComposableRewardCalculator:
  def __init__(self):
    self.components = {}
    self.enabled_components = set()

  def add_component(self, name: str, component: RewardComponent):
    self.components[name] = component

  def enable_component(self, name: str):
    self.enabled_components.add(name)

  def disable_component(self, name: str):
    self.enabled_components.remove(name)

  def is_enabled(self, name: str) -> bool:
    return self.components[name].enabled

  def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
    reward = 0.0

    current_metrics = metrics_tracker.get_episode_stats()

    for name in self.enabled_components:
      reward += self.components[name].calculate_step_reward(env_tracker, current_metrics)

    return reward

  def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
    reward = 0.0

    current_metrics = metrics_tracker.get_episode_stats()

    for name in self.enabled_components:
      reward += self.components[name].calculate_episode_reward(current_metrics)

    return reward

  def current_score(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
    return self.calculate_step_reward(env_tracker, metrics_tracker) + self.calculate_episode_reward(metrics_tracker)

  def reset(self) -> None:
    for name in self.enabled_components:
      self.components[name].reset()