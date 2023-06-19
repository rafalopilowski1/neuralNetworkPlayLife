from lib.deep_learning.input import Input
from lib.game_of_life.board import get_random


class Generator:
    """
    Generates training data for the game of life.
    """

    def __init__(self, width: int, height: int, iterations: int):
        """
        :type width: int
        :type height: int
        :type iterations: int
        :param width: Width of the board
        :param height: Height of the board
        :param iterations: Number of iterations to generate
        """
        self.width = width
        self.height = height
        self.board = get_random(width, height)
        self.iterations = iterations

    def generate(self, path: str):
        """
        Generates training data and writes it to a file.
        :param path: Path to the file to write to
        :return: None
        """
        strings = self.board.get_training_data(self.iterations)
        with open(path, 'w') as f:
            for string in strings:
                f.write(string + '\n')

    def get_data(self) -> list[Input]:
        """
        Gets the training data.
        :return: Training data
        """
        return self.board.get_data(self.iterations)
