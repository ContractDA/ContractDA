import json
from contractda.design._system import System
from contractda.sets._fol_clause_set import FOLClauseSet
from contractda.design_api._design_mgr import DesignLevelManager

if __name__ == "__main__":
    with open("./example/design_files/simple_design_composition1.json", "r") as file:
        json_obj = json.load(file)

    design_mgr = DesignLevelManager()
    design_mgr.read_design_json(json_obj)

    design = design_mgr.get_design("test_sys_composition1")
    design.report()
    print(design)
    print(design_mgr.verify_design_compatibility(design=design))
    print(design_mgr.verify_design_consistensy(design=design))
    print("Refinement:",design_mgr.verify_design_refinement(design=design))
    print("Indpendent:", design_mgr.verify_system_independent(system=design))

    with open("./example/design_files/simple_design_composition1_failure.json", "r") as file:
        json_obj = json.load(file)
    design_mgr.read_design_json(json_obj)
    design = design_mgr.get_design("test_sys_composition1_failure")
    design.report()
    print(design)
    print(design_mgr.verify_design_compatibility(design=design))
    print(design_mgr.verify_design_consistensy(design=design))
    print(design_mgr.verify_design_refinement(design=design))
    print("Indpendent:", design_mgr.verify_system_independent(system=design))

    with open("./example/design_files/simple_design_feedback_composition.json", "r") as file:
        json_obj = json.load(file)
    design_mgr.read_design_json(json_obj)
    design = design_mgr.get_design("test_sys_feedback_composition1")
    design.report()
    print(design)
    print(design_mgr.verify_design_compatibility(design=design))
    print(design_mgr.verify_design_consistensy(design=design))
    print(design_mgr.verify_design_refinement(design=design))
    print(design_mgr.verify_system_independent(system=design))
