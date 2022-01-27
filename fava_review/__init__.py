from __future__ import annotations
from typing import Optional, Any

from fava.core import FavaLedger
from fava.ext import FavaExtensionBase

from fava_review import pivot_review
from fava_review.pivot_review import PivotReview


class FavaIncomeExpenseReview(FavaExtensionBase):
    report_title = "Income/Expense Review"

    def __init__(self, ledger: FavaLedger, config: Optional[str] = None) -> None:
        super().__init__(ledger, config)
        self.review = PivotReview(self.ledger)

    def get_income_expenses_review_by_month(self) -> list[dict[str, Any]]:
        try:
            return self.review.income_and_expense_by_month()
        except Exception:
            raise

    def current_operating_currency(self) -> str:
        return self.review.current_operating_currency()
