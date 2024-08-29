from abc import ABC
from contractda.cli._program import Context, global_context

class BaseCommand(ABC):
    """Base Class for commands
    
    The command has access to the program context to modify the context for performing certain tasks. 
    """
    def __init__(self):
        self.name = ""
        self.context: Context = global_context

    def exec(self, *args):
        pass