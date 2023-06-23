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

    width = 5
    height = 5

    generator = Generator(width, height, 30)
    generator.generate('training_data.csv')
    data = generator.get_data()

    max_epoch = 1000
    layers = [Layer(4, 4), Layer(4, 3), Layer(3, 2), Layer(2, 1)]
    neural_network = NeuralNetwork(*layers)

    controller = TrainingController(Training(data, width, height), neural_network, window.ui, max_epoch, window)

    app.aboutToQuit.connect(controller.stop)

    controller.train()

    sys.exit(app.exec())
