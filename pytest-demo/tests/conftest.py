import pytest

@pytest.fixture(scope="session", autouse=True)
def setup_suite():
    print("STARTING TESTS")
    yield
    print("FINISHED TESTS")

@pytest.fixture
def item():
    return "zero"