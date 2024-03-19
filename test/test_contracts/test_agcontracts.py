import pytest

from contractda.contracts import AGContract
from contractda.vars import Var, RealVar
from contractda.solvers import Z3Interface

def test_ag_contract_quotient():
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")

    c1 = AGContract(vars=[x, z], assumption="x >= 0", guarantee="z == 2 * x")
    c2 = AGContract(vars=[y, z], assumption="z >= 1", guarantee="y == 2 * z")
    c3 = AGContract(vars=[x, y], assumption="x >= 2", guarantee="y == 4 * x")

    c2_q = c3.quotient(c1)
    print(c2_q)
    assert(c2_q.is_refined_by(c2) == True)
    assert(c2.is_refined_by(c2_q) == False)

    c3_new = c2_q.composition(c1)
    assert(c3.is_refined_by(c3_new) == True)
    assert(c3_new.is_refined_by(c3) == False)

def test_ag_contract_conjunction():
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")

    c1 = AGContract(vars=[x, y], assumption="x >= 0 && x <= 10", guarantee="y <= 1.2*x && y >= 0.8 * x")
    c2 = AGContract(vars=[x, y], assumption="x > 10", guarantee="y <= 1.1*x && y >= 0.9 * x")
    cs = AGContract(vars=[x, y], assumption="x >= 0", guarantee="y <= 1.1*x + 1 && y >= 0.9*x - 1")
    c12 = c1.conjunction(c2)
    assert(cs.is_refined_by(c12))
    assert(c1.is_refined_by(c12))
    assert(c2.is_refined_by(c12))
    assert(c12.is_refined_by(c1) == False)
    assert(c12.is_refined_by(c2) == False)
    assert(c12.is_refined_by(cs) == False)

def test_ag_contract_implication():
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")

    c1 = AGContract(vars=[x, y], assumption="x >= 0 && x <= 10", guarantee="y <= 1.2*x && y >= 0.8 * x")
    c2 = AGContract(vars=[x, y], assumption="x > 10", guarantee="y <= 1.1*x && y >= 0.9 * x")
    cs = AGContract(vars=[x, y], assumption="x >= 0", guarantee="y <= 1.1*x + 1 && y >= 0.9*x - 1")
    c2_q = c1.implication(cs)
    cs_new = c1.conjunction(c2_q)
    assert(c1.is_refined_by(cs_new))
    assert(c2_q.is_refined_by(cs_new))
    assert(cs.is_refined_by(cs_new))
    assert(cs_new.is_refined_by(cs) == False)


def test_ag_contract_replaceability():
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")    
    c1 = AGContract(vars=[x, y], assumption="x >= 0", guarantee="y == 2 * x")
    c2 = AGContract(vars=[x, y], assumption="x >= -2", guarantee="y == 2 * x && x <= 4")
    c3 = AGContract(vars=[x, y], assumption="x >= -4", guarantee="y == 2 * x && x <= -1")

    assert(c1.is_replaceable_by(c2))
    assert(c2.is_replaceable_by(c3))
    assert(not c1.is_replaceable_by(c3))

    c1 = AGContract(vars=[x, y, z], assumption="true", guarantee="y == z + 1 || y == x * z")
    c2 = AGContract(vars=[y, z], assumption="true", guarantee="z == y + 1")
    cs = AGContract(vars=[x, y, z], assumption="x != 1", guarantee="y == x / (1 - x)")

    c12 = c1.composition(c2)

    c1_r = AGContract(vars=[x, y, z], assumption="true", guarantee="y == z + 1")
    c2_r = AGContract(vars=[y, z], assumption="true", guarantee="z == y + 1")

    c12_r = c1_r.composition(c2_r)
    assert(cs.is_replaceable_by(c12) == True)
    assert(c1.is_replaceable_by(c1_r) == True)
    assert(c1.is_replaceable_by(c2_r) == True)
    assert(cs.is_replaceable_by(c12_r) == False)
    assert(cs.is_replaceable_by(cs) == True)

def test_ag_contract_strong_replaceability():
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")    
    c1 = AGContract(vars=[x, y], assumption="x >= 0", guarantee="y == 2 * x")
    c3 = AGContract(vars=[x, y], assumption="x >= -2", guarantee="y == 2 * x && x <= 4")
    c4 = AGContract(vars=[x, y], assumption="x >= 2", guarantee="y == 2 * x && x <= 10")
    c5 = AGContract(vars=[x, y], assumption="x >= 2", guarantee="y == 2 * x && x <= -1")
    c6 = AGContract(vars=[x, y], assumption="x >= -1", guarantee="y == 2 * x && y >= 1")
    c7 = AGContract(vars=[x, y], assumption="x >= -4", guarantee="y == 2 * x && x <= -1")
    c8 = AGContract(vars=[x, y], assumption="x >= -4", guarantee="y == 2 * x && y >= -1")

    assert(not c1.is_strongly_replaceable_by(c3))
    assert(not c1.is_strongly_replaceable_by(c4))
    assert(not c1.is_strongly_replaceable_by(c5))
    assert(not c1.is_strongly_replaceable_by(c6))
    assert(c1.is_strongly_replaceable_by(c8))
    assert(not c8.is_strongly_replaceable_by(c8))

    c1 = AGContract(vars=[x, y, z], assumption="true", guarantee="y == z + 1 || y == x * z")
    c2 = AGContract(vars=[y, z], assumption="true", guarantee="z == y + 1")
    cs = AGContract(vars=[x, y, z], assumption="x != 1", guarantee="y == x / (1 - x)")

    c12 = c1.composition(c2)

    c1_r = AGContract(vars=[x, y, z], assumption="true", guarantee="y == z + 1")
    c2_r = AGContract(vars=[y, z], assumption="true", guarantee="z == y + 1")

    c12_r = c1_r.composition(c2_r)
    assert(cs.is_strongly_replaceable_by(c12) == True)
    assert(c1.is_strongly_replaceable_by(c1_r) == True)
    assert(c1.is_strongly_replaceable_by(c2_r) == True)
    assert(cs.is_strongly_replaceable_by(c12_r) == False)
    assert(cs.is_strongly_replaceable_by(cs) == True)


def test_ag_contract_conformance():
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")

    c1 = AGContract(vars=[x, y], assumption="x >= 0", guarantee="y == 2 * x")
    c2 = AGContract(vars=[x, y], assumption="x >= 2", guarantee="y == 2 * x")
    c3 = AGContract(vars=[x, y], assumption="x >= -2", guarantee="y == 2 * x && x <= 4")
    c4 = AGContract(vars=[x, y], assumption="x >= 2", guarantee="y == 2 * x && x <= 10")
    c5 = AGContract(vars=[x, y], assumption="x >= 2", guarantee="y == 2 * x && x <= -1")
    c6 = AGContract(vars=[x, y], assumption="x >= -1", guarantee="y == 2 * x && y >= 1")

    assert(c1.is_conformed_by(c2))
    assert(not c2.is_conformed_by(c1))
    assert(not c1.is_conformed_by(c3))
    assert(not c3.is_conformed_by(c1))
    assert(c1.is_conformed_by(c4))
    assert(not c4.is_conformed_by(c1))
    assert(c1.is_conformed_by(c5))
    assert(not c5.is_conformed_by(c1))
    assert(c1.is_conformed_by(c6))
    assert(not c6.is_conformed_by(c1))

def test_ag_contract_strong_dominance():
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")

    c1 = AGContract(vars=[x, y], assumption="x >= 0", guarantee="y == 2 * x")
    c2 = AGContract(vars=[x, y], assumption="x >= 2", guarantee="y == 2 * x")
    c3 = AGContract(vars=[x, y], assumption="x >= -2", guarantee="y == 2 * x && x <= 4")
    c4 = AGContract(vars=[x, y], assumption="x >= 2", guarantee="y == 2 * x && x <= 10")
    c5 = AGContract(vars=[x, y], assumption="x >= 2", guarantee="y == 2 * x && x <= -1")
    c6 = AGContract(vars=[x, y], assumption="x >= -1", guarantee="y == 2 * x && y >= 1")

    assert(not c1.is_strongly_dominated_by(c2))
    assert(not c2.is_strongly_dominated_by(c1))
    assert(not c1.is_strongly_dominated_by(c3))
    assert(not c3.is_strongly_dominated_by(c1))
    assert(not c1.is_strongly_dominated_by(c4))
    assert(not c4.is_strongly_dominated_by(c1))
    assert(not c1.is_strongly_dominated_by(c5))
    assert(c1.is_strongly_dominated_by(c6))
    assert(not c6.is_strongly_dominated_by(c1))

def test_ag_contract_receptiveness():
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")


    c1 = AGContract(vars=[x, z], assumption="x >= 0", guarantee="z == 2 * x")
    c2 = AGContract(vars=[y, z], assumption="z >= 1", guarantee="y == 2 * z")
    c3 = AGContract(vars=[x, y], assumption="x >= 2", guarantee="y == 4 * x")
    c4 = AGContract(vars=[x, z], assumption="x >= -5", guarantee="z == 2 * x && x < 1")
    c5 = AGContract(vars=[x, y, z], assumption="true", guarantee="y == z + 1 || y == x * z")
    c6 = AGContract(vars=[y, z], assumption="true", guarantee="z == y + 1")
    c7 = AGContract(vars=[x, y, z], assumption="x != 1", guarantee="y == x / (1 - x)")
    c8 = AGContract(vars=[x, y, z], assumption="x >= 0", guarantee="y == x && x >= 2")
    c9 = AGContract(vars=[x, y, z], assumption="x * y <= 5", guarantee="y == 2*x")
    c10 = AGContract(vars=[x, y], assumption="x >= -1", guarantee="y == 2 * x && y >= 1")

    assert(c1.is_receptive())
    assert(c2.is_receptive())
    assert(c3.is_receptive())
    assert(not c4.is_receptive())
    assert(c5.is_receptive())
    assert(c6.is_receptive())
    assert(c7.is_receptive())
    assert(not c8.is_receptive())
    assert(not c9.is_receptive())
    assert(not c10.is_receptive())


def test_contract_composition():
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")

    c1 = AGContract(vars=[x, z], assumption="x >= 0", guarantee="z == 2 * x")
    c2 = AGContract(vars=[y, z], assumption="z >= 1", guarantee="y == 2 * z")
    c3 = AGContract(vars=[x, y], assumption="x >= 2", guarantee="y == 4 * x")

    c12 = c1.composition(c2)
    assert(c3.is_refined_by(c12) == True)

    c1 = AGContract(vars=[x, z], assumption="x >= -5", guarantee="z == 2 * x && x < 1")
    c2 = AGContract(vars=[y, z], assumption="z >= 1", guarantee="y == 2 * z")
    c3 = AGContract(vars=[x, y], assumption="x >= 2", guarantee="y == 4 * x")

    c12 = c1.composition(c2)
    assert(c3.is_refined_by(c12) == True)

    for i100 in range(0, 100, 5):
        i = i100/100.0
        c1 = AGContract(vars=[x, z], assumption="x >= 0", guarantee="z == 2 * x")
        c2 = AGContract(vars=[y, z], assumption="z >= 1", guarantee="y == 2 * z")
        c3 = AGContract(vars=[x, y], assumption=f"x >= {i}", guarantee="y == 4 * x")
        c12 = c1.composition(c2)
        if i >= 0.5:
            assert(c3.is_refined_by(c12) == True)
        else:
            assert(c3.is_refined_by(c12) == False)

    c1 = AGContract(vars=[x, y, z], assumption="true", guarantee="y == z + 1 || y == x * z")
    c2 = AGContract(vars=[y, z], assumption="true", guarantee="z == y + 1")
    c3 = AGContract(vars=[x, y, z], assumption="x != 1", guarantee="y == x / (1 - x)")

    c12 = c1.composition(c2)
    assert(c3.is_refined_by(c12) == True)

    c1 = AGContract(vars=[x, y, z], assumption="true", guarantee="y == z + 1")
    c2 = AGContract(vars=[y, z], assumption="true", guarantee="z == y + 1")
    c3 = AGContract(vars=[x, y, z], assumption="x != 1", guarantee="y == x / (1 - x)")

    c12 = c1.composition(c2)
    assert(c3.is_refined_by(c12) == True)