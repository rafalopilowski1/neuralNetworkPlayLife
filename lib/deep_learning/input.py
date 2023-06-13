class Input:

    def __init__(self, input: list[int], lives: int):
        self.input = input
        self.lives = lives

    def __repr__(self):
        return f"(Input: {self.input}, lives: {self.lives})"

    def __str__(self):
        return f"{','.join(str(x) for x in self.input)},{self.lives}"

    def __eq__(self, other):
        for i in range(len(self.input)):
            if self.input[i] != other.points[i]:
                return False
        return self.lives == other.category

    def __hash__(self) -> int:
        hash = sum([point.__hash__() for point in self.input])
        hash += self.lives.__hash__()
        return hash
