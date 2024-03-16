from contractda.contracts import CBContract
from contractda.vars import Var, RealVar

if __name__ == "__main__":
    I1 = RealVar("I1")
    I2 = RealVar("I2")
    V = RealVar("V")

    c1 = CBContract(vars = [I1, V], constraint="I1 * V <= 8", behavior="V == 2 * I1")
    c2 = CBContract(vars = [I2, V], constraint="I2 * V <= 16", behavior="V == 4 * I2")

    c12 = c1.composition(c2)
    print(c12)

    c3 = CBContract(vars = [I1, I2, V], constraint="(I1 + I2)*V <= 12", behavior="V == 4 * (I1 + I2) / 3")
    print(c3)
    print(c3.intrinsic_behavior)
    print(c3.is_refined_by(c12))

    c3 = CBContract(vars = [I1, I2, V], constraint="(I1 + I2)*V < 12", behavior="V == 4 * (I1 + I2) / 3")
    print(c3)
    print(c3.intrinsic_behavior)
    print(c3.is_refined_by(c12))
    
    c3 = CBContract(vars = [I1, I2, V], constraint="(I1 + I2)*V < 12.1", behavior="V == 4 * (I1 + I2) / 3")
    print(c3)
    print(c3.intrinsic_behavior)
    print(c3.is_refined_by(c12))

    c1 = CBContract(vars = [I1, V], constraint="I1 * V <= 6", behavior="V == 3 * I1")
    c2 = CBContract(vars = [I2, V], constraint="I2 * V <= 2", behavior="V == 6 * I2")

    c12 = c1.composition(c2)
    print(c12)
    c3 = CBContract(vars = [I1, I2, V], constraint="(I1 + I2)*V <= 5", behavior="V == 2 * (I1 + I2)")
    print(c3)
    print(c3.intrinsic_behavior)
    print(c3.is_refined_by(c12))