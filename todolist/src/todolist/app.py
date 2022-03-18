from todolist.commands import CommandQuit


class ToDoApp:
    def __init__(self, io):
        self._in, self._out = io
        self._commands = {'quit': CommandQuit(self)}
        self._is_running = True

    def register_command(self, cmd_id, cmd):
        self._commands[cmd_id] = cmd

    def run(self):
        while self._is_running:
            self._out("ToDo list:\n\n\n> ")

            cmd_text = self._in()

            self._commands[cmd_text].execute()            
        
        self._out('Bye!\n')
            