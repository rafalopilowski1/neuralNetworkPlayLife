from typing import List

from lib.deep_learning.input import Input


class Training:
    """
    This class is used to store training data and provide methods to get data for a specific generation.
    """
    training_data: List[Input] = []
    width: int
    height: int

    def __init__(self, training_data: List[Input], width, height):
        """
        :type training_data: List[Input]
        :param training_data:  List of training data
        :param width: Width of the grid
        :param height: Height of the grid
        """
        self.training_data = training_data
        self.width = width
        self.height = height

    def get_generation(self, gen_count):
        """
        Get inputs for a specific generation
        :param gen_count: Amount of generations
        :return: List of inputs for a specific generation
        """
        given_gen = list(filter(lambda x: x.input[2] == gen_count, self.training_data))
        result = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(given_gen[i * self.width + j])
            result.append(row)
        return result

    def get_max_generation(self):
        """
        Get the maximum generation
        :return: Maximum generation
        """
        return max([input.input[2] for input in self.training_data])
