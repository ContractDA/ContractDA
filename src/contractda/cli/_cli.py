from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from contractda.cli.commands._cmd_mgr import CommandManager
from contractda.logger._logger import LOG
import click

class ContractDACmdShell():
    def initialize(self, command_mgr: CommandManager):
        self._command_mgr = command_mgr
        # prompt_toolkit related member
        self._completer = WordCompleter(self._command_mgr.get_command_names())
        self._session = PromptSession()


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

