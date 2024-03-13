from pymonad.either import Left, Right


def divide(y: int):
    def for_x(x: int) -> float:
        return Right(x / y) if y != 0 else Left("Error: Division by zero")

    return for_x


result = Right(10).then(divide(2)).then(divide(5))

print(result)
