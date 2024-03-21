from contractda.contracts import AGContract
from contractda.vars import Var, RealVar, CategoricalVar
from contractda.sets import ExplicitSet
if __name__ == "__main__":
    w = CategoricalVar("w", range(0, 5))
    x = CategoricalVar("x", range(0, 7))
    y = CategoricalVar("y", range(0, 8))
    z = CategoricalVar("z", range(0, 3))

    c1 = AGContract([w, x, y], 
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)]),
                    guarantee=ExplicitSet([x, y], [(0, 0), (0, 1), (1, 1), (2, 2), (3, 3), (4, 3), (5, 5), (5, 6), (6, 5), (6, 6)]))
    
    c2 = AGContract([x, y], 
                    assumption=ExplicitSet([y], [tuple([0]), tuple([1]), tuple([2]), tuple([3]), tuple([4]), tuple([5]), tuple([6])]),
                    guarantee=ExplicitSet([x, y], [(0, 1), (1, 1), (2, 2), (3, 3), (4, 3), (5, 5), (5, 6), (6, 5), (6, 6)]))
    
    cs = AGContract([w, x, y], 
                    assumption=ExplicitSet([w], [tuple([0])]),
                    guarantee=ExplicitSet([x, y], [(0, 1), (1, 1), (2, 2), (3, 3), (4, 3)]))
    
    cs.is_independent_decomposition_of(c1, c2)