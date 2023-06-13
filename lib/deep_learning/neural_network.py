from lib.deep_learning.layer import Layer
import lib.deep_learning.layer as layer_lib


class NeuralNetwork:

    def __init__(self, layers: list[Layer]):
        self.layers: list[Layer] = layers

    def forward_propagate(self, inputs):
        outputs = [inputs]
        for layer in self.layers:
            outputs.append(layer.forward_propagate(outputs[-1]))
        return outputs

    def backpropagate(self, input, expected, learning_rate):
        layers_result = self.forward_propagate(input)
        expected = [expected]
        for i, layer in enumerate(reversed(self.layers)):
            signal_error = layer_lib.signal_error(layers_result[-i - 1], expected)
            layer.update(signal_error, learning_rate, layers_result[-i - 2])
            if i < len(self.layers) - 1:
                expected = [sum([signal_error[j] * layer.perceptrons[j].weights[i] for j in range(len(signal_error))])
                            for i in range(len(layers_result[-i - 2]))]

    def train(self, inputs, outputs, max_epoch, learning_rate):
        error = 1
        for i in range(max_epoch):
            print(f"Epoch {i + 1}, error: {error}")
            for input, output in zip(inputs, outputs):
                self.backpropagate(input, output, learning_rate)
            avg_error = 0
            for input, output in zip(inputs, outputs):
                avg_error += abs(output - self.predict(input))
            error = avg_error / len(inputs)

    def predict(self, inputs):
        return self.forward_propagate(inputs)[-1][0]
