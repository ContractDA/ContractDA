import pytest

from contractda.contracts import CBContract
from contractda.vars import Var, RealVar


def test_contract_composition_resistor():
    I1 = RealVar("I1")
    I2 = RealVar("I2")
    V = RealVar("V")
    c1 = CBContract(vars = [I1, V], constraint="I1 * V <= 8", behavior="V == 2 * I1")
    c2 = CBContract(vars = [I2, V], constraint="I2 * V <= 16", behavior="V == 4 * I2")

    c12 = c1.composition(c2)
    c12_gold = CBContract(vars = [I1, I2, V], constraint="I1 * V <= 8 && I2 * V <= 16", behavior="V == 2*I1 && V == 4 * I2")

    assert(c12.constraint.is_equivalence(c12_gold.constraint))
    assert(c12.intrinsic_behavior.is_equivalence(c12_gold.intrinsic_behavior))

def test_contract_refinement_resistor_1():
    I1 = RealVar("I1")
    I2 = RealVar("I2")
    V = RealVar("V")
    c1 = CBContract(vars = [I1, V], constraint="I1 * V <= 8", behavior="V == 2 * I1")
    c2 = CBContract(vars = [I2, V], constraint="I2 * V <= 16", behavior="V == 4 * I2")

    c12 = c1.composition(c2)
    for i10 in range(100, 150, 2):
        i = i10/10.0
        c3 = CBContract(vars = [I1, I2, V], constraint=f"(I1 + I2)*V <= {i}", behavior="V == 4 * (I1 + I2) / 3")
        if i <= 12:
            assert(c3.is_refined_by(c12) == True)
        else:
            assert(c3.is_refined_by(c12) == False)

def test_contract_refinement_resistor_2():
    I1 = RealVar("I1")
    I2 = RealVar("I2")
    V = RealVar("V")
    c1 = CBContract(vars = [I1, V], constraint="I1 * V <= 6", behavior="V == 3 * I1")
    c2 = CBContract(vars = [I2, V], constraint="I2 * V <= 2", behavior="V == 6 * I2")

    c12 = c1.composition(c2)
    for i10 in range(50, 100, 2):
        i = i10/10.0
        # gold: <= 6
        c3 = CBContract(vars = [I1, I2, V], constraint=f"(I1 + I2)*V <= {i}", behavior="V == 2 * (I1 + I2)")
        if i <= 6:
            assert(c3.is_refined_by(c12) == True)
        else:
            assert(c3.is_refined_by(c12) == False)

def test_contract_refinement_resistor_3():
    I1 = RealVar("I1")
    I2 = RealVar("I2")
    V = RealVar("V")
    c1 = CBContract(vars = [I1, V], constraint="I1 * V <= 6", behavior="V == 3 * I1")
    c2 = CBContract(vars = [I2, V], constraint="I2 * V <= 4", behavior="V == 6 * I2")

    c12 = c1.composition(c2)
    for i10 in range(75, 125, 2):
        i = i10/10.0
        # gold: <= 9
        c3 = CBContract(vars = [I1, I2, V], constraint=f"(I1 + I2)*V <= {i}", behavior="V == 2 * (I1 + I2)")
        if i <= 9:
            assert(c3.is_refined_by(c12) == True)
        else:
            assert(c3.is_refined_by(c12) == False)