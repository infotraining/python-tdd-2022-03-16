import pytest


class RecentlyUsedList:
    def __init__(self):
        self._rul = []

    def add(self, item):
        self._remove_if_duplicate(item)
        self._rul.insert(0, item)

    def _remove_if_duplicate(self, item):
        if item in self._rul:
            self._rul.remove(item)
        
    def empty(self):
        return len(self._rul) == 0

    def last(self):
        return self._rul[0]

    def __getitem__(self, index):
        return self._rul[index]

    def __len__(self):
        return len(self._rul)


class Test_RecentlyUsedList:
    
    def test_when_created_is_empty(self):
        rul = RecentlyUsedList()
        assert rul.empty()


    def test_when_item_is_added_then_is_not_empty(self):
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
    def test_when_items_added_then_last_return_recently_added(self, items, expected_last):
        rul = RecentlyUsedList()

        for item in items:
            rul.add(item)

        assert rul.last() == expected_last


    def test_when_empty_then_last_raises_IndexError(self):
        rul = RecentlyUsedList()

        with pytest.raises(IndexError):
            rul.last()


    def test_is_indexable(self):
        rul = RecentlyUsedList()

        rul.add('one')
        rul.add('two')
        rul.add('three')

        assert rul[0] == 'three'
        assert rul[1] == 'two'
        assert rul[2] == 'one'



class Test_RecentlyUsedList_InsertingDuplicate:

    @pytest.fixture
    def rul(self):
        rul = RecentlyUsedList()
        rul.add('one')
        rul.add('two')
        rul.add('three')

        return rul


    def test_does_not_change_the_length(self, rul):
        len1 = len(rul)

        # Act
        rul.add('one')
        len2 = len(rul)

        # Assert
        assert len1 == len2


    def test_moves_value_to_the_front(self, rul):
        # Act
        rul.add('one')

        # Assert
        assert rul[0] == 'one'
        assert rul[1] == 'three'
        assert rul[2] == 'two'
