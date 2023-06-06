from typing import List


def dot(input_data: List[float], weights: List[float]):
    return sum([x[0] * x[1] for x in zip(input_data, weights)])