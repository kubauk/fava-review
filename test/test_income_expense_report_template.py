from typing import Sequence

from fava.core import FavaLedger
from hamcrest import assert_that, contains_exactly
from hamcrest.core.matcher import Matcher

from fava_review import FavaIncomeExpenseReview


def test_table_header_contains_all_fields(example_ledger: FavaLedger, extension_template_soup: callable,
                                          client) -> None:
    template_soup = extension_template_soup("FavaIncomeExpenseReview.html",
                                            FavaIncomeExpenseReview(example_ledger))
    tags: Sequence[str] = [t.get_text().strip() for t in template_soup.select('thead th')]
    matchers: Matcher[Sequence[str]] = contains_exactly(
        'account', '2020-10', '2020-11', '2020-12', '2021-01', '2021-02', '2021-03', '2021-04', 'total')
    assert_that(tags, matchers)


def test_table_body_contains_all_fields(example_ledger: FavaLedger, extension_template_soup: callable,
                                        client) -> None:
    template_soup = extension_template_soup("FavaIncomeExpenseReview.html", FavaIncomeExpenseReview(example_ledger))

    tags: Sequence[Sequence[str]] = [[c.get_text().strip() for c in row.find_all('td')]
                                     for row in template_soup.select('tbody tr')]
    matchers: Matcher[Sequence[Sequence[str]]] = contains_exactly(
        ['Expenses:Groceries', '10.00', '20.00', '30.00', '0', '0', '60.00', '70.00', '190.00'],
        ['Income:Salary:ABC', '-1000.00', '-1000.00', '-1000.00',
         '-1000.00', '-1000.00', '-1000.00', '-1000.00', '-7000.00'])
    assert_that(tags, matchers)


def test_table_footer_contains_all_fields(example_ledger: FavaLedger, extension_template_soup: callable,
                                          client) -> None:
    template_soup = extension_template_soup("FavaIncomeExpenseReview.html", FavaIncomeExpenseReview(example_ledger))
    tags: Sequence[str] = [t.get_text() for t in template_soup.select('tfoot td')]
    matchers: Matcher[Sequence[str]] = contains_exactly(
        'total', '-990.00', '-980.00', '-970.00', '-1000.00', '-1000.00', '-940.00', '-930.00', '-6810.00')
    assert_that(tags, matchers)


def test_table_body_account_names_are_links(example_ledger: FavaLedger, extension_template_soup: callable,
                                            client) -> None:
    template_soup = extension_template_soup("FavaIncomeExpenseReview.html", FavaIncomeExpenseReview(example_ledger))
    tags: Sequence[str] = [link.get_text().strip() for link in template_soup.select('tbody td a')]
    matchers: Matcher[Sequence[str]] = contains_exactly('Expenses:Groceries', 'Income:Salary:ABC')
    assert_that(tags, matchers)

