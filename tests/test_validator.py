"""Tests for the row validator."""

import pytest

from resilient_data_importer_cli.exceptions import InvalidTypeError
from resilient_data_importer_cli.validator import parse_user_id, validate_row


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("7", 7), (" 7 ", 7), ("", None), (None, None)],
)
def test_parse_user_id_valid(raw: str | None, expected: int | None) -> None:
    """Valid and empty ids convert as expected."""
    assert parse_user_id(raw) == expected


@pytest.mark.parametrize("raw", ["abc", "7.5", "0", "-3"])
def test_parse_user_id_invalid(raw: str) -> None:
    """Bad ids raise InvalidTypeError."""
    with pytest.raises(InvalidTypeError):
        parse_user_id(raw)


def test_validate_row_builds_user() -> None:
    """A full row becomes a User, with unknown columns in extra."""
    row = {"user_id": "1", "name": "Aline", "email": "a@x.com", "city": "Kigali"}
    user = validate_row(row)
    assert user.user_id == 1
    assert user.name == "Aline"
    assert user.email == "a@x.com"
    assert user.extra == {"city": "Kigali"}


def test_validate_row_without_id() -> None:
    """A row with no user_id column gets user_id None."""
    row = {"name": "Aline", "email": "a@x.com", "city": "Kigali"}
    assert validate_row(row).user_id is None
