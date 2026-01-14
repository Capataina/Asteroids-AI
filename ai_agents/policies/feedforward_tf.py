"""
TensorFlow-based Feedforward Neural Network Policy.

This module provides a TensorFlow implementation of the feedforward policy,
matching the interface of the NumPy version for compatibility with existing
training infrastructure.
"""

import tensorflow as tf
from typing import List, Optional
import numpy as np


class FeedforwardPolicyTF:
    """
    TensorFlow feedforward neural network policy.
    Architecture: Input -> Hidden (tanh) -> Output (sigmoid)

    Maintains interface compatibility with the NumPy FeedforwardPolicy.
    """

    def __init__(
        self,
        weights: Optional[List[float]],
        input_size: int,
        hidden_size: int,
        output_size: int
    ):
        """
        Initialize the TensorFlow policy.

        Args:
            weights: Flat parameter vector to load, or None to initialize randomly.
            input_size: Number of input features.
            hidden_size: Number of hidden units.
            output_size: Number of output units.
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Build the model
        self.model = self._build_model()

        # Load weights if provided
        if weights is not None:
            self.set_weights(weights)

    def _build_model(self) -> tf.keras.Model:
        """Build the Keras sequential model."""
        model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=(self.input_size,)),
            tf.keras.layers.Dense(
                self.hidden_size,
                activation='tanh',
                kernel_initializer='glorot_uniform',
                bias_initializer='zeros',
                name='hidden'
            ),
            tf.keras.layers.Dense(
                self.output_size,
                activation='sigmoid',
                kernel_initializer='glorot_uniform',
                bias_initializer='zeros',
                name='output'
            )
        ])
        return model

    def set_weights(self, weights: List[float]) -> None:
        """
        Load weights from a flat parameter vector.

        The vector layout matches the NumPy version:
        - W1: input_size * hidden_size (row-major)
        - b1: hidden_size
        - W2: hidden_size * output_size (row-major)
        - b2: output_size

        Args:
            weights: Flat list of floats containing all network parameters.
        """
        weights_array = np.array(weights, dtype=np.float32)
        idx = 0

        # W1: input_size x hidden_size
        w1_size = self.input_size * self.hidden_size
        W1 = weights_array[idx:idx + w1_size].reshape(self.input_size, self.hidden_size)
        idx += w1_size

        # b1: hidden_size
        b1 = weights_array[idx:idx + self.hidden_size]
        idx += self.hidden_size

        # W2: hidden_size x output_size
        w2_size = self.hidden_size * self.output_size
        W2 = weights_array[idx:idx + w2_size].reshape(self.hidden_size, self.output_size)
        idx += w2_size

        # b2: output_size
        b2 = weights_array[idx:idx + self.output_size]

        # Set weights in the model
        # Keras Dense layers expect [kernel, bias] format
        self.model.layers[0].set_weights([W1, b1])
        self.model.layers[1].set_weights([W2, b2])

    def get_weights(self) -> List[float]:
        """
        Extract weights as a flat parameter vector.

        Returns:
            Flat list of floats containing all network parameters.
        """
        weights = []

        # Get weights from each layer
        W1, b1 = self.model.layers[0].get_weights()
        W2, b2 = self.model.layers[1].get_weights()

        # Flatten in the same order as set_weights expects
        weights.extend(W1.flatten().tolist())
        weights.extend(b1.flatten().tolist())
        weights.extend(W2.flatten().tolist())
        weights.extend(b2.flatten().tolist())

        return weights

    def forward(self, state: List[float]) -> List[float]:
        """
        Forward pass through the network.

        Args:
            state: Input state vector.

        Returns:
            Output action vector (values in [0, 1] due to sigmoid).
        """
        # Convert to tensor and add batch dimension
        state_tensor = tf.constant([state], dtype=tf.float32)

        # Forward pass
        output = self.model(state_tensor, training=False)

        # Convert back to list (remove batch dimension)
        return output.numpy()[0].tolist()

    def forward_batch(self, states: List[List[float]]) -> List[List[float]]:
        """
        Batched forward pass for efficiency.

        Args:
            states: List of input state vectors.

        Returns:
            List of output action vectors.
        """
        states_tensor = tf.constant(states, dtype=tf.float32)
        outputs = self.model(states_tensor, training=False)
        return outputs.numpy().tolist()

    @staticmethod
    def get_parameter_count(input_size: int, hidden_size: int, output_size: int) -> int:
        """
        Calculate total number of parameters.

        Args:
            input_size: Number of input features.
            hidden_size: Number of hidden units.
            output_size: Number of output units.

        Returns:
            Total parameter count.
        """
        w1 = input_size * hidden_size
        b1 = hidden_size
        w2 = hidden_size * output_size
        b2 = output_size
        return w1 + b1 + w2 + b2
