"""
Pareto objective definitions and extraction helpers.
"""

from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple
from training.config.pareto import ParetoConfig


@dataclass(frozen=True)
class ObjectiveSpec:
    name: str
    direction: str  # "max" or "min"
    extractor: Callable[[Dict, ParetoConfig], float]


def _extract_kills(metrics: Dict, _config: ParetoConfig) -> float:
    return float(metrics.get("kills", 0.0))


def _extract_hits(metrics: Dict, _config: ParetoConfig) -> float:
    return float(metrics.get("hits", 0.0))


def _extract_time_alive(metrics: Dict, config: ParetoConfig) -> float:
    if "time_alive" in metrics:
        return float(metrics.get("time_alive", 0.0))
    steps = float(metrics.get("steps_survived", 0.0))
    return steps * config.FRAME_DELAY


def _extract_accuracy(metrics: Dict, config: ParetoConfig) -> float:
    shots = float(metrics.get("shots_fired", 0.0))
    hits = float(metrics.get("hits", 0.0))
    if shots <= 0:
        return 0.0
    if config.ACCURACY_ZERO_BELOW_MIN_SHOTS and shots < config.ACCURACY_MIN_SHOTS:
        return 0.0
    return max(0.0, min(1.0, hits / shots))


def _extract_softmin_ttc(metrics: Dict, _config: ParetoConfig) -> float:
    return float(metrics.get("softmin_ttc", 0.0))


OBJECTIVE_REGISTRY = {
    "kills": ObjectiveSpec("kills", "max", _extract_kills),
    "hits": ObjectiveSpec("hits", "max", _extract_hits),
    "time_alive": ObjectiveSpec("time_alive", "max", _extract_time_alive),
    "accuracy": ObjectiveSpec("accuracy", "max", _extract_accuracy),
    "softmin_ttc": ObjectiveSpec("softmin_ttc", "max", _extract_softmin_ttc),
}


def get_objective_specs(config: ParetoConfig) -> List[ObjectiveSpec]:
    specs = []
    for name in config.OBJECTIVES:
        if name not in OBJECTIVE_REGISTRY:
            raise ValueError(f"Unknown Pareto objective: {name}")
        specs.append(OBJECTIVE_REGISTRY[name])
    return specs


def compute_objective_matrix(
    per_agent_metrics: List[Dict],
    config: ParetoConfig
) -> Tuple[List[List[float]], List[str], List[str]]:
    """
    Compute objective vectors for a population.

    Returns:
        (objective_vectors, directions, names)
    """
    specs = get_objective_specs(config)
    vectors: List[List[float]] = []
    for metrics in per_agent_metrics:
        vector = [spec.extractor(metrics, config) for spec in specs]
        vectors.append(vector)
    directions = [spec.direction for spec in specs]
    names = [spec.name for spec in specs]
    return vectors, directions, names
