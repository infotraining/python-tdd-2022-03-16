import os.path
import unittest

from unittest.mock import patch

from my_module import rm


class NoMockingTestCase(unittest.TestCase):
    def test_provided_extension_should_be_used(self):
        filename = 'file.md'
        open(filename, 'w').close()
        self.assertTrue(os.path.isfile(filename))
        rm(filename)
        self.assertFalse(os.path.isfile(filename))

    def test_when_extension_is_missing_then_use_default_one(self):
        filename = 'file.txt'
        open(filename, 'w').close()
        self.assertTrue(os.path.isfile(filename))
        rm('file')
        self.assertFalse(os.path.isfile(filename))


class PatchingTestCase(unittest.TestCase):
    @patch('my_module.os')
    def test_provided_extension_should_be_used(self, os_mock):
        rm('file.md')
        os_mock.remove.assert_called_once_with('file.md')

    @patch('my_module.os')
    def test_when_extension_is_missing_then_use_default_one(self, os_mock):
        rm('file')
        os_mock.remove.assert_called_once_with('file.txt')


@patch('my_module.os')
class ClassPatchingTestCase(unittest.TestCase):
    def test_provided_extension_should_be_used(self, os_mock):
        rm('file.md')
        os_mock.remove.assert_called_once_with('file.md')

    def test_when_extension_is_missing_then_use_default_one(self, os_mock):
        rm('file')
        os_mock.remove.assert_called_once_with('file.txt')


class PatchingInSetupTestCase(unittest.TestCase):
    def setUp(self):
        self.os_patcher = patch('my_module.os')
        self.os_mock = self.os_patcher.start()

    def tearDown(self):
        self.os_patcher.stop()

    def test_provided_extension_should_be_used(self):
        rm('file.md')
        self.os_mock.remove.assert_called_once_with('file.md')

    def test_when_extension_is_missing_then_use_default_one(self):
        rm('file')
        self.os_mock.remove.assert_called_once_with('file.txt')


if __name__ == "__main__":
    unittest.main()
