from typing import List
from lib.deep_learning.layer import Layer


class NeuralNetowrk:

    def __init__(self, threshold: float):
        self.layers: List[Layer] = []
        self.connections = []
