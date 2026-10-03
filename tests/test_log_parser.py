from datetime import datetime

import pytest

from models.log_entry import HTTPMethod, LogLevel
from parsers.log_parser import parse_log_line


def test_parse_log_line():
    log_line = "2026-09-24 10:15:02 ERROR POST /api/login 500 340ms"
    
    result = parse_log_line(log_line)

    assert result.timestamp == datetime.fromisoformat("2026-09-24 10:15:02")
    assert result.level == LogLevel.ERROR
    assert result.method == HTTPMethod.POST
    assert result.endpoint == "/api/login"
    assert result.status_code == 500
    assert result.response_time == 340


def test_parse_invalid_log_line():
    log_line = "2026-09-24 ERROR POST"

    with pytest.raises(ValueError):
        parse_log_line(log_line)


def test_invalid_timestamp():
    log_line = "2026-99-99 10:15:02 ERROR POST /api/login 500 340ms"

    with pytest.raises(ValueError):
        parse_log_line(log_line)


def test_invalid_log_level():
    log_line = "2026-09-24 10:15:02 UNKNOWN POST /api/login 500 340ms"

    with pytest.raises(ValueError):
        parse_log_line(log_line)


def test_invalid_http_method():
    log_line = "2026-09-24 10:15:02 ERROR FETCH /api/login 500 340ms"

    with pytest.raises(ValueError):
        parse_log_line(log_line)


def test_invalid_status_code():
    log_line = "2026-09-24 10:15:02 ERROR POST /api/login ABC 340ms"

    with pytest.raises(ValueError):
        parse_log_line(log_line)


def test_invalid_response_time():
    log_line = "2026-09-24 10:15:02 ERROR POST /api/login 500 ABCms"

    with pytest.raises(ValueError):
        parse_log_line(log_line)
