from typing import Dict, Tuple

from ai_agents.neuroevolution.neat.genes import ConnectionGene


class InnovationTracker:
    """
    Tracks global innovation numbers for NEAT connections and node splits.
    """
    def __init__(self, start_innovation: int = 0, start_node_id: int = 0):
        self._next_innovation = start_innovation
        self._next_node_id = start_node_id
        self._connection_map: Dict[Tuple[int, int], int] = {}
        self._split_map: Dict[Tuple[int, int, int], Tuple[int, int, int]] = {}

    def get_connection_innovation(self, in_node: int, out_node: int) -> int:
        key = (in_node, out_node)
        if key in self._connection_map:
            return self._connection_map[key]
        innovation = self._next_innovation
        self._next_innovation += 1
        self._connection_map[key] = innovation
        return innovation

    def split_connection(self, connection: ConnectionGene) -> Tuple[int, int, int]:
        key = (connection.in_node, connection.out_node, connection.innovation)
        if key in self._split_map:
            return self._split_map[key]

        new_node_id = self._next_node_id
        self._next_node_id += 1
        innov1 = self.get_connection_innovation(connection.in_node, new_node_id)
        innov2 = self.get_connection_innovation(new_node_id, connection.out_node)
        self._split_map[key] = (new_node_id, innov1, innov2)
        return new_node_id, innov1, innov2

    @property
    def next_node_id(self) -> int:
        return self._next_node_id
