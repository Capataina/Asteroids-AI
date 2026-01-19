"""
Pareto (Multi-Objective) Configuration.

Defines the objective set and evaluation behavior for multi-objective
selection/update logic shared across training methods.
"""


class ParetoConfig:
    """Configuration for Pareto objective evaluation and ranking."""

    # Enable/disable Pareto objectives.
    ENABLED = True

    # Objective list (order matters for reporting only).
    OBJECTIVES = ["hits", "time_alive", "softmin_ttc"]

    # Accuracy handling: avoid treating 1 lucky shot as perfect accuracy.
    ACCURACY_MIN_SHOTS = 5
    ACCURACY_ZERO_BELOW_MIN_SHOTS = True

    # Frame delay for converting steps -> time (fallback if time_alive missing).
    FRAME_DELAY = 1.0 / 60.0

    # Soft-min TTC risk proxy (seconds).
    RISK_TTC_MAX = 5.0
    RISK_TAU = 1.0

    # If True, use fitness as a tie-breaker when Pareto rank and crowding are equal.
    FITNESS_TIEBREAKER = True

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Unknown ParetoConfig parameter: {key}")

    def to_dict(self) -> dict:
        return {
            "pareto_enabled": self.ENABLED,
            "pareto_objectives": list(self.OBJECTIVES),
            "pareto_accuracy_min_shots": self.ACCURACY_MIN_SHOTS,
            "pareto_accuracy_zero_below_min_shots": self.ACCURACY_ZERO_BELOW_MIN_SHOTS,
            "pareto_frame_delay": self.FRAME_DELAY,
            "pareto_risk_ttc_max": self.RISK_TTC_MAX,
            "pareto_risk_tau": self.RISK_TAU,
            "pareto_fitness_tiebreaker": self.FITNESS_TIEBREAKER,
        }
