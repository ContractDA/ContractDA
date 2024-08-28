from abc import ABC
from contractda.cli._program import Context, global_context

class BaseCommand(ABC):
    def __init__(self):
        self.name = ""
        self.context: Context = global_context

    def exec(self, *args):
        pass