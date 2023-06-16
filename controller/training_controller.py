from PySide6.QtCore import QObject, Signal, Slot, QThread
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidgetItem

from lib.deep_learning.input import Input
from models.training_model import Training
from views.gui_window import GuiWindow


def get_background(lives):
    if lives == 1:
        return QColor(255, 255, 255)
    else:
        return QColor(0, 0, 0)


class TrainWorker(QObject):
    progress = Signal(int)
    ended = Signal()

    on_training_data_generated: Signal(QTableWidgetItem, Input) = None
    on_training_ended: Signal = None

    training_model: Training = None
    neural_network = None

    window: GuiWindow = None

    def __init__(self, on_training_data_generated, on_training_ended, training_model, neural_network, window,
                 parent=None):
        self.on_training_data_generated = on_training_data_generated
        self.on_training_ended = on_training_ended

        self.training_model = training_model
        self.neural_network = neural_network

        self.window = window

        super().__init__(parent)

        self.on_training_data_generated.connect(self.display_cell)
        self.on_training_ended.connect(self.generate_training_data)

    @Slot()
    def generate_training_data(self):
        first_generation = list(filter(lambda elem: elem.input[2] == 0, self.training_model.training_data))
        for i, input in enumerate(first_generation):
            table_cell = QTableWidgetItem()
            table_cell.setBackground(get_background(input.lives))
            self.on_training_data_generated.emit(table_cell, input)
            self.progress.emit(int((i / len(first_generation)) * 100))
        self.progress.emit(100)
        self.ended.emit()

    @Slot(QTableWidgetItem, Input)
    def display_cell(self, table_cell: QTableWidgetItem, input: Input):
        self.window.ui.tableWidget.setItem(input.input[0], input.input[1], table_cell)

    @Slot()
    def train(self):
        inputs = [input.input for input in self.training_model.training_data]
        outputs = [input.lives for input in self.training_model.training_data]
        self.neural_network.train(inputs, outputs, 1000, 1)
        self.on_training_ended.emit()


class TrainingController(QObject):
    on_training_data_generated = Signal(QTableWidgetItem, Input)
    on_training_ended = Signal()
    training_model: Training = None

    window: GuiWindow = None
    neural_network = None

    train_thread: QThread = None
    train_worker: TrainWorker = None

    def __init__(self, training_model: Training, neural_network, window, parent=None):
        super().__init__(parent)
        self.window = window
        self.training_model = training_model
        self.neural_network = neural_network

    def train(self):
        self.train_thread = QThread()
        self.train_worker = TrainWorker(self.on_training_data_generated, self.on_training_ended, self.training_model,
                                        self.neural_network, self.window)
        self.train_worker.moveToThread(self.train_thread)
        self.train_thread.started.connect(self.train_worker.train)
        self.train_worker.progress.connect(self.window.ui.progressBar.setValue)
        self.train_thread.start()
        self.train_worker.ended.connect(self.train_thread.exit)
