from PySide6.QtGui import QColor


def get_background(lives):
    if lives >= 0.5:
        return QColor(255, 255, 255)
    else:
        return QColor(0, 0, 0)
