from lib.game_of_life.board import Board


class Generator:

    def __init__(self, width: int, height: int, iterations: int):
        self.width = width
        self.height = height
        self.board = Board.get_random(width, height)
        self.iterations = iterations

    def generate(self, path: str):
        print('generate')
        strings = self.board.get_training_data(self.iterations)
        with open(path, 'w') as f:
            for string in strings:
                f.write(string + '\n')
