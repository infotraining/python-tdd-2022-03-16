import queue
import threading

import pytest

from todolist.app import ToDoApp

class FakeIO:
    def __init__(self):
        self.inputs = queue.Queue()
        self.outputs = queue.Queue()

    def print(self, txt):
        self.outputs.put(txt)

    def input(self):
        return self.inputs.get()

    def get_output(self):
        return self.outputs.get(timeout=1)

    def send_input(self, cmd):
        self.inputs.put(cmd)


@pytest.fixture
def fake_io():
    return FakeIO()

def test_app_simple_run(fake_io):
    app = ToDoApp(io=(fake_io.input, fake_io.print))

    thread_app = threading.Thread(target=app.run, daemon=True)
    thread_app.start()

    prompt = fake_io.get_output()
    assert prompt == "ToDo list:\n\n\n> "

    fake_io.send_input("quit")
    assert fake_io.get_output() == "Bye!\n"

    thread_app.join(timeout=1)



def test_app_run(fake_io):
    app = ToDoApp(io=(fake_io.input, fake_io.print))

    app_thread = threading.Thread(target=app.run, daemon=True)
    app_thread.start()

    welcome = fake_io.get_output()
    assert welcome == ("ToDo list:\n"
                       "\n"
                       "\n"
                       "> ")

    fake_io.send_input("add buy milk")
    welcome = fake_io.get_output()
    assert welcome == ("ToDo list:\n"
                       "1. buy milk\n"
                       "\n"
                       "> ")

    fake_io.send_input("add buy eggs")
    welcome = fake_io.get_output()
    assert welcome == ("ToDo list:\n"
                       "1. buy milk\n"
                       "2. buy eggs\n"
                       "\n"
                       "> ")

    fake_io.send_input("quit")
    app_thread.join(timeout=1)
    assert fake_io.get_output() == "Bye!\n"