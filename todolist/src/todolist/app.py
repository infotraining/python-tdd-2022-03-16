class ToDoApp:
    def __init__(self, io):
        self._in, self._out = io

    def run(self):
        self._out("ToDo list:\n\n\n> ")

        cmd_text = self._in()
        
        if cmd_text == 'quit':
            self._out('Bye!\n')