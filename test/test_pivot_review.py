from decimal import Decimal
from typing import NamedTuple, Callable

import petl
from fava.core import FavaLedger
from fava.util.date import Interval
from hamcrest import assert_that, is_
from hamcrest.core.base_matcher import BaseMatcher, T
from hamcrest.core.description import Description
from hamcrest.core.matcher import Matcher
from hamcrest.core.string_description import StringDescription
from petl import Table, MemorySource

from fava_review.pivot_review import PivotReview
from fava_review.pivot_review import bean_query_to_petl


def test_monthly_income_and_expenses_query(example_ledger: FavaLedger):
    pivot_review = PivotReview(example_ledger)
    rows = pivot_review.income_and_expense_by(Interval.MONTH)

    assert_that(rows, is_([{'account': 'Expenses:Groceries', '2020-10': Decimal('10.00'),
                            '2020-11': Decimal('20.00'), '2020-12': Decimal('30.00'),
                            '2021-01': Decimal('0.00'), '2021-02': Decimal('0.00'),
                            '2021-03': Decimal('60.00'), '2021-04': Decimal('70.00'),
                            'total': Decimal('190.00')},
                           {'account': 'Income:Salary:ABC', '2020-10': Decimal('-1000.00'),
                            '2020-11': Decimal('-1000.00'), '2020-12': Decimal('-1000.00'),
                            '2021-01': Decimal('-1000.00'), '2021-02': Decimal('-1000.00'),
                            '2021-03': Decimal('-1000.00'), '2021-04': Decimal('-1000.00'),
                            'total': Decimal('-7000.00')},
                           {'account': 'total', '2020-10': Decimal('-990.00'),
                            '2020-11': Decimal('-980.00'), '2020-12': Decimal('-970.00'),
                            '2021-01': Decimal('-1000.00'), '2021-02': Decimal('-1000.00'),
                            '2021-03': Decimal('-940.00'), '2021-04': Decimal('-930.00'),
                            'total': Decimal('-6810.00')}]))


def test_yearly_income_and_expenses_query(example_ledger: FavaLedger):
    pivot_review = PivotReview(example_ledger)
    rows = pivot_review.income_and_expense_by(Interval.YEAR)

    assert_that(rows, is_([{'account': 'Expenses:Groceries',
                            '2020': Decimal('60.00'), '2021': Decimal('130.00'), 'total': Decimal('190.00')},
                           {'account': 'Income:Salary:ABC',
                            '2020': Decimal('-3000.00'), '2021': Decimal('-4000.00'), 'total': Decimal('-7000.00')},
                           {'account': 'total',
                            '2020': Decimal('-2940.00'), '2021': Decimal('-3870.00'), 'total': Decimal('-6810.00')}]))


def test_quarterly_income_and_expenses_query(example_ledger: FavaLedger):
    pivot_review = PivotReview(example_ledger)
    rows = pivot_review.income_and_expense_by(Interval.QUARTER)

    assert_that(rows, is_([{'account': 'Expenses:Groceries',
                            '2020Q4': Decimal('60.00'), '2021Q1': Decimal('60.00'), '2021Q2': Decimal('70.00'),
                            'total': Decimal('190.00')},
                           {'account': 'Income:Salary:ABC',
                            '2020Q4': Decimal('-3000.00'), '2021Q1': Decimal('-3000.00'), '2021Q2': Decimal('-1000.00'),
                            'total': Decimal('-7000.00')},
                           {'account': 'total',
                            '2020Q4': Decimal('-2940.00'), '2021Q1': Decimal('-2940.00'), '2021Q2': Decimal('-930.00'),
                            'total': Decimal('-6810.00')}]))


def petl_matching_csv(param) -> Matcher[Table]:
    class PetlMatcher(BaseMatcher[Table]):
        @staticmethod
        def _check_and_describe(item: T, mismatch_description: Description):
            if not isinstance(item, Table):
                mismatch_description.append_text("item was not PETL Table, but was ").append_text(item)
                return False

            mem_source = MemorySource('')
            petl.tocsv(item, mem_source, lineterminator='\n')

            return True

        def _matches(self, item: T) -> bool:
            return self._check_and_describe(item, StringDescription())

        def describe_to(self, description: Description) -> None:
            description.append_text("A PETL Table which produces csv:\n").append_text(param)

        def describe_mismatch(self, item: T, mismatch_description: Description) -> None:
            self._check_and_describe(item, mismatch_description)

    return PetlMatcher()


def test_bean_query_to_petl():
    # noinspection PyPep8Naming
    TestTuple = NamedTuple('TestTuple',
                           [('year', int), ('total', Decimal),
                            ('account', str), ('month', int),
                            ('currency', str)])
    t = bean_query_to_petl(
        [TestTuple(account='Expenses:EatingOut', month=2, year=2022, total=Decimal(2), currency='GBP')], Interval.MONTH)
    assert_that(list(petl.dicts(t)),
                is_([{'date': '2022-02', 'account': 'Expenses:EatingOut', 'total': Decimal('2'), 'currency': 'GBP'}]))


def test_starting_currency_matches_currency_with_more_positions(load_ledger: Callable):
    ledger = load_ledger('no-operating-currency-and-usd-more-than-gbp.beancount')
    review = PivotReview(ledger)
    assert_that(review.best_starting_currency(), is_('USD'))


def test_starting_currency_matches_first_operating_currency(load_ledger: Callable):
    ledger = load_ledger('gbp-first-operating-currency-and-usd-more-than-gbp.beancount')
    review = PivotReview(ledger)
    assert_that(review.best_starting_currency(), is_('GBP'))
