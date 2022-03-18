import functools
import re

from todo.commands import CommandQuit, CommandAdd, CommandDel


class TODOApp:
    def __init__(self,
                 io=(input, functools.partial(print, end="")),
                 dbmanager=None):
        self._in, self._out = io
        self._dbmanager = dbmanager
        self._is_running = True
        self._to_do_list = self._dbmanager.load() if self._dbmanager is not None else []
        self._commands = {
            'quit': CommandQuit(self),
            'add': CommandAdd(self._to_do_list),
            'del': CommandDel(self._to_do_list)
        }

    def run(self):
        while self._is_running:
            self._out(self.prompt(self.to_do_list()))
            cmd = self._in()
            self._dispatch(cmd)

        if self._dbmanager is not None:
            self._dbmanager.save(self._to_do_list)
        self._out("bye!\n")

    def is_running(self):
        return self._is_running

    def register_cmd(self, id, cmd):
        self._commands[id] = cmd

    def _dispatch(self, cmd):
        cmd_id, cmd_args = self._parse_command(cmd)
        if cmd_id in self._commands:
            self._commands[cmd_id].execute(args=cmd_args)
        else:
            self._out("Unknown command. Please try again...\n")

    def prompt(self, output):
        return f"TODOs:\n{output}\n\n> "

    def to_do_list(self):
        enumerated_items = enumerate(self._to_do_list, start=1)
        return "\n".join(
            "{}. {}".format(idx, entry) for idx, entry in enumerated_items
        )

    def _parse_command(self, cmd_text):
        m = re.match(r'^([\w]+)\s*(.+)*', cmd_text)
        return m.group(1, 2)
