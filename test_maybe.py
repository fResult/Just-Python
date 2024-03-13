from monads.maybe import Some, Nothing

def divide(y: float):
    def for_x(x: float) -> float:
        if y == 0:
            return Nothing()
        return Some(x / y)

    return for_x


divided_result = Some(10).map(divide(2)).map(divide(0))
Some(10).map(divide(5)).map(divide(2)).map(divide(0))

if divided_result.is_some():
    print(f"The result is Right: {divided_result.value}")
else:
    print(f"The result is Left: {divided_result}")


divided_result = Some(10).map(divide(0)).map(divide(2))

if divided_result.is_some():
    print(f"The result is Right: {divided_result.value}")
else:
    print(f"The result is Left: {divided_result}")


divided_result = Some(10).map(divide(2)).map(divide(2.5))

if divided_result.is_some():
    print(f"The result is Right: {divided_result.value}")
else:
    print(f"The result is Left: {divided_result}")
