
from unittest.mock import Mock
import pytest

from todolist.app import ToDoApp


@pytest.fixture
def input_mock():
    return Mock()


@pytest.fixture
def output_mock():
    return Mock()


@pytest.fixture
def app(input_mock, output_mock):
    app = ToDoApp(io=(input_mock, output_mock))
    return app