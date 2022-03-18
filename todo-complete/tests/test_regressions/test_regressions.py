import io
import queue
import threading
from unittest.mock import Mock

import pytest

from todo.app import TODOApp
from todo.basic_db import BasicDB


def test_double_quotes_in_list_item_step_1(fake_io, tmpdir):
    thread_app = threading.Thread(
        target=TODOApp(
            io=(fake_io.input, fake_io.print),
            dbmanager=BasicDB(tmpdir / "db")
        ).run,
        daemon=True
    )
    thread_app.start()
    fake_io.get_output()

    fake_io.send_input("add buy coffee")
    fake_io.send_input('add install "Windows 11"')
    fake_io.send_input('quit')
    thread_app.join(timeout=1)

    while True:
        try:
            fake_io.get_output()
        except queue.Empty:
            break

    thread_app = threading.Thread(
        target=TODOApp(
            io=(fake_io.input, fake_io.print),
            dbmanager=BasicDB(tmpdir / "db")
        ).run,
        daemon=True
    )
    thread_app.start()
    fake_io.get_output()


def test_double_quotes_in_list_item_step_2_with_mocks(tmpdir):
    app = TODOApp(
        io=(Mock(side_effect=["add buy coffee", 'add install "Windows 11"', "quit"]), Mock()),
        dbmanager=BasicDB(tmpdir / "db")
    )
    app.run()

    restarted_app = TODOApp(
        io=(Mock(return_value="quit"), Mock()),
        dbmanager=BasicDB(tmpdir / "db"))
    restarted_app.run()


def test_double_quotes_in_list_item_step_3_with_fake_file():
    fake_file = io.StringIO()
    fake_file.close = Mock()

    app = TODOApp(
        io=(Mock(side_effect=["add buy coffee", 'add install "Windows 11"', "quit"]), Mock()),
        dbmanager=BasicDB(None, _fileopener=Mock(
            side_effect=[FileNotFoundError, fake_file]
        ))
    )

    app.run()

    # reset file
    fake_file.seek(0)

    restarted_app = TODOApp(
        io=(Mock(side_effect=["add buy coffee", 'add install "Windows 11"', "quit"]), Mock()),
        dbmanager=BasicDB(None, _fileopener=Mock(
            return_value=fake_file
        ))
    )

    restarted_app.run()


def test_basid_db_save_and_load_data_with_quotes():
    fake_file = io.StringIO()
    fake_file.close = Mock()

    data = ["buy milk", 'install "Focal Fossa"']

    dbmanager = BasicDB(None, _fileopener=Mock(return_value=fake_file))

    dbmanager.save(data)
    fake_file.seek(0)
    loaded_data = dbmanager.load()

    assert loaded_data == data
