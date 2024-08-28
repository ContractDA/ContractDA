from contractda.cli.commands._cmd_mgr import BaseCommand

class ExitCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "exit"
    def exec(self, *args):
        return exit()
    
class ReportStatusCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "report_status"
    def exec(self, *args):
        self.context.report()



class TestCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "test"
    
    def exec(self, *args):
        print("test!")

class Test2Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "test2"
    
    def exec(self, *args):
        print("test2!")
