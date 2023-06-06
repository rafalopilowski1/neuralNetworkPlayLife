import sys
from PySide6.QtWidgets import QApplication
from lib.game_of_life.gen import Generator
from views.gui_window import GuiWindow

if __name__ == "__main__":
    app = QApplication([])
    window = GuiWindow()
    window.show()

    # generator = Generator(10, 10, 10)
    # generator.generate('training_data.csv')

    sys.exit(app.exec())
