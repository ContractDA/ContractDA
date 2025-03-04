from contractda.vars import Var, RealVar, IntVar
from contractda.sets import FOLClauseSet
from contractda.contracts import AGContract
from contractda.simulator import Simulator, Stimulus
import random
from matplotlib import pyplot as plt

if __name__ == "__main__":
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    w = RealVar("w")
    f = RealVar("f")

    c = AGContract(vars=[x, y, z, w], assumption="2 <= x && x <= 8", guarantee="z==2*x && y == 2*w")
    simulator = Simulator(contract=c)
    env = FOLClauseSet(vars = [x, y, z, w, f], expr="(2<=x && x < 3) && (w == z && f == y/x)")
    pure_env = FOLClauseSet(vars = [x, y, z, w, f], expr="(w == z && f == y/x)")
    ret = simulator.simulate(environement=env)
    print(ret[0])

    # sweep to generate all values
    xs = [i/10.0 for i in range(20, 82, 2)]
    results = []
    for x_value in xs:
        print(x_value)
        s1 = Stimulus(stimulus_map={x: x_value})
        ret = simulator.simulate(stimulus=s1, environement=pure_env)
        results.append(ret[0])

    for r in results:
        print(r)

    y = [r.value(y) for r in results]
    f = [r.value(f) for r in results]
    print(y)
    print(f)

    plt.rcParams['text.usetex'] = True
    fig = plt.figure(figsize=(6, 3))
    plt.plot(xs, y, marker='o', linestyle='-', color='r', label='y')
    plt.plot(xs, f, marker='o', linestyle='-', color='b', label='f')
    plt.legend()
    plt.ylim(0, 35)
    plt.ylabel("value")
    plt.xlabel("x")
    #plt.show()
    plt.minorticks_on()
    # Customize minor ticks (remove labels but keep ticks visible)
    plt.tick_params(axis='y', which='minor', length=4, color='gray', labelbottom=False)
    plt.grid(True)
    plt.savefig('contract_sweep.pdf', bbox_inches="tight")
