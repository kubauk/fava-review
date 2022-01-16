from fava.core import FavaLedger


class PivotReview:
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
        return types, rows
