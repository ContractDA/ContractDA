from contractda.design._design import Design
from contractda.design._system import System
from contractda.logger._logger import LOG
import json

class DesignLevelManager():
    def __init__(self):
        self._design = dict()
        self._systems = dict()
        self._ports = dict()
        self._connections = dict()
        self._map_port_to_system = dict()

    def read_design_json(self, json_obj):
        # TODO 1: read all systems in the design file
        system = System.from_dict(json_obj)
        self._systems[system.system_name] = system
        # 
        pass

    def read_system_json(self, json_obj):
        pass


    def read_design_from_file(self, file_path):
        # check file format
        # if format_is_json(file_path)
            with open(file_path, "r") as design_file:
                json_obj = json.load(design_file)
                self.read_design_json(json_obj)

    def create_empty_design(self, name):
        if name not in self._designs:
            new_design = Design(name=name)
            self._designs[name] = new_design
        else:
            LOG.error(f"Duplicate design name {name}")
        
    def check_system(self, system: str | System):
        pass

    def compile_system(self, system: str | System):
        system._frozen = True
        pass


    def set_objective():
        pass
