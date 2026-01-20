import math
from typing import Dict, List, Tuple

from ai_agents.neuroevolution.neat.genes import ConnectionGene, NodeGene


class NEATNetwork:
    """
    Feedforward NEAT network compiled from a genome.
    """

    def __init__(
        self,
        nodes: Dict[int, NodeGene],
        connections: Dict[int, ConnectionGene],
        input_ids: List[int],
        output_ids: List[int],
        bias_id: int
    ):
        self.nodes = nodes
        self.input_ids = list(input_ids)
        self.output_ids = list(output_ids)
        self.bias_id = bias_id
        self.incoming, self.order = self._compile(connections)

    def _compile(self, connections: Dict[int, ConnectionGene]) -> Tuple[Dict[int, List[Tuple[int, float]]], List[int]]:
        enabled = [c for c in connections.values() if c.enabled]
        incoming: Dict[int, List[Tuple[int, float]]] = {node_id: [] for node_id in self.nodes.keys()}
        adjacency: Dict[int, List[int]] = {node_id: [] for node_id in self.nodes.keys()}
        in_degree: Dict[int, int] = {node_id: 0 for node_id in self.nodes.keys()}

        for conn in enabled:
            incoming.setdefault(conn.out_node, []).append((conn.in_node, conn.weight))
            adjacency.setdefault(conn.in_node, []).append(conn.out_node)
            in_degree[conn.out_node] = in_degree.get(conn.out_node, 0) + 1

        queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
        order: List[int] = []
        while queue:
            node_id = queue.pop(0)
            order.append(node_id)
            for neighbor in adjacency.get(node_id, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(self.nodes):
            raise ValueError("Cycle detected in feedforward NEAT network.")

        return incoming, order

    def activate(self, inputs: List[float]) -> List[float]:
        values: Dict[int, float] = {}
        for node_id, value in zip(self.input_ids, inputs):
            values[node_id] = value
        if self.bias_id is not None:
            values[self.bias_id] = 1.0

        for node_id in self.order:
            node_type = self.nodes[node_id].node_type
            if node_type in ("input", "bias"):
                continue
            total = 0.0
            for in_id, weight in self.incoming.get(node_id, []):
                total += values.get(in_id, 0.0) * weight
            if node_type == "output":
                values[node_id] = self._sigmoid(total)
            else:
                values[node_id] = math.tanh(total)

        return [values.get(node_id, 0.0) for node_id in self.output_ids]

    @staticmethod
    def _sigmoid(x: float) -> float:
        x = max(-500.0, min(500.0, x))
        return 1.0 / (1.0 + math.exp(-x))
