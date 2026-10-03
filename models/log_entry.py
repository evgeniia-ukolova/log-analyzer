from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


@dataclass
class LogEntry:
    timestamp: datetime
    level: LogLevel
    method: HTTPMethod
    endpoint: str
    status_code: int
    response_time: int