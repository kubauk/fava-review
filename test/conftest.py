import os
import sys
from pathlib import Path
from typing import Callable

import bs4
import jinja2 as jinja2
import pytest as pytest
from fava.core import FavaLedger
from fava.template_filters import FILTERS
from pytest import fixture


@fixture
def example_ledger():
    ledger = FavaLedger(os.path.join(os.path.dirname(__file__), 'example.beancount'))
    ledger.load_file()
    return ledger


@pytest.fixture
def extension_template():
    extension_directory = Path(os.path.dirname(__file__)).parent.absolute()
    fava_directory = os.path.dirname(sys.modules['fava'].__file__)

    def add_template_filters(env: jinja2.Environment, filters: list[Callable]) -> jinja2.Environment:
        for f in filters:
            env.filters[f.__name__] = f
        return env

    def template_loader(template_file):
        join = os.path.join(fava_directory, 'templates')
        loader = jinja2.FileSystemLoader(searchpath=[os.path.join(extension_directory, 'fava_review', 'templates'),
                                                     join])
        env = add_template_filters(jinja2.Environment(loader=loader), FILTERS)
        return env.get_template(template_file)

    return template_loader


@pytest.fixture
def extension_template_soup(extension_template):
    def soup_of(template_file, extension):
        template = extension_template(template_file)
        return bs4.BeautifulSoup(template.render(extension=extension))

    return soup_of
