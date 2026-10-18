"""Tests for the CSV reader."""

from collections.abc import Callable

import pytest
from pytest_mock import MockerFixture

from resilient_data_importer_cli.exceptions import (
    FileFormatError,
    FileReadError,
    InputFileNotFoundError,
    MissingColumnsError,
)
from resilient_data_importer_cli.reader import read_rows

GOOD = "user_id,name,email\n1,Aline,a@x.com\n2,Eric,e@x.com\n"
MESSY_HEADER = " Name , EMAIL \nAline,a@x.com\n"
NO_EMAIL = "user_id,name\n1,Aline\n"


def test_reads_rows(make_csv: Callable[[str], str]) -> None:
    """Each data row comes back with its file line number."""
    rows = list(read_rows(make_csv(GOOD)))
    assert rows[0] == (2, {"user_id": "1", "name": "Aline", "email": "a@x.com"})
    assert len(rows) == 2


def test_header_is_normalised(make_csv: Callable[[str], str]) -> None:
    """Header names are stripped and lowercased."""
    rows = list(read_rows(make_csv(MESSY_HEADER)))
    assert rows[0][1] == {"name": "Aline", "email": "a@x.com"}


def test_missing_file() -> None:
    """A path that does not exist raises InputFileNotFoundError."""
    with pytest.raises(InputFileNotFoundError):
        list(read_rows("nope.csv"))


def test_empty_file(make_csv: Callable[[str], str]) -> None:
    """An empty file raises FileFormatError."""
    path = make_csv("")
    with pytest.raises(FileFormatError):
        list(read_rows(path))


def test_missing_columns(make_csv: Callable[[str], str]) -> None:
    """A header without email raises MissingColumnsError."""
    path = make_csv(NO_EMAIL)
    with pytest.raises(MissingColumnsError):
        list(read_rows(path))


def test_unreadable_file(make_csv: Callable[[str], str], mocker: MockerFixture) -> None:
    """A failure to open the file raises FileReadError."""
    mocker.patch(
        "resilient_data_importer_cli.reader.open",
        side_effect=PermissionError("denied"),
        create=True,
    )
    path = make_csv(GOOD)
    with pytest.raises(FileReadError):
        list(read_rows(path))
