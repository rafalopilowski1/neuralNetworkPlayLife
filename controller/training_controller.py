from PySide6.QtCore import QObject, Signal, QThread, Slot
from PySide6.QtGui import QColorConstants, QColor
from PySide6.QtWidgets import QTableWidgetItem, QTableWidget, QHeaderView

from controller.training_worker import TrainWorker
from controller.utils import get_background
from models.training_model import Training
from views_qt.ui_mainwindow import Ui_MainWindow


class TrainingController(QObject):
    on_training_data_generated = Signal(QTableWidgetItem, QColor)
    on_training_ended = Signal()
    on_training_ongoing = Signal(str)
    gen_count = 0
    training_model: Training = None

    ui: Ui_MainWindow = None
    neural_network = None

    train_thread: QThread = None
    train_worker: TrainWorker = None

    def __init__(self, training_model: Training, neural_network, ui, parent=None):
        super().__init__(parent)
        self.ui = ui
        self.training_model = training_model
        self.neural_network = neural_network

        self.on_training_ongoing.connect(self.display_training_progress)

        self.ui.trainButton.clicked.connect(self.on_train_button_clicked)

        for table in [self.ui.train_before_tableWidget, self.ui.train_after_tableWidget, self.ui.gen_before_tableWidget,
                      self.ui.gen_after_tableWidget]:
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            table.horizontalHeader().setVisible(False)
            table.verticalHeader().setVisible(False)
            table.setRowCount(self.training_model.width)
            table.setColumnCount(self.training_model.height)
            table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            for i in range(self.training_model.width):
                for j in range(self.training_model.height):
                    table.setItem(i, j, QTableWidgetItem())
                    table.item(i, j).setBackground(QColorConstants.Gray)

        self.ui.previousButton.clicked.connect(self.decrease_gen_count)
        self.ui.previousButton.setEnabled(False)
        self.ui.nextButton.clicked.connect(self.increase_gen_count)

    def train(self):
        self.train_thread = QThread(parent=self)
        self.train_thread.setTerminationEnabled(True)
        self.train_worker = TrainWorker(self.on_training_data_generated, self.on_training_ended,
                                        self.on_training_ongoing, self.training_model,
                                        self.neural_network, self.ui)
        self.train_worker.moveToThread(self.train_thread)
        self.train_thread.started.connect(self.train_worker.train)
        self.train_worker.progress.connect(self.ui.progressBar.setValue)
        self.train_thread.start()
        self.train_worker.ended.connect(self.train_thread.exit)
        self.train_worker.ended.connect(self.ui.statusBar.clearMessage)
        self.train_worker.ended.connect(self.enable_cell_selection)
        self.train_thread.finished.connect(self.enable_train_section)
        self.train_thread.finished.connect(self.train_worker.deleteLater)

    @Slot(int, int, name="cell_clicked")
    def on_cell_clicked(self, row: int, column: int):
        table: QTableWidget = self.sender()
        item: QTableWidgetItem = table.item(row, column)
        item.setBackground(
            QColorConstants.White if item.background().color() == QColorConstants.Black else QColorConstants.Black)
        self.ui.train_after_tableWidget.item(row, column).setBackground(
            get_background(self.neural_network.predict(
                [row, column, self.gen_count + 1, 1 if item.background().color() == QColorConstants.Black else 0])))

    @Slot()
    def stop(self):
        self.train_thread.requestInterruption()
        self.train_thread.quit()
        self.train_thread.wait()

    @Slot(str)
    def display_training_progress(self, progress: str):
        self.ui.statusBar.showMessage(progress)

    @Slot(name="train_button")
    def on_train_button_clicked(self):
        self.ui.trainButton.setEnabled(False)
        for table in [self.ui.train_before_tableWidget, self.ui.train_after_tableWidget]:
            table.setEnabled(False)
        self.train()

    @Slot(name="enable_train_section")
    def enable_train_section(self):
        self.ui.trainButton.setEnabled(True)
        for table in [self.ui.train_before_tableWidget, self.ui.train_after_tableWidget]:
            table.setEnabled(True)

    @Slot(name="increase_gen_count")
    def increase_gen_count(self):
        current_gen = self.training_model.get_generation(self.gen_count)
        next_gen = self.training_model.get_generation(self.gen_count + 1)

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

        self.gen_count += 1
        self.ui.genLcdNumber.display(self.gen_count)
        if self.gen_count > 0:
            self.ui.previousButton.setEnabled(True)
        if self.gen_count == self.training_model.get_max_generation():
            self.ui.nextButton.setEnabled(False)

    @Slot(name="decrease_gen_count")
    def decrease_gen_count(self):
        current_gen = self.training_model.get_generation(self.gen_count)
        next_gen = self.training_model.get_generation(self.gen_count - 1)

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

        self.gen_count -= 1
        self.ui.genLcdNumber.display(self.gen_count)
        if self.gen_count == 0:
            self.ui.previousButton.setEnabled(False)
        if self.gen_count != self.training_model.get_max_generation():
            self.ui.nextButton.setEnabled(True)

    @Slot(name="enable_cell_selection")
    def enable_cell_selection(self):
        for table in [self.ui.train_before_tableWidget, self.ui.gen_before_tableWidget]:
            table.cellClicked.connect(self.on_cell_clicked)
