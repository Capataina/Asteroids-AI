from typing import TYPE_CHECKING, Dict, Any
if TYPE_CHECKING:
    from Asteroids import AsteroidsGame


class MetricsTracker:
  def __init__(self, game: 'AsteroidsGame'):
    self.game = game
    self.total_shots_fired = 0
    self.total_hits = 0
    self.total_kills = 0

  def update(self, game: 'AsteroidsGame') -> None:
    self.game = game

  def reset(self) -> None:
    self.total_shots_fired = 0
    self.total_hits = 0
    self.total_kills = 0
    
  def get_total_shots_fired(self) -> int:
    return self.total_shots_fired

  def get_total_hits(self) -> int:
    return self.total_hits

  def get_total_kills(self) -> int:
    return self.total_kills

  def get_accuracy(self) -> float:
    return self.total_hits / self.total_shots_fired if self.total_shots_fired > 0 else 0.0