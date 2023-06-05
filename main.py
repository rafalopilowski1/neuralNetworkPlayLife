import sys
from PySide6.QtWidgets import QApplication
from views.gui_window import GuiWindow

if __name__ == "__main__":
    app = QApplication([])
    window = GuiWindow()
    window.show()
    sys.exit(app.exec())
