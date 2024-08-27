from contractda.cli.commands._cmd_mgr import BaseCommand

class ExitCommand(BaseCommand):
    def __init__(self):
        self.name = "exit"
    def exec(self, *args):
        return exit()
    
class HistoryCommand(BaseCommand):
    def __init__(self):
        self.name = "history"
    def exec(self, *args):
        raise NotImplementedError

class TestCommand(BaseCommand):
    def __init__(self):
        self.name = "test"
    
    def exec(self, *args):
        print("test!")

class Test2Command(BaseCommand):
    def __init__(self):
        self.name = "test2"
    
    def exec(self, *args):
        print("test2!")
