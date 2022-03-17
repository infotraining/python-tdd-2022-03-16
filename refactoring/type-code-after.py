from abc import ABC, abstractmethod
from contextlib import redirect_stdout
import io
import unittest


def Shape(name):
    cls = SHAPE_NAME_TO_CLASS[name]
    return cls()


class ShapeBase(ABC):
    @abstractmethod
    def draw(self):
        pass


class Circle(ShapeBase):
    def draw(self):
        print('o')


class Dot(ShapeBase):
    def draw(self):
        print('.')


SHAPE_NAME_TO_CLASS = {
    'circle': Circle,
    'dot': Dot
}


class ShapeTests(unittest.TestCase):
    def test_circle(self):
        self._test(shape=Shape('circle'),
                   expected_output='o')

    def test_dot(self):
        self._test(shape=Shape('dot'),
                   expected_output='.')

    def _test(self, shape, expected_output):
        f = io.StringIO()
        with redirect_stdout(f):
            shape.draw()
        output = f.getvalue()
        self.assertEqual(output, expected_output+'\n')


if __name__ == "__main__":
    unittest.main()
