import os
import sys
from pathlib import Path
from typing import Callable

import bs4
import jinja2
import pytest
from fava.application import create_app
from fava.core import FavaLedger

TEST_BEANCOUNT_FILES = [os.path.join(os.path.dirname(__file__), 'example.beancount')]


@pytest.fixture
def fava_app():
    return create_app(TEST_BEANCOUNT_FILES, load=True)


@pytest.fixture
def test_request(request, fava_app):
    path = request.param if hasattr(request, 'param') else 'http://localhost/beancount/extension/FavaReview/'
    with fava_app.test_request_context(path=path) as ctx:
        ctx.push()
        ctx.match_request()
        fava_app.preprocess_request()
        yield fava_app
        ctx.pop()


@pytest.fixture
def load_ledger() -> Callable:
    def ledger_loader(filename: str):
        ledger = FavaLedger(os.path.join(os.path.dirname(__file__), filename))
        ledger.load_file()
        return ledger

    return ledger_loader


@pytest.fixture
def example_ledger(test_request, load_ledger: Callable) -> FavaLedger:
    return load_ledger('example.beancount')


@pytest.fixture
def extension_template(fava_app) -> Callable:
    extension_directory = Path(os.path.dirname(__file__)).parent.absolute()
    fava_directory = os.path.dirname(sys.modules['fava'].__file__)

    def template_loader(template_file):
        fava_app.jinja_env.loader = jinja2.FileSystemLoader(
            searchpath=[os.path.join(extension_directory, 'fava_review', 'templates'),
                        (os.path.join(fava_directory, 'templates'))])
        return fava_app.jinja_env.get_template(template_file)

    return template_loader


@pytest.fixture
def extension_template_soup(extension_template) -> Callable:
    def soup_of(template_file, extension):
        template = extension_template(template_file)
        return bs4.BeautifulSoup(template.render(extension=extension))

    return soup_of
