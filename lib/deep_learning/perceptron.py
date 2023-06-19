import numpy as np


def sigmoid(z):
    """
    Sigmoid function
    :param z: Net input
    :return: Sigmoid value
    """
    return 1 / (1 + np.exp(-z))


def signal_error(output: int, expected: int) -> float:
    """
    Signal error
    :param output: Given output
    :param expected: Expected output
    :return: Error
    """
    return (expected - output) * output * (1 - output)


class Perceptron:
    """
    Perceptron class
    """

    def __init__(self, input_count):
        """
        Constructor
        :param input_count: Number of inputs
        """
        self.weights = np.random.randn(input_count)
        self.bias = np.random.randn()

    def activate(self, input_data: np.ndarray[float]):
        """
        Activate the perceptron
        :param input_data: Numpy array of input data
        :return: Output of the perceptron
        """
        if len(input_data) != len(self.weights):
            raise Exception("Wrong input data for this perceptron!")
        return sigmoid(np.dot(input_data, self.weights) + self.bias)

    def update(self, delta, learning_rate, inputs):
        """
        Update the perceptron
        :param delta: Delta value
        :param learning_rate: Learning rate
        :param inputs: Inputs
        :return: None
        """
        self.weights += learning_rate * delta * np.array(inputs)
        self.bias += learning_rate * delta
