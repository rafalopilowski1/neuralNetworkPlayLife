from PySide6.QtCore import QObject, Signal, QThread, Slot
from PySide6.QtGui import QColorConstants, QColor
from PySide6.QtWidgets import QTableWidgetItem, QTableWidget

from controller.training_worker import TrainWorker
from controller.utils import get_background
from models.training_model import Training


class TrainingController(QObject):
    """
    Qt Controller for training section
    """
    on_training_data_generated = Signal(QTableWidgetItem, QColor)
    on_training_ended = Signal()
    on_training_ongoing = Signal(str)
    gen_count = 0

    def __init__(self, training_model: Training, neural_network, ui, max_epoch, parent=None):
        """
        Constructor setting up the training controller

        :type max_epoch: int
        :type ui: Ui_MainWindow
        :type neural_network: NeuralNetwork
        :type training_model: Training
        :type parent: QObject

        :param training_model: Training Qt model
        :param neural_network: Neural network
        :param ui: UI view
        :param max_epoch: Maximum number of epoch
        :param parent: Qt parent
        """
        super().__init__(parent)
        self.train_worker = None
        self.train_thread = None
        self.max_epoch = max_epoch
        self.ui = ui
        self.training_model = training_model
        self.neural_network = neural_network

        self.on_training_ongoing.connect(self.display_training_progress)

        self.ui.trainButton.clicked.connect(self.on_train_button_clicked)

        self.initialize_table_widgets()

        self.ui.previousButton.clicked.connect(self.decrease_gen_count)
        self.ui.previousButton.setEnabled(False)
        self.ui.nextButton.clicked.connect(self.increase_gen_count)

        self.show_gens_on_tables(self.gen_count + 1)

    def initialize_table_widgets(self):
        for table in [self.ui.train_before_tableWidget, self.ui.train_after_tableWidget, self.ui.gen_before_tableWidget,
                      self.ui.gen_after_tableWidget]:
            table.setRowCount(self.training_model.width)
            table.setColumnCount(self.training_model.height)
            for i in range(self.training_model.width):
                for j in range(self.training_model.height):
                    table.setItem(i, j, QTableWidgetItem())
                    table.item(i, j).setBackground(QColorConstants.Gray)

    def train(self):
        """
        Train the neural network on a separate thread
        :return: None
        """
        self.train_thread = QThread(parent=self)
        self.train_thread.setTerminationEnabled(True)

        self.train_worker = TrainWorker(self.on_training_data_generated, self.on_training_ended,
                                        self.on_training_ongoing, self.training_model,
                                        self.neural_network, self.ui, self.max_epoch)
        self.train_worker.moveToThread(self.train_thread)
        self.train_worker.progress.connect(self.ui.progressBar.setValue)

        self.train_thread.started.connect(self.train_worker.train)
        self.train_thread.started.connect(self.disable_cell_selection)
        self.train_thread.start()

        self.train_worker.ended.connect(self.train_thread.exit)
        self.train_worker.ended.connect(self.ui.statusBar.clearMessage)
        self.train_worker.ended.connect(self.enable_cell_selection)

        self.train_thread.finished.connect(self.enable_train_section)
        self.train_thread.finished.connect(self.train_worker.deleteLater)

    @Slot(int, int, name="cell_clicked")
    def on_cell_clicked(self, row: int, column: int):
        """
        Slot called when a cell is clicked, update the cell color and the neural network prediction
        :param row: X coordinate
        :param column: Y coordinate
        :return: None
        """
        table: QTableWidget = self.sender()
        item: QTableWidgetItem = table.item(row, column)
        item.setBackground(
            QColorConstants.White if item.background().color() == QColorConstants.Black else QColorConstants.Black)
        self.ui.train_after_tableWidget.item(row, column).setBackground(
            get_background(self.neural_network.predict(
                [row, column, self.gen_count + 1, 1 if item.background().color() == QColorConstants.Black else 0])))

    @Slot()
    def stop(self):
        """
        Stop the training thread
        :return: None
        """
        self.train_thread.requestInterruption()
        self.train_thread.quit()
        self.train_thread.wait()

    @Slot(str)
    def display_training_progress(self, progress: str):
        """
        Display the training progress in the status bar
        :param progress: Progress message
        :return: None
        """
        self.ui.statusBar.showMessage(progress)

    @Slot(name="train_button")
    def on_train_button_clicked(self):
        """
        Slot called when the train button is clicked, start the training
        :return: None
        """
        self.ui.trainButton.setEnabled(False)
        for table in [self.ui.train_before_tableWidget, self.ui.train_after_tableWidget]:
            table.setEnabled(False)
        self.train()

    @Slot(name="enable_train_section")
    def enable_train_section(self):
        """
        Slot called when the training is finished, enable the training section
        :return: None
        """
        self.ui.trainButton.setEnabled(True)
        for table in [self.ui.train_before_tableWidget, self.ui.train_after_tableWidget]:
            table.setEnabled(True)

    @Slot(name="increase_gen_count")
    def increase_gen_count(self):
        """
        Slot called when the next button is clicked, increase the generation count and refresh the UI
        :return: None
        """
        self.show_gens_on_tables(self.gen_count + 1)

        self.gen_count += 1
        self.ui.genLcdNumber.display(self.gen_count)
        if self.gen_count > 0:
            self.ui.previousButton.setEnabled(True)
        if self.gen_count == self.training_model.get_max_generation():
            self.ui.nextButton.setEnabled(False)

    def show_gens_on_tables(self, goal_gen: int):
        current_gen = self.training_model.get_generation(self.gen_count)
        next_gen = self.training_model.get_generation(goal_gen)
        for row in range(self.training_model.width):
            for column in range(self.training_model.height):
                self.ui.gen_before_tableWidget.item(row, column).setBackground(
                    get_background(current_gen[column][row].lives))
                self.ui.train_before_tableWidget.item(row, column).setBackground(
                    get_background(current_gen[column][row].lives))

                self.ui.gen_after_tableWidget.item(row, column).setBackground(
                    get_background(next_gen[column][row].lives))
                if self.train_thread.isRunning():
                    continue
                self.ui.train_after_tableWidget.item(row, column).setBackground(
                    get_background(self.neural_network.predict(current_gen[column][row].input)))

    @Slot(name="decrease_gen_count")
    def decrease_gen_count(self):
        """
        Slot called when the previous button is clicked, decrease the generation count and refresh the UI
        :return: None
        """
        self.show_gens_on_tables(self.gen_count - 1)

        self.gen_count -= 1
        self.ui.genLcdNumber.display(self.gen_count)
        if self.gen_count == 0:
            self.ui.previousButton.setEnabled(False)
        if self.gen_count != self.training_model.get_max_generation():
            self.ui.nextButton.setEnabled(True)

    @Slot(name="enable_cell_selection")
    def enable_cell_selection(self):
        """
        Slot called when the training is finished, enable the cell selection
        :return: None
        """
        self.ui.train_before_tableWidget.cellClicked.connect(self.on_cell_clicked)

    @Slot(name="disable_cell_selection")
    def disable_cell_selection(self):
        """
        Slot called when the training is started, disable the cell selection
        :return: None
        """
        self.ui.train_before_tableWidget.cellClicked.disconnect(self.on_cell_clicked)
