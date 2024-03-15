from contractda.contracts import CBContract
from contractda.vars import Var, RealVar

if __name__ == "__main__":
    I1 = RealVar("I1")
    I2 = RealVar("I2")
    V = RealVar("V")

    c1 = CBContract(vars = [I1, V], constraint="I1 * V <= 8", behavior="V == 2 * I1")
    c2 = CBContract(vars = [I2, V], constraint="I2 * V <= 16", behavior="V == 4 * I2")

    c1.composition(c2)
    print(c1)