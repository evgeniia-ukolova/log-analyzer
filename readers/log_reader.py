from collections.abc import Iterator
from pathlib import Path

from models.log_entry import LogEntry
from parsers.log_parser import parse_log_line


def read_log_file(file_path: Path) -> Iterator[str]:
    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            yield line


def read_log_entries(file_path: Path) -> Iterator[LogEntry]:
    for line in read_log_file(file_path):
        yield parse_log_line(line)