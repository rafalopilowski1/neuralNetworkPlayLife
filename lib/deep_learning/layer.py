from lib.deep_learning import perceptron
from lib.deep_learning.perceptron import Perceptron


class Layer:

    def __init__(self, num_inputs, num_neurons):
        self.perceptrons = [Perceptron(num_inputs) for _ in range(num_neurons)]

    def forward_propagate(self, inputs):
        return [perceptron.activate(inputs) for perceptron in self.perceptrons]

    def signal_error(self, outputs, expected) -> float:
        errors = [perceptron.signal_error(output, expected) for _, output in zip(self.perceptrons, outputs)]
        return sum(errors) / len(errors)

    def update(self, delta, learning_rate, output):
        for perceptron in self.perceptrons:
            perceptron.update(delta, learning_rate, output)
