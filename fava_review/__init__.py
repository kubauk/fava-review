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

    def get_income_statement_report(self) -> list[dict[str, Any]]:
        try:
            return self.review.income_statement_by(g.interval)
        except Exception:
            raise

    def get_balance_sheet_report(self) -> list[dict[str, Any]]:
        try:
            return self.review.balance_sheet_by(g.interval)
        except Exception:
            raise

    def current_operating_currency(self) -> str:
        return self.review.current_operating_currency()
