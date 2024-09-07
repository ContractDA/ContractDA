from __future__ import annotations
import argparse

from contractda.logger._logger import LOG
from contractda.cli._cli import ContractDACmdShell, ShellCommand

class HistoryCommand(ShellCommand):
        def __init__(self, shell_instance: ContractDACmdShell):
            super().__init__(shell_instance)
            self.name = "history"
        def exec(self, *args):
            hist_commands = self._shell_instance._session.history.get_strings()
            for i, commands in enumerate(hist_commands):
                print(i, commands)
                
class HelpCommand(ShellCommand):
        def __init__(self, shell_instance: ContractDACmdShell):
            super().__init__(shell_instance)
            self.name = "help"
        def exec(self, *args):
            command_strings = self._shell_instance._command_mgr.get_command_names()
            for command in command_strings:
                print(command)

class SourceCommand(ShellCommand):
    def __init__(self, shell_instance: ContractDACmdShell):
        super().__init__(shell_instance)
        self.name = "source"
        
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("file", type=str, help="File name")
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        
        try:
            file_path = parsed_args.file
            with open(file_path, "r") as input_file:
                buffer = [line for line in input_file]
                buffer.reverse()
                
                self._shell_instance._buffer.extend(buffer)
        except:
            print("Error during execution")
            return -1
        return 0