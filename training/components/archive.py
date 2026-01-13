"""
Behavior Archive

Maintains a historical archive of novel behaviors encountered during training.
This archive is used to compute novelty scores - behaviors are compared against
both the current population and this historical record.
"""

import random
from typing import List, Optional
from training.components.novelty import compute_behavior_novelty


class BehaviorArchive:
    """
    Archive of historically novel behaviors.

    Behaviors are added when they exceed a novelty threshold.
    Archive size is capped with random replacement when full.
    """

    def __init__(
        self,
        max_size: int = 500,
        novelty_threshold: float = 0.3,
        k_nearest: int = 15
    ):
        """
        Initialize the behavior archive.

        Args:
            max_size: Maximum number of behaviors to store
            novelty_threshold: Minimum novelty score to be added to archive
            k_nearest: Number of neighbors for novelty calculation
        """
        self.max_size = max_size
        self.novelty_threshold = novelty_threshold
        self.k_nearest = k_nearest
        self.behaviors: List[List[float]] = []

    def maybe_add(
        self,
        behavior: List[float],
        population_behaviors: List[List[float]]
    ) -> bool:
        """
        Add behavior to archive if it's novel enough.

        Args:
            behavior: The behavior vector to potentially add
            population_behaviors: Current population behaviors (for novelty calc)

        Returns:
            True if behavior was added, False otherwise
        """
        # Calculate novelty against current population and archive
        novelty = compute_behavior_novelty(
            behavior,
            population_behaviors,
            self.behaviors,
            self.k_nearest
        )

        if novelty >= self.novelty_threshold:
            self._add(behavior)
            return True

        return False

    def _add(self, behavior: List[float]) -> None:
        """Add a behavior to the archive, evicting if necessary."""
        if len(self.behaviors) >= self.max_size:
            # Random replacement
            idx = random.randint(0, len(self.behaviors) - 1)
            self.behaviors[idx] = behavior
        else:
            self.behaviors.append(behavior)

    def add_batch(
        self,
        behaviors: List[List[float]],
        novelty_scores: List[float]
    ) -> int:
        """
        Add multiple behaviors based on pre-computed novelty scores.

        Args:
            behaviors: List of behavior vectors
            novelty_scores: Corresponding novelty scores

        Returns:
            Number of behaviors added
        """
        added = 0
        for behavior, novelty in zip(behaviors, novelty_scores):
            if novelty >= self.novelty_threshold:
                self._add(behavior)
                added += 1
        return added

    def get_behaviors(self) -> List[List[float]]:
        """Get all behaviors in the archive."""
        return self.behaviors.copy()

    def size(self) -> int:
        """Get current archive size."""
        return len(self.behaviors)

    def clear(self) -> None:
        """Clear the archive."""
        self.behaviors = []

    def set_threshold(self, threshold: float) -> None:
        """Update the novelty threshold."""
        self.novelty_threshold = threshold

    def get_stats(self) -> dict:
        """Get archive statistics."""
        return {
            'size': len(self.behaviors),
            'max_size': self.max_size,
            'fill_ratio': len(self.behaviors) / self.max_size if self.max_size > 0 else 0,
            'novelty_threshold': self.novelty_threshold,
        }
