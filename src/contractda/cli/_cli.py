from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from contractda.cli.commands._cmd_mgr import CommandManager
from contractda.cli.commands._base_command import BaseCommand
from contractda.logger._logger import LOG
import click

class ContractDACmdShell():
    def initialize(self, command_mgr: CommandManager, shell_level_commands: list[BaseCommand]):
        self._command_mgr = command_mgr
        # prompt_toolkit related member
        self._completer = WordCompleter(self._command_mgr.get_command_names())
        self._session = PromptSession()
        # post processing
        self._command_mgr.add_commands(shell_level_commands)

    def interactive_shell(self):
        while True:
            try: 
                user_input = self._session.prompt("> ", completer=self._completer)
                # retrieve command name
                tokens = user_input.split()
                if not tokens:
                    continue
                
                command_name = tokens[0]
                args = tokens[1:]
                self._command_mgr.execute_command(command_name, *args)

            except KeyboardInterrupt:
                break
            except EOFError:
                break
        
class ShellCommand(BaseCommand):
    def __init__(self, shell_instance: ContractDACmdShell):
        super().__init__()
        self._shell_instance = shell_instance
    def exec(self, *args):
        pass

