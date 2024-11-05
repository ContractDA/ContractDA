from contractda.simulator import Simulator, Stimulus
from contractda.contracts import AGContract
from contractda.vars import Var, RealVar

if __name__ == "__main__":
    x = RealVar("x")
    y = RealVar("y")
    c = AGContract([x, y], assumption="x >= 0", guarantee="y <= 2*x && y >= 1.8*x")

    sti = Stimulus({x: 50})
    #prober = [y]
    sim = Simulator(contract=c)
    sim.simulate(stimulus = sti) # need a prober to specify what we are interested to see