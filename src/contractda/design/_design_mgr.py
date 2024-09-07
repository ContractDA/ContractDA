
from contractda.design._system import System, Port, Connection
from contractda.logger._logger import LOG
import json

class DesignLevelManager():
    """The manager for all objects and the interface to perform system level task
    Mapping of names uses hierarchical names to avoid conflicts.
    """
    def __init__(self):
        self._systems = dict()
        self._ports = dict()
        self._connections = dict()
        self._modules = dict()
        self._libs = dict()

        self._designs: dict[str, System] = dict()# the entry to the top level systems


    def read_design_json(self, json_obj):
        system = System.from_dict(json_obj, self)
        if system.system_name in self._designs:
            LOG.error(f"Design name {system.system_name} already existed! Reading aborted!")
            return 
        self.register_design(system=system)

    def read_design_from_file(self, file_path):
        # check file format
        # if format_is_json(file_path)
            with open(file_path, "r") as design_file:
                json_obj = json.load(design_file)
                self.read_design_json(json_obj)
        
    def check_system(self, system: str | System):
        pass

    def register_design(self, system: System):
        """Puts the systems, ports, and connections in the manager
        Recursively put them in the manager for every subsystem
        """
        tmp_sys: dict = dict() 
        tmp_ports:  dict = dict() 
        tmp_connections:  dict = dict() 
        hier_names = []
        self._designs[system.system_name] = system

        self._register_system(system, tmp_sys, tmp_ports, tmp_connections, hier_names)

        try:
            self._systems.update(tmp_sys)
            self._ports.update(tmp_ports)
            self._connections.update(tmp_connections)
        except Exception:
            LOG.error("Unknown error when registering systems.")

        return 

    @staticmethod
    def _register_system(system: System, tmp_sys, tmp_ports, tmp_connections, hier_names):
        # systems
        LOG.debug(f"Registering system {system.system_name}")
        

        hier_names_level = list(hier_names)
        hier_names_level.append(system.system_name)
        
        tmp_sys[_build_hier_name(hier_names_level)] = system
        system._set_hier_name(_build_hier_name(hier_names_level))
        # ports
        for port in system.ports.values():
            hier_names_port = hier_names_level + [port.port_name]
            tmp_ports[_build_hier_name(hier_names_port)] = port
        # connection
        for connection in system.connections.values():
            hier_names_conn = hier_names_level + [connection.name]
            tmp_connections[_build_hier_name(hier_names_conn)] = connection

        # recursive for subsystems
        for subsystem in system.subsystems.values():
            DesignLevelManager._register_system(subsystem, tmp_sys, tmp_ports, tmp_connections, hier_names_level)

    def summary(self):
        print(f"======== Design Manager Summary ========")
        print(f"     Systems: {len(self._systems)}")
        print(f"     Ports: {len(self._ports)}")
        print(f"     Connections: {len(self._connections)}")

    def get_system(self, name: str) -> System | None:
        if name in self._systems:
            return self._systems[name]
        else:
            return None
        
    def get_port(self, name: str) -> Port | None:
        if name in self._ports:
            return self._ports[name]
        else:
            return None

    def get_connection(self, name: str) -> Connection | None:
        if name in self._connections:
            return self._connections[name]
        else:
            return None

    def get_design(self, name: str) -> System | None:
        if name in self._designs:
            return self._designs[name]
        else:
            return None

def _build_hier_name(hier_names):
    return ".".join(hier_names)
    

def _decode_hier_name(hier_name):
    return hier_name.split(".")



