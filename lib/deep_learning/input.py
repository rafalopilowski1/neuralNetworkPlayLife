from typing import List


class Cell:

    def __init__(self, input: List[float], lives: bool):
        self.input = input
        self.lives = lives

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"(Input: {self.input}, lives: {self.lives})"

    def __eq__(self, other):
        for i in range(len(self.input)):
            if self.input[i] != other.points[i]:
                return False
        return self.lives == other.category

    def __hash__(self) -> int:
        hash = sum([point.__hash__() for point in self.input])
        hash += self.lives.__hash__()
        return hash