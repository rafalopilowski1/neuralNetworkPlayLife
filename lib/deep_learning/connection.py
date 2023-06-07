from typing import Optional

from lib.deep_learning.perceptron import Perceptron


class Connection:

    def __init__(
        self,
        to_perceptron_weight_index: int,
        from_perceptron: Optional[Perceptron] = None,
        to_perceptron: Optional[Perceptron] = None,
    ):
        self.from_perceptron: Optional[Perceptron] = from_perceptron
        self.to_perceptron: Optional[Perceptron] = to_perceptron
        self.to_perceptron_weight_index: int = to_perceptron_weight_index