
import cmd
from todolist.commands import Command, CommandAdd, CommandQuit


def test_CommandQuit_execute_quits_the_loop(app):
    cmd_quit = CommandQuit(app)
    assert app._is_running == True

    cmd_quit.execute()

    assert app._is_running == False


def test_AddCommand_execute_item_is_added_to_the_list(app):
    cmd_add = CommandAdd(app)

    cmd_add.execute(arg="buy coffee")

    assert app.todo_list[-1] == "buy coffee"
