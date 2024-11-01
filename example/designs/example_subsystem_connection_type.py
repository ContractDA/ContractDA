import json
from contractda.design._system import System
from contractda.sets._fol_clause_set import FOLClauseSet
from contractda.design._design_mgr import DesignLevelManager

if __name__ == "__main__":
    design_mgr = DesignLevelManager()
    design_mgr.read_design_from_file("./example/design_files/simple_design.json")

    sys = design_mgr.get_system("test_sys")
    print(sys.is_cascade())
    print(sys.is_feedback())
    print(sys.is_parallel())

    design_mgr.read_design_from_file("./example/design_files/simple_design_feedback_composition.json")
    sys = design_mgr.get_system("test_sys_feedback_composition1")
    print(sys.is_cascade())
    print(sys.is_feedback())
    print(sys.is_parallel())