"""Data model for imported users."""

from dataclasses import dataclass, field


@dataclass
class User:
    """A user record imported from one CSV row.

    Attributes:
        name: The user's name.
        email: The user's email address.
        user_id: The numeric id, or None when the row has no id.
        extra: Any other CSV columns, stored as strings.
    """

    name: str
    email: str
    user_id: int | None = None
    extra: dict[str, str] = field(default_factory=dict)
