import random
from typing import Dict, List, Optional, Tuple

from ai_agents.neuroevolution.neat.genes import ConnectionGene, NodeGene
from ai_agents.neuroevolution.neat.network import NEATNetwork


class Genome:
    def __init__(
        self,
        nodes: Dict[int, NodeGene],
        connections: Dict[int, ConnectionGene],
        input_ids: List[int],
        output_ids: List[int],
        bias_id: int
    ):
        self.nodes = nodes
        self.connections = connections
        self.input_ids = list(input_ids)
        self.output_ids = list(output_ids)
        self.bias_id = bias_id

    @staticmethod
    def create_minimal(
        input_ids: List[int],
        output_ids: List[int],
        bias_id: int,
        innovation_tracker,
        weight_range: Tuple[float, float] = (-1.0, 1.0)
    ) -> "Genome":
        nodes: Dict[int, NodeGene] = {}
        for node_id in input_ids:
            nodes[node_id] = NodeGene(node_id=node_id, node_type="input")
        nodes[bias_id] = NodeGene(node_id=bias_id, node_type="bias")
        for node_id in output_ids:
            nodes[node_id] = NodeGene(node_id=node_id, node_type="output")

        connections: Dict[int, ConnectionGene] = {}
        sources = list(input_ids) + [bias_id]
        for src in sources:
            for dst in output_ids:
                innovation = innovation_tracker.get_connection_innovation(src, dst)
                weight = random.uniform(weight_range[0], weight_range[1])
                connections[innovation] = ConnectionGene(
                    innovation=innovation,
                    in_node=src,
                    out_node=dst,
                    weight=weight,
                    enabled=True
                )

        return Genome(nodes, connections, input_ids, output_ids, bias_id)

    def copy(self) -> "Genome":
        nodes = {nid: NodeGene(node_id=gene.node_id, node_type=gene.node_type) for nid, gene in self.nodes.items()}
        connections = {
            innov: ConnectionGene(
                innovation=gene.innovation,
                in_node=gene.in_node,
                out_node=gene.out_node,
                weight=gene.weight,
                enabled=gene.enabled
            )
            for innov, gene in self.connections.items()
        }
        return Genome(nodes, connections, self.input_ids, self.output_ids, self.bias_id)

    def build_network(self) -> NEATNetwork:
        return NEATNetwork(self.nodes, self.connections, self.input_ids, self.output_ids, self.bias_id)

    def to_dict(self) -> Dict:
        return {
            "input_ids": list(self.input_ids),
            "output_ids": list(self.output_ids),
            "bias_id": self.bias_id,
            "nodes": [
                {"node_id": gene.node_id, "node_type": gene.node_type}
                for gene in self.nodes.values()
            ],
            "connections": [
                {
                    "innovation": gene.innovation,
                    "in_node": gene.in_node,
                    "out_node": gene.out_node,
                    "weight": gene.weight,
                    "enabled": gene.enabled
                }
                for gene in self.connections.values()
            ]
        }

    @staticmethod
    def from_dict(data: Dict) -> "Genome":
        nodes = {
            node["node_id"]: NodeGene(node_id=node["node_id"], node_type=node["node_type"])
            for node in data["nodes"]
        }
        connections = {
            conn["innovation"]: ConnectionGene(
                innovation=conn["innovation"],
                in_node=conn["in_node"],
                out_node=conn["out_node"],
                weight=conn["weight"],
                enabled=conn["enabled"]
            )
            for conn in data["connections"]
        }
        return Genome(nodes, connections, data["input_ids"], data["output_ids"], data["bias_id"])

    def num_nodes(self) -> int:
        return len(self.nodes)

    def num_connections(self) -> int:
        return len(self.connections)

    def num_enabled_connections(self) -> int:
        return sum(1 for gene in self.connections.values() if gene.enabled)

    def mutate_weights(self, mutation_prob: float, sigma: float) -> int:
        mutated = 0
        for gene in self.connections.values():
            if random.random() < mutation_prob:
                gene.weight += random.gauss(0.0, sigma)
                mutated += 1
        return mutated

    def mutate_add_connection(
        self,
        innovation_tracker,
        max_attempts: int = 30,
        weight_range: Tuple[float, float] = (-1.0, 1.0)
    ) -> Optional[int]:
        sources = [
            node_id
            for node_id, node in self.nodes.items()
            if node.node_type in ("input", "bias", "hidden")
        ]
        targets = [
            node_id
            for node_id, node in self.nodes.items()
            if node.node_type in ("hidden", "output")
        ]
        existing = {(gene.in_node, gene.out_node) for gene in self.connections.values()}

        for _ in range(max_attempts):
            in_node = random.choice(sources)
            out_node = random.choice(targets)
            if in_node == out_node:
                continue
            if (in_node, out_node) in existing:
                continue
            if self._creates_cycle(in_node, out_node):
                continue
            innovation = innovation_tracker.get_connection_innovation(in_node, out_node)
            weight = random.uniform(weight_range[0], weight_range[1])
            self.connections[innovation] = ConnectionGene(
                innovation=innovation,
                in_node=in_node,
                out_node=out_node,
                weight=weight,
                enabled=True
            )
            return innovation

        return None

    def mutate_add_node(self, innovation_tracker) -> Optional[Tuple[int, int, int]]:
        enabled_connections = [gene for gene in self.connections.values() if gene.enabled]
        if not enabled_connections:
            return None

        connection = random.choice(enabled_connections)
        connection.enabled = False

        new_node_id, innov1, innov2 = innovation_tracker.split_connection(connection)
        self.nodes[new_node_id] = NodeGene(node_id=new_node_id, node_type="hidden")

        self.connections[innov1] = ConnectionGene(
            innovation=innov1,
            in_node=connection.in_node,
            out_node=new_node_id,
            weight=1.0,
            enabled=True
        )
        self.connections[innov2] = ConnectionGene(
            innovation=innov2,
            in_node=new_node_id,
            out_node=connection.out_node,
            weight=connection.weight,
            enabled=True
        )
        return new_node_id, innov1, innov2

    def _creates_cycle(self, in_node: int, out_node: int) -> bool:
        """Check if adding a connection from in_node to out_node would create a cycle."""
        return Genome._would_create_cycle(self.connections, in_node, out_node)

    @staticmethod
    def _would_create_cycle(
        connections: Dict[int, "ConnectionGene"],
        in_node: int,
        out_node: int
    ) -> bool:
        """
        Check if adding a connection from in_node to out_node would create a cycle.

        This is a static method so it can be used during crossover before the
        genome is fully constructed.

        Args:
            connections: Existing connections dict
            in_node: Source node of the proposed connection
            out_node: Target node of the proposed connection

        Returns:
            True if adding this connection would create a cycle
        """
        # Build adjacency list from existing enabled connections
        adjacency: Dict[int, List[int]] = {}
        for gene in connections.values():
            if not gene.enabled:
                continue
            adjacency.setdefault(gene.in_node, []).append(gene.out_node)

        # Check if there's a path from out_node back to in_node
        # If so, adding in_node -> out_node would create a cycle
        stack = [out_node]
        visited = set()
        while stack:
            node = stack.pop()
            if node == in_node:
                return True
            if node in visited:
                continue
            visited.add(node)
            for nxt in adjacency.get(node, []):
                if nxt not in visited:
                    stack.append(nxt)
        return False

    @staticmethod
    def compatibility_distance(
        genome_a: "Genome",
        genome_b: "Genome",
        c1: float,
        c2: float,
        c3: float
    ) -> float:
        genes_a = genome_a.connections
        genes_b = genome_b.connections
        if not genes_a and not genes_b:
            return 0.0

        innovations_a = sorted(genes_a.keys())
        innovations_b = sorted(genes_b.keys())
        set_b = set(innovations_b)

        max_a = innovations_a[-1] if innovations_a else 0
        max_b = innovations_b[-1] if innovations_b else 0

        excess = 0
        disjoint = 0
        weight_diffs = []

        for innov in innovations_a:
            if innov in genes_b:
                weight_diffs.append(abs(genes_a[innov].weight - genes_b[innov].weight))
            else:
                if innov > max_b:
                    excess += 1
                else:
                    disjoint += 1

        for innov in innovations_b:
            if innov not in genes_a:
                if innov > max_a:
                    excess += 1
                else:
                    disjoint += 1

        n = max(len(genes_a), len(genes_b))
        if n < 20:
            n = 1

        w = sum(weight_diffs) / len(weight_diffs) if weight_diffs else 0.0
        return (c1 * excess + c2 * disjoint) / n + c3 * w

    @staticmethod
    def crossover(
        parent_a: "Genome",
        parent_b: "Genome",
        fitness_a: float,
        fitness_b: float,
        inherit_disabled_prob: float
    ) -> "Genome":
        if fitness_b > fitness_a:
            parent_a, parent_b = parent_b, parent_a
            fitness_a, fitness_b = fitness_b, fitness_a

        equal_fitness = abs(fitness_a - fitness_b) < 1e-9

        nodes: Dict[int, NodeGene] = {}
        for node_id, gene in parent_a.nodes.items():
            nodes[node_id] = NodeGene(node_id=gene.node_id, node_type=gene.node_type)
        if equal_fitness:
            for node_id, gene in parent_b.nodes.items():
                if node_id not in nodes:
                    nodes[node_id] = NodeGene(node_id=gene.node_id, node_type=gene.node_type)

        connections: Dict[int, ConnectionGene] = {}
        innovations = set(parent_a.connections.keys()) | set(parent_b.connections.keys())
        for innov in innovations:
            gene_a = parent_a.connections.get(innov)
            gene_b = parent_b.connections.get(innov)

            # Determine which gene to potentially add
            candidate = None
            enabled = True

            if gene_a and gene_b:
                chosen = gene_a if random.random() < 0.5 else gene_b
                if not gene_a.enabled or not gene_b.enabled:
                    if random.random() < inherit_disabled_prob:
                        enabled = False
                candidate = ConnectionGene(
                    innovation=innov,
                    in_node=chosen.in_node,
                    out_node=chosen.out_node,
                    weight=chosen.weight,
                    enabled=enabled
                )
            elif gene_a:
                candidate = ConnectionGene(
                    innovation=gene_a.innovation,
                    in_node=gene_a.in_node,
                    out_node=gene_a.out_node,
                    weight=gene_a.weight,
                    enabled=gene_a.enabled
                )
            elif gene_b and equal_fitness:
                candidate = ConnectionGene(
                    innovation=gene_b.innovation,
                    in_node=gene_b.in_node,
                    out_node=gene_b.out_node,
                    weight=gene_b.weight,
                    enabled=gene_b.enabled
                )

            # Only add the connection if it wouldn't create a cycle
            # (only check enabled connections since disabled ones don't affect network topology)
            if candidate is not None:
                if not candidate.enabled:
                    # Disabled connections can't create cycles in the active network
                    connections[innov] = candidate
                elif not Genome._would_create_cycle(connections, candidate.in_node, candidate.out_node):
                    connections[innov] = candidate
                # else: skip this connection to prevent cycle

        child = Genome(nodes, connections, parent_a.input_ids, parent_a.output_ids, parent_a.bias_id)
        return child
