"""Shared fixtures for the test suite."""

from collections.abc import Callable
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from resilient_data_importer_cli.storage import UserRepository


@pytest.fixture
def make_csv(tmp_path: Path) -> Callable[[str], str]:
    """Return a function that writes text to a temporary CSV file.

    Args:
        tmp_path: pytest's temporary folder.

    Returns:
        A function taking the file text and returning the file's path.
    """

    def _make(text: str) -> str:
        path = tmp_path / "users.csv"
        path.write_text(text, encoding="utf-8")
        return str(path)

    return _make


@pytest.fixture
def mock_repo(mocker: MockerFixture) -> UserRepository:
    """Return a fake UserRepository that starts empty.

    Args:
        mocker: The pytest-mock fixture.

    Returns:
        A mock that only allows add, all and save, and whose all() is empty.
    """
    repo = mocker.create_autospec(UserRepository, instance=True)
    repo.all.return_value = []
    return repo
