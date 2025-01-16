from contractda.simulator import Simulator, Stimulus, ClauseEvaluator
from contractda.contracts import AGContract
from contractda.vars import Var, RealVar, IntVar
from contractda.sets import FOLClauseSet
if __name__ == "__main__":
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    c = AGContract([x, y, z], assumption="x <= 5 && y >= 3", guarantee="z == x + y")

    sim = Simulator(contract=c)

    success, failure = sim.auto_simulate(max_depth=3)
    for e in success:
        print("success: ", e)
    for e in failure:
        print("fail: ", e)