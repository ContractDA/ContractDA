from contractda.cli import ContractDACmdShell
from contractda.cli.commands._cmd_mgr import CommandManager
from contractda.cli.commands._cli_commands import HelpCommand, HistoryCommand


if __name__ == "__main__":

    mgr = CommandManager()
    shell = ContractDACmdShell()

    shell_commands = [HelpCommand(shell), HistoryCommand(shell)]

    shell.initialize(mgr, shell_level_commands=shell_commands)
    shell.interactive_shell()


    
    
