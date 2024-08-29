from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from contractda.cli.commands._cmd_mgr import CommandManager
from contractda.cli.commands._base_command import BaseCommand
from contractda.logger._logger import LOG
import click

class ContractDACmdShell():
    """ContractDA Shell for command line interface"""
    def __init__(self):
        self._intro = "ContractDA: a design automation tool for contract-based design"
        self._prompt = "> "

    def initialize(self, command_mgr: CommandManager, shell_level_commands: list[BaseCommand]):
        """Initialize the shell with supported commands

        :param CommandManager command_mgr: the manager that manages all commands
        :param list[BaseCommand] shell_level_commands: the commands that requires access to the shell information such as history commands and all available commands.

        """
        self._command_mgr = command_mgr
        # prompt_toolkit related member
        self._completer = WordCompleter(self._command_mgr.get_command_names())
        self._session = PromptSession()
        # post processing
        self._command_mgr.add_commands(shell_level_commands)
        print(self._intro)


    def interactive_shell(self):
        """Starts the shell for receiving user inputs and execute the corresponding commands"""
        while True:
            try: 
                user_input = self._session.prompt(self._prompt, completer=self._completer)
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
    """Class ShellCommand, a special command that has access to the shell"""
    def __init__(self, shell_instance: ContractDACmdShell):
        super().__init__()
        self._shell_instance = shell_instance
    def exec(self, *args):
        pass

