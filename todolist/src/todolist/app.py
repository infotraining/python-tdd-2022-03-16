from todolist.commands import CommandQuit, CommandAdd


class ToDoApp:
    def __init__(self, io):
        self._in, self._out = io
        self._commands = {
            'quit': CommandQuit(self),
            'add': CommandAdd(self)
        }
        self._is_running = True
        self.todo_list = []

    def register_command(self, cmd_id, cmd):
        self._commands[cmd_id] = cmd

    def run(self):
        while self._is_running:
            self._out("ToDo list:\n\n\n> ")

            cmd_text = self._in()

            cmd_id, cmd_arg = self._parse(cmd_text)

            self._commands[cmd_id].execute(cmd_arg)            
        
        self._out('Bye!\n')
            

    def _parse(self, cmd_text):
        if ' ' in cmd_text:
            cmd_id, cmd_arg = cmd_text.split(' ', maxsplit=1) 
            return cmd_id, cmd_arg
        return cmd_text, ""
