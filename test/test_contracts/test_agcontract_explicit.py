import pytest

from contractda.contracts import AGContract
from contractda.vars import Var, RealVar, CategoricalVar
from contractda.sets import ExplicitSet


def test_contract_composition():
    w = CategoricalVar("w", range(0,5))
    x = CategoricalVar("x", range(0,5))
    y = CategoricalVar("y", range(0,5))
    z = CategoricalVar("z", range(0,5))

    c1 = AGContract(vars=[w, x, y], # given w + x <= 4
                    assumption=ExplicitSet([w, x], [ (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                                                     (1, 0), (1, 1), (1, 2), (1, 3), 
                                                     (2, 0), (2, 1), (2, 2), 
                                                     (3, 0), (3, 1),
                                                     (4, 0)]),
                    guarantee=ExplicitSet([w, x, y], [(0, 0, 0), (0, 1, 1), (0, 2, 2), (0, 3, 3), (0, 4, 4),
                                                      (1, 0, 1), (1, 1, 2), (1, 2, 3), (1, 3, 4), (1, 4, 0),
                                                      (2, 0, 2), (2, 1, 3), (2, 2, 4), (2, 3, 0), (2, 4, 0),
                                                      (3, 0, 3), (3, 1, 4), (3, 2, 2), (3, 3, 0), (3, 4, 0),
                                                      (4, 0, 4), (4, 1, 4), (4, 2, 1), (4, 3, 0), (4, 4, 0),
                                                      ]))# y = w + x
    # given y <= 2, z = 2y
    c2 = AGContract(vars=[y, z], 
                    assumption=ExplicitSet([y], [tuple([0]), tuple([1]), tuple([2])]),
                    guarantee=ExplicitSet([y, z], [(0, 0), (1, 2), (2, 4), 
                                                   (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
                                                   (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)])
    )

    c12 = c1.composition(c2)
    cs = AGContract(vars=[w, x, y, z], # w + x <= 2
                    assumption=ExplicitSet([w, x], [ (0, 0), (0, 1), (0, 2),
                                                     (1, 0), (1, 1), 
                                                     (2, 0)]),
                    guarantee=ExplicitSet([w, x, z], [(0, 0, 0), (0, 1, 2), (0, 2, 4),
                                                      (1, 0, 2), (1, 1, 4),
                                                      (2, 0, 4)])# z = 2(w + x)
    )
    assert(not c12.is_refined_by(cs))
    assert(cs.is_refined_by(c12))
   


def test_contract_feedback_composition():
    x = CategoricalVar("x", range(0,3))
    y = CategoricalVar("y", range(0,3))
    z = CategoricalVar("z", range(0,3))


    cs = AGContract(vars=[x, y, z], # given y and z are free
                    assumption=ExplicitSet([x,], [tuple([0]), tuple([1]), tuple([2])]),
                    guarantee=ExplicitSet([y, z], [(0, 0), (0, 1), (0, 2),
                                                   (1, 0), (1, 1), (1, 2),
                                                   (2, 0), (2, 1), (2, 2)])
    )# y = w + x
    c1 = AGContract(vars=[x, y, z], # given any x z are free
                    assumption=ExplicitSet([x, y], [(0, 0), (0, 1), (0, 2),
                                                    (1, 0), (1, 1), (1, 2),
                                                    (2, 0), (2, 1), (2, 2)]),
                    guarantee=ExplicitSet([z], [tuple([0]), tuple([1]), tuple([2])])
    )# y = w + x
    c2 = AGContract(vars=[y, z], # given any z y are free
                    assumption=ExplicitSet([z], [tuple([0]), tuple([1]), tuple([2])]),
                    guarantee=ExplicitSet([y], [tuple([0]), tuple([1]), tuple([2])])
    )# y = w + x

    c1_refined = AGContract(vars=[x, y, z], # given any x z are free
                    assumption=ExplicitSet([x, y], [(0, 0), (0, 1), (0, 2),
                                                    (1, 0), (1, 1), (1, 2),
                                                    (2, 0), (2, 1), (2, 2)]),
                    guarantee=ExplicitSet([y, z], [(0, 1), (1, 2), (2, 0)]))
                    # z = y + 1 mod 3
    c2_refined = AGContract(vars=[y, z], # y = z
                    assumption=ExplicitSet([z], [tuple([0]), tuple([1]), tuple([2])]),
                    guarantee=ExplicitSet([y, z], [(0, 0), (1, 1), (2, 2)])
    )# y = w + x
    assert(c2.is_refined_by(c2_refined))
    assert(not c2_refined.is_refined_by(c2))
    assert(c1.is_refined_by(c1_refined))
    assert(not c1_refined.is_refined_by(c1))
    c12 = c1.composition(c2)
    c12_prime = c1_refined.composition(c2_refined)
    print("c12:", c12)
    print("c12_prime:", c12_prime)

    assert(cs.is_refined_by(c12))
    assert(c12.is_refined_by(cs))
    assert(cs.is_refined_by(c12_prime))
    assert(not c12_prime.is_refined_by(cs))
    assert(c12.is_refined_by(c12_prime))
    assert(not c12_prime.is_refined_by(c12))
    #assert(False)