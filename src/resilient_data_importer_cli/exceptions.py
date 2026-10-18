"""Custom exceptions for the resilient data importer."""


class ImporterError(Exception):
    """Base class for every error raised by the importer."""


class FileReadError(ImporterError):
    """Raised when the input file cannot be read. Stops the import."""


class InputFileNotFoundError(FileReadError):
    """Raised when the CSV path does not exist."""


class FileFormatError(FileReadError):
    """Raised when the file cannot be read as a valid CSV."""


class MissingColumnsError(FileFormatError):
    """Raised when a required column (name or email) is missing from the header."""


class StorageError(ImporterError):
    """Raised when the JSON storage file cannot be read or written."""


class RowValidationError(ImporterError):
    """Base class for row-level problems. The row is skipped and reported."""


class InvalidTypeError(RowValidationError):
    """Raised when a value cannot be converted, e.g. a user_id of 7.5."""


class DuplicateUserError(RowValidationError):
    """Raised when a row repeats an existing user_id, or an identical row."""
