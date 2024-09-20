
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
        """Read the design from a json file"""
        system = System.from_dict(json_obj, self)
        if system.system_name in self._designs:
            LOG.error(f"Design name {system.system_name} already existed! Reading aborted!")
            return 
        self.register_design(system=system)

    def export_design_json(self, system: str | System):
        """Write the design to a json file"""

    def read_design_from_file(self, file_path):
        # check file format
        # if format_is_json(file_path)
            with open(file_path, "r") as design_file:
                json_obj = json.load(design_file)
                self.read_design_json(json_obj)
        
    def check_system(self, system: str | System):
        pass

    def verify_design(self, system: str | System):
        """Verify if the design has any potential issues
        This function encapsulate many verification problems and summarize the result.
        """
        pass

    def verify_system(self, system: str | System):
        """Verify if the design has any potential issues
        This function encapsulate many verification problems and summarize the result.
        """
        pass

    def verify_design_refinement(self, system: str | System, hierarchical=True):
        """Verify if the given design satisfy refinement relation, hierarchical mean if the relation need to checked hierarchically"""
        system_obj = self._verify_system_obj_or_str(system=system)

    def verify_system_refinement(self, system: str | System, hierarchical=True):
        """Verify if the given design satisfy refinement relation, hierarchical mean if the relation need to checked hierarchically"""
        system_obj = self._verify_system_obj_or_str(system=system)
        


    def verify_design_independent(self, system: str | System, hierarchical=True):
        """Verify if the given design may suffer from incompatible problems during independent design process"""
        if isinstance(system, str):
            system = self.get_design(system)
        if system is None:
            LOG.error(f"No such design, verification fails")
            return 
        
    def verify_system_independent(self, system: str | System, hierarchical=True):
        """Verify if the given design satisfy refinement relation, hierarchical mean if the relation need to checked hierarchically"""
        system_obj = self._verify_system_obj_or_str(system=system)
        
        # to verify independent design in system
        # 1. detect feedback loop
        # 2. bottom up: find leaf systems and check if they are receptive
        # 3. propagate leaf system up for pure refinement
        # 4. detect loop: composition of receptive does not guarantee to be receptive
        # 3. color up all those systems up that can be ensured to be receptive
        # 2. if feedback loop does not exist, check if receptive can be established -> should be done bottom up?
        # 2. For feedback loop, check feedback condition
        # 3. For system not involve in feedback loop, try to estabilish its receptiveness. check strong replaceability
        # 4. check receptiveness in the leaf
        # 5. 
        system.verify_contract_in

    def verify_design_connection(self, system: str | System, hierarchical=True):
        pass

    def verify_system_connection(self, system: str | System, hierarchical=True):
        pass

    def verify_design_consistensy(self, system: str | System, hierarchical=True):
        system_obj = self._verify_system_obj_or_str(system=system)
        pass

    def verify_system_consistensy(self, system: str | System, hierarchical=True) -> bool:
        """Check if the system contracts in a system are consistent

        :param str | System system: the system instance or its name for checking contract consistency
        :param VarType | str port_type: the type of the port
        :param PortDirection | str direction: the direction of the port. See PortDirection
        """
        system_obj = self._verify_system_obj_or_str(system=system)
        self._generate_system_contracts(system_obj)
        inconsistent_contracts = []
        for contract in system_obj.contracts:
            if not contract.contract_obj.is_consistent():
                inconsistent_contracts.append(contract)
        return len(inconsistent_contracts) == 0
        


    def verify_design_compatibility(self, system: str | System, hierarchical=True):
        pass

    def verify_system_compatibility(self, system: str | System, hierarchical=True):
        """Check if the system contracts in a system are consistent

        :param str | System system: the system instance or its name for checking contract consistency
        :param VarType | str port_type: the type of the port
        :param PortDirection | str direction: the direction of the port. See PortDirection
        """
        system_obj = self._verify_system_obj_or_str(system=system)
        self._generate_system_contracts(system_obj)
        inconsistent_contracts = []
        for contract in system_obj.contracts:
            if not contract.contract_obj.is_compatible():
                inconsistent_contracts.append(contract)
        return len(inconsistent_contracts) == 0

    def synthesize_systems(self):
        pass

    def simulate_design(self, system: str | System, simulator):
        pass

    def simulate_system(self, system: str | System, simulator):
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

    def _generate_system_contracts(self, system: System):
        system._convert_system_contract_to_contract_object()
        for subsystem in system.subsystems.values():
            self._generate_system_contracts(system=subsystem)

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
        
    def _verify_system_obj_or_str(self, system: str | System) :
        if isinstance(system, str):
            system_obj = self.get_system(system)
        elif isinstance(system, System):
            system_obj = system
        else:
            LOG.error(f"argument system must be a instance of string or System")
            raise Exception(f"Type Error")

        if system_obj is None:
            LOG.error(f"No such system {system}")
            raise Exception(f"Object not found")
        if system_obj.system_name not in self._systems:
            LOG.error(f"No such system {system_obj.system_name}")
            raise Exception(f"Object not found")
        if self.get_system(system_obj.system_name) != system_obj:
            LOG.error(f"System registered not matched with the instance")
            raise Exception(f"Object not found")
        return system_obj
    
    def _verify_design_obj_or_str(self, design: str | System) :
        if isinstance(design, str):
            design_obj = self.get_system(design)
        elif isinstance(design, System):
            design_obj = design
        else:
            LOG.error(f"argument design must be a instance of string or System")
            raise Exception(f"Type Error")

        if design_obj is None:
            LOG.error(f"No such design {design}")
            raise Exception(f"Object not found")
        if design_obj.system_name not in self._systems:
            LOG.error(f"No such design {design_obj.system_name}")
            raise Exception(f"Object not found")
        if self.get_system(design_obj.system_name) != design_obj:
            LOG.error(f"Design registered not matched with the instance")
            raise Exception(f"Object not found")
        return design_obj

def _build_hier_name(hier_names):
    return ".".join(hier_names)
    

def _decode_hier_name(hier_name):
    return hier_name.split(".")



