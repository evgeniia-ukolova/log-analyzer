from main import main
import pytest


def test_main_filters_by_status(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "server.log"

    log_file.write_text(
        "2026-09-24 10:15:01 INFO GET /api/users 200 120ms\n"
        "2026-09-24 10:15:02 ERROR POST /api/login 500 340ms\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", str(log_file), "--status", "500"],
    )

    main()

    output = capsys.readouterr().out

    assert "Всего запросов: 1" in output
    assert "Ошибок: 1" in output
    assert "500: 1" in output
    assert "200: 1" not in output


def test_main_filters_by_method(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "server.log"

    log_file.write_text(
        "2026-09-24 10:15:01 INFO GET /api/users 200 120ms\n"
        "2026-09-24 10:15:02 ERROR POST /api/login 500 340ms\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", str(log_file), "--method", "GET"],
    )

    main()

    output = capsys.readouterr().out

    assert "Всего запросов: 1" in output
    assert "/api/users: 1" in output
    assert "/api/login: 1" not in output


def test_main_combines_filters(tmp_path, monkeypatch, capsys):              # несколько фильтров работают вместе 
    log_file = tmp_path / "server.log"

    log_file.write_text(
        "2026-09-24 10:15:01 INFO GET /api/users 200 120ms\n"
        "2026-09-24 10:15:02 ERROR POST /api/login 500 340ms\n"
        "2026-09-24 10:15:03 INFO GET /api/products 200 95ms\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            str(log_file),
            "--status",
            "200",
            "--method",
            "GET",
        ],
    )

    main()

    output = capsys.readouterr().out

    assert "Всего запросов: 2" in output
    assert "Ошибок: 0" in output
    assert "200: 2" in output
    assert "/api/login: 1" not in output


def test_main_file_not_found(monkeypatch, tmp_path):
    missing_file = tmp_path / "missing.log"

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", str(missing_file)],
    )

    with pytest.raises(SystemExit):
        main()



def test_main_invalid_log_line(monkeypatch, tmp_path):
    log_file = tmp_path / "invalid.log"

    log_file.write_text(
        "2026-09-24 ERROR POST\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", str(log_file)],
    )

    with pytest.raises(SystemExit):
        main()


def test_main_top_endpoints(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "server.log"

    log_file.write_text(
        "2026-09-24 10:15:01 INFO GET /api/users 200 120ms\n"
        "2026-09-24 10:15:02 INFO GET /api/users 200 100ms\n"
        "2026-09-24 10:15:03 INFO GET /api/products 200 95ms\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", str(log_file), "--top", "1"],
    )

    main()

    output = capsys.readouterr().out

    assert "/api/users: 2" in output
    assert "/api/products: 1" not in output


def test_main_top_must_be_positive(monkeypatch, tmp_path):
    log_file = tmp_path / "server.log"

    log_file.write_text(
        "2026-09-24 10:15:01 INFO GET /api/users 200 120ms\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", str(log_file), "--top", "0"],
    )

    with pytest.raises(SystemExit):
        main()
































