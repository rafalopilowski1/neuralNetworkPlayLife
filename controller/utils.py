from PySide6.QtGui import QColor


def get_background(lives):
    """
    Get the background color for a cell
    :param lives: How much the cell is alive
    :return: Qt color
    """
    color_amount = 255 * lives
    return QColor(color_amount, color_amount, color_amount)
