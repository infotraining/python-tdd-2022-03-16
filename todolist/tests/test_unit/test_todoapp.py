from unittest.mock import Mock, call
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


def test_todoapp_prompt(input_mock, output_mock, app):
    input_mock.return_value = 'quit'

    app.run()

    assert output_mock.call_args_list[0] == call("ToDo list:\n\n\n> ")


def test_todoapp_quit_prints_bye_and_exits(input_mock, output_mock, app):
    input_mock.return_value = 'quit'

    app.run()

    assert output_mock.call_args == call("Bye!\n")


def test_todoapp_run_loops_until_quit(input_mock, app):
    input_mock.side_effect = ['cmd', 'cmd', 'cmd', 'quit']

    app.run()

    assert input_mock.call_count == 4
