from PySide6.QtGui import QColor


def get_background(lives):
    color_amount = 255 * lives
    return QColor(color_amount, color_amount, color_amount)
