from copy import deepcopy
from random import random
from typing import List

from lib.deep_learning.input import Input
from lib.game_of_life.cell import Cell


def get_random(width, height):
    cells = [
        Cell(i % width, i // width, (random() >= 0.5))
        for i in range(width * height)
    ]
    return Board(width, height, cells)


class Board:

    def __init__(self, width, height, cells: List[Cell]):
        self.width = width
        self.height = height
        self.cells = cells

    def next_generation(self):
        next_cells = deepcopy(self.cells)
        for cell in next_cells:
            cell.next_generation(next_cells)
        return Board(self.width, self.height, next_cells)

    def get_sample_iterations(self, iterations: int):
        boards = []
        current = deepcopy(self)
        for _ in range(iterations+1):
            next = current.next_generation()
            boards.append(next)
            current = next
        return boards

    def get_training_data(self, iterations: int):
        inputs = self.get_data(iterations)
        return [str(input) for input in inputs]

    def get_data(self, iterations):
        boards = self.get_sample_iterations(iterations)
        inputs = []
        for i in range(iterations):
            for cell in boards[i].cells:
                next_generation_cell = boards[i + 1].cells[cell.x +
                                                           cell.y * self.width]
                inputs.append(
                    Input(
                        [cell.x, cell.y, i, int(cell.lives)],
                        int(next_generation_cell.lives)))

        return inputs
