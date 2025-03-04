from contractda.design_api import DesignLevelManager, DesignExpression
from contractda.simulator import Simulator, Stimulus, ClauseEvaluator
from contractda.vars import RealVar
from contractda.sets import FOLClauseSet

if __name__ == "__main__":
    design_path = "./example/design_files/simple_design_simulation.json"
    mgr = DesignLevelManager()
    mgr.read_design_from_file(file_path=design_path)

    obj = RealVar("obj")

    print("1")
    system = mgr.get_system("sim_sys_1")
    system.report()
    stimulus = {system.ports["a"]: 5}
    print(stimulus)
    ret = mgr.evaluate_system(system="sim_sys_1", 
                              objective=DesignExpression(expr="obj == sim_sys_1.a + sim_sys_1.x", aux_vars=[obj], clause_type=FOLClauseSet),
                              stimulus=stimulus,
                              system_compose_level=0)
    print(ret[0])

    ret = mgr.evaluate_system(system="sim_sys_1", 
                              objective=DesignExpression(expr="obj == sim_sys_1.a + sim_sys_1.sub1.t", aux_vars=[obj], clause_type=FOLClauseSet),
                              stimulus=stimulus,
                              system_compose_level=1)
    print(ret[0])

    ret = mgr.evaluate_system(system="sim_sys_1", 
                              objective=DesignExpression(expr="obj == sim_sys_1.a + sim_sys_1.x", aux_vars=[obj], clause_type=FOLClauseSet),
                              environement=DesignExpression(expr="sim_sys_1.a >= 4.2 && sim_sys_1.a <= 4.5"),
                              system_compose_level=0)
    print(ret[0])
    ret = mgr.evaluate_system(system="sim_sys_1", 
                              objective=DesignExpression(expr="obj == sim_sys_1.a + sim_sys_1.x", aux_vars=[obj], clause_type=FOLClauseSet),
                              environement=DesignExpression(expr="sim_sys_1.a >= 4.2 && sim_sys_1.a <= 4.5"),
                              system_compose_level=1)
    print(ret[0])

    ret = mgr.evaluate_range_system(system="sim_sys_1", 
                              objective=DesignExpression(expr="obj == sim_sys_1.a + sim_sys_1.x", aux_vars=[obj], clause_type=FOLClauseSet),
                              environement=DesignExpression(expr="sim_sys_1.a >= 3 && sim_sys_1.a <= 4"),
                              system_compose_level=0)
    print(ret)

