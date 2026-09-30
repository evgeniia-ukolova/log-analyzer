import pytest
from pathlib import Path

from readers.log_reader import read_log_file, read_log_entries
from models.log_entry import LogEntry



def test_read_log_file():
    file_path = Path("data/server.log")

    lines = list(read_log_file(file_path))

    assert len(lines) == 5


def test_read_log_file_skips_empty_lines(tmp_path):
    file_path = tmp_path/"test.log"

    file_path.write_text(
    "2026-09-24 10:15:01 INFO GET /api/users 200 120ms\n"
    "\n"
    "2026-09-24 10:15:02 ERROR POST /api/login 500 340ms\n",
    encoding="utf-8",
    )

    lines = list(read_log_file(file_path))

    assert len(lines) == 2


def test_read_log_file_not_found(tmp_path):
    file_path = tmp_path / "missing.log"

    with pytest.raises(FileNotFoundError):
        list(read_log_file(file_path))


def test_read_empty_log_file(tmp_path):
    file_path = tmp_path / "test.log"

    file_path.touch()
    lines = list(read_log_file(file_path))

    assert len(lines) == 0

    
def test_read_log_entries():
    file_path = Path("data/server.log")
    entries = list(read_log_entries(file_path))

    assert len(entries) == 5
    assert isinstance(entries[0], LogEntry)






























