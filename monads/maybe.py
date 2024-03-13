from typing import Self, TypeVar, Callable

R = TypeVar('R')

class Maybe:
    def is_some(self: Self) -> bool:
        return self.__class__ == Some

class Some[T](Maybe):
    def __init__(self: Self, value: T):
        self.value = value

    def map(self: Self, func: Callable[[T], R]) -> Self:
        return func(self.value)

    def __str__(self: Self):
        return f"Some({self.value})"


class Nothing[T](Maybe):
    def map(self: Self, func: Callable[[T], R]) -> Self:
        return self

    def __str__(self: Self) -> Self:
        return f"Nothing"
