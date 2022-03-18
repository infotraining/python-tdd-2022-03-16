from unittest.mock import patch
import pytest
import os
import my_module

CONTENT = "abc"

def test_E2E_removing_file_with_extension(tmp_path):
    p = tmp_path / "file_1.md"
    p.write_text(CONTENT)
    assert len(list(tmp_path.iterdir())) == 1

    my_module.rm(str(p))

    assert len(list(tmp_path.iterdir())) == 0

def test_E2E_removing_file_without_extension(tmp_path):
    p = tmp_path / "file_1.txt"
    p.write_text(CONTENT)
    assert len(list(tmp_path.iterdir())) == 1

    filename = str(p.parent / "file_1") 
    my_module.rm(str(filename))

    assert len(list(tmp_path.iterdir())) == 0


@patch('my_module.os', spec=True)
def test_unit_removing_file_with_extension(os_mock, tmp_path):

    my_module.rm("file.md")

    os_mock.remove.assert_called_once_with("file.md")

    
@patch('my_module.os', spec=True)
def test_unit_removing_file_without_extension(os_mock, tmp_path):

    my_module.rm("file")
    
    os_mock.remove.assert_called_once_with("file.txt")