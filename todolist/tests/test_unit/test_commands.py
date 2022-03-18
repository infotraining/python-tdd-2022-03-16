
from todolist.commands import Command, CommandQuit


def test_CommandQuit_execute_quits_the_loop(app):
    cmd_quit = CommandQuit(app)
    assert app._is_running == True

    cmd_quit.execute()

    assert app._is_running == False