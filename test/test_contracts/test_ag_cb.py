import pytest
import math
from contractda.contracts import CBContract, AGContract
from contractda.vars import Var, RealVar

def test_cb_ag_compatibility():
    I1 = RealVar("I1")
    I2 = RealVar("I2")
    V = RealVar("V")
    c1 = CBContract(vars = [I1, V], constraint="I1 * V <= 6", behavior="V == 3 * I1")
    c2 = CBContract(vars = [I2, V], constraint="I2 * V <= 2", behavior="V == 6 * I2")

    c12 = c1.composition(c2)

    c3 = CBContract(vars = [I1, I2, V], constraint="(I1 + I2)*V <= 6", behavior="V == 2 * (I1 + I2)")



    # golden value sqrt(10) because at this point V = 2*sqrt(3), I1 + I2 = sqrt(3), I1 = 2/3*sqrt(3), I2 = 1/3 * sqrt(3)
    # the constraint I2*V <= 2 reaches the boundary 
    for i100 in range(330,370, 2):
        i = i100/100.0
        cag = AGContract(vars=[I1, I2, V], assumption=f"V <= {i} && V >= 0", guarantee="V == 2 * (I1 + I2)")
        if i <= 2*math.sqrt(3):
            assert(cag.is_refined_by(c12) == True)
            assert(cag.is_refined_by(c3) == True)
            assert(c12.is_refined_by(cag) == False)
            assert(c3.is_refined_by(cag) == False)

