from pathlib import Path
from collections.abc import Iterator

from parsers.log_parser import parse_log_line
from models.log_entry import LogEntry



def read_log_file(file_path: Path) -> Iterator[str]:    
    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            yield line


def read_log_entries(file_path: Path) -> Iterator[LogEntry]:
    lines = read_log_file(file_path) 

    for line in lines:
        yield parse_log_line(line)










































