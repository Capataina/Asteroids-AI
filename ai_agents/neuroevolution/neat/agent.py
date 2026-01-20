from typing import List, Any

from ai_agents.base_agent import BaseAgent
from ai_agents.neuroevolution.neat.genome import Genome


class NEATAgent(BaseAgent):
    """
    Agent wrapper for a NEAT genome.
    """
    def __init__(self, genome: Genome):
        self.genome = genome
        self.network = genome.build_network()

    def get_action(self, state: Any) -> List[float]:
        return self.network.activate(state)

    def reset(self) -> None:
        pass
