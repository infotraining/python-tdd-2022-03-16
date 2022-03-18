class CommandQuit:
    def __init__(self, app):
        self._app = app

    def execute(self, args=None):
        self._app._is_running = False


class CommandAdd:
    def __init__(self, todo_list):
        self._todo_list = todo_list

    def execute(self, args=None):
        self._todo_list.append(args)


class CommandDel:
    def __init__(self, todo_list):
        self._todo_list = todo_list

    def execute(self, args=None):
        index = int(args)
        self._todo_list.pop(index - 1)
