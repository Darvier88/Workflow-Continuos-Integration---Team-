from datetime import date


def report_overdue(loans, today):
    """Reporta los préstamos vencidos.

    Un préstamo está vencido si su fecha límite (due_date) es ANTERIOR
    a la fecha de referencia 'today'.

    Args:
        loans: lista de préstamos. Cada préstamo es un dict que contiene
               al menos la clave 'due_date' como 'YYYY-MM-DD'.
        today: fecha de referencia, str 'YYYY-MM-DD' o datetime.date.

    Returns:
        Lista con los préstamos vencidos (mismo formato que entraron).
    """
    if isinstance(today, str):
        today = date.fromisoformat(today)

    overdue = []
    for loan in loans:
        due = loan["due_date"]
        if isinstance(due, str):
            due = date.fromisoformat(due)
        if due < today:
            overdue.append(loan)
    return overdue