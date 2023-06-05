from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot
from views_qt.ui_mainwindow import Ui_MainWindow
from views.about_dialog import AboutDialog


class GuiWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionAbout.triggered.connect(self.on_about_menu_triggered)
        self.ui.actionQuit.triggered.connect(self.on_about_quit_triggered)
        self.ui.trainButton.clicked.connect(self.on_train_button_clicked)

    @Slot(name="about_menu")
    def on_about_menu_triggered(self):
        dlg = AboutDialog()
        dlg.exec()

    @Slot(name="about_quit")
    def on_about_quit_triggered(self):
        self.close()

    @Slot(name="train_button")
    def on_train_button_clicked(self):
        pass
