import csv
import os

from pymonad.either import Left, Right

def read_csv_file(file_path: str):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as csv_file:
            return Right(row for row in csv.reader(csv_file))

    return Left("Error: File not found")


def remove_row(row_index: int):
    def for_rows(rows: list[list[str]]):
        if (len(rows) > 0):
            return Right(rows[row_index:])

        return Left("Error: Unable to remove row")

    return for_rows


def extract_column(column_index: int):
    def for_rows(rows: list[list[str]]):
        if len(rows) > column_index:
            return Right(rows[column_index] for row in rows)

        return("Error: Unable to extract column")

    return for_rows
