from datetime import date

import pytest

from loans import (
    BookAlreadyLoanedError,
    BookNotFoundError,
    MemberLoanLimitExceededError,
    MemberNotFoundError,
    loan_book,
)


@pytest.fixture
def state():
    return {
        "members": [
            {"id": "M001", "name": "Juan"},
            {"id": "M002", "name": "Ana"},
        ],
        "books": [
            {"code": "B001", "title": "1984"},
            {"code": "B002", "title": "Brave New World"},
            {"code": "B003", "title": "Fahrenheit 451"},
            {"code": "B004", "title": "We"},
        ],
        "loans": [],
    }


def test_loan_book_appends_entry(state):
    result = loan_book(state, "B001", "M001", today=date(2026, 6, 3))
    assert len(result["loans"]) == 1
    loan = result["loans"][0]
    assert loan["book_code"] == "B001"
    assert loan["member_id"] == "M001"
    assert loan["loan_date"] == "2026-06-03"
    assert loan["due_date"] == "2026-06-17"


def test_loan_unknown_book_raises(state):
    with pytest.raises(BookNotFoundError):
        loan_book(state, "B999", "M001")


def test_loan_unknown_member_raises(state):
    with pytest.raises(MemberNotFoundError):
        loan_book(state, "B001", "M999")


def test_book_already_loaned_cannot_be_loaned_again(state):
    loan_book(state, "B001", "M001", today=date(2026, 6, 3))
    with pytest.raises(BookAlreadyLoanedError):
        loan_book(state, "B001", "M002")


def test_member_loan_limit_is_three(state):
    loan_book(state, "B001", "M001", today=date(2026, 6, 3))
    loan_book(state, "B002", "M001", today=date(2026, 6, 3))
    loan_book(state, "B003", "M001", today=date(2026, 6, 3))
    with pytest.raises(MemberLoanLimitExceededError):
        loan_book(state, "B004", "M001")


def test_loan_uses_custom_loan_days(state):
    result = loan_book(state, "B001", "M001", today=date(2026, 6, 3), loan_days=7)
    assert result["loans"][0]["due_date"] == "2026-06-10"