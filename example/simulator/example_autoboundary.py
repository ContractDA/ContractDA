from contractda.simulator import Simulator, Stimulus, ClauseEvaluator
from contractda.contracts import AGContract
from contractda.vars import Var, RealVar, IntVar
from contractda.sets import FOLClauseSet
if __name__ == "__main__":
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    c = AGContract([x, y, z], assumption="x <= 5 && y >= 3", guarantee="z == x + y")

    ib, ob = c.assumption.generate_boundary_set(max_depth=3)
    for i in ib:
        print("in", i)
    for o in ob:
        print("ex", o)

    print()
    c = AGContract([x, y, z], assumption="(x <= 5 && x >= 3) || (y >= 3 && y<= 4)", guarantee="z == x + y")

    ib, ob = c.assumption.generate_boundary_set(max_depth=3)
    print(len(ib), len(ob))
    for i in ib:
        print("in", i)
    for o in ob:
        print("ex", o)

    c = AGContract([x, y, z], assumption="(x <= 5 && x >= 3) || (!(y >= 3))", guarantee="z == x + y")
    print()
    ib, ob = c.assumption.generate_boundary_set(max_depth=3)
    print(len(ib), len(ob))
    for i in ib:
        print("in", i)
    for o in ob:
        print("ex", o)
    # sti = Stimulus({x: 50})
    # obj = RealVar("obj")

    # eval = ClauseEvaluator(FOLClauseSet(vars = [x, y, obj], expr= "obj == y"), clause_objective=[obj])
    
    # #prober = [y]
    # sim = Simulator(contract=c, evaluator= eval)
    # ret = sim.simulate(stimulus = sti, num_unique_simulations=10) # need a prober to specify what we are interested to see
    # for beh in ret:
    #     print(beh)
    # # FOLClauseSet([x], expr="x")
    # obj_val = sim.evaluate(stimulus=sti)
    # print(f"obj: {obj_val}")
    # obj_val = sim.evaluate_range(stimulus=sti)
    # print(f"max obj: {obj_val}")
