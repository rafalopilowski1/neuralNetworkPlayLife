from typing import List

from lib.deep_learning.input import Input


class Training:
    training_data: List[Input] = []

    def __init__(self, training_data: List[Input]):
        self.training_data = training_data
