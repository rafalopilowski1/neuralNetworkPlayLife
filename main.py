import sys

from PySide6.QtWidgets import QApplication

from lib.deep_learning.layer import Layer
from lib.deep_learning.neural_network import NeuralNetwork
from lib.game_of_life.gen import Generator
from views.gui_window import GuiWindow

if __name__ == "__main__":
    app = QApplication([])
    window = GuiWindow()
    window.show()

    generator = Generator(10, 10, 10)
    generator.generate('training_data.csv')
    data = generator.get_data()
    inputs = [input.input for input in data]
    outputs = [input.lives for input in data]
    neuralNetwork = NeuralNetwork(
        [Layer(4, 4), Layer(4, 2), Layer(2, 1)])
    neuralNetwork.train(inputs, outputs, 1000, 1)
    print(neuralNetwork.predict([0, 0, 0, 0]))
    sys.exit(app.exec())
