from contractda.contracts import CBContract, AGContract
from contractda.vars import Var, RealVar

if __name__ == "__main__":
    I1 = RealVar("I1")
    I2 = RealVar("I2")
    V = RealVar("V")

    c1 = CBContract(vars = [I1, V], constraint="I1 * V <= 6", behavior="V == 3 * I1")
    c2 = CBContract(vars = [I2, V], constraint="I2 * V <= 2", behavior="V == 6 * I2")

    cs = c1.composition(c2)
    print("cs: ", cs)
    c3 = CBContract(vars = [I1, I2, V], constraint="(I1 + I2)*V <= 5", behavior="V == 2 * (I1 + I2)")
    print("Is c3 refined by composition of c1 and c2?")
    print(c3.is_refined_by(cs))

    cag = AGContract(vars=[I1, I2, V], assumption="V <= 3.2 && V >= 0", guarantee="V == 2 * (I1 + I2)")
    print("Is cag refined by c3?")
    print(cag.is_refined_by(c3))
