from typing import List


class Cell:

    def __init__(self, x, y, lives):
        self.x = x
        self.y = y
        self.lives = lives

    def next_generation(self, cells):
        nearby_cells = [
            cell for cell in cells if cell != self and cell.is_nearby(self)
        ]
        if self.lives:
            if len(nearby_cells) < 2 or len(nearby_cells) > 3:
                self.lives = False
        else:
            if len(nearby_cells) == 3:
                self.lives = True

    def is_nearby(self, cell) -> bool:
        distance_x = abs(self.x - cell.x)
        distance_y = abs(self.y - cell.y)
        return distance_x <= 1 and distance_y <= 1