from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class EpisodeResult:
    """
    Data structure containing results from a single episode.
    """
    total_reward: float
    """Total reward accumulated during episode (step + episode rewards)."""
    steps: int
    """Number of steps taken in episode."""
    metrics: Dict[str, Any]
    """Episode metrics from MetricsTracker (accuracy, kills, time_alive, etc.)."""
    done_reason: str
    """Reason episode ended: 'collision', 'timeout', or 'manual'."""

    def __str__(self) -> str:
        return f"EpisodeResult(total_reward={self.total_reward}, steps={self.steps}, metrics={self.metrics}, done_reason={self.done_reason})"
