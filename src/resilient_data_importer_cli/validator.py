"""Validate CSV rows and build User objects."""

from resilient_data_importer_cli.exceptions import InvalidTypeError
from resilient_data_importer_cli.models import User


def parse_user_id(user_id: str | None) -> int | None:
    """Convert a raw user_id value to an int.

    Args:
        user_id: The text from the CSV cell, or None if the column is absent.

    Returns:
        The id as a positive int, or None when the cell is empty or absent.

    Raises:
        InvalidTypeError: If the value is not a positive whole number.
    """
    if user_id is None or user_id == "":
        return None
    try:
        user_id = user_id.strip().replace(" ", "")
        value = int(user_id)
        if value <= 0:
            return None
    except ValueError:
        raise InvalidTypeError("The user id is not a number.")

    return value


def validate_row(row: dict[str, str]) -> User:
    """Build a User from one CSV row.

    Args:
        row: The row as a dict of strings, with lowercase column names.

    Returns:
        A User with unrecognised columns stored in extra.

    Raises:
        InvalidTypeError: If user_id is not a positive whole number, or if
            name or email is missing from the row.
    """
    user_id = parse_user_id(str(row["user_id"]))
    name = row["name"]
    email = row["email"]
    if name is None or email is None:
        raise InvalidTypeError("Name and email should not be None")
    extra = {}
    for each in row.items():
        if each[0] != "name" and each[0] != "email" and each[0] != "user_id":
            extra[each[0]] = each[1]

    return User(name=name, email=email, user_id=user_id, extra=extra)
