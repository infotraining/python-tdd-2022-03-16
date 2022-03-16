import pytest


class RecentlyUsedList:
    def __init__(self):
        self._rul = []

    def add(self, item):
        self._rul.insert(0, item)

    def empty(self):
        return len(self._rul) == 0

    def last(self):
        return self._rul[0]

    def __getitem__(self, index):
        return self._rul[index]


def test_RecentlyUsedList_when_created_is_empty():
    rul = RecentlyUsedList()
    assert rul.empty()

def test_RecentlyUsedList_when_item_is_added_then_is_not_empty():
    # Arrange / Given
    rul = RecentlyUsedList()
    
    # Act / When
    rul.add("one")

    # Assert / Then

    assert not rul.empty()

@pytest.mark.parametrize("items,expected_last", [
    (["one"], "one"),
    (["one", "two"], "two"),
    (["one", "two", "three", "four"], "four")
]
)
def test_RecentlyUsedList_when_items_added_then_last_return_recently_added(items, expected_last):
    rul = RecentlyUsedList()

    for item in items:
        rul.add(item)

    assert rul.last() == expected_last

def test_RecentlyUsedList_when_empty_then_last_raises_IndexError():
    rul = RecentlyUsedList()

    with pytest.raises(IndexError):
        rul.last()

def test_RecentlyUsedList_is_indexable():
    rul = RecentlyUsedList()

    rul.add('one')
    rul.add('two')
    rul.add('three')

    assert rul[0] == 'three'
    assert rul[1] == 'two'
    assert rul[2] == 'one'