from pathlib import Path

from readers.log_reader import read_log_entries
from analyzers.log_analyzer import count_requests, count_status_codes, count_errors, average_response_time, count_endpoints, top_endpoints, slowest_requests


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
















