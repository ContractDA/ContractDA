from contractda.simulator import Simulator, Stimulus, ClauseEvaluator
from contractda.contracts import AGContract
from contractda.vars import Var, RealVar
from contractda.sets import FOLClauseSet
if __name__ == "__main__":
    x = RealVar("x")
    y = RealVar("y")
    c = AGContract([x, y], assumption="x >= 0", guarantee="y <= 2*x && y >= 1.8*x")

    sti = Stimulus({x: 50})
    obj = RealVar("obj")

    eval = ClauseEvaluator(FOLClauseSet(vars = [x, y, obj], expr= "obj == y"), clause_objective=[obj])
    
    #prober = [y]
    sim = Simulator(contract=c, evaluator= eval)
    sim.simulate(stimulus = sti) # need a prober to specify what we are interested to see
    #FOLClauseSet([x], expr="x")
    obj_val = sim.evaluate(stimulus=sti)
    print(f"obj: {obj_val}")
    obj_val = sim.evaluate_range(stimulus=sti)
    print(f"max obj: {obj_val}")
