import queue

import pytest


class FakeIO:
    def __init__(self):
        self.inputs = queue.Queue()
        self.outputs = queue.Queue()

    def print(self, txt):
        self.outputs.put(txt)

    def input(self):
        return self.inputs.get()

    def get_output(self):
        return self.outputs.get(timeout=1)
        # return self.outputs.get()

    def send_input(self, cmd):
        self.inputs.put(cmd)


@pytest.fixture
def fake_io():
    return FakeIO()
