from PySide6.QtCore import QObject, Signal, Slot, QThread
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidgetItem

from controller.utils import get_background


class TrainWorker(QObject):
    """
    Qt Worker for training section
    """
    progress = Signal(int)
    ended = Signal()

    def __init__(self, on_training_data_generated, on_training_ended, on_training_ongoing, training_model,
                 neural_network, ui, max_epoch,
                 parent=None):
        """
        Constructor setting up the training worker
        :param on_training_data_generated: Qt Signal for training data generated
        :param on_training_ended: Qt Signal for training ended
        :param on_training_ongoing: Qt Signal for training ongoing
        :param training_model: Training model
        :param neural_network: Neural network
        :param ui: UI view
        :param max_epoch: Maximum number of epoch
        :param parent: Qt parent
        """
        super().__init__(parent)

        self.on_training_data_generated = on_training_data_generated
        self.on_training_ended = on_training_ended
        self.on_training_ongoing = on_training_ongoing

        self.training_model = training_model
        self.neural_network = neural_network

        self.ui = ui

        self.max_epoch = max_epoch

        self.on_training_data_generated.connect(self.display_cell)
        self.on_training_ended.connect(self.predict_first_board)

    @Slot()
    def predict_first_board(self):
        """
        Display the first board after training
        :return: None
        """
        first_generation = list(filter(lambda elem: elem.input[2] == 0, self.training_model.training_data))
        for i, input in enumerate(first_generation):
            self.on_training_data_generated.emit(self.ui.train_before_tableWidget.item(input.input[0], input.input[1]),
                                                 get_background(input.input[3]))
            self.on_training_data_generated.emit(self.ui.train_after_tableWidget.item(input.input[0], input.input[1]),
                                                 get_background(self.neural_network.predict(input.input)))
            self.progress.emit(int((i / len(first_generation)) * 100))
        self.progress.emit(100)
        self.progress.emit(0)
        self.ended.emit()

    @Slot()
    def train(self):
        """
        Train the neural network
        :return: None
        """
        inputs = [input.input for input in self.training_model.training_data]
        outputs = [input.lives for input in self.training_model.training_data]
        self.neural_network.train(inputs, outputs, self.max_epoch, 1, self.on_training_ongoing)
        if QThread.currentThread().isInterruptionRequested():
            return
        self.on_training_ended.emit()

    @Slot(QTableWidgetItem, QColor)
    def display_cell(self, table_item: QTableWidgetItem, color: QColor):
        """
        Display a cell in a table
        :param table_item: Qt table item
        :param color: Qt color
        :return: None
        """
        table_item.setBackground(color)
