import os

from fava.core import FavaLedger
from pytest import fixture


@fixture
def example_ledger():
    ledger = FavaLedger(os.path.join(os.path.dirname(__file__), 'example.beancount'))
    ledger.load_file()
    return ledger
