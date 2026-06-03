import json
from datetime import date
from overdue import report_overdue


def cmd_overdue():
    with open("data.json", encoding="utf-8") as f:
        state = json.load(f)
    vencidos = report_overdue(state["loans"], date.today().isoformat())
    if not vencidos:
        print("No hay préstamos vencidos.")
    for ln in vencidos:
        print(f"Libro {ln['book_code']} — miembro {ln['member_id']} — vencía {ln['due_date']}")


if __name__ == "__main__":
    cmd_overdue()