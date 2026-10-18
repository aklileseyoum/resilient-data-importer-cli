"""Entry point: set up logging and start the CLI."""

import logging
import sys

from resilient_data_importer_cli.cli import run

LOG_FILE = "importer.log"


def configure_logging() -> None:
    """Send every message to a log file and warnings to the console."""
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

    root.addHandler(file_handler)
    root.addHandler(console_handler)


def main() -> None:
    """Configure logging, run the CLI, and exit with its status code."""
    configure_logging()
    sys.exit(run())


if __name__ == "__main__":
    main()
