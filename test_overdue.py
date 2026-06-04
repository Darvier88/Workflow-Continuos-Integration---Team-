from overdue import report_overdue


def test_reporta_solo_los_vencidos():
    loans = [
        {"book_code": "B001", "member_id": "M001", "due_date": "2026-06-01"},
        {"book_code": "B002", "member_id": "M001", "due_date": "2026-06-20"},
    ]
    result = report_overdue(loans, "2026-06-10")
    assert [ln["book_code"] for ln in result] == ["B001"]


def test_sin_vencidos():
    loans = [{"book_code": "B001", "member_id": "M001", "due_date": "2026-06-20"}]
    assert report_overdue(loans, "2026-06-01") == []


def test_fecha_limite_exacta_no_esta_vencida():
    # due_date == today  ->  NO vencido (comparación estricta '<')
    loans = [{"book_code": "B001", "member_id": "M001", "due_date": "2026-06-10"}]
    assert report_overdue(loans, "2026-06-10") == []


def test_lista_vacia():
    assert report_overdue([], "2026-06-10") == []


def test_acepta_objeto_date():
    from datetime import date
    loans = [{"book_code": "B001", "member_id": "M001", "due_date": "2026-06-01"}]
    assert report_overdue(loans, date(2026, 6, 10)) == loans