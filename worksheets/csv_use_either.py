import csv
import os

from typing import Callable
from pymonad.either import Either, Left, Right

type PredicateFn[T] = Callable[[T], bool]
type MapperFn[T, R] = Callable[[T], R]
type ErrorMessage = str


def is_list_more_than[T](n: int):
    def for_list(xs: list[T]) -> bool:
        return len(xs) > n

    return for_list


def is_remaining[T](xs: list[T]) -> bool:
    return is_list_more_than(0)(xs)


def read_csv_file(file_path: str) -> Either[ErrorMessage, list[list[str]]]:
    if os.path.isfile(file_path):
        with open(file_path, "r") as csv_file:
            return Right([row for row in csv.reader(csv_file)])

    return Left("Error: File not found")


def remove_n_first_rows(n: int):
    def for_rows(rows: list[list[str]]) -> Either[ErrorMessage, list[list[str]]]:
        return (
            Right(rows[n:])
            if is_remaining(rows)
            else Left("Error: Unable to remove row")
        )

    return for_rows


def extract_column(column_index: int):
    def for_rows(rows: list[list[str]]) -> Either[ErrorMessage, list[str]]:
        return (
            Right([cols[column_index] for cols in rows])
            if is_list_more_than(column_index)(rows)
            else Left(f"Error::[{extract_column.__name__}]: Unable to extract column")
        )

    return for_rows


def is_digit(text: str) -> bool:
    return text.isdigit()


def convert_to[T, R](converter: MapperFn[T, R]):
    def for_validation_fn(predicate: PredicateFn[T]):
        def for_xs(xs: list[T]) -> Either[ErrorMessage, R]:
            converted_column = [converter(x) if predicate(x) else None for x in xs]

            return (
                Right(converted_column)
                if all(x is not None for x in converted_column)
                else Left(f"Error::[{convert_to.__name__}]: Unable to convert to float")
            )

        return for_xs

    return for_validation_fn


def average(numbers: list[float]) -> Either[ErrorMessage, float]:
    has_some_numbers = is_remaining

    return (
        Right(sum(numbers) / len(numbers))
        if has_some_numbers(numbers)
        else Left(f"Error::[{average.__name__}]: Division by zero")
    )


print(Right(["1", "2", "3"]).bind(convert_to(float)(is_digit)).bind(average))
print(Right(["x", "2", "3"]).bind(convert_to(float)(is_digit)).bind(average))
print(Right([]).bind(convert_to(float)(is_digit)).bind(average))

SCORE_COL_IDX = 1

extract_score_column = extract_column(SCORE_COL_IDX)
remove_header_row = remove_n_first_rows(1)

# FIXME: Wait for https://github.com/jasondelaat/pymonad/issues/34 is fixed, then update PyMonad version
avg_score = (
    read_csv_file("src/mocks/example.csv")
    .bind(remove_header_row)
    .bind(extract_score_column)
    .bind(convert_to(float)(is_digit))
    .bind(average)
)

if avg_score.is_right():
    print(f"The average result is {avg_score.value}")
else:
    print(f"Error: processing data: {avg_score}")
