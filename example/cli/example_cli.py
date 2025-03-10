from contractda.cli import ContractDACmdShell
from contractda.cli.commands._cmd_mgr import CommandManager
from contractda.cli._cli_commands import HelpCommand, HistoryCommand, SourceCommand


if __name__ == "__main__":

    mgr = CommandManager()
    shell = ContractDACmdShell()

    shell_commands = [HelpCommand(shell), HistoryCommand(shell), SourceCommand(shell)]

    shell.initialize(mgr, shell_level_commands=shell_commands)
    shell.interactive_shell()


    
    
