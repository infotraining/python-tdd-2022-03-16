import pytest


class RecentlyUsedList:
    def __init__(self, max_len=None):
        self._rul = []
        assert max_len is None or max_len > 0
        self._max_len = max_len

    def add(self, item):
        self._check_not_empty_string(item)
        self._remove_if_duplicate(item)
        self._remove_older_when_full()
        self._rul.insert(0, item)

    def _remove_older_when_full(self):
        if len(self) == self._max_len:
            self._rul.pop()

    def _remove_if_duplicate(self, item):
        if item in self._rul:
            self._rul.remove(item)

    def _check_not_empty_string(self, item):
        if not item:
            raise ValueError()

    def empty(self):
        return len(self._rul) == 0

    def last(self):
        return self._rul[0]

    def __getitem__(self, index):
        return self._rul[index]

    def __len__(self):
        return len(self._rul)


class Test_RecentlyUsedList:

    @pytest.mark.initial_state
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

    @pytest.mark.smoke
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


class Test_RecentlyUsedList_InsertingEmptyString:

    def test_raises_ValueError(self):
        rul = RecentlyUsedList()

        with pytest.raises(ValueError):
            rul.add("")


class Test_RecentlyUsedList_BoundedCapacity:

    def test_limits_the_length_of_list(self):
        # Arrange
        rul = RecentlyUsedList(max_len=3)
        rul.add('one')
        rul.add('two')
        rul.add('three')

        # Act
        rul.add('four')

        # Assert
        assert len(rul) == 3

    def test_when_adding_item_then_first_inserted_item_is_dropped(self):
        # Arrange
        rul = RecentlyUsedList(max_len=3)
        rul.add('one')
        rul.add('two')
        rul.add('three')

        rul.add('four')

        assert rul[0] == 'four'
        assert rul[1] == 'three'
        assert rul[2] == 'two'
