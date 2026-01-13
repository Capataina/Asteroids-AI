import math
from typing import List

class FeedforwardPolicy:
    """
    Feedforward neural network policy.
    Architecture: Input -> Hidden (tanh) -> Output (sigmoid)
    """
    def __init__(self, weights: List[float], input_size: int, hidden_size: int, output_size: int):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self._unpack(weights)

    def _unpack(self, weights: List[float]):
        idx = 0
        # W1: input_size x hidden_size
        self.W1 = []
        for i in range(self.input_size):
            row = weights[idx:idx + self.hidden_size]
            self.W1.append(row)
            idx += self.hidden_size

        # b1: hidden_size
        self.b1 = weights[idx:idx + self.hidden_size]
        idx += self.hidden_size

        # W2: hidden_size x output_size
        self.W2 = []
        for i in range(self.hidden_size):
            row = weights[idx:idx + self.output_size]
            self.W2.append(row)
            idx += self.output_size

        # b2: output_size
        self.b2 = weights[idx:idx + self.output_size]

    def forward(self, state: List[float]) -> List[float]:
        # Layer 1: Linear + tanh
        hidden = []
        for j in range(self.hidden_size):
            activation = self.b1[j]
            for i in range(self.input_size):
                activation += self.W1[i][j] * state[i]
            hidden.append(math.tanh(activation))

        # Layer 2: Linear + sigmoid
        output = []
        for k in range(self.output_size):
            activation = self.b2[k]
            for j in range(self.hidden_size):
                activation += self.W2[j][k] * hidden[j]
            output.append(self._sigmoid(activation))
        
        return output

    @staticmethod
    def _sigmoid(x: float) -> float:
        x = max(-500, min(500, x))
        return 1.0 / (1.0 + math.exp(-x))

    @staticmethod
    def get_parameter_count(input_size: int, hidden_size: int, output_size: int) -> int:
        w1 = input_size * hidden_size
        b1 = hidden_size
        w2 = hidden_size * output_size
        b2 = output_size
        return w1 + b1 + w2 + b2
