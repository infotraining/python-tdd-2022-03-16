import pytest


def myapp():
    print("MyApp Started")
    print("Bye!")

@pytest.mark.console_io
@pytest.mark.smoke
def test_capsys(capsys):
    myapp()

    out, err = capsys.readouterr()

    assert out == "MyApp Started\nBye!\n"
