class Cell:
    """
    Cell class
    """

    def __init__(self, x, y, lives):
        """
        Constructor
        :type x: int
        :type y: int
        :type lives: bool
        :param x: X coordinate
        :param y: Y coordinate
        :param lives: Whether the cell lives
        """
        self.x = x
        self.y = y
        self.lives = lives

    def next_generation(self, cells):
        """
        Determine whether the cell lives in the next generation
        :param cells: All cells
        :return: None
        """
        nearby_living_cells = [
            cell for cell in cells if cell != self and cell.is_nearby(self) and cell.lives
        ]
        if self.lives:
            if len(nearby_living_cells) < 2 or len(nearby_living_cells) > 3:
                self.lives = False
        else:
            if len(nearby_living_cells) == 3:
                self.lives = True

    def is_nearby(self, cell) -> bool:
        """
        Determine whether the cell is nearby
        :param cell: Given cell
        :return: Whether the cell is nearby
        """
        distance_x = abs(self.x - cell.x)
        distance_y = abs(self.y - cell.y)
        return distance_x <= 1 and distance_y <= 1
