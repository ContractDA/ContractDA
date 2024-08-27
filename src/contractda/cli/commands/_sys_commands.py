from contractda.cli.commands._cmd_mgr import BaseCommand

class AddComponentCommand(BaseCommand):
    def __init__(self):
        self.name = "add_component"
    
    def exec(self, *args):
        print("add_components")
        raise NotImplementedError()