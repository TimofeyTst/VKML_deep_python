class CustomList(list):
    def __zip_with_defaults__(self, other):
        if isinstance(other, list):
            self_len = len(self)
            other_len = len(other)
            for i in range(max(self_len, other_len)):
                first = self[i] if i < self_len else 0
                second = other[i] if i < other_len else 0
                yield first, second
        else:
            raise TypeError("Unsupported operand type")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __add__(self, other):
        if isinstance(other, (list, CustomList)):
            return CustomList(
                first + second for first, second in self.__zip_with_defaults__(other)
            )
        else:
            raise TypeError("Unsupported operand type for +")

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, (list, CustomList)):
            return CustomList(
                first - second for first, second in self.__zip_with_defaults__(other)
            )
        else:
            raise TypeError("Unsupported operand type for -")

    def __rsub__(self, other):
        if isinstance(other, (list, CustomList)):
            return CustomList(
                second - first for first, second in self.__zip_with_defaults__(other)
            )
        else:
            raise TypeError("Unsupported operand type for -")

    def __eq__(self, other):
        if isinstance(other, CustomList):
            return sum(self) == sum(other)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, CustomList):
            return sum(self) < sum(other)
        else:
            raise TypeError("Unsupported operand type for <")

    def __le__(self, other):
        if isinstance(other, CustomList):
            return sum(self) <= sum(other)
        else:
            raise TypeError("Unsupported operand type for <=")

    def __gt__(self, other):
        if isinstance(other, CustomList):
            return sum(self) > sum(other)
        else:
            raise TypeError("Unsupported operand type for >")

    def __ge__(self, other):
        if isinstance(other, CustomList):
            return sum(self) >= sum(other)
        else:
            raise TypeError("Unsupported operand type for >=")

    def __str__(self):
        return f"CustomList({list(self)}) = {sum(self)}"
