import abc


class Command(abc.ABC):
    @abc.abstractmethod
    def execute():
        pass

class CommandQuit(Command):
    def __init__(self, app):
        self._app = app

    def execute(self):
        self._app._is_running = False