import argparse

from contractda.cli.commands._cmd_mgr import BaseCommand
from contractda.logger._logger import LOG

class ReadDesignFromFileCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "read_design_from_file"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("-file", type=str, help="File name", required=True)
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        
        try:
            file_path = parsed_args.file
            print(file_path)
            self.context._design_mgr.read_design_from_file(file_path)
        except:
            print("Error during execution")
            return -1
        return 0

class ReportSystemCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "report_design"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("system_name", type=str, help="system name")
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        except Exception as e:
            print("?????")
            print(type(e))
            return -1
        
        system_name = parsed_args.system_name      
        if system_name not in self.context._design_mgr._systems:
            err_msg = "system does not exist!"
            LOG.error(err_msg)
            print(err_msg)
            return -1
        self.context._design_mgr._systems[system_name].report()
        return 0
    
class ReportSystemsCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "report_designs"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        except Exception as e:
            print(type(e))
            return -1
        
        print(len(self.context._design_mgr._systems.values()), "systems")
        for sys in self.context._design_mgr._systems.values():
            sys.report()
        return 0