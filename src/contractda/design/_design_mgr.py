from contractda.design._design import Design
from contractda.design._system import System
from contractda.logger._logger import LOG

class DesignLevelManager():
    def __init__(self):
        self._designs = dict()

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
