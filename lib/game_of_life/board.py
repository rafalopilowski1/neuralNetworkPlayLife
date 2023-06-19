from copy import deepcopy
from random import random
from typing import List

from lib.deep_learning.input import Input
from lib.game_of_life.cell import Cell


def get_random(width, height):
    """
    Get a random first board
    :param width: Width of the board
    :param height: Height of the board
    :return: Random board
    """
    cells = [
        Cell(i % width, i // width, (random() >= 0.5))
        for i in range(width * height)
    ]
    return Board(width, height, cells)


class Board:
    """
    This class is used to store the board and provide methods to get the next generation.
    """

    def __init__(self, width, height, cells: List[Cell]):
        """
        Constructor
        :type width: int
        :type height: int
        :type cells: List[Cell]
        :param width: Width of the board
        :param height: Height of the board
        :param cells: List of cells
        """
        self.width = width
        self.height = height
        self.cells = cells

    def next_generation(self):
        """
        Get the board with the next generation
        :return: Board with the next generation
        """
        next_cells = deepcopy(self.cells)
        for cell in next_cells:
            cell.next_generation(next_cells)
        return Board(self.width, self.height, next_cells)

    def get_sample_iterations(self, iterations: int):
        """
        Get a list of boards with the next generations
        :param iterations: Number of boards
        :return: List of boards with the next generations
        """
        boards = []
        current = deepcopy(self)
        for _ in range(iterations+1):
            next = current.next_generation()
            boards.append(next)
            current = next
        return boards

    def get_training_data(self, iterations: int):
        """
        Get the training data for saving to a file
        :param iterations: Number of boards
        :return: List of training data strings
        """
        inputs = self.get_data(iterations)
        return [str(input) for input in inputs]

    def get_data(self, iterations):
        """
        Get the training data
        :param iterations: Number of boards
        :return: Training data
        """
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
