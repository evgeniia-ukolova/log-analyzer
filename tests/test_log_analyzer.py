from pathlib import Path
from datetime import date

from readers.log_reader import read_log_entries
from analyzers.log_analyzer import (
    count_requests, 
    count_status_codes, 
    count_errors, 
    average_response_time, 
    count_endpoints, 
    top_endpoints, 
    slowest_requests, 
    filter_by_level, 
    filter_by_status, 
    filter_by_method, 
    filter_by_endpoint, 
    filter_by_response_time,
    filter_by_date,
    build_report
    )
from models.log_entry import LogLevel, HTTPMethod



def test_count_requests():
    entries = read_log_entries(Path("data/server.log"))

    result = count_requests(entries)

    assert result == 5

    
def test_count_requests_empty():
    result = count_requests([])

    assert result == 0    


def test_count_status_codes():
    entries = read_log_entries(Path("data/server.log"))

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


def test_count_errors():
    entries = read_log_entries(Path("data/server.log"))

    result = count_errors(entries)

    assert result == 2


def test_average_response_time():
    entries = read_log_entries(Path("data/server.log"))

    result = average_response_time(entries)

    assert result == 189


def test_average_response_time_empty():
    result = average_response_time([])

    assert result == 0    


def test_count_endpoints():
    entries = read_log_entries(Path("data/server.log"))

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


def test_top_endpoints():
    entries = read_log_entries(Path("data/server.log"))

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


def test_slowest_requests():
    entries = read_log_entries(Path("data/server.log"))

    result = slowest_requests(entries)

    assert [entry.response_time for entry in result] == [340, 210, 180, 120, 95]


def test_slowest_requests_empty():
    result = slowest_requests([])

    assert result == []


def test_filter_by_level():
    entries = read_log_entries(Path("data/server.log"))

    result = list(filter_by_level(entries, LogLevel.ERROR))

    assert len(result) == 1
    assert result[0].level == LogLevel.ERROR


def test_filter_by_status():
    entries = read_log_entries(Path("data/server.log"))

    result = list(filter_by_status(entries, 500))

    assert len(result) == 1
    assert result[0].status_code == 500


def test_filter_by_method():
    entries = read_log_entries(Path("data/server.log"))

    result = list(filter_by_method(entries, HTTPMethod.DELETE))

    assert len(result) == 1
    assert result[0].method == HTTPMethod.DELETE
  

def test_filter_by_endpoint():
    entries = read_log_entries(Path("data/server.log"))

    result = list(filter_by_endpoint(entries, "/api/users/15"))

    assert len(result) == 2
    assert all(entry.endpoint == "/api/users/15" for entry in result) 


def test_filter_by_response_time():
    entries = read_log_entries(Path("data/server.log"))

    result = list(filter_by_response_time(entries, 200))

    assert len(result) == 2
    assert all(entry.response_time >= 200 for entry in result)


def test_filter_by_date():
    entries = read_log_entries(Path("data/server.log"))

    result = list(filter_by_date(entries, date(2026, 9, 24)))

    assert len(result) == 5
    assert all(entry.timestamp.date() == date(2026, 9, 24) for entry in result)


def test_build_report():
    entries = read_log_entries(Path("data/server.log"))

    report = build_report(entries)

    assert report.total_requests == 5
    assert report.error_count == 2
    assert report.average_response_time == 189
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















































