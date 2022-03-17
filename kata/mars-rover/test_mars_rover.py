import pytest
import math


# class UnboundedGrid:
#     def wrap(self, x, y):
#         return (x, y)


# def test_UnboundedGrid_returns_unchanged_coordinates():
#     grid = UnboundedGrid()
#     assert grid.wrap(100, 100) == (100, 100)


class Grid:
    def __init__(self, max_width=math.inf, max_height=math.inf) -> None:
        self.max_width = max_width
        self.max_height = max_height

    def wrap(self, x, y):
        return (x % self.max_width, y % self.max_height)


def test_Grid_when_overflow_wraps_the_coordinates():
    grid = Grid(5, 5)

    assert grid.wrap(5, 5) == (0, 0)
    assert grid.wrap(6, 6) == (1, 1)


class Rover:
    def __init__(self, position, direction, grid=Grid()) -> None:
        self.position = position
        self.direction = direction
        self.grid = grid
        self.clockwise_direction_sequence = ['E', 'S', 'W', 'N']
        self.counterclockwise_direction_sequence = self.clockwise_direction_sequence[::-1]
        self._longitudinal_strides = {
            "N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
        self.FORWARD = 1
        self.BACKWARD = -1

    def _move(self, sense):
        x, y = self.position
        hor_stride, ver_stride = self._longitudinal_strides[self.direction]
        self.position = self.grid.wrap(
            x + hor_stride * sense, y + ver_stride * sense)

    def move_forward(self):
        self._move(self.FORWARD)

    def move_backward(self):
        self._move(self.BACKWARD)
    
    def move(self, command_sequence):
        command_abbreviations = {"F": self.move_forward, "B": self.move_backward,
                                 "R": self.turn_right, "L": self.turn_left}
        for abbreviation in command_sequence:
            try:
                command_abbreviations[abbreviation]()
            except KeyError:
                raise ValueError('Command unknown')

    def turn_left(self):
        index = self.clockwise_direction_sequence.index(self.direction)
        self.direction = self.clockwise_direction_sequence[index - 1]

    def turn_right(self):
        index = self.counterclockwise_direction_sequence.index(self.direction)
        self.direction = self.counterclockwise_direction_sequence[index - 1]


def test_Rover_accepts_coordinates_and_direction():
    rover = Rover(position=(1, 1), direction="N")
    assert rover.direction == "N"
    assert rover.position == (1, 1)


@pytest.mark.parametrize("start_direction,end_direction", [
    ('N', 'W'),
    ('W', 'S'),
    ('S', 'E'),
    ('E', 'N')
])
def test_Rover_turns_left(start_direction, end_direction):
    rover = Rover(position=(1, 1), direction=start_direction)
    rover.turn_left()
    assert rover.direction == end_direction
    assert rover.position == (1, 1)


@pytest.mark.parametrize("start_direction,end_direction", [
    ('N', 'E'),
    ('E', 'S'),
    ('S', 'W'),
    ('W', 'N')
])
def test_Rover_turns_right(start_direction, end_direction):
    rover = Rover(position=(1, 1), direction=start_direction)
    rover.turn_right()
    assert rover.direction == end_direction
    assert rover.position == (1, 1)


@pytest.mark.parametrize("start_position,start_direction,end_position", [
    ((1, 1), 'N', (1, 2)),
    ((1, 1), 'E', (2, 1)),
    ((1, 1), 'S', (1, 0)),
    ((1, 1), 'W', (0, 1))
])
def test_Rover_moves_forward(start_position, start_direction, end_position):
    rover = Rover(position=start_position, direction=start_direction)
    rover.move_forward()
    assert rover.position == end_position
    assert rover.direction == start_direction


@pytest.mark.parametrize("start_position,start_direction,end_position", [
    ((1, 4), 'N', (1, 0)),
    ((4, 1), 'E', (0, 1)),
    ((1, 0), 'S', (1, 4)),
    ((0, 1), 'W', (4, 1))
])
def test_Rover_moves_forward_and_wraps(start_position, start_direction, end_position):
    rover = Rover(position=start_position,
                  direction=start_direction, grid=Grid(5, 5))

    rover.move_forward()
    assert rover.position == end_position
    assert rover.direction == start_direction


def test_Rover_moves_using_command_sequence():
    command_sequence = "FFRFFBFLR"
    rover = Rover(position=(0, 0), direction="N")
    rover.move(command_sequence)
    assert rover.position == (2, 2)
    assert rover.direction == "E"

def test_Rover_raises_ValueError_with_wrong_sequence():
    command_sequence = "xFFRFFBFLR"
    rover = Rover(position=(0, 0), direction="N")
    with pytest.raises(ValueError):
        rover.move(command_sequence)