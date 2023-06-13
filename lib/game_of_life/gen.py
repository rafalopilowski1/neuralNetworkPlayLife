from lib.deep_learning.input import Input
from lib.game_of_life.board import get_random


class Generator:

    def __init__(self, width: int, height: int, iterations: int):
        self.width = width
        self.height = height
        self.board = get_random(width, height)
        self.iterations = iterations

    def generate(self, path: str):
        strings = self.board.get_training_data(self.iterations)
        with open(path, 'w') as f:
            for string in strings:
                f.write(string + '\n')

    def get_data(self) -> list[Input]:
        return self.board.get_data(self.iterations)
