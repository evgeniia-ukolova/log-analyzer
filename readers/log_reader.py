# берем строки из файла

from pathlib import Path

from parsers.log_parser import parse_log_line



def read_log_file(file_path: Path):
    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            yield line


def read_log_entries(file_path: Path):

    lines = read_log_file(file_path) 

    for line in lines:
        yield parse_log_line(line)










































