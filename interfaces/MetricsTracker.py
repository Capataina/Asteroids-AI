from typing import TYPE_CHECKING, Dict, Any
if TYPE_CHECKING:
    from Asteroids import AsteroidsGame

class MetricsTracker:
  def __init__(self, game: 'AsteroidsGame'):
    self.game = game
    self.total_shots_fired = 0
    self.total_hits = 0
    self.total_kills = 0
    self.time_alive = 0

  def update(self, game: 'AsteroidsGame') -> None:
    self.game = game

  def reset(self) -> None:
    self.total_shots_fired = 0
    self.total_hits = 0
    self.total_kills = 0
    self.time_alive = 0

  def get_total_shots_fired(self) -> int:
    return self.total_shots_fired

  def get_total_hits(self) -> int:
    return self.total_hits

  def get_total_kills(self) -> int:
    return self.total_kills

  def get_time_alive(self) -> float:
    return self.time_alive

  def get_accuracy(self) -> float:
    return self.total_hits / self.total_shots_fired if self.total_shots_fired > 0 else 0.0

  def kills_per_minute(self) -> float:
    return self.total_kills / self.time_alive * 60
  
  def get_episode_stats(self) -> Dict[str, Any]:
    return {
      "total_shots_fired": self.total_shots_fired,
      "total_hits": self.total_hits,
      "total_kills": self.total_kills,
      "time_alive": self.time_alive,
      "accuracy": self.get_accuracy(),
      "kills_per_minute": self.kills_per_minute()
    }