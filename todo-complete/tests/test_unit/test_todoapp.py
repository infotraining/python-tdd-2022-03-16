import threading
from unittest.mock import Mock, call
import pytest

from todo.app import TODOApp


@pytest.fixture
def todo_app(fake_io):
    app = TODOApp(io=(fake_io.input, fake_io.print))
    thd_app = threading.Thread(target=app.run, daemon=True)
    thd_app.start()
    prompt = fake_io.get_output()
    assert prompt == "TODOs:\n\n\n> "

    yield app

    thd_app.join(timeout=1)


def test_todoapp_quit_breaks_a_loop(fake_io, todo_app):
    fake_io.send_input("quit")
    assert fake_io.get_output() == 'bye!\n'


def wait_for_loop_end(todo_app):
    while todo_app.is_running():
        pass


def test_todoapp_loop_executes_a_command(fake_io, todo_app):
    mock_cmd = Mock()
    todo_app.register_cmd("cmd", mock_cmd)
    fake_io.send_input("cmd")
    fake_io.send_input("quit")
    wait_for_loop_end(todo_app)

    mock_cmd.execute.assert_called_once()


def test_todoapp_loop_args_are_passed_to_the_command(fake_io, todo_app):
    mock_cmd = Mock()
    todo_app.register_cmd("cmd", mock_cmd)
    fake_io.send_input("cmd abc def")
    fake_io.send_input("quit")
    wait_for_loop_end(todo_app)

    mock_cmd.execute.assert_called_with(args="abc def")


def test_todoapp_loop_unknown_command_is_ignored(fake_io, todo_app):
    fake_io.send_input("unknown_cmd")
    fake_io.send_input("quit")
    assert fake_io.get_output() == "Unknown command. Please try again...\n"


def test_todoapp_run_loads_data_from_db():
    dbmanager = Mock(
        load=Mock(return_value=['buy milk', 'buy coffee'])
    )
    app = TODOApp(io=(Mock(return_value="quit"), Mock()),
                  dbmanager=dbmanager)
    app.run()

    dbmanager.load.assert_called_with()
    assert app._to_do_list == ["buy milk", "buy coffee"]


def test_todoapp_run_saves_data_to_db():
    dbmanager = Mock(
        load=Mock(return_value=["buy milk", "buy coffee"]),
        save=Mock()
    )

    app = TODOApp(io=(Mock(return_value="quit"), Mock()),
                  dbmanager=dbmanager)

    app.run()

    dbmanager.save.assert_called_with(["buy milk", "buy coffee"])