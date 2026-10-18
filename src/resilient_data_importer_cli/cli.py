"""Command-line interface for the importer."""

from datetime import datetime
from pathlib import Path

from resilient_data_importer_cli.exceptions import ImporterError
from resilient_data_importer_cli.importer import import_users
from resilient_data_importer_cli.reader import read_rows
from resilient_data_importer_cli.storage import JsonUserRepository

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_PATH = f"output/users_{stamp}.json"


def run() -> int:
    """Ask for a CSV path, import it, and report the result.

    Returns:
        0 if the import succeeded, 1 if it failed.
    """
    print("=" * 30)
    print("Welcome User")
    print("=" * 30)
    path = input("Enter the path to your csv file: ")
    try:
        Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
        repo = JsonUserRepository(OUTPUT_PATH)
        count = import_users(read_rows(path), repo)

    except ImporterError as err:
        print("Error:", err)
        return 1
    else:
        print(f"Imported {count} users.")
        print(f"Saved to {OUTPUT_PATH}")
        return 0
    finally:
        print("Goodbye!")
