# итоговый отчёт

from dataclasses import dataclass


@dataclass
class LogReport:
    total_requests: int
    error_count: int
    average_response_time: float
    status_counts: dict[int, int]
    endpoint_counts: dict[str, int]


    








































