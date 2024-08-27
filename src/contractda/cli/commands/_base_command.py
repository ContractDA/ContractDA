from abc import ABC

class BaseCommand(ABC):
    def __init__(self):
        self.name = ""

    def exec(self, *args):
        pass