from _decimal import Decimal
from typing import NamedTuple

from fava.core import FavaLedger
from hamcrest import assert_that, contains_exactly, contains_inanyorder
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.string_description import StringDescription

from fava_review.pivot_review import PivotReview

ResultRow = NamedTuple


class RowResultMatcher(BaseMatcher[ResultRow]):
    def _matches(self, item: ResultRow) -> bool:
        return self._describe_and_check(item, StringDescription())

    def describe_to(self, description: Description) -> None:
        description.append_text('ResultRow matching {}'.format(self._params))

    def describe_mismatch(self, item: ResultRow, mismatch_description: Description) -> None:
        self._describe_and_check(item, mismatch_description)

    def _describe_and_check(self, item: ResultRow, description: Description) -> bool:
        fields = list(item._fields)
        for key in self._params.keys():
            if key not in item._fields:
                description.append_text("ResultRow was missing field {}.".format(key))
                return False
            else:
                fields.remove(key)

        if len(fields) != 0:
            description.append_text("Unexpected fields in ResultRow: {}".format(fields))
            return False

        for key in self._params.keys():
            if self._params[key] != getattr(item, key):
                description.append_text(
                    "ResultRow['{}'] was {} but expected {}".format(key, item[key], self._params[key]))
                return False
        return True

    def __init__(self, param) -> None:
        super().__init__()
        self._params = param


def row(param) -> RowResultMatcher:
    return RowResultMatcher(param)


def test_monthly_income_and_expenses_query(example_ledger: FavaLedger):
    pivot_review = PivotReview(example_ledger)
    types, rows = pivot_review.income_and_expense_by_month()
    assert_that(types, contains_exactly(
        ('year', int), ('month', int), ('account', str), ('total', Decimal), ('currency', str)))

    assert_that(rows, contains_inanyorder(
        row({'year': 2020, 'month': 10, 'account': 'Income:Salary:ABC', 'total': Decimal('-1000.00'),
             'currency': 'GBP'}),
        row({'year': 2020, 'month': 11, 'account': 'Income:Salary:ABC', 'total': Decimal('-1000.00'),
             'currency': 'GBP'}),
        row({'year': 2020, 'month': 12, 'account': 'Income:Salary:ABC', 'total': Decimal('-1000.00'),
             'currency': 'GBP'}),
        row({'year': 2021, 'month': 1, 'account': 'Income:Salary:ABC', 'total': Decimal('-1000.00'),
             'currency': 'GBP'}),
        row({'year': 2021, 'month': 2, 'account': 'Income:Salary:ABC', 'total': Decimal('-1000.00'),
             'currency': 'GBP'}),
        row({'year': 2021, 'month': 3, 'account': 'Income:Salary:ABC', 'total': Decimal('-1000.00'),
             'currency': 'GBP'}),
        row({'year': 2021, 'month': 4, 'account': 'Income:Salary:ABC', 'total': Decimal('-1000.00'),
             'currency': 'GBP'})))
