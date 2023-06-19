from PySide6.QtWidgets import QDialog

from views_qt.ui_dialog import Ui_Dialog


class AboutDialog(QDialog):
    """
    About dialog
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
