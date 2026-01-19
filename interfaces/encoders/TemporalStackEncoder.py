from typing import List

from interfaces.StateEncoder import StateEncoder
from interfaces.EnvironmentTracker import EnvironmentTracker


class TemporalStackEncoder(StateEncoder):
    """
    Wraps a base encoder and concatenates recent states plus deltas.

    Output layout:
      [s(t), s(t-1), ..., s(t-N+1), delta(t), delta(t-1), ..., delta(t-N+2)]
    where delta(k) = s(k) - s(k-1).
    """

    def __init__(self, base_encoder: StateEncoder, stack_size: int = 4, include_deltas: bool = True):
        if stack_size < 1:
            raise ValueError("stack_size must be >= 1")
        self.base_encoder = base_encoder
        self.stack_size = stack_size
        self.include_deltas = include_deltas
        self._history: List[List[float]] = []

    def encode(self, environment_tracker: EnvironmentTracker) -> List[float]:
        state = list(self.base_encoder.encode(environment_tracker))

        if not self._history:
            self._history = [state[:] for _ in range(self.stack_size)]
        else:
            self._history.append(state[:])
            if len(self._history) > self.stack_size:
                self._history = self._history[-self.stack_size:]

        stacked: List[float] = []
        for frame in self._history:
            stacked.extend(frame)

        if self.include_deltas:
            for idx in range(1, len(self._history)):
                prev = self._history[idx - 1]
                curr = self._history[idx]
                stacked.extend([curr[i] - prev[i] for i in range(len(curr))])

        return stacked

    def get_state_size(self) -> int:
        base_size = self.base_encoder.get_state_size()
        stack_count = self.stack_size
        delta_count = (self.stack_size - 1) if self.include_deltas else 0
        return base_size * (stack_count + delta_count)

    def reset(self) -> None:
        self._history = []
        self.base_encoder.reset()

    def clone(self) -> "TemporalStackEncoder":
        return TemporalStackEncoder(
            base_encoder=self.base_encoder.clone(),
            stack_size=self.stack_size,
            include_deltas=self.include_deltas
        )
