import queue
import threading

import pytest

from todo.app import TODOApp


def test_app_run(fake_io):
    app = TODOApp(io=(fake_io.input, fake_io.print))

    app_thread = threading.Thread(target=app.run, daemon=True)
    app_thread.start()

    welcome = fake_io.get_output()
    assert welcome == ("TODOs:\n"
                       "\n"
                       "\n"
                       "> ")

    fake_io.send_input("add buy milk")
    welcome = fake_io.get_output()
    assert welcome == ("TODOs:\n"
                       "1. buy milk\n"
                       "\n"
                       "> ")

    fake_io.send_input("add buy eggs")
    welcome = fake_io.get_output()
    assert welcome == ("TODOs:\n"
                       "1. buy milk\n"
                       "2. buy eggs\n"
                       "\n"
                       "> ")

    fake_io.send_input("del 1")
    welcome = fake_io.get_output()
    assert welcome == ("TODOs:\n"
                       "1. buy eggs\n"
                       "\n"
                       "> ")

    fake_io.send_input("quit")
    app_thread.join(timeout=1)
    assert fake_io.get_output() == "bye!\n"
