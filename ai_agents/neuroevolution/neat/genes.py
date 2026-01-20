from dataclasses import dataclass


@dataclass
class NodeGene:
    node_id: int
    node_type: str  # "input", "hidden", "output", "bias"


@dataclass
class ConnectionGene:
    innovation: int
    in_node: int
    out_node: int
    weight: float
    enabled: bool = True
