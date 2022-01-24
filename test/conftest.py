import os
import sys
from pathlib import Path

import bs4
import jinja2 as jinja2
import pytest as pytest
from fava.application import app, _pull_beancount_file
from fava.core import FavaLedger
from pytest import fixture

app.config['BEANCOUNT_FILES'] = [os.path.join(os.path.dirname(__file__), 'example.beancount')]


@fixture
def client():
    with app.app_context():
        with app.test_request_context():
            _pull_beancount_file(None, {'bfile': 'beancount'})
            yield app


@fixture
def example_ledger():
    ledger = FavaLedger(os.path.join(os.path.dirname(__file__), 'example.beancount'))
    ledger.load_file()
    return ledger


@pytest.fixture
def extension_template():
    extension_directory = Path(os.path.dirname(__file__)).parent.absolute()
    fava_directory = os.path.dirname(sys.modules['fava'].__file__)

    def template_loader(template_file):
        app.jinja_env.loader = jinja2.FileSystemLoader(
            searchpath=[os.path.join(extension_directory, 'fava_review', 'templates'),
                        (os.path.join(fava_directory, 'templates'))])
        return app.jinja_env.get_template(template_file)

    return template_loader


@pytest.fixture
def extension_template_soup(extension_template):
    def soup_of(template_file, extension):
        template = extension_template(template_file)
        return bs4.BeautifulSoup(template.render(extension=extension))

    return soup_of
