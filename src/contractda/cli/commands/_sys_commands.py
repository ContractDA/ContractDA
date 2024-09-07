import argparse

from contractda.cli.commands._cmd_mgr import BaseCommand
from contractda.logger._logger import LOG

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