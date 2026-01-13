from typing import List

class LinearPolicy:
    """
    Simple linear policy.
    action[i] = sum(weights[i*state_size + j] * state[j])
    """
    def __init__(self, weights: List[float], input_size: int, output_size: int):
        self.weights = weights
        self.input_size = input_size
        self.output_size = output_size
    
    def forward(self, state: List[float]) -> List[float]:
        actions = []
        for i in range(self.output_size):
            start_idx = i * self.input_size
            # Dot product
            action_value = sum(self.weights[start_idx + j] * state[j] for j in range(self.input_size))
            actions.append(action_value)
        return actions
