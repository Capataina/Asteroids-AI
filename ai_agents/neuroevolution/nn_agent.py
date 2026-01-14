from typing import List, Any
from ai_agents.base_agent import BaseAgent
from ai_agents.policies.feedforward import FeedforwardPolicy
from interfaces.StateEncoder import StateEncoder
from interfaces.ActionInterface import ActionInterface

class NNAgent(BaseAgent):
    """
    Agent wrapping a FeedforwardPolicy.
    """
    def __init__(self, parameter_vector: List[float], state_encoder: StateEncoder, action_interface: ActionInterface, hidden_size: int = 24):
        self.state_encoder = state_encoder
        self.action_interface = action_interface
        input_size = state_encoder.get_state_size()
        output_size = 3
        self.policy = FeedforwardPolicy(parameter_vector, input_size, hidden_size, output_size)

    def get_action(self, state: List[float]) -> List[float]:
        return self.policy.forward(state)

    def reset(self) -> None:
        pass
    
    @staticmethod
    def get_parameter_count(input_size: int, hidden_size: int, output_size: int = 3) -> int:
        return FeedforwardPolicy.get_parameter_count(input_size, hidden_size, output_size)
