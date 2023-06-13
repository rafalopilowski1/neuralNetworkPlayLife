from lib.deep_learning import perceptron as perc_lib
from lib.deep_learning.perceptron import Perceptron


def signal_error(outputs, expected) -> list[float]:
    return [perc_lib.signal_error(output, expect) for output, expect in zip(outputs, expected)]


class Layer:

    def __init__(self, num_inputs, num_neurons):
        self.perceptrons = [Perceptron(num_inputs) for _ in range(num_neurons)]

    def forward_propagate(self, inputs):
        return [perceptron.activate(inputs) for perceptron in self.perceptrons]

    def update(self, deltas, learning_rate, outputs):
        for perceptron, delta, output in zip(self.perceptrons, deltas, outputs):
            perceptron.update(delta, learning_rate, output)
