"""Tests for the command-line interface."""

import pytest

from resilient_data_importer_cli import cli


def test_run_success(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path
) -> None:
    """A good CSV imports and run() returns 0."""
    csv_path = tmp_path / "users.csv"
    csv_path.write_text("user_id,name,email\n1,Aline,a@x.com\n", encoding="utf-8")
    monkeypatch.setattr("builtins.input", lambda _: str(csv_path))
    monkeypatch.setattr(cli, "OUTPUT_PATH", str(tmp_path / "out" / "users.json"))
    assert cli.run() == 0
    assert "Goodbye!" in capsys.readouterr().out


def test_run_missing_file(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path
) -> None:
    """A missing file prints the error and run() returns 1."""
    monkeypatch.setattr("builtins.input", lambda _: "nope.csv")
    monkeypatch.setattr(cli, "OUTPUT_PATH", str(tmp_path / "out" / "users.json"))
    assert cli.run() == 1
    assert "Goodbye!" in capsys.readouterr().out
