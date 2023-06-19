class Input:
    """
    Class representing an input to the neural network.
    """

    def __init__(self, input: list[int], lives: int):
        """
        Constructor
        :param input: Vector of points
        :param lives: Answer to the input
        """
        self.input = input
        self.lives = lives

    def __repr__(self):
        """
        Representation of the object
        :return: Debug string
        """
        return f"(Input: {self.input}, lives: {self.lives})"

    def __str__(self):
        """
        String representation of the object
        :return: Input as a string
        """
        return f"{','.join(str(x) for x in self.input)},{self.lives}"

    def __eq__(self, other):
        """
        Equality operator
        :param other: Another input
        :return: Whether the two inputs are equal
        """
        for i in range(len(self.input)):
            if self.input[i] != other.points[i]:
                return False
        return self.lives == other.category

    def __hash__(self) -> int:
        """
        Hash function
        :return: Integer hash
        """
        hash = sum([point.__hash__() for point in self.input])
        hash += self.lives.__hash__()
        return hash
