import json
from contractda.design._system import System
from contractda.design._design_mgr import DesignLevelManager

if __name__ == "__main__":
    with open("./example/design_files/simple_design.json", "r") as file:
        json_obj = json.load(file)

    sys = System.from_dict(json_obj)
    design_mgr = DesignLevelManager()
    design_mgr.register_system(sys)

    print(design_mgr._connections)
