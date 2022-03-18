from unittest.mock import Mock, call
from todolist.app import ToDoApp


def test_todoapp_prompt():
    mock_input = Mock(return_value='quit')
    mock_output = Mock()
    app = ToDoApp(io=(mock_input, mock_output))

    app.run()

    assert mock_output.call_args_list[0] == call("ToDo list:\n\n\n> ")


def test_todoapp_quit_prints_bye_and_exits():
    mock_input = Mock(return_value='quit')
    mock_output = Mock()
    app = ToDoApp(io=(mock_input, mock_output))

    app.run()

    assert mock_output.call_args == call("Bye!\n")


def test_todoapp_run_loops_until_quit():
    mock_input = Mock()
    mock_input.side_effect = ['cmd', 'cmd', 'cmd', 'quit']
    mock_output = Mock()
    app = ToDoApp(io=(mock_input, mock_output))

    app.run()

    assert mock_input.call_count == 4
