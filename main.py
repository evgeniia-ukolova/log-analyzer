import argparse
from pathlib import Path

from analyzers.log_analyzer import build_report
from readers.log_reader import read_log_entries


def main():
    parser = argparse.ArgumentParser(
        description="Анализатор серверных логов"
    )

    parser.add_argument(
        "file",
        type=Path,
        help="Путь к лог-файлу",
    )

    args = parser.parse_args()

    try:
        entries = read_log_entries(args.file)
        report = build_report(entries)
    except FileNotFoundError:
        parser.error(f"Файл не найден: {args.file}")
    except ValueError as error:
        parser.error(f"Некорректные данные в лог-файле: {error}")

    print(f"Всего запросов: {report.total_requests}")
    print(f"Ошибок: {report.error_count}")
    print(f"Среднее время ответа: {report.average_response_time} ms")

    print("\nHTTP-статусы:")
    for status_code, count in report.status_counts.items():
        print(f"{status_code}: {count}")

    print("\nEndpoints:")
    for endpoint, count in sorted(
        report.endpoint_counts.items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        print(f"{endpoint}: {count}")


if __name__ == "__main__":
    main()





















