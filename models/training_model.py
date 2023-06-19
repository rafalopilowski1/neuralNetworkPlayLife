from typing import List

from lib.deep_learning.input import Input


class Training:
    training_data: List[Input] = []
    width: int
    height: int

    def __init__(self, training_data: List[Input], width, height):
        self.training_data = training_data
        self.width = width
        self.height = height

    def get_generation(self, gen_count):
        given_gen = list(filter(lambda x: x.input[2] == gen_count, self.training_data))
        result = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(given_gen[i * self.width + j])
            result.append(row)
        return result

    def get_max_generation(self):
        return max([input.input[2] for input in self.training_data])
