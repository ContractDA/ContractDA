import pytest

from contractda.contracts import AGContract
from contractda.vars import Var, RealVar, CategoricalVar
from contractda.sets import ExplicitSet

def test_contract_replaceble():
    w = CategoricalVar("w", range(0,3))
    x = CategoricalVar("x", range(0,3))
    y = CategoricalVar("y", range(0,3))
    z = CategoricalVar("z", range(0,3))


    c1 = AGContract(vars=[x],
                    assumption=ExplicitSet([x], [tuple([0])]),
                    guarantee=ExplicitSet([x, y, z], [(0, 1, 2), (0, 0, 1)]))
    
    c2 = AGContract(vars=[x],
                    assumption=ExplicitSet([x], [tuple([0]), tuple([1])]),
                    guarantee=ExplicitSet([x, y, z], [(0, 1, 2), (1, 2, 1), (2, 2, 1)]))

    c3 = AGContract(vars=[x],
                    assumption=ExplicitSet([x], [tuple([0]), tuple([1])]),
                    guarantee=ExplicitSet([x, y, z], [(0, 1, 2), (1, 2, 1)]))

    c4 = AGContract(vars=[x],
                    assumption=ExplicitSet([x], [tuple([0]), tuple([1])]),
                    guarantee=ExplicitSet([x, y, z], [(1, 2, 1)]))
    
    c5 = AGContract(vars=[x],
                    assumption=ExplicitSet([x], [tuple([0]), tuple([1]), tuple([2])]),
                    guarantee=ExplicitSet([x, y, z], [(1, 2, 1), (2, 2, 1)]))
    
    c6 = AGContract(vars=[x],
                    assumption=ExplicitSet([x], [tuple([0]), tuple([1]), tuple([2])]),
                    guarantee=ExplicitSet([x, y, z], [(0, 0, 1), (1, 2, 1), (2, 2, 1)]))
    
    assert(c1.is_replaceable_by(c2))
    assert(c1.is_replaceable_by(c3))
    assert(c4.is_replaceable_by(c5))
    assert(c3.is_replaceable_by(c5))
    assert(not c1.is_replaceable_by(c4))
    assert(not c1.is_replaceable_by(c5))
    assert(c1.is_replaceable_by(c6))

    c7 = AGContract(vars=[w, x],
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0)]),
                    guarantee=ExplicitSet([w, x, y, z], [(0, 0, 1, 2), (0, 0, 2, 1), (0, 1, 2, 2), (0, 2, 1, 0), 
                                                         (1, 1, 2, 2), (2, 2, 1, 2), (2, 0, 1, 1), (1, 2, 2, 2)]))
    
    c8 = AGContract(vars=[w, x],
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1)]),
                    guarantee=ExplicitSet([w, x, y, z], [(0, 0, 1, 2), (0, 0, 2, 1), (0, 1, 2, 2), (0, 2, 1, 0), 
                                                         (1, 1, 2, 2), (2, 2, 1, 2), (2, 0, 1, 1), (1, 2, 2, 2), (2, 1, 2, 3)]))

    c9 = AGContract(vars=[w, x],
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1)]),
                    guarantee=ExplicitSet([w, x, y, z], [(0, 0, 1, 2), (0, 0, 2, 1), (0, 1, 2, 2), (0, 2, 1, 0), 
                                                         (1, 1, 2, 2), (2, 2, 1, 2), (1, 2, 2, 2), (2, 1, 2, 3)]))
    
    c10 = AGContract(vars=[w, x],
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (2, 2)]),
                    guarantee=ExplicitSet([w, x, y, z], [(0, 0, 1, 2), (0, 0, 2, 1), (0, 1, 2, 2), (0, 2, 1, 0), 
                                                         (1, 1, 2, 2), (2, 2, 1, 2), (2, 0, 1, 1), (1, 2, 2, 2), (2, 1, 2, 3)]))
    c11 = AGContract(vars=[w, x],
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (2, 2)]),
                    guarantee=ExplicitSet([w, x, y, z], [(0, 0, 1, 2), (0, 0, 2, 1), (0, 1, 2, 2), (0, 2, 1, 0), 
                                                         (1, 1, 2, 2), (2, 2, 1, 2), (2, 0, 1, 1), (1, 2, 2, 2)]))
    
    c12 = AGContract(vars=[w, x],
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (2, 2)]),
                    guarantee=ExplicitSet([w, x, y, z], [(0, 0, 1, 2), (0, 0, 2, 1), (0, 2, 1, 0), 
                                                         (1, 1, 2, 2), (2, 2, 1, 2), (2, 0, 1, 1), (1, 2, 2, 2)]))
    assert(c7.is_replaceable_by(c8))
    assert(c7.is_replaceable_by(c9))
    assert(c7.is_replaceable_by(c10))
    assert(c7.is_replaceable_by(c11))
    assert(c7.is_replaceable_by(c12))    

def test_contract_strongly_replaceable():
    w = CategoricalVar("w", range(0,3))
    x = CategoricalVar("x", range(0,3))
    y = CategoricalVar("y", range(0,3))
    z = CategoricalVar("z", range(0,3))


    c1 = AGContract(vars=[x],
                    assumption=ExplicitSet([x], [tuple([0])]),
                    guarantee=ExplicitSet([x, y, z], [(0, 1, 2), (0, 0, 1)]))
    
    c2 = AGContract(vars=[x],
                    assumption=ExplicitSet([x], [tuple([0]), tuple([1])]),
                    guarantee=ExplicitSet([x, y, z], [(0, 1, 2), (1, 2, 1), (2, 2, 1)]))

    c3 = AGContract(vars=[x],
                    assumption=ExplicitSet([x], [tuple([0]), tuple([1])]),
                    guarantee=ExplicitSet([x, y, z], [(0, 1, 2), (1, 2, 1)]))

    c4 = AGContract(vars=[x],
                    assumption=ExplicitSet([x], [tuple([0]), tuple([1])]),
                    guarantee=ExplicitSet([x, y, z], [(1, 2, 1)]))
    
    c5 = AGContract(vars=[x],
                    assumption=ExplicitSet([x], [tuple([0]), tuple([1]), tuple([2])]),
                    guarantee=ExplicitSet([x, y, z], [(1, 2, 1), (2, 2, 1)]))
    
    c6 = AGContract(vars=[x],
                    assumption=ExplicitSet([x], [tuple([0]), tuple([1]), tuple([2])]),
                    guarantee=ExplicitSet([x, y, z], [(0, 0, 1), (1, 2, 1), (2, 2, 1)]))
    
    assert(c1.is_strongly_replaceable_by(c2))
    assert(c1.is_strongly_replaceable_by(c3))
    assert(not c1.is_strongly_replaceable_by(c4))
    assert(not c1.is_strongly_replaceable_by(c5))
    assert(c1.is_strongly_replaceable_by(c6))

    c7 = AGContract(vars=[w, x],
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0)]),
                    guarantee=ExplicitSet([w, x, y, z], [(0, 0, 1, 2), (0, 0, 2, 1), (0, 1, 2, 2), (0, 2, 1, 0), 
                                                         (1, 1, 2, 2), (2, 2, 1, 2), (2, 0, 1, 1), (1, 2, 2, 2)]))
    
    c8 = AGContract(vars=[w, x],
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1)]),
                    guarantee=ExplicitSet([w, x, y, z], [(0, 0, 1, 2), (0, 0, 2, 1), (0, 1, 2, 2), (0, 2, 1, 0), 
                                                         (1, 1, 2, 2), (2, 2, 1, 2), (2, 0, 1, 1), (1, 2, 2, 2), (2, 1, 2, 3)]))

    c9 = AGContract(vars=[w, x],
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1)]),
                    guarantee=ExplicitSet([w, x, y, z], [(0, 0, 1, 2), (0, 0, 2, 1), (0, 1, 2, 2), (0, 2, 1, 0), 
                                                         (1, 1, 2, 2), (2, 2, 1, 2), (1, 2, 2, 2), (2, 1, 2, 3)]))
    
    c10 = AGContract(vars=[w, x],
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (2, 2)]),
                    guarantee=ExplicitSet([w, x, y, z], [(0, 0, 1, 2), (0, 0, 2, 1), (0, 1, 2, 2), (0, 2, 1, 0), 
                                                         (1, 1, 2, 2), (2, 2, 1, 2), (2, 0, 1, 1), (1, 2, 2, 2), (2, 1, 2, 3)]))
    c11 = AGContract(vars=[w, x],
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (2, 2)]),
                    guarantee=ExplicitSet([w, x, y, z], [(0, 0, 1, 2), (0, 0, 2, 1), (0, 1, 2, 2), (0, 2, 1, 0), 
                                                         (1, 1, 2, 2), (2, 2, 1, 2), (2, 0, 1, 1), (1, 2, 2, 2)]))
    
    c12 = AGContract(vars=[w, x],
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (2, 2)]),
                    guarantee=ExplicitSet([w, x, y, z], [(0, 0, 1, 2), (0, 0, 2, 1), (0, 2, 1, 0), 
                                                         (1, 1, 2, 2), (2, 2, 1, 2), (2, 0, 1, 1), (1, 2, 2, 2)]))
    assert(c7.is_strongly_replaceable_by(c8))
    assert(not c7.is_strongly_replaceable_by(c9))
    assert(c7.is_strongly_replaceable_by(c10))
    assert(c7.is_strongly_replaceable_by(c11))
    assert(not c7.is_strongly_replaceable_by(c12))

def test_contract_receptiveness():
    w = CategoricalVar("w", range(0,3))
    x = CategoricalVar("x", range(0,3))
    y = CategoricalVar("y", range(0,3))
    z = CategoricalVar("z", range(0,3))


    c1 = AGContract(vars=[x],
                    assumption=ExplicitSet([x], [tuple([0]), tuple([1]), tuple([2])]),
                    guarantee=ExplicitSet([x, y, z], [(0, 1, 2), (0, 0, 1), (1, 2, 1), (2, 2, 1)]))
    assert(c1.is_receptive())

    c2 = AGContract(vars=[x],
                    assumption=ExplicitSet([x], [tuple([0]), tuple([1]), tuple([2])]),
                    guarantee=ExplicitSet([x, y, z], [(0, 1, 2), (0, 0, 1), (2, 2, 1)]))
    assert(not c2.is_receptive())

    c3 = AGContract(vars=[x],
                    assumption=ExplicitSet([x], [tuple([0]), tuple([2])]),
                    guarantee=ExplicitSet([x, y, z], [(0, 1, 2), (0, 0, 1), (2, 2, 1)]))
    assert(c3.is_receptive())

    c4 = AGContract(vars=[w, x],
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0)]),
                    guarantee=ExplicitSet([w, x, y, z], [(0, 0, 1, 2), (0, 0, 2, 1), (0, 1, 2, 2), (0, 2, 1, 0), 
                                                         (1, 1, 2, 2), (2, 2, 1, 2), (2, 0, 1, 1), (1, 2, 2, 2)]))
    assert(c4.is_receptive())

    c5 = AGContract(vars=[w, x],
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (1, 1), (2, 0)]),
                    guarantee=ExplicitSet([w, x, y, z], [(0, 0, 1, 2), (0, 0, 2, 1), (0, 2, 1, 0), 
                                                         (1, 1, 2, 2), (2, 2, 1, 2), (2, 0, 1, 1), (1, 2, 2, 2), (1, 1, 1, 1)]))
    assert(not c5.is_receptive())

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