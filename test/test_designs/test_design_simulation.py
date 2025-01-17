import json
from contractda.design_api import DesignLevelManager

def test_design_simulation():
    design_path = "./example/design_files/simple_design_simulation.json"
    mgr = DesignLevelManager()
    mgr.read_design_from_file(file_path=design_path)

    system = mgr.get_system("sim_sys_1.sub2")
    stimulus = {system.ports["a"]: 7}
    ret = mgr.simulate_system(system="sim_sys_1.sub2", stimulus=stimulus)
    assert(len(ret) == 1)
    assert(ret[0].value(var = system.ports["a"].var) == 7)
    assert(ret[0].value(var = system.ports["t2"].var) == 14)


def test_design_autosimulation():
    design_path = "./example/design_files/simple_design_simulation.json"
    mgr = DesignLevelManager()
    mgr.read_design_from_file(file_path=design_path)
    _,_,_ = mgr.auto_simulate_system(system="sim_sys_1")
