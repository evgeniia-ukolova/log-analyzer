import pytest
from datetime import datetime

from models.log_entry import LogLevel, HTTPMethod
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






