from lib.deep_learning.layer import Layer


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
        for i, layer in enumerate(reversed(self.layers)):
            signal_error = layer.signal_error(layers_result[-i - 1], expected)
            layer.update(signal_error, learning_rate, layers_result[-i - 2])
            expected = signal_error

    def train(self, inputs, outputs, max_err, learning_rate):
        i = 0
        error = 1
        while error > max_err:
            i += 1
            print(f"Epoch {i + 1}, error: {error}")
            for input, output in zip(inputs, outputs):
                self.backpropagate(input, output, learning_rate)
            avg_error = 0
            for input, output in zip(inputs, outputs):
                avg_error += abs(output - self.predict(input))
            error = avg_error / len(inputs)

    def predict(self, inputs):
        return self.forward_propagate(inputs)[-1][0]
