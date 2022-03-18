import abc


class Command(abc.ABC):
    @abc.abstractmethod
    def execute(self, arg=None):
        pass

class CommandQuit(Command):
    def __init__(self, app):
        self._app = app

    def execute(self, arg=None):
        self._app._is_running = False


class CommandAdd(Command):
    def __init__(self, app):
        self._app = app

    def execute(self, arg):
        self._app.todo_list.append(arg)