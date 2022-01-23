from typing import Optional

from fava.core import FavaLedger
from fava.ext import FavaExtensionBase

from fava_review import pivot_review
from fava_review.pivot_review import PivotReview


class FavaIncomeExpenseReview(FavaExtensionBase):
    report_title = "Income/Expense Review"

    def __init__(self, ledger: FavaLedger, config: Optional[str] = None) -> None:
        super().__init__(ledger, config)
        self.review = PivotReview(self.ledger)

    def get_income_expenses_review_by_month(self):
        try:
            return self.review.income_and_expense_by_month()

        except Exception as e:
            return e
