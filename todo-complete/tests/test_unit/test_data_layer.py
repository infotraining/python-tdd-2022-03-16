from unittest.mock import Mock, MagicMock

from todo.basic_db import BasicDB


def test_basic_db_load(tmpdir):
    mock_file = MagicMock(
        read=Mock(return_value='["first", "second"]')
    )
    mock_file.__enter__.return_value = mock_file
    mock_opener = Mock(return_value=mock_file)
    db = BasicDB(tmpdir / "db", _fileopener=mock_opener)

    loaded = db.load()

    assert loaded == ["first", "second"]
    assert mock_opener.call_args[0][0] == tmpdir / "db"
    mock_file.read.assert_called_with()


def test_basic_db_missing_load(tmpdir):
    mock_opener = Mock(side_effect=FileNotFoundError)
    db = BasicDB(tmpdir / "db", _fileopener=mock_opener)

    loaded = db.load()

    assert loaded == []
    assert mock_opener.call_args[0][0] == tmpdir / "db"


def test_basic_db_save(tmpdir):
    mock_file = MagicMock(write=Mock())
    mock_file.__enter__.return_value = mock_file
    mock_opener = Mock(return_value=mock_file)

    db = BasicDB(tmpdir / "db", _fileopener=mock_opener)
    loaded = db.save(["first", "second"])

    assert mock_opener.call_args[0][0:2] == (tmpdir / "db", "w+")
    mock_file.write.assert_called_with('["first", "second"]')