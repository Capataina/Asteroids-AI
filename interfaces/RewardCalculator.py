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
    self.component_scores = {}  # Tracks score per component
    self.score_history = []     # Tracks reward per step
  
  def add_component(self, component: RewardComponent):
    self.components[component.name] = component
    self.enabled_components.add(component.name)
    self.component_scores[component.name] = 0.0

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
      self.component_scores[name] += component_reward

    self.score += reward
    self.score_history.append(reward)

    return reward

  def calculate_episode_reward(self, metrics_tracker: MetricsTracker) -> float:
    reward = 0.0

    for name in self.enabled_components:
      component_reward = self.components[name].calculate_episode_reward(metrics_tracker)
      # Ensure we always get a number, never None
      if component_reward is not None:
        reward += component_reward
        self.component_scores[name] += component_reward

    self.score += reward
    # Episode rewards are technically "end of game" so append to last step or new step?
    # Appending as a final step makes sense for timeline
    self.score_history.append(reward)

    return reward
  
  def get_reward_breakdown(self) -> dict:
    """Returns a dictionary of rewards contributed by each component."""
    return self.component_scores.copy()
    
  def get_quarterly_scores(self) -> list:
    """Returns the total score accumulated in each quarter of the episode."""
    total_steps = len(self.score_history)
    if total_steps == 0:
        return [0.0, 0.0, 0.0, 0.0]
        
    quarter_len = total_steps / 4
    quarters = [0.0, 0.0, 0.0, 0.0]
    
    for i, reward in enumerate(self.score_history):
        q_idx = min(int(i / quarter_len), 3)
        quarters[q_idx] += reward
        
    return quarters

  def current_score(self, env_tracker: EnvironmentTracker, metrics_tracker: MetricsTracker) -> float:
    return self.score

  def reset(self) -> None:
    for name in self.enabled_components:
      self.components[name].reset()
    self.score = 0.0
    self.score_history = []
    # Also reset the component scores
    for name in self.component_scores:
        self.component_scores[name] = 0.0