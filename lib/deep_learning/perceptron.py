from copy import deepcopy
import random
from typing import List
from utils.utils import dot


class Perceptron:

    def __init__(self, learning_rate):
        self.weights = []
        self.threshold = random.random()
        self.learning_rate = learning_rate

    def set_weights(self, weights: List[float]):
        self.weights = weights

    def get_result(self, input_data: List[float]):
        if len(self.weights) == 0:
            self.weights = [random.random() for x in range(len(input_data))]
        elif len(input_data) != len(self.weights):
            raise Exception("Wrong input data for this perceptron!")
        return int(dot(input_data, weights=self.weights) >= self.threshold)

    def learn(self, input_data: List[float], expected: int):
        given = self.get_result(input_data)
        # print(f"Given: {given}")
        self.weights.append(self.threshold)
        # print(f"Weight before: {self.weights}")
        input_data.append(-1)
        # print(f"Input before: {input_data}")
        diff = [(expected - given) * self.learning_rate * x
                for x in input_data]
        # print(f"Diff: {diff}")
        input_data.pop()
        # print(f"Input after: {input_data}")
        self.weights = [x[0] + x[1] for x in zip(self.weights, diff)]
        # print(f"Weights after: {self.weights}")
        self.threshold = self.weights.pop()
        # print(f"New threshold: {self.threshold}")
    def backpropagate(self, input_data: List[float], expected: int):
        pass