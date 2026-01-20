from typing import List

from ai_agents.neuroevolution.neat.genome import Genome


class Species:
    def __init__(self, species_id: int, representative: Genome):
        self.species_id = species_id
        self.representative = representative
        self.members: List[Genome] = []
        self.best_fitness = float("-inf")
        self.stagnation = 0

    def reset(self, representative: Genome):
        self.representative = representative
        self.members = []

    def add(self, genome: Genome):
        self.members.append(genome)
