"""Tests for the JSON repository."""

import json
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from resilient_data_importer_cli.exceptions import StorageError
from resilient_data_importer_cli.models import User
from resilient_data_importer_cli.storage import JsonUserRepository


def test_add_and_all(tmp_path: Path) -> None:
    """Added users come back from all()."""
    repo = JsonUserRepository(str(tmp_path / "out.json"))
    user = User(name="Aline", email="a@x.com", user_id=1)
    repo.add(user)
    assert repo.all() == [user]


def test_save_writes_json(tmp_path: Path) -> None:
    """save() writes every user to the file as JSON."""
    path = tmp_path / "out.json"
    repo = JsonUserRepository(str(path))
    user = User(name="Aline", email="a@x.com", user_id=1)
    repo.add(user)
    repo.save()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data == [{"name": "Aline", "email": "a@x.com", "user_id": 1, "extra": {}}]


def test_save_failure_raises_storage_error(
    tmp_path: Path, mocker: MockerFixture
) -> None:
    """A failed write raises StorageError."""
    mocker.patch(
        "resilient_data_importer_cli.storage.open",
        side_effect=OSError("disk full"),
        create=True,
    )
    path = tmp_path / "out.json"
    repo = JsonUserRepository(str(path))
    with pytest.raises(StorageError):
        repo.save()
