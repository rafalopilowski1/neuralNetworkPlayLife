from copy import deepcopy
from random import choice
from typing import List

from lib.deep_learning.input import Input
from lib.game_of_life.cell import Cell


def get_random(width, height):
    cells = [
        Cell(i % width, i // width, choice([True, False]))
        for i in range(width * height)
    ]
    return Board(width, height, cells)


class Board:

    def __init__(self, width, height, cells: List[Cell]):
        self.width = width
        self.height = height
        self.cells = cells

    def next_generation(self):
        previous_cells = deepcopy(self.cells)
        for cell in self.cells:
            cell.next_generation(self.cells)
        return Board(self.width, self.height, previous_cells)

    def get_sample_iterations(self, iterations: int):
        boards = [self]
        for i in range(iterations):
            boards.append(boards[i].next_generation())
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
