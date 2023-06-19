from PySide6.QtCore import Signal, QThread

import lib.deep_learning.layer as layer_lib
from lib.deep_learning.layer import Layer


class NeuralNetwork:
    """
    Neural network class
    """

    def __init__(self, *layers):
        """
        Constructor
        :param layers: Layers of the neural network
        """
        self.layers: list[Layer] = [*layers]

    def forward_propagate(self, inputs):
        """
        Forward propagate the inputs through the neural network
        :param inputs: Inputs
        :return: History of the outputs of each layer
        """
        outputs = [inputs]
        for layer in self.layers:
            outputs.append(layer.forward_propagate(outputs[-1]))
        return outputs

    def backpropagate(self, input, expected, learning_rate):
        """
        Backpropagate the error through the neural network
        :param input: Input
        :param expected: Expected output
        :param learning_rate: Learning rate
        :return: None
        """
        layers_result = self.forward_propagate(input)
        expected = [expected]
        for i, layer in enumerate(reversed(self.layers)):
            signal_error = layer_lib.signal_error(layers_result[-i - 1], expected)
            layer.update(signal_error, learning_rate, layers_result[-i - 2])
            if i < len(self.layers) - 1:
                expected = [sum([signal_error[j] * layer.perceptrons[j].weights[i] for j in range(len(signal_error))])
                            for i in range(len(layers_result[-i - 2]))]

    def train(self, inputs, outputs, max_epoch, learning_rate, progress_signal: Signal(str)):
        """
        Train the neural network
        :param inputs: Inputs
        :param outputs: Outputs
        :param max_epoch: Maximum number of epochs
        :param learning_rate: Learning rate
        :param progress_signal: Qt signal to send the progress
        :return: None
        """
        error = 1
        for i in range(max_epoch):
            if QThread.currentThread().isInterruptionRequested():
                break
            progress_signal.emit(f"Epoch {i + 1}, error: {error}")
            for input, output in zip(inputs, outputs):
                self.backpropagate(input, output, learning_rate)
            avg_error = 0
            for input, output in zip(inputs, outputs):
                avg_error += abs(output - self.predict(input))
            error = avg_error / len(inputs)

    def predict(self, inputs):
        """
        Predict the output of the neural network
        :param inputs: Inputs
        :return: Answer
        """
        return self.forward_propagate(inputs)[-1][0]
