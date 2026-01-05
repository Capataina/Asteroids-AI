from interfaces.EnvironmentTracker import EnvironmentTracker
from interfaces.MetricsTracker import MetricsTracker

class RewardComponent:
  def __init__(self, name: str):
    self.name = name

  def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
    pass

  def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
    pass

  def reset(self) -> None:
    pass

class ComposableRewardCalculator:
  def __init__(self):
    self.score = 0.0
    self.components = {}
    self.enabled_components = set()
  
  def add_component(self, component: RewardComponent):
    self.components[component.name] = component
    self.enabled_components.add(component.name)

  def enable_component(self, name: str):
    self.enabled_components.add(name)

  def disable_component(self, name: str):
    self.enabled_components.discard(name)

  def is_enabled(self, name: str) -> bool:
    return name in self.enabled_components

  def calculate_step_reward(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker, debug: bool = False) -> float:
    reward = 0.0

    for name in self.enabled_components:
      component_reward = self.components[name].calculate_step_reward(env_tracker, metrics_tracker)
      if debug and abs(component_reward) > 0.1:
        print(f"    {name}: {component_reward:.2f}")
      reward += component_reward

    self.score += reward

    return reward

  def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
    reward = 0.0

    for name in self.enabled_components:
      component_reward = self.components[name].calculate_episode_reward(metrics_tracker)
      # Ensure we always get a number, never None
      if component_reward is not None:
        reward += component_reward

    self.score += reward

    return reward

  def current_score(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
    return self.score

  def reset(self) -> None:
    for name in self.enabled_components:
      self.components[name].reset()
    self.score = 0.0