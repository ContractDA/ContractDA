from contractda.simulator import Simulator, Stimulus, ClauseEvaluator
from contractda.contracts import AGContract
from contractda.vars import Var, RealVar, IntVar
from contractda.sets import FOLClauseSet
if __name__ == "__main__":
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    c = AGContract([x, y, z], assumption="x <= 5 && y >= 3", guarantee="z == x + y || z == x*y")

    sim = Simulator(contract=c)

    env, result = sim.auto_simulate(num_unique_simulations=1, use_generator=True)
    for success, failure in env:
        print("new pair: ")
        for e in success:
            print("    success: ", e)
        for e in failure:
            print("    fail: ", e)

    for sti, ret in result.items():
        print("result pair: ", sti)
        for success, failure in ret:
            for e in success:
                print("    success: ", e)
            for e in failure:
                print("    fail: ", e)