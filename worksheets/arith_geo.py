from typing import Literal, Callable

type ArithGeo = Literal["Arithmetic", "Geometric", "-1"]


def removed_n_items[T](n: int) -> Callable[[list[T]], list[T]]:
    return lambda arr: arr[n:]


def lte_n_items[T](n: int) -> Callable[[list[T]], bool]:
    return lambda items: len(items) <= n


def is_same_fixed_arith(first: int, second: int) -> Callable[[int, int], int]:
    return lambda curr, prev: curr - prev == second - first


def is_same_fixed_geo(first: int, second: int) -> Callable[[int, int], int]:
    return lambda curr, prev: curr / prev == second / first


removed_2_items = removed_n_items(2)
lte_2_items = lte_n_items(2)


def is_arithmetic(arr: list[int]) -> bool:
    if lte_2_items(arr):
        return False

    is_fixed = is_same_fixed_arith(first=arr[0], second=arr[1])

    return all(
        is_fixed(n, prev=arr[idx - 1])
        for idx, n in enumerate(removed_2_items(arr), start=2)
    )


def is_geometric(arr: list[int]) -> bool:
    if lte_2_items(arr):
        return False

    is_fixed = is_same_fixed_geo(first=arr[0], second=arr[1])

    return not lte_2_items(arr) and all(
        is_fixed(curr, prev=arr[idx - 1])
        for idx, curr in enumerate(removed_2_items(arr), start=2)
    )


def arith_geo(arr: list[int]) -> ArithGeo:
    return (
        "Arithmetic"
        if is_arithmetic(arr)
        else "Geometric"
        if is_geometric(arr)
        else "-1"
    )


print(arith_geo([1, 2, 3, 4, 5]) == "Arithmetic")
print(arith_geo([1, 3, 5, 7, 9]) == "Arithmetic")
print(arith_geo([1, 2, 4, 8, 16]) == "Geometric")
print(arith_geo([1, 3, 9, 27, 81]) == "Geometric")
print(arith_geo([3, 5, 6, 7, 8]) == "-1")
print(arith_geo([1, 2]) == "-1")
print(arith_geo([1]) == "-1")
