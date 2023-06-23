from PySide6.QtWidgets import QDialog

from views_qt.ui_dialog import Ui_AboutDialog


class AboutDialog(QDialog):
    """
    About dialog
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
