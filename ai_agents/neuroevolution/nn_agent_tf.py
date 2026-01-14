"""
TensorFlow-based Neural Network Agent.

This module provides a TensorFlow implementation of the neural network agent,
matching the interface of the NumPy-based NNAgent for compatibility with
existing training infrastructure.
"""

from typing import List
from ai_agents.base_agent import BaseAgent
from ai_agents.policies.feedforward_tf import FeedforwardPolicyTF
from interfaces.StateEncoder import StateEncoder
from interfaces.ActionInterface import ActionInterface


class NNAgentTF(BaseAgent):
    """
    Agent wrapping a TensorFlow FeedforwardPolicyTF.

    Interface-compatible with NNAgent for drop-in replacement.
    """

    def __init__(
        self,
        parameter_vector: List[float],
        state_encoder: StateEncoder,
        action_interface: ActionInterface,
        hidden_size: int = 24
    ):
        """
        Initialize the TensorFlow agent.

        Args:
            parameter_vector: Flat list of network weights.
            state_encoder: Encoder for converting game state to input vector.
            action_interface: Interface for converting outputs to game actions.
            hidden_size: Number of hidden units in the network.
        """
        self.state_encoder = state_encoder
        self.action_interface = action_interface
        input_size = state_encoder.get_state_size()
        output_size = 3  # signed turn, thrust, shoot
        self.policy = FeedforwardPolicyTF(parameter_vector, input_size, hidden_size, output_size)

    def get_action(self, state: List[float]) -> List[float]:
        """
        Get action from the policy given a state.

        Args:
            state: Encoded state vector.

        Returns:
            Action vector with values in [0, 1].
        """
        return self.policy.forward(state)

    def reset(self) -> None:
        """Reset agent state (no-op for feedforward policies)."""
        pass

    def get_weights(self) -> List[float]:
        """
        Get the current network weights as a flat vector.

        Returns:
            Flat list of all network parameters.
        """
        return self.policy.get_weights()

    @staticmethod
    def get_parameter_count(input_size: int, hidden_size: int, output_size: int = 3) -> int:
        """
        Calculate total number of parameters for the network.

        Args:
            input_size: Number of input features.
            hidden_size: Number of hidden units.
            output_size: Number of output units.

        Returns:
            Total parameter count.
        """
        return FeedforwardPolicyTF.get_parameter_count(input_size, hidden_size, output_size)
