"""Tests for the entry point."""

import logging
from pathlib import Path

import pytest

from resilient_data_importer_cli import main


def test_main_exits_with_run_status(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """main() sets up logging and exits with the CLI's status code."""
    root = logging.getLogger()
    saved_handlers = root.handlers[:]
    saved_level = root.level
    monkeypatch.setattr(main, "LOG_FILE", str(tmp_path / "importer.log"))
    monkeypatch.setattr(main, "run", lambda: 0)
    try:
        with pytest.raises(SystemExit) as exc_info:
            main.main()
        assert exc_info.value.code == 0
    finally:
        for handler in root.handlers[:]:
            if handler not in saved_handlers:
                handler.close()
                root.removeHandler(handler)
        root.setLevel(saved_level)
