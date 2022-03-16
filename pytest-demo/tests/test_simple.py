import pytest


def test_something():
    a = 5
    b = 10
    assert a + b == 15


@pytest.fixture
def greetings():
    print('HELLO!')
    yield
    print('\nGOODBYE')


@pytest.fixture(scope="class")
def provide_current_time(request):
    import datetime
    request.cls.now = datetime.datetime.utcnow()

    print("\nENTER CLS")
    yield
    print("\nEXIT CLS")


@pytest.mark.usefixtures("provide_current_time")
class TestMultiple:
    def test_first(self):
        print("\nRUNNING AT", self.now)
        assert 5 == 5

    @pytest.mark.usefixtures("greetings")
    def test_second(self):
        assert 10 == 10

    def test_third(self):
        assert "abc" == "abc"


# using fixture for dependency injection
@pytest.fixture
def random_number_generator():
    import random
    def _number_provider():
        return random.choice(range(10))
    yield _number_provider

def test_something_random(random_number_generator):
    a = random_number_generator()
    b = 10
    assert a + b >= 10