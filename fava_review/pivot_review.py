from decimal import Decimal

import petl
from fava.core import FavaLedger
from petl import Table
from petl.transform.joins import JoinView


def bean_query_to_petl(rows) -> petl.Table:
    t = petl.fromdicts([nt._asdict() for nt in rows])
    t = petl.fieldmap(t, {'date': lambda rec: ReviewDate("{}-{:02d}".format(rec['year'], rec['month'])),
                          'account': lambda rec: AccountName(rec['account'].strip()),
                          'total': lambda rec: rec['total'],
                          'currency': lambda rec: rec['currency']})
    return t


class AccountName(str):
    pass


class ReviewDate(str):
    pass


class PivotReview(object):
    QUERY = 'SELECT year, month, root(account, 4) as account, sum(number) as total, currency ' \
            'WHERE (account ~ "{}" OR account ~ "{}") ' \
            'GROUP BY year, month, account, currency ' \
            'ORDER BY year, month, currency, account ' \
            'FLATTEN'

    def __init__(self, ledger: FavaLedger) -> None:
        self._ledger = ledger
        super().__init__()

    def income_and_expense_by_month(self):
        _, types, rows = self._ledger.query_shell.execute_query(self.QUERY.format('Income', 'Expenses'))

        t = bean_query_to_petl(rows)
        t = petl.pivot(t, 'account', 'date', 'total', sum, Decimal(0))
        types.append('total')
        t = self.add_total_column_and_row(t)
        return list(petl.dicts(t))

    @staticmethod
    def add_total_column_and_row(view: Table) -> Table:
        # Add total column
        view = PivotReview.add_totals_column(view)
        # Add total row
        view = petl.transpose(PivotReview.add_totals_column(petl.transpose(view)))
        return view

    @staticmethod
    def add_totals_column(table: Table) -> JoinView:
        def sum_row(key, rows):
            records = list(rows)
            total = Decimal(0)
            for record in records:
                for i in range(1, len(record)):
                    total += record[i]
            return key, total

        return petl.join(table, petl.rowreduce(table, 'account', sum_row, ['account', 'total']), 'account')
