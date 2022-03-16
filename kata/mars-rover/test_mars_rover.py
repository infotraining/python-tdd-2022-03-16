import pytest


class Rover:
    def __init__(self, position, direction) -> None:
        self.position = position
        self.direction = direction
        self.clockwise_direction_sequence = ['E', 'S', 'W', 'N']
        self.counterclockwise_direction_sequence = self.clockwise_direction_sequence[::-1]

    def turn_left(self):
        index = self.clockwise_direction_sequence.index(self.direction)
        self.direction = self.clockwise_direction_sequence[index - 1]

    def turn_right(self):
        index = self.counterclockwise_direction_sequence.index(self.direction)
        self.direction = self.counterclockwise_direction_sequence[index - 1]

    def move_forward(self):
        pass

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