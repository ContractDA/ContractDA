import argparse

from contractda.cli.commands._cmd_mgr import BaseCommand
from contractda.logger._logger import LOG
from contractda.design._design_exceptions import ObjectNotFoundException, IncompleteContractException

class ReadDesignFromFileCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "read_design_from_file"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("-file", type=str, help="File name", required=True)
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        
        try:
            file_path = parsed_args.file
            print(file_path)
            self.context._design_mgr.read_design_from_file(file_path)
        except:
            print("Error during execution")
            return -1
        return 0
    
class ReportDesignCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "report_design"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("design_name", type=str, help="design name")
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        except Exception as e:
            print("?????")
            print(type(e))
            return -1
        
        design_name = parsed_args.design_name      
        design = self.context._design_mgr.get_design(design_name)
        if design is None:
            err_msg = f"design {design_name} does not exist!"
            LOG.error(err_msg)
            print(err_msg)
            return -1
        design.report()
        return 0

class ReportSystemCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "report_system"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("system_name", type=str, help="system name")
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        except Exception as e:
            print("?????")
            print(type(e))
            return -1
        
        system_name = parsed_args.system_name      
        system = self.context._design_mgr.get_system(system_name)
        if system is None:
            err_msg = f"system {system_name} does not exist!"
            LOG.error(err_msg)
            print(err_msg)
            return -1
        system.report()
        return 0
    
class ReportSystemsCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "report_systems"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        except Exception as e:
            print(type(e))
            return -1
        
        print(len(self.context._design_mgr._systems.values()), "systems")
        for sys in self.context._design_mgr._systems.values():
            print(sys.hier_name)
        return 0
    
class ReportDesignsCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "report_designs"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        except Exception as e:
            print(type(e))
            return -1
        
        print(len(self.context._design_mgr._designs.values()), "designs")
        for sys in self.context._design_mgr._designs.values():
            print(sys.hier_name)
        return 0
    
class ReportPortCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "report_port"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("port_name", type=str, help="port name")
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        except Exception as e:
            print("?????")
            print(type(e))
            return -1
        
        port_name = parsed_args.port_name      
        port = self.context._design_mgr.get_port(port_name)
        if port is None:
            err_msg = f"port {port_name} does not exist!"
            LOG.error(err_msg)
            print(err_msg)
            return -1
        port.report()
        return 0
    
class ReportConnectionCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "report_connection"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("connection_name", type=str, help="connection name")
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        except Exception as e:
            print("?????")
            print(type(e))
            return -1
        
        conn_name = parsed_args.connection_name      
        conn = self.context._design_mgr.get_connection(conn_name)
        if conn is None:
            err_msg = f"connection {conn_name} does not exist!"
            LOG.error(err_msg)
            print(err_msg)
            return -1
        conn.report()
        return 0
    
class VerifyDesignCompatibilityCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "verify_design_compatibility"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("design_name", type=str, help="design name")
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        except Exception as e:
            print("?????")
            print(type(e))
            return -1
        
        design_name = parsed_args.design_name      
        try:
            ret = self.context._design_mgr.verify_design_compatibility(design=design_name)
        except ObjectNotFoundException as e:
            error_msg = f"{str(e)}"
            LOG.info(error_msg)
            print(error_msg)
            return -1
                    
        if ret:
            info_msg = f"Not all contracts are compatible"
            LOG.info(info_msg)
            print(info_msg)
            for sys, fail_list in ret.items():
                contract_names_str = ", ".join([system_contract.name for system_contract in fail_list])
                info_msg = f"{sys.system_name}: ({contract_names_str})"
                LOG.info(info_msg)
            return 0
        else:
            info_msg = f"All contracts are compatible"
            LOG.info(info_msg)
            print(info_msg)
            return 0
        return 0
    
class VerifySystemCompatibilityCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "verify_system_compatibility"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("system_name", type=str, help="system name")
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        except Exception as e:
            print("?????")
            print(type(e))
            return -1
        
        system_name = parsed_args.system_name      
        try:
            ret = self.context._design_mgr.verify_system_compatibility(system=system_name)
        except ObjectNotFoundException as e:
            error_msg = f"{str(e)}"
            LOG.info(error_msg)
            print(error_msg)
            return -1
                    
        if ret:
            info_msg = f"Not all contracts are compatible"
            LOG.info(info_msg)
            print(info_msg)
            contract_names_str = ", ".join([system_contract.name for system_contract in ret])
            info_msg = f"Incompatible contracts: ({contract_names_str})"
            LOG.info(info_msg)
            return 0
        else:
            info_msg = f"All contracts are compatible"
            LOG.info(info_msg)
            print(info_msg)
            return 0
        return 0
    
class VerifyDesignConsistensyCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "verify_design_consistensy"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("design_name", type=str, help="design name")
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        except Exception as e:
            print("?????")
            print(type(e))
            return -1
        
        design_name = parsed_args.design_name      
        try:
            ret = self.context._design_mgr.verify_design_consistensy(design=design_name)
        except ObjectNotFoundException as e:
            error_msg = f"{str(e)}"
            LOG.info(error_msg)
            print(error_msg)
            return -1
                    
        if ret:
            info_msg = f"Not all contracts are consistent"
            LOG.info(info_msg)
            print(info_msg)
            for sys, fail_list in ret.items():
                contract_names_str = ", ".join([system_contract.name for system_contract in fail_list])
                info_msg = f"{sys.system_name}: ({contract_names_str})"
                LOG.info(info_msg)
            return 0
        else:
            info_msg = f"All contracts are consistent"
            LOG.info(info_msg)
            print(info_msg)
            return 0
        return 0
    
class VerifySystemConsistensyCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "verify_system_consistensy"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("system_name", type=str, help="system name")
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        except Exception as e:
            print("?????")
            print(type(e))
            return -1
        
        system_name = parsed_args.system_name      
        try:
            ret = self.context._design_mgr.verify_system_consistensy(system=system_name)
        except ObjectNotFoundException as e:
            error_msg = f"{str(e)}"
            LOG.info(error_msg)
            print(error_msg)
            return -1
                    
        if ret:
            info_msg = f"Not all contracts are consistent"
            LOG.info(info_msg)
            print(info_msg)
            contract_names_str = ", ".join([system_contract.name for system_contract in ret])
            info_msg = f"Incompatible contracts: ({contract_names_str})"
            LOG.info(info_msg)
            return 0
        else:
            info_msg = f"All contracts are consistent"
            LOG.info(info_msg)
            print(info_msg)
            return 0
        return 0
    
class VerifyDesignRefinementCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "verify_design_refinement"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("design_name", type=str, help="design name")
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        except Exception as e:
            print("?????")
            print(type(e))
            return -1
        
        design_name = parsed_args.design_name      
        try:
            ret = self.context._design_mgr.verify_design_refinement(design=design_name)
        except ObjectNotFoundException as e:
            error_msg = f"{str(e)}"
            LOG.info(error_msg)
            print(error_msg)
            return -1
                    
        if ret:
            info_msg = f"Not all systems satisfy refinement relation with their subsystems"
            LOG.info(info_msg)
            print(info_msg)

            system_names_str = ", ".join([system.hier_name for system in ret])
            info_msg = f"Refinement violation systems: ({system_names_str})"
            LOG.info(info_msg)
            return 0
        else:
            info_msg = f"All systems satisfy the refinement relation with their subsystems"
            LOG.info(info_msg)
            print(info_msg)
            return 0
        return 0
    
class VerifySystemRefinementCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "verify_system_refinement"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("system_name", type=str, help="system name")
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        except Exception as e:
            print("?????")
            print(type(e))
            return -1
        
        system_name = parsed_args.system_name      
        try:
            ret = self.context._design_mgr.verify_system_refinement(system=system_name)
        except ObjectNotFoundException as e:
            error_msg = f"{str(e)}"
            LOG.info(error_msg)
            print(error_msg)
            return -1
        except IncompleteContractException as e:
            error_msg = f"{str(e)}"
            LOG.info(error_msg)
            print(error_msg)
            return -1            
                    
        if not ret:
            info_msg = f"The system \"{system_name}\" does not satisfy refinement with its subsystems"
            LOG.info(info_msg)
            print(info_msg)
            return 0
        else:
            info_msg = f"The system \"{system_name}\" satisfy refinement with its subsystems"
            LOG.info(info_msg)
            print(info_msg)
            return 0
        return 0
    
class VerifyDesignConnectionCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "verify_design_connection"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("design_name", type=str, help="design name")
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        except Exception as e:
            print("?????")
            print(type(e))
            return -1
        
        design_name = parsed_args.design_name      
        try:
            ret = self.context._design_mgr.verify_design_connection(design=design_name)
        except ObjectNotFoundException as e:
            error_msg = f"{str(e)}"
            LOG.info(error_msg)
            print(error_msg)
            return -1
                    
        if ret:
            info_msg = f"Connections error found in systems: "
            LOG.info(info_msg)
            print(info_msg)

            system_names_str = ", ".join([system.hier_name for system in ret])
            info_msg = f"Violated system list: ({system_names_str})"
            LOG.info(info_msg)
            return 0
        else:
            info_msg = f"Connections are well-defined in systems"
            LOG.info(info_msg)
            print(info_msg)
            return 0
        return 0
    
class VerifySystemConnectionCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "verify_system_connection"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("system_name", type=str, help="system name")
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            print(e)
            return -1
        except Exception as e:
            print("?????")
            print(type(e))
            return -1
        
        system_name = parsed_args.system_name      
        try:
            ret = self.context._design_mgr.verify_system_connection(system=system_name)
        except ObjectNotFoundException as e:
            error_msg = f"{str(e)}"
            LOG.info(error_msg)
            print(error_msg)
            return -1
                    
        if not ret:
            info_msg = f"The system \"{system_name}\" has connection error"
            LOG.info(info_msg)
            print(info_msg)
            return 0
        else:
            info_msg = f"The system \"{system_name}\"'s connectioin is well-defined"
            LOG.info(info_msg)
            print(info_msg)
            return 0
        
class AutoSimulateSystemCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.name = "auto_simulate_system"
    
    def exec(self, *args):
        parser = argparse.ArgumentParser(prog=self.name, exit_on_error=False)
        parser.add_argument("system_name", type=str, help="system name")
        parser.add_argument("-num", type=int, help="number of unique behavior", default=1)
        parser.add_argument("-depth", type=int, help="number of unique behavior", default=3)
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return -1
        except argparse.ArgumentError as e:
            return -1
        except Exception as e:
            return -1
        
        system_name = parsed_args.system_name    
        num_unique_simulations = parsed_args.num
        max_depth = parsed_args.depth  
        try:
            sim_behaviors, violate_behaviors, result_map = self.context._design_mgr.auto_simulate_system(system=system_name, 
                                                                num_unique_simulations=num_unique_simulations, 
                                                                max_depth=max_depth)
        except ObjectNotFoundException as e:
            error_msg = f"{str(e)}"
            LOG.info(error_msg)
            print(error_msg)
            return -1

        print("Simulation Behavior")     
        for behavior in sim_behaviors:
            print(behavior)
            for ret in result_map[behavior]:
                print("    ", ret)

        print("Violation Inputs")
        for behavior in violate_behaviors:
            print(behavior)