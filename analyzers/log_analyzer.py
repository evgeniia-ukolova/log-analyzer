from collections import Counter
from collections.abc import Iterable, Iterator
from datetime import date

from models.log_entry import HTTPMethod, LogEntry, LogLevel
from models.log_report import LogReport


def count_requests(entries: Iterable[LogEntry]) -> int:
    return sum(1 for _ in entries)


def count_status_codes(
    entries: Iterable[LogEntry],
) -> dict[int, int]:
    return dict(Counter(entry.status_code for entry in entries))


def count_errors(entries: Iterable[LogEntry]) -> int:
    return sum(
        1
        for entry in entries
        if entry.status_code >= 400
    )


def average_response_time(entries: Iterable[LogEntry]) -> float:
    total_time = 0
    count = 0

    for entry in entries:
        total_time += entry.response_time
        count += 1

    if count == 0:
        return 0.0

    return total_time / count


def count_endpoints(
    entries: Iterable[LogEntry],
) -> dict[str, int]:
    return dict(Counter(entry.endpoint for entry in entries))


def top_endpoints(
    entries: Iterable[LogEntry],
) -> list[tuple[str, int]]:
    endpoint_counts = count_endpoints(entries)

    return sorted(
        endpoint_counts.items(),
        key=lambda item: item[1],
        reverse=True,
    )


def slowest_requests(
    entries: Iterable[LogEntry],
) -> list[LogEntry]:
    return sorted(
        entries,
        key=lambda entry: entry.response_time,
        reverse=True,
    )


def filter_by_level(
    entries: Iterable[LogEntry],
    level: LogLevel,
) -> Iterator[LogEntry]:
    for entry in entries:
        if entry.level == level:
            yield entry


def filter_by_status(
    entries: Iterable[LogEntry],
    status_code: int,
) -> Iterator[LogEntry]:
    for entry in entries:
        if entry.status_code == status_code:
            yield entry


def filter_by_method(
    entries: Iterable[LogEntry],
    method: HTTPMethod,
) -> Iterator[LogEntry]:
    for entry in entries:
        if entry.method == method:
            yield entry


def filter_by_endpoint(
    entries: Iterable[LogEntry],
    endpoint: str,
) -> Iterator[LogEntry]:
    for entry in entries:
        if entry.endpoint == endpoint:
            yield entry


def filter_by_response_time(
    entries: Iterable[LogEntry],
    min_response_time: int,
) -> Iterator[LogEntry]:
    for entry in entries:
        if entry.response_time >= min_response_time:
            yield entry


def filter_by_date(
    entries: Iterable[LogEntry],
    target_date: date,
) -> Iterator[LogEntry]:
    for entry in entries:
        if entry.timestamp.date() == target_date:
            yield entry


def build_report(entries: Iterable[LogEntry]) -> LogReport:
    total_requests = 0
    error_count = 0
    total_response_time = 0

    status_counts: Counter[int] = Counter()
    endpoint_counts: Counter[str] = Counter()
    slowest_request: LogEntry | None = None

    for entry in entries:
        total_requests += 1
        total_response_time += entry.response_time

        if entry.status_code >= 400:
            error_count += 1

        status_counts[entry.status_code] += 1
        endpoint_counts[entry.endpoint] += 1

        if (
            slowest_request is None
            or entry.response_time > slowest_request.response_time
        ):
            slowest_request = entry

    if total_requests == 0:
        average_response_time = 0.0
    else:
        average_response_time = total_response_time / total_requests

    return LogReport(
        total_requests=total_requests,
        error_count=error_count,
        average_response_time=average_response_time,
        status_counts=dict(status_counts),
        endpoint_counts=dict(endpoint_counts),
        slowest_request=slowest_request,
    )