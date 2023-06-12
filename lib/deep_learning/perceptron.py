import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def signal_error(output: int, expected: int) -> float:
    return (expected - output) * output * (1 - output)


class Perceptron:

    def __init__(self, input_count):
        self.weights = np.random.randn(input_count)
        self.bias = np.random.randn()

    def activate(self, input_data: np.ndarray[float]):
        if len(input_data) != len(self.weights):
            raise Exception("Wrong input data for this perceptron!")
        return sigmoid(np.dot(input_data, self.weights) + self.bias)

    def update(self, delta, learning_rate, inputs):
        self.weights += learning_rate * delta * np.array(inputs)
        self.bias += learning_rate * delta
