"""
Data storage models for training analytics.

Contains the AnalyticsData class that holds all training metrics and state.
"""

from datetime import datetime
from typing import List, Dict, Any


class AnalyticsData:
    """Stores all training analytics data and tracking state."""

    SCHEMA_VERSION = "2.0"

    def __init__(self):
        # Core data storage
        self.generations_data: List[Dict[str, Any]] = []
        self.fresh_game_data: Dict[int, Dict[str, Any]] = {}
        self.distributions_data: Dict[int, Dict[str, Any]] = {}

        # Configuration
        self.config: Dict[str, Any] = {}
        self.start_time: datetime = datetime.now()

        # Tracking state for stagnation detection
        self.all_time_best_fitness: float = float('-inf')
        self.all_time_best_generation: int = 0
        self.generations_since_improvement: int = 0

    def set_config(self, config: Dict[str, Any]):
        """Store training configuration."""
        self.config = config

    def update_best_tracking(self, generation: int, best_fitness: float):
        """Update all-time best tracking and stagnation counter.

        Args:
            generation: Current generation number
            best_fitness: Best fitness from current generation
        """
        if best_fitness > self.all_time_best_fitness:
            self.all_time_best_fitness = best_fitness
            self.all_time_best_generation = generation
            self.generations_since_improvement = 0
        else:
            self.generations_since_improvement += 1
