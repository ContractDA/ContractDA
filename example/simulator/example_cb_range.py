from contractda.simulator import Simulator, Stimulus, ClauseEvaluator
from contractda.contracts import CBContract
from contractda.vars import Var, RealVar, IntVar
from contractda.sets import FOLClauseSet


if __name__ == "__main__":
    I = RealVar("I")
    V = RealVar("V")
    c = CBContract([I, V], constraint="I*V <= 8", behavior="V == 2*I")

    obj = RealVar("obj")
    env = FOLClauseSet(vars = [I, V], expr="V >= 1 && V <= 2")
    print("Environment: ", env)
    print("Contract:", c)
    objective_clause = FOLClauseSet(vars = [I, V, obj], expr= "obj == I+V")
    print("Objective:", objective_clause)
    eval = ClauseEvaluator(objective_clause, clause_objective=[obj])
    sim = Simulator(contract=c, evaluator= eval)
    obj_val = sim.evaluate(environement=env)
    assert(obj_val[0] >= 1.5 and obj_val[0] <= 3)
    obj_val = sim.evaluate_range(environement=env)
    assert(obj_val == ([3.0], [1.5]))
    print("max: ", obj_val[0], "min:", obj_val[1])