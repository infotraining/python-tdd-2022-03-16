import queue
import threading

from todo.basic_db import BasicDB
from todo.app import TODOApp


def test_persistence(tmpdir, fake_io):
    path_db = tmpdir / "db"
    thd_app = threading.Thread(
        target=TODOApp(io=(fake_io.input, fake_io.print),
                       dbmanager=BasicDB(path_db)).run,
        daemon=True
    )

    thd_app.start()

    welcome = fake_io.get_output()
    assert welcome == (
        "TODOs:\n"
        "\n"
        "\n"
        "> "
    )

    fake_io.send_input("add buy milk")
    welcome = fake_io.get_output()
    assert welcome == ("TODOs:\n"
                       "1. buy milk\n"
                       "\n"
                       "> ")

    fake_io.send_input("quit")
    thd_app.join(timeout=1)

    while True:
        try:
            fake_io.get_output()
        except queue.Empty:
            break

    thd_app = threading.Thread(
        target=TODOApp(io=(fake_io.input, fake_io.print),
                       dbmanager=BasicDB(path_db)).run,
        daemon=True
    )

    thd_app.start()

    welcome = fake_io.get_output()
    assert welcome == (
        "TODOs:\n"
        "1. buy milk\n"
        "\n"
        "> "
    )

    fake_io.send_input("quit")
    thd_app.join(timeout=1)
