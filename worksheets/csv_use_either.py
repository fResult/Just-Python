import csv
import os

from typing import Callable
from pymonad.either import Either, Left, Right


type MapperFn[T, R] = Callable[[T], R]


def is_list_more_than[T](n: int):
    def for_list(xs: list[T]) -> bool:
        return len(xs) > n

    return for_list


def is_remaining[T](xs: list[T]) -> bool:
    return is_list_more_than(0)(xs)


def read_csv_file(file_path: str):
    if os.path.isfile(file_path):
        with open(file_path, "r") as csv_file:
            return Right(row for row in csv.reader(csv_file))

    return Left("Error: File not found")


def remove_row(row_index: int):
    def for_rows(rows: list[list[str]]):
        if is_remaining(list):
            return Right(rows[row_index:])

        return Left("Error: Unable to remove row")

    return for_rows


def extract_column(column_index: int):
    def for_row(row: list[str]):
        columns = row
        if is_list_more_than(column_index)(columns):
            return Right(col[column_index] for col in columns)

        return Left(f"Error::[{extract_column.__name__}]: Unable to extract column")

    return for_row


def convert_to[T, R](converter: MapperFn[T, R]):
    def for_columns(columns: list[str]):
        converted_column = [converter(col) if col.isdigit() else None for col in columns]

        if all(x is not None for x in converted_column):
            return Right(converted_column)

        return Left(f"Error::[{convert_to.__name__}]: Unable to convert to float")

    return for_columns


def average(numbers: list[float]) -> Either[str, float]:
    has_some_numbers = is_remaining

    return (
        Right(sum(numbers) / len(numbers))
        if has_some_numbers(numbers)
        else Left(f"Error::[{average.__name__}]: Division by zero")
    )


print(Right(["1", "2", "3"]).bind(convert_to(float)).bind(average))
print(Right(["x", "2", "3"]).bind(convert_to(float)).bind(average))
print(Right([]).bind(convert_to(float)).bind(average))
