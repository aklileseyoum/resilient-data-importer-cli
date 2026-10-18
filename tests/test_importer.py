"""Tests for the importer."""

import pytest

from resilient_data_importer_cli.exceptions import DuplicateUserError
from resilient_data_importer_cli.importer import check_duplicate, import_users
from resilient_data_importer_cli.models import User
from resilient_data_importer_cli.storage import UserRepository

GOOD_ROWS = [
    (2, {"user_id": "1", "name": "Aline", "email": "a@x.com"}),
    (3, {"user_id": "2", "name": "Eric", "email": "e@x.com"}),
]


def test_imports_valid_rows(mock_repo: UserRepository) -> None:
    """Valid rows are added and the repository is saved once."""
    count = import_users(GOOD_ROWS, mock_repo)
    assert count == 2
    assert mock_repo.add.call_count == 2
    mock_repo.save.assert_called_once()


def test_skips_bad_id(
    mock_repo: UserRepository, caplog: pytest.LogCaptureFixture
) -> None:
    """A row with a bad id is skipped and a warning is logged."""
    rows = [(2, {"user_id": "abc", "name": "Aline", "email": "a@x.com"})]
    count = import_users(rows, mock_repo)
    assert count == 0
    mock_repo.add.assert_not_called()
    assert "skipped" in caplog.text


def test_skips_duplicate(mock_repo: UserRepository) -> None:
    """A row whose id is already stored is skipped."""
    mock_repo.all.return_value = [User(name="Aline", email="a@x.com", user_id=1)]
    count = import_users(GOOD_ROWS[:1], mock_repo)
    assert count == 0
    mock_repo.add.assert_not_called()


def test_check_duplicate_by_id() -> None:
    """Users with the same id are duplicates."""
    existing = [User(name="A", email="a@x.com", user_id=1)]
    new = User(name="B", email="b@x.com", user_id=1)
    with pytest.raises(DuplicateUserError):
        check_duplicate(new, existing)


def test_check_duplicate_without_id() -> None:
    """Without an id, only a fully identical user is a duplicate."""
    existing = [User(name="A", email="a@x.com")]
    different = User(name="A", email="other@x.com")
    check_duplicate(different, existing)
    with pytest.raises(DuplicateUserError):
        check_duplicate(User(name="A", email="a@x.com"), existing)
