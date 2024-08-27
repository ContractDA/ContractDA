import inspect

from abc import ABC
from contractda.logger._logger import LOG
from contractda.cli.commands._base_command import BaseCommand
import contractda.cli.commands._basic_commands as basic_commands
import contractda.cli.commands._sys_commands as sys_commands

class CommandManager():
    """Class for managing all command"""
    def __init__(self):
        self._command_map: dict = dict()
        self.get_commands_in_module(basic_commands)
        self.get_commands_in_module(sys_commands)
        
    def get_commands_in_module(self, module):
        classes = inspect.getmembers(module, inspect.isclass)
        for cls_name, cls in classes:
            LOG.debug(f"Class {cls_name} found!")
            if issubclass(cls, BaseCommand) and cls_name != "BaseCommand":
                LOG.debug(f"Class {cls_name} found as a command")
                self.add_command(cls())


    def add_command(self, new_command: BaseCommand):
        # need to check conflict
        name = new_command.name
        if name in self._command_map:
            LOG.error(f"Command {name} already exists, the original one will be replaced...")
        self._command_map[name] = new_command

    def get_command_names(self):
        return self._command_map.keys()
    
    def execute_command(self, command_name, *args):
        command = self.get_command(command_name)
        if command is None:
            LOG.error(f"Unknown Command {command_name}")
            return -1
        try:
            ret = command.exec(*args)
        except NotImplementedError:
            LOG.error(f"Command {command_name} is currently not supported!")
            ret = -1

        return ret
    
    def get_command(self, command_name: str) -> BaseCommand | None:
        if command_name in self._command_map:
            return self._command_map[command_name]
        else:
            return None
    


