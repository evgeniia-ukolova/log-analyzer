from datetime import datetime

from models.log_entry import LogLevel, HTTPMethod, LogEntry



def parse_log_line(log_line: str) -> LogEntry:                  # превращает одну строку лога в объект LogEntry
    parts = log_line.split()
    date_str, time_str, level_str, method, endpoint, status_code_str, response_time_str = parts

    timestamp = f"{date_str} {time_str}"
    timestamp = datetime.fromisoformat(timestamp)

    level = LogLevel(level_str)

    method = HTTPMethod(method)

    status_code = int(status_code_str)

    response_time = int(response_time_str.removesuffix("ms"))

    log_entry = LogEntry(
        timestamp=timestamp,
        level=level,
        method=method,
        endpoint=endpoint,
        status_code=status_code,
        response_time=response_time,
    )
    return log_entry


