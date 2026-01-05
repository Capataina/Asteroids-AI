"""
Neural Network GA Agent

A feedforward neural network policy for the genetic algorithm.
Unlike the linear GAAgent, this can learn non-linear decision boundaries,
enabling behaviors like "IF close AND approaching THEN dodge".

Architecture: Input -> Hidden (tanh) -> Output (sigmoid)
"""

import math
from typing import List
from interfaces.StateEncoder import StateEncoder
from interfaces.ActionInterface import ActionInterface
from training.base.BaseAgent import BaseAgent


class NeuralNetworkGAAgent(BaseAgent):
    """
    GA agent with a feedforward neural network policy.

    The parameter vector is interpreted as neural network weights:
    - W1: input_size x hidden_size weights
    - b1: hidden_size biases
    - W2: hidden_size x output_size weights
    - b2: output_size biases
    """

    def __init__(
        self,
        parameter_vector: List[float],
        state_encoder: StateEncoder,
        action_interface: ActionInterface,
        hidden_size: int = 24
    ):
        """
        Initialize neural network GA agent.

        Args:
            parameter_vector: Flat list of all network weights and biases
            state_encoder: VectorEncoder instance for state representation
            action_interface: ActionInterface instance for action conversion
            hidden_size: Number of neurons in hidden layer (default: 24)
        """
        self.parameter_vector = [float(x) for x in parameter_vector]
        self.state_encoder = state_encoder
        self.action_interface = action_interface
        self.hidden_size = hidden_size

        # Network dimensions
        self.input_size = state_encoder.get_state_size()
        self.output_size = 4  # left, right, thrust, shoot

        # Unpack parameter vector into weight matrices and biases
        self._unpack_parameters()

    def _unpack_parameters(self):
        """Unpack flat parameter vector into weight matrices and biases."""
        idx = 0

        # W1: input_size x hidden_size
        w1_size = self.input_size * self.hidden_size
        self.W1 = []
        for i in range(self.input_size):
            row = self.parameter_vector[idx:idx + self.hidden_size]
            self.W1.append(row)
            idx += self.hidden_size

        # b1: hidden_size
        self.b1 = self.parameter_vector[idx:idx + self.hidden_size]
        idx += self.hidden_size

        # W2: hidden_size x output_size
        self.W2 = []
        for i in range(self.hidden_size):
            row = self.parameter_vector[idx:idx + self.output_size]
            self.W2.append(row)
            idx += self.output_size

        # b2: output_size
        self.b2 = self.parameter_vector[idx:idx + self.output_size]

    @staticmethod
    def get_parameter_count(input_size: int, hidden_size: int, output_size: int = 4) -> int:
        """
        Calculate total number of parameters needed for the network.

        Args:
            input_size: Size of input (state) vector
            hidden_size: Number of hidden neurons
            output_size: Size of output (action) vector

        Returns:
            Total parameter count
        """
        w1 = input_size * hidden_size
        b1 = hidden_size
        w2 = hidden_size * output_size
        b2 = output_size
        return w1 + b1 + w2 + b2

    def get_action(self, state: List[float]) -> List[float]:
        """
        Get action from state using neural network forward pass.

        Args:
            state: Encoded state vector from VectorEncoder

        Returns:
            Action vector [left, right, thrust, shoot] with values in [0.0, 1.0]
        """
        return self._forward(state)

    def _forward(self, state: List[float]) -> List[float]:
        """
        Neural network forward pass.

        Input -> Linear -> tanh -> Linear -> sigmoid -> Output

        Args:
            state: Input state vector

        Returns:
            Output action vector
        """
        # Layer 1: Linear + tanh
        hidden = []
        for j in range(self.hidden_size):
            # Dot product: sum(W1[i][j] * state[i]) + b1[j]
            activation = self.b1[j]
            for i in range(self.input_size):
                activation += self.W1[i][j] * state[i]
            # tanh activation
            hidden.append(math.tanh(activation))

        # Layer 2: Linear + sigmoid
        output = []
        for k in range(self.output_size):
            # Dot product: sum(W2[j][k] * hidden[j]) + b2[k]
            activation = self.b2[k]
            for j in range(self.hidden_size):
                activation += self.W2[j][k] * hidden[j]
            # sigmoid activation
            output.append(self._sigmoid(activation))

        return output

    @staticmethod
    def _sigmoid(x: float) -> float:
        """Sigmoid activation function."""
        # Clip to avoid overflow
        x = max(-500, min(500, x))
        return 1.0 / (1.0 + math.exp(-x))

    def reset(self) -> None:
        """Reset agent state for new episode."""
        # No internal state to reset for feedforward network
        pass
