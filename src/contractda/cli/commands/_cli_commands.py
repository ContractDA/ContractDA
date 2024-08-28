from __future__ import annotations

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