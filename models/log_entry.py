from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class LogEntry:
    timestamp: datetime
    level: LogLevel
    method: str
    endpoint: str
    status_code: int
    response_time: int



# LogLevel — допустимые уровни логов.
# LogEntry — одна запись из лога.
# timestamp — дата и время.
# method — GET, POST и т.д.
# endpoint — например /api/users.
# status_code — например 200, 404, 500.
# response_time — время ответа в миллисекундах.