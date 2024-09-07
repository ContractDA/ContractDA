import json
from contractda.design._system import System
from contractda.design._design_mgr import DesignLevelManager

if __name__ == "__main__":
    with open("./example/design_files/simple_design.json", "r") as file:
        json_obj = json.load(file)

    sys = System.from_dict(json_obj)
    design_mgr = DesignLevelManager()
    design_mgr.register_design(sys)

    design = design_mgr.get_design("test_sys")
    design.report()
    print(design)

    sys1 = design_mgr.get_system("test_sys.sub1")
    sys1.report()
    for port_name, port in sys1.ports.items():
        print(port)
        port.report()
