import os

import pytest

from xerparser_dev.reader import Reader


@pytest.fixture(scope="session")
def sample_xer_path():
    """Returns the path to the sample.xer file"""
    return os.path.join(os.path.dirname(__file__), "fixtures", "sample.xer")


@pytest.fixture(scope="session")
def sample_xer(sample_xer_path):
    """Returns a Reader instance initialized with the sample XER file"""
    return Reader(sample_xer_path)


@pytest.fixture(scope="session")
def fixtures_dir():
    """Returns the path to the fixtures directory"""
    fixture_dir = os.path.join(os.path.dirname(__file__), "fixtures")
    os.makedirs(fixture_dir, exist_ok=True)
    return fixture_dir
