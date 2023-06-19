import sys

from PySide6.QtWidgets import QApplication

from controller.training_controller import TrainingController
from lib.deep_learning.layer import Layer
from lib.deep_learning.neural_network import NeuralNetwork
from lib.game_of_life.gen import Generator
from models.training_model import Training
from views.gui_window import GuiWindow

if __name__ == "__main__":
    app = QApplication([])
    window = GuiWindow()
    window.show()

    generator = Generator(10, 10, 10)
    generator.generate('training_data.csv')
    data = generator.get_data()

    neural_network = NeuralNetwork(Layer(4, 3), Layer(3, 2), Layer(2, 1))

    controller = TrainingController(Training(data, 10, 10), neural_network, window.ui)

    app.aboutToQuit.connect(controller.stop)

    controller.train()

    sys.exit(app.exec())
