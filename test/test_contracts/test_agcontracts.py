import pytest

from contractda.contracts import AGContract
from contractda.vars import Var, RealVar


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