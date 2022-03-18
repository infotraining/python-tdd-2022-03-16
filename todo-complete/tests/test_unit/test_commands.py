import pytest

from todo.app import TODOApp
from todo.commands import CommandQuit, CommandAdd, CommandDel


def test_quit_cmd_ends_run_loop():
    app = TODOApp()
    cmd_quit = CommandQuit(app)
    assert app._is_running == True

    cmd_quit.execute()

    assert app._is_running == False


def test_add_cmd_appends_item_to_the_list():
    todo_list = []
    cmd_add = CommandAdd(todo_list)

    cmd_add.execute(args="buy milk")

    assert todo_list[-1] == "buy milk"


def test_del_cmd_deletes_item_with_a_given_index():
    todo_list = ['buy eggs', 'buy milk', 'buy coffee']
    cmd_del = CommandDel(todo_list)

    cmd_del.execute(args='2')

    assert todo_list == ['buy eggs', 'buy coffee']
