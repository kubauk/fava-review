from _decimal import Decimal
from typing import NamedTuple, Any

import petl
from fava.core import FavaLedger
from hamcrest import assert_that, contains_exactly, contains_inanyorder, equal_to
from hamcrest.core.base_matcher import BaseMatcher, T
from hamcrest.core.description import Description
from hamcrest.core.matcher import Matcher
from hamcrest.core.string_description import StringDescription
from petl import Table, MemorySource

from fava_review.pivot_review import PivotReview
from fava_review.pivot_review import bean_query_to_petl

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

    def __init__(self, param: Any) -> None:
        super().__init__()
        self._params = param


def row(param) -> BaseMatcher[ResultRow]:
    return RowResultMatcher(param)


def test_monthly_income_and_expenses_query(example_ledger: FavaLedger):
    pivot_review = PivotReview(example_ledger)
    types, rows = pivot_review.income_and_expense_by_month()
    assert_that(types, contains_exactly(
        ('account', str), ('y2020m10', Decimal), ('y2020m11', Decimal), ('y2020m12', Decimal), ('y2021m01', Decimal),
        ('y2021m02', Decimal), ('y2021m03', Decimal), ('y2021m04', Decimal), ('total', Decimal)))

    assert_that(rows, contains_inanyorder(
        row({'account': 'Income:Salary:ABC', 'y2020m10': Decimal('-1000'), 'y2020m11': Decimal('-1000'),
             'y2020m12': Decimal('-1000'), 'y2021m01': Decimal('-1000'), 'y2021m02': Decimal('-1000'),
             'y2021m03': Decimal('-1000'), 'y2021m04': Decimal('-1000'), 'total': Decimal('-7000')}),
        row({'account': 'total', 'y2020m10': Decimal('-1000'), 'y2020m11': Decimal('-1000'),
             'y2020m12': Decimal('-1000'), 'y2021m01': Decimal('-1000'), 'y2021m02': Decimal('-1000'),
             'y2021m03': Decimal('-1000'), 'y2021m04': Decimal('-1000'), 'total': Decimal('-7000')})))


def petl_matching_csv(param) -> Matcher[Table]:
    class PetlMatcher(BaseMatcher[Table]):
        @staticmethod
        def _check_and_describe(item: T, mismatch_description: Description):
            if not isinstance(item, Table):
                mismatch_description.append_text("item was not PETL Table, but was ").append_text(item)
                return False

            mem_source = MemorySource('')
            petl.tocsv(item, mem_source, lineterminator='\n')

            if not equal_to(param) \
                    .matches(mem_source.getvalue().decode(), mismatch_description):
                return False

            return True

        def _matches(self, item: T) -> bool:
            return self._check_and_describe(item, StringDescription())

        def describe_to(self, description: Description) -> None:
            description.append_text("A PETL Table which produces csv:\n").append_text(param)

        def describe_mismatch(self, item: T, mismatch_description: Description) -> None:
            self._check_and_describe(item, mismatch_description)

    return PetlMatcher()


def test_bean_query_to_petl():
    TestNamedTuple = NamedTuple('moo', [('account', str), ('month', int)])
    t = bean_query_to_petl([TestNamedTuple(account='Expenses:EatingOut', month=2)])
    assert_that(t, petl_matching_csv("account,month\nExpenses:EatingOut,2\n"))
