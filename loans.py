"""Feature 2: loan a book to a member."""
from datetime import date, timedelta
from typing import Optional

DEFAULT_LOAN_DAYS = 14
MAX_LOANS_PER_MEMBER = 3


class LoanError(Exception):
    """Base error for any loan-rule violation."""


class BookNotFoundError(LoanError):
    pass


class MemberNotFoundError(LoanError):
    pass


class BookAlreadyLoanedError(LoanError):
    pass


class MemberLoanLimitExceededError(LoanError):
    pass

def loan_book(
    state: dict,
    book_code: str,
    member_id: str,
    today: Optional[date] = None,
    loan_days: int = DEFAULT_LOAN_DAYS,
) -> dict:
    """Append a loan to state and return it.

    Rules enforced:
      - the book must exist in the catalogue,
      - the member must be registered,
      - the book must not already be on loan,
      - the member must hold fewer than MAX_LOANS_PER_MEMBER books.

    The caller is responsible for persisting the returned state.
    """
    if today is None:
        today = date.today()

    if not any(b["code"] == book_code for b in state["books"]):
        raise BookNotFoundError(f"Book '{book_code}' is not in the catalogue.")

    if not any(m["id"] == member_id for m in state["members"]):
        raise MemberNotFoundError(f"Member '{member_id}' is not registered.")

    if any(l["book_code"] == book_code for l in state["loans"]):
        raise BookAlreadyLoanedError(f"Book '{book_code}' is already on loan.")

    held = sum(1 for l in state["loans"] if l["member_id"] == member_id)
    if held >= MAX_LOANS_PER_MEMBER:
        raise MemberLoanLimitExceededError(
            f"Member '{member_id}' already holds {MAX_LOANS_PER_MEMBER} books."
        )

    due = today + timedelta(days=loan_days)
    state["loans"].append(
        {
            "book_code": book_code,
            "member_id": member_id,
            "loan_date": today.isoformat(),
            "due_date": due.isoformat(),
        }
    )
    return state


# ---- CLI wiring ----

def register_parser(subparsers) -> None:
    """Register the `loan` subcommand on the main argparse parser."""
    p = subparsers.add_parser("loan", help="Loan a book to a member.")
    p.add_argument("--book", required=True, help="Book code (e.g. B001).")
    p.add_argument("--member", required=True, help="Member ID (e.g. M001).")
    p.add_argument(
        "--days",
        type=int,
        default=DEFAULT_LOAN_DAYS,
        help=f"Loan length in days (default: {DEFAULT_LOAN_DAYS}).",
    )
    p.set_defaults(func=_cli_loan)


def _cli_loan(args) -> int:
    from storage import load_state, save_state

    state = load_state()
    try:
        loan_book(state, args.book, args.member, loan_days=args.days)
    except LoanError as e:
        print(f"ERROR: {e}")
        return 1
    save_state(state)
    print(f"OK: book '{args.book}' loaned to member '{args.member}'.")
    return 0