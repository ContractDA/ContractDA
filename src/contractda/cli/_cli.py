from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter, PathCompleter, Completer, merge_completers
from prompt_toolkit.document import Document
from prompt_toolkit.buffer import Buffer
from contractda.cli.commands._cmd_mgr import CommandManager
from contractda.cli.commands._base_command import BaseCommand
from contractda.logger._logger import LOG
import click

class CustomPathCompleter(Completer):
    def __init__(self):
        self.path_completer = PathCompleter()

    def get_completions(self, document: Document, complete_event):
        # Split the text before the cursor to handle multiple paths
        text_before_cursor = document.text_before_cursor
        words = text_before_cursor.split(' ')

        # Use the last word for path completion
        if words:
            last_word = words[-1]
            new_document = Document(last_word, len(last_word))
            yield from self.path_completer.get_completions(new_document, complete_event)


class ContractDACmdShell():
    """ContractDA Shell for command line interface"""
    def __init__(self):
        self._intro = "ContractDA: a design automation tool for contract-based design"
        self._prompt = "> "
        self._buffer = [] # store the additional commands to be executed

    def initialize(self, command_mgr: CommandManager, shell_level_commands: list[BaseCommand]):
        """Initialize the shell with supported commands

        :param CommandManager command_mgr: the manager that manages all commands
        :param list[BaseCommand] shell_level_commands: the commands that requires access to the shell information such as history commands and all available commands.

        """
        self._command_mgr = command_mgr
        # prompt_toolkit related member
        word_completer = WordCompleter(self._command_mgr.get_command_names())
        file_completer = CustomPathCompleter()
        self._completer = merge_completers([word_completer, file_completer])
    
        self._session = PromptSession(completer=self._completer)
        # post processing
        self._command_mgr.add_commands(shell_level_commands)
        print(self._intro)


    def interactive_shell(self):
        """Starts the shell for receiving user inputs and execute the corresponding commands"""
        while True:
            try: 
                if len(self._buffer) != 0:
                    user_input = self._buffer.pop()
                    #print(self._buffer)
                    print(self._prompt + user_input)
                else:
                    user_input = self._session.prompt(self._prompt)
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

    def batch_operation(self, file:str):
        """Starts the shell for running batch"""
        with open(file, "r") as batch_file:
            self._buffer = [line for line in batch_file]
            self._buffer.reverse()

        while len(self._buffer) != 0:
            try: 
                # TODO: handle the buffer
                user_input = self._buffer.pop()
                print(self._prompt + user_input)
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

