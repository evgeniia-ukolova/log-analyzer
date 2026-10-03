from datetime import datetime

from models.log_entry import HTTPMethod, LogEntry, LogLevel


def parse_log_line(log_line: str) -> LogEntry:
    parts = log_line.split()

    if len(parts) != 7:
        raise ValueError("Некорректный формат строки лога")

    (
        date_str,
        time_str,
        level_str,
        method_str,
        endpoint,
        status_code_str,
        response_time_str,
    ) = parts

    timestamp = datetime.fromisoformat(f"{date_str} {time_str}")
    level = LogLevel(level_str)
    method = HTTPMethod(method_str)
    status_code = int(status_code_str)
    response_time = int(response_time_str.removesuffix("ms"))

    return LogEntry(
        timestamp=timestamp,
        level=level,
        method=method,
        endpoint=endpoint,
        status_code=status_code,
        response_time=response_time,
    )
