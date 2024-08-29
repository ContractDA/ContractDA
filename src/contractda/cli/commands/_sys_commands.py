from contractda.cli.commands._cmd_mgr import BaseCommand

class AddSystemCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "add_system"
    
    def exec(self, *args):
        print("add_system")
        self.context._design_mgr.create_empty_design()
        raise NotImplementedError()