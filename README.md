# Log Analyzer

Учебный CLI-проект на Python для анализа серверных логов.

## Цель

Практика Python Core на проекте, приближенном к задачам backend-разработки.

## Возможности

Программа умеет:

- читать лог-файлы;
- парсить строки логов;
- считать общее количество запросов;
- считать HTTP-статусы;
- определять количество ошибок;
- считать среднее время ответа;
- находить самый медленный запрос;
- считать популярность endpoints;
- фильтровать записи;
- обрабатывать логи через генераторы без загрузки всего файла в память.

## Формат лога

Пример строки:

2026-09-24 10:15:02 ERROR POST /api/login 500 340ms

Поля:

дата время уровень HTTP-метод endpoint статус время_ответа

## Запуск

python main.py data/server.log

## Фильтры

По HTTP-статусу:

python main.py data/server.log --status 500

По HTTP-методу:

python main.py data/server.log --method GET

По endpoint:

python main.py data/server.log --endpoint /api/users/15

По минимальному времени ответа:

python main.py data/server.log --min-response-time 200

По дате:

python main.py data/server.log --date 2026-09-24

По уровню лога:

python main.py data/server.log --level ERROR

Несколько фильтров можно использовать одновременно:

python main.py data/server.log --status 200 --method GET

## Top endpoints

Показать только N самых частых endpoints:

python main.py data/server.log --top 3

## Тесты

Запуск тестов:

python -m pytest

На текущем этапе проект покрыт 44 тестами.

## Стек

- Python
- pytest
- argparse
- pathlib
- dataclasses
- Enum
- generators
- type hints