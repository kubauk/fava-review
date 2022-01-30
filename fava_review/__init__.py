from __future__ import annotations
from typing import Optional, Any

from fava.application import g
from fava.core import FavaLedger
from fava.ext import FavaExtensionBase

from fava_review import pivot_review
from fava_review.pivot_review import PivotReview


class FavaReview(FavaExtensionBase):
    report_title = "Fava Review"

    def __init__(self, ledger: FavaLedger, config: Optional[str] = None) -> None:
        super().__init__(ledger, config)
        self.review = PivotReview(self.ledger)

    def get_income_expenses_review(self) -> list[dict[str, Any]]:
        try:
            return self.review.income_and_expense_by(g.interval)
        except Exception:
            raise

    def get_assets_liabilities_review(self) -> list[dict[str, Any]]:
        return self.get_income_expenses_review()

    def current_operating_currency(self) -> str:
        return self.review.current_operating_currency()
