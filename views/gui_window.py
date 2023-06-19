from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QAbstractItemView, QHeaderView

from views.about_dialog import AboutDialog
from views_qt.ui_mainwindow import Ui_MainWindow


class GuiWindow(QMainWindow):
    """
    The main GUI window
    """
    def __init__(self):
        """
        Initialize the GUI window
        """
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionAbout.triggered.connect(self.on_about_menu_triggered)
        self.ui.actionQuit.triggered.connect(self.on_about_quit_triggered)

        for table in [self.ui.train_before_tableWidget, self.ui.train_after_tableWidget, self.ui.gen_before_tableWidget,
                      self.ui.gen_after_tableWidget]:
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.ui.gen_before_tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.gen_after_tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.train_before_tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.train_after_tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    @Slot(name="about_menu")
    def on_about_menu_triggered(self):
        """
        Shows "About" dialog
        :return: None
        """
        dlg = AboutDialog()
        dlg.exec()

    @Slot(name="about_quit")
    def on_about_quit_triggered(self):
        """
        Closes the application
        :return: None
        """
        self.close()
