import argparse
from pathlib import Path
from datetime import date

from analyzers.log_analyzer import (
    build_report,
    filter_by_status,
    filter_by_method,
    filter_by_endpoint,
    filter_by_response_time,
    filter_by_date,
    filter_by_level,
)
from readers.log_reader import read_log_entries
from models.log_entry import HTTPMethod, LogLevel



def main() -> None:
    parser = argparse.ArgumentParser(
        description="Анализатор серверных логов"
    )

    parser.add_argument(
        "file",
        type=Path,
        help="Путь к лог-файлу",
    )

    parser.add_argument(
        "--status",
        type=int,
        help="Фильтровать запросы по HTTP-статусу",
    )

    parser.add_argument(
        "--method",
        type=HTTPMethod,
        help="Фильтровать запросы по HTTP-методу",
    )

    parser.add_argument(
        "--endpoint",
        type=str,
        help="Фильтровать запросы по endpoint",
    )

    parser.add_argument(
        "--min-response-time",
        type=int,
        help="Фильтровать запросы по минимальному времени ответа",
    )

    parser.add_argument(
        "--date",
        type=date.fromisoformat,
        help="Фильтровать запросы по дате в формате YYYY-MM-DD",
    )

    parser.add_argument(
        "--level",
        type=LogLevel,
        help="Фильтровать запросы по уровню лога",
    )

    parser.add_argument(
        "--top",
        type=int,
        help="Показать N самых частых endpoints",
    )






    args = parser.parse_args()

    try:
        entries = read_log_entries(args.file)

        if args.status is not None:
            entries = filter_by_status(entries, args.status)

        if args.method is not None:
            entries = filter_by_method(entries, args.method)

        if args.endpoint is not None:
            entries = filter_by_endpoint(entries, args.endpoint)

        if args.min_response_time is not None:
            entries = filter_by_response_time(
                entries,
                args.min_response_time,
            )

        if args.level is not None:
            entries = filter_by_level(entries, args.level)

        if args.date is not None:
            entries = filter_by_date(entries, args.date)

        if args.top is not None and args.top <= 0:
                    parser.error("--top должен быть больше 0")







        report = build_report(entries)

    except FileNotFoundError:
        parser.error(f"Файл не найден: {args.file}")
    except ValueError as error:
        parser.error(f"Некорректные данные в лог-файле: {error}")

    print(f"Всего запросов: {report.total_requests}")
    print(f"Ошибок: {report.error_count}")
    print(f"Среднее время ответа: {report.average_response_time} ms")

    if report.slowest_request is not None:
        print(
            "Самый медленный запрос: "
            f"{report.slowest_request.method.value} "
            f"{report.slowest_request.endpoint} "
            f"{report.slowest_request.response_time} ms"
        )


    print("\nHTTP-статусы:")
    for status_code, count in report.status_counts.items():
        print(f"{status_code}: {count}")

    print("\nEndpoints:")

    sorted_endpoints = sorted(
        report.endpoint_counts.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    if args.top is not None:
        sorted_endpoints = sorted_endpoints[:args.top]

    for endpoint, count in sorted_endpoints:
        print(f"{endpoint}: {count}")



if __name__ == "__main__":
    main()





















