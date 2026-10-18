"""Store users in a JSON file."""

import json
from abc import ABC, abstractmethod
from dataclasses import asdict

from resilient_data_importer_cli.exceptions import StorageError
from resilient_data_importer_cli.models import User


class UserRepository(ABC):
    """Interface for anything that can store users."""

    @abstractmethod
    def add(self, user: User) -> None:
        """Add a user.

        Args:
            user: The user to store.
        """

    @abstractmethod
    def all(self) -> list[User]:
        """Return every user added so far."""

    @abstractmethod
    def save(self) -> None:
        """Write the users to permanent storage."""


class JsonUserRepository(UserRepository):
    """Keeps users in memory and writes them to a JSON file."""

    def __init__(self, path: str) -> None:
        """Create the repository.

        Args:
            path: Where the JSON file will be written.
        """
        self.users: list[User] = []
        self.path = path

    def add(self, user: User) -> None:
        """Add a user to the in-memory list.

        Args:
            user: The user to store.
        """
        self.users.append(user)

    def all(self) -> list[User]:
        """Return every user added so far."""
        return self.users

    def save(self) -> None:
        """Write all users to the JSON file, replacing its contents.

        Raises:
            StorageError: If the file cannot be written.
        """
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump([asdict(user) for user in self.users], f, indent=2)
        except OSError as err:
            raise StorageError("Can't save the json file.") from err
