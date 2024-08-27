from contractda.cli import ContractDACmdShell
from contractda.cli.commands._cmd_mgr import CommandManager
from contractda.cli.commands._basic_commands import TestCommand, Test2Command, ExitCommand
import contractda.cli.commands._basic_commands as basic_commands


if __name__ == "__main__":

    mgr = CommandManager()

    shell = ContractDACmdShell()
    shell.initialize(mgr)
    shell.interactive_shell()


    
    
