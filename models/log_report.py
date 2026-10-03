from dataclasses import dataclass

from models.log_entry import LogEntry


@dataclass
class LogReport:
    total_requests: int
    error_count: int
    average_response_time: float
    status_counts: dict[int, int]
    endpoint_counts: dict[str, int]
    slowest_request: LogEntry | None
