from datetime import date

import pytest

from analyzers.log_analyzer import (
    average_response_time,
    build_report,
    count_endpoints,
    count_errors,
    count_requests,
    count_status_codes,
    filter_by_date,
    filter_by_endpoint,
    filter_by_level,
    filter_by_method,
    filter_by_response_time,
    filter_by_status,
    slowest_requests,
    top_endpoints,
)
from models.log_entry import HTTPMethod, LogLevel
from readers.log_reader import read_log_entries


@pytest.fixture
def log_file(tmp_path):
    file_path = tmp_path / "server.log"

    file_path.write_text(
        "2026-09-24 10:15:01 INFO GET /api/users 200 120ms\n"
        "2026-09-24 10:15:02 ERROR POST /api/login 500 340ms\n"
        "2026-09-24 10:15:03 INFO GET /api/products 200 95ms\n"
        "2026-09-24 10:15:04 WARNING GET /api/users/15 404 180ms\n"
        "2026-09-24 10:15:05 INFO DELETE /api/users/15 204 210ms\n",
        encoding="utf-8",
    )

    return file_path


def test_count_requests(log_file):
    entries = read_log_entries(log_file)

    result = count_requests(entries)

    assert result == 5


def test_count_requests_empty():
    result = count_requests([])

    assert result == 0


def test_count_status_codes(log_file):
    entries = read_log_entries(log_file)

    result = count_status_codes(entries)

    assert result == {
        200: 2,
        500: 1,
        404: 1,
        204: 1,
    }


def test_count_status_codes_empty():
    result = count_status_codes([])

    assert result == {}


def test_count_errors(log_file):
    entries = read_log_entries(log_file)

    result = count_errors(entries)

    assert result == 2


def test_average_response_time(log_file):
    entries = read_log_entries(log_file)

    result = average_response_time(entries)

    assert result == 189.0


def test_average_response_time_empty():
    result = average_response_time([])

    assert result == 0.0


def test_count_endpoints(log_file):
    entries = read_log_entries(log_file)

    result = count_endpoints(entries)

    assert result == {
        "/api/users": 1,
        "/api/login": 1,
        "/api/products": 1,
        "/api/users/15": 2,
    }


def test_count_endpoints_empty():
    result = count_endpoints([])

    assert result == {}


def test_top_endpoints(log_file):
    entries = read_log_entries(log_file)

    result = top_endpoints(entries)

    assert result == [
        ("/api/users/15", 2),
        ("/api/users", 1),
        ("/api/login", 1),
        ("/api/products", 1),
    ]


def test_top_endpoints_empty():
    result = top_endpoints([])

    assert result == []


def test_slowest_requests(log_file):
    entries = read_log_entries(log_file)

    result = slowest_requests(entries)

    assert [entry.response_time for entry in result] == [
        340,
        210,
        180,
        120,
        95,
    ]


def test_slowest_requests_empty():
    result = slowest_requests([])

    assert result == []


def test_filter_by_level(log_file):
    entries = read_log_entries(log_file)

    result = list(filter_by_level(entries, LogLevel.ERROR))

    assert len(result) == 1
    assert result[0].level == LogLevel.ERROR


def test_filter_by_status(log_file):
    entries = read_log_entries(log_file)

    result = list(filter_by_status(entries, 500))

    assert len(result) == 1
    assert result[0].status_code == 500


def test_filter_by_method(log_file):
    entries = read_log_entries(log_file)

    result = list(filter_by_method(entries, HTTPMethod.DELETE))

    assert len(result) == 1
    assert result[0].method == HTTPMethod.DELETE


def test_filter_by_endpoint(log_file):
    entries = read_log_entries(log_file)

    result = list(filter_by_endpoint(entries, "/api/users/15"))

    assert len(result) == 2
    assert all(
        entry.endpoint == "/api/users/15"
        for entry in result
    )


def test_filter_by_response_time(log_file):
    entries = read_log_entries(log_file)

    result = list(filter_by_response_time(entries, 200))

    assert len(result) == 2
    assert all(
        entry.response_time >= 200
        for entry in result
    )


def test_filter_by_date(log_file):
    entries = read_log_entries(log_file)
    target_date = date(2026, 9, 24)

    result = list(filter_by_date(entries, target_date))

    assert len(result) == 5
    assert all(
        entry.timestamp.date() == target_date
        for entry in result
    )


def test_build_report(log_file):
    entries = read_log_entries(log_file)

    report = build_report(entries)

    assert report.total_requests == 5
    assert report.error_count == 2
    assert report.average_response_time == 189.0

    assert report.status_counts == {
        200: 2,
        500: 1,
        404: 1,
        204: 1,
    }

    assert report.endpoint_counts == {
        "/api/users": 1,
        "/api/login": 1,
        "/api/products": 1,
        "/api/users/15": 2,
    }

    assert report.slowest_request is not None
    assert report.slowest_request.response_time == 340
    assert report.slowest_request.endpoint == "/api/login"
    