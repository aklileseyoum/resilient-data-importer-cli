"""Read user rows from a CSV file."""

import csv
from collections.abc import Iterator
from contextlib import contextmanager
from typing import TextIO

from resilient_data_importer_cli.exceptions import (
    FileFormatError,
    FileReadError,
    InputFileNotFoundError,
    MissingColumnsError,
)


@contextmanager
def open_csv(path: str) -> Iterator[TextIO]:
    """Open a CSV file for reading.

    Args:
        path: Path to the CSV file.

    Yields:
        The open text file.

    Raises:
        InputFileNotFoundError: If the path does not exist.
        FileReadError: If the file cannot be opened.
    """
    try:
        # The file is closed by "with f" below; open() sits in try so yield stays outside.
        f = open(path, newline="", encoding="utf-8")  # noqa: SIM115
    except FileNotFoundError as err:
        raise InputFileNotFoundError(f"{path} cannot be found.") from err
    except OSError:
        raise FileReadError("File cannot be read.")
    with f:
        yield f


def read_rows(path: str) -> Iterator[tuple[int, dict[str, str]]]:
    """Yield each data row of a CSV file with its line number.

    Header names are stripped and lowercased.

    Args:
        path: Path to the CSV file.

    Yields:
        A tuple of the file line number and the row as a dict of strings.

    Raises:
        InputFileNotFoundError: If the path does not exist.
        FileReadError: If the file cannot be opened.
        FileFormatError: If the file is empty.
        MissingColumnsError: If a required column is missing from the header.
    """
    with open_csv(path) as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise FileFormatError("empty file")
        reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]
        if "name" not in reader.fieldnames or "email" not in reader.fieldnames:
            raise MissingColumnsError("We need both name and email")
        for row in reader:
            yield reader.line_num, row
