from .app import TODOApp
from .basic_db import BasicDB

TODOApp(dbmanager=BasicDB("todo.data")).run()