from copy import deepcopy
from random import choice
from typing import List
from lib.deep_learning.input import Input
from lib.game_of_life.cell import Cell


class Board:

    def __init__(self, width, height, cells: List[Cell]):
        self.width = width
        self.height = height
        self.cells = cells

    def next_generation(self):
        print('board next generation')
        previous_cells = deepcopy(self.cells)
        for cell in self.cells:
            cell.next_generation(self.cells)
        return Board(self.width, self.height, previous_cells)

    def get_random(width, height):
        print('get random')
        cells = [
            Cell(i % width, i // width, choice([True, False]))
            for i in range(width * height)
        ]
        return Board(width, height, cells)

    def get_sample_iterations(self, iterations: int):
        print('get sample iterations')
        boards = [self]
        for i in range(iterations):
            boards.append(boards[i].next_generation())
        return boards

    def get_training_data(self, iterations: int) -> List[Input]:
        print('get training data')
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
        return [str(input) for input in inputs]
