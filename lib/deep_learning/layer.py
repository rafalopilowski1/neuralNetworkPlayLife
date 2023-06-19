from lib.deep_learning import perceptron as perc_lib
from lib.deep_learning.perceptron import Perceptron


def signal_error(outputs, expected) -> list[float]:
    """
    Calculates the error between the outputs and the expected values
    :param outputs: Outputs from the neural network
    :param expected: Expected values
    :return: List of errors
    """
    return [perc_lib.signal_error(output, expect) for output, expect in zip(outputs, expected)]


class Layer:
    """
    Class representing a layer of the neural network.
    """

    def __init__(self, num_inputs, num_neurons):
        """
        Constructor
        :param num_inputs: Number of inputs to the layer
        :param num_neurons: Number of neurons in the layer
        """
        self.perceptrons = [Perceptron(num_inputs) for _ in range(num_neurons)]

    def forward_propagate(self, inputs):
        """
        Forward propagates the inputs through the layer
        :param inputs: Inputs to the layer
        :return: List of outputs from the layer
        """
        return [perceptron.activate(inputs) for perceptron in self.perceptrons]

    def update(self, deltas, learning_rate, outputs):
        """
        Updates the weights of the layer
        :param deltas: Deltas from the previous layer
        :param learning_rate: Learning rate of the neural network
        :param outputs: Outputs from the previous layer
        :return: None
        """
        for perceptron, delta, output in zip(self.perceptrons, deltas, outputs):
            perceptron.update(delta, learning_rate, output)
