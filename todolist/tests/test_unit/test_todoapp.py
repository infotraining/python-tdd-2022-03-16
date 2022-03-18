import abc
from unittest.mock import Mock, call
import pytest
from todolist.app import ToDoApp


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
    app.register_command('cmd', Mock())

    app.run()

    assert input_mock.call_count == 4


def test_todoapp_loop_executes_command(input_mock, app):
    input_mock.side_effect = ['cmd', 'quit']
    cmd_mock = Mock()
    app.register_command('cmd', cmd_mock)

    app.run()

    cmd_mock.execute.assert_called_once()


def test_todoapp_argument_is_passed_to_the_execute(input_mock, app):
    input_mock.side_effect = ['cmd arg', 'quit']
    cmd_mock = Mock()
    app.register_command('cmd', cmd_mock)

    app.run()

    cmd_mock.execute.assert_called_once_with('arg')
