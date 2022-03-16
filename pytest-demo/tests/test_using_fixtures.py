import pytest

@pytest.fixture(autouse=True)
def setup_teardown():
    # Setup
    print("\nBefore test")

    yield

    # Teardown
    print("\nAfter test")

@pytest.fixture
def lst(item):
    # Arrange
    lst = []
    lst.append(item)
    lst.append("one")
    lst.append("two")
    lst.append("three")

    return lst

@pytest.fixture
def item():
    return "four"

@pytest.fixture
def last_one(lst):
    lst.append("last")
    return lst[-1]

def test_list_append(lst, item, last_one):
    assert item == "four"
    assert last_one == "last"
    # Act
    lst.append(item)

    # Assert
    assert len(lst) == 6


def test_list_remove(lst):    
    # Act
    lst.remove("two")

    # Assert
    assert len(lst) == 3
