from typing import Optional

from fava.ext import FavaExtensionBase
from flask import get_template_attribute

from fava_review import pivot_review
from fava_review.pivot_review import PivotReview


class FavaReview(FavaExtensionBase):
    report_title = "Review"

    def __init__(self, ledger: "FavaLedger", config: Optional[str] = None) -> None:
        super().__init__(ledger, config)

    def get_datetime(self):

        try:
            table = get_template_attribute("_query_table.html", "querytable")
            review = PivotReview(self.ledger)
            return table(self.ledger, None, *review.income_and_expense_by_month())

        except Exception as e:
            return e
