from typing import List

from lib.deep_learning.perceptron import Perceptron


class Layer:

    def __init__(self, perceptrons: List[Perceptron]):
        self.perceptrons = []