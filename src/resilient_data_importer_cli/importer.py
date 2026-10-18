"""Run the import: validate rows, skip bad ones, store the rest."""

import logging
from collections.abc import Iterable

from resilient_data_importer_cli.exceptions import (
    DuplicateUserError,
    RowValidationError,
)
from resilient_data_importer_cli.models import User
from resilient_data_importer_cli.storage import UserRepository
from resilient_data_importer_cli.validator import validate_row

logger = logging.getLogger(__name__)


def check_duplicate(user: User, existing: list[User]) -> None:
    """Raise if the user is already in the list.

    Two users are duplicates when they share a user_id. When there is no
    user_id, they are duplicates if every field matches.

    Args:
        user: The user about to be added.
        existing: The users already stored.

    Raises:
        DuplicateUserError: If the user is a duplicate.
    """
    if user.user_id is not None:
        value = any(user.user_id == each.user_id for each in existing)
    else:
        value = any(user == each for each in existing)
    if value:
        raise DuplicateUserError("This user is already in the data")


def import_users(
    rows: Iterable[tuple[int, dict[str, str]]], repo: UserRepository
) -> int:
    """Validate each row and store the valid, non-duplicate users.

    Bad and duplicate rows are skipped and logged as warnings. The repository
    is saved at the end.

    Args:
        rows: Pairs of (line number, row dict), such as read_rows yields.
        repo: Where the users are stored.

    Returns:
        The number of users imported.

    Raises:
        StorageError: If the repository cannot be saved.
    """
    count = 0
    for line_no, row in rows:
        try:
            user = validate_row(row)
            check_duplicate(user, repo.all())
        except RowValidationError as err:
            logger.warning("line %d skipped: %s", line_no, err)
            continue
        repo.add(user)
        count += 1
        logger.info("Row successfully saved")

    repo.save()
    return count
