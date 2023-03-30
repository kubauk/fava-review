import os
import sys
from pathlib import Path
from typing import Callable

import bs4
import jinja2 as jinja2
import pytest as pytest
from fava.application import app, _pull_beancount_file, _perform_global_filters
from fava.core import FavaLedger
from pytest import fixture

app.config['BEANCOUNT_FILES'] = [os.path.join(os.path.dirname(__file__), 'example.beancount')]


@fixture
def test_request(request):
    path = request.param if hasattr(request, 'param') else '/extension_report/FavaReview'
    with app.test_request_context(path=path):
        _pull_beancount_file(None, {'bfile': 'beancount'})
        _perform_global_filters()
        yield app


@fixture
def load_ledger() -> Callable:
    def ledger_loader(filename: str):
        ledger = FavaLedger(os.path.join(os.path.dirname(__file__), filename))
        ledger.load_file()
        return ledger

    return ledger_loader


@fixture
def example_ledger(load_ledger: Callable, test_request) -> FavaLedger:
    return load_ledger('example.beancount')


@pytest.fixture
def extension_template() -> Callable:
    extension_directory = Path(os.path.dirname(__file__)).parent.absolute()
    fava_directory = os.path.dirname(sys.modules['fava'].__file__)

    def template_loader(template_file):
        app.jinja_env.loader = jinja2.FileSystemLoader(
            searchpath=[os.path.join(extension_directory, 'fava_review', 'templates'),
                        (os.path.join(fava_directory, 'templates'))])
        return app.jinja_env.get_template(template_file)

    return template_loader


@pytest.fixture
def extension_template_soup(extension_template) -> Callable:
    def soup_of(template_file, extension):
        template = extension_template(template_file)
        return bs4.BeautifulSoup(template.render(extension=extension))

    return soup_of
