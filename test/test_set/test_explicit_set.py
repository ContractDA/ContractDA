from contractda.sets._explicit_set import ExplicitSet
from contractda.vars._var import CategoricalVar
import pytest

@pytest.fixture
def all_vars():
    return {
    "v": CategoricalVar("v", range(1,10)),
    "w": CategoricalVar("w", range(1,10)),
    "x": CategoricalVar("x", range(1,10)),
    "y": CategoricalVar("y", range(1,10)),
    "z": CategoricalVar("z", range(1,10))
    }

######## Test basic data

@pytest.fixture
def basic_expr():
    return [(1, 2, 3), (2, 3, 4), (1, 3, 5), (3, 3, 2), (1, 10, 23)]

@pytest.fixture
def basic_var_list(all_vars):
    return [all_vars["x"], all_vars["w"], all_vars["z"]]

@pytest.fixture
def basic_explicit_set(basic_var_list, basic_expr):
    eset = ExplicitSet(basic_var_list, basic_expr)
    return eset

def test_explicit_set(basic_explicit_set):
    print(basic_explicit_set)

def test_internal_vars(basic_explicit_set, basic_var_list):
    var_names = [var.id for var in basic_var_list]
    gold_internal_var_names = sorted(var_names)
    for var, name in zip(basic_explicit_set.internal_vars, gold_internal_var_names):
        assert(var.id == name)

def test_ordered_vars(basic_explicit_set, basic_var_list):
    var_names = [var.id for var in basic_var_list]
    for var, name in zip(basic_explicit_set.ordered_vars, var_names):
        assert(var.id == name)

def test_ordered_expr(basic_explicit_set, basic_expr):
    expr = basic_explicit_set.ordered_expr
    assert(len(expr) == len(basic_expr))
    assert(set(expr) == set(basic_expr))
    for elem in expr:
        assert(elem in basic_expr)
    
def test_explicit_set_iter(basic_explicit_set, basic_expr):

    result_iter = [e for e in basic_explicit_set] 
    result_set = set(result_iter)
    assert(result_set == set(basic_expr))
    assert(len(result_iter) == len(basic_expr))

def test_explicit_set_sample(basic_explicit_set, basic_expr):
    sample = basic_explicit_set.sample()
    sample = basic_explicit_set._convert_elem_to_external(sample)
    assert(sample in basic_expr)


############### Test Operations
        
@pytest.fixture
def expr_a(basic_expr):
    return basic_expr

@pytest.fixture
def expr_b():
    return [(1, 2, 1), (2, 3, 4), (1, 3, 2)]

@pytest.fixture
def vars_a(all_vars):
    return [all_vars["x"], all_vars["w"], all_vars["v"]]

@pytest.fixture
def vars_b(all_vars):
    return [all_vars["y"], all_vars["z"], all_vars["x"]]

@pytest.fixture
def set_a(vars_a, expr_a):
    return ExplicitSet(vars_a, expr_a)

@pytest.fixture
def set_b(vars_b, expr_b):
    return ExplicitSet(vars_b, expr_b)

def test_explicit_set_intersect(set_a, set_b, all_vars):
    set_c = ExplicitSet.intersect(set_a, set_b)
    assert(set(set_c._vars) == set(all_vars.values()))


def test_explicit_set_project1(set_a, set_b, all_vars):
    a = CategoricalVar("a", range(1,3))
    b = CategoricalVar("b", range(1,3))
    c = CategoricalVar("c", range(1,3))
    d = CategoricalVar("d", range(1,5))
    e = CategoricalVar("e", range(1,4))
    vars = [b, a, c]
    expr = [(1, 2, 1), (1, 2, 2), (1, 1, 1)]
    test_set = ExplicitSet(vars, expr)
    test1 = test_set.project([a, b], is_refine=False)
    test2 = ExplicitSet.project(test_set, [b, a], is_refine=True)
    test3 = ExplicitSet.project(test_set, [a, b, d, e], is_refine=False)
    test4 = ExplicitSet.project(test_set, [a, b, e, d], is_refine=True)

    gold1 = [(2, 1), (1, 1)]
    gold2 = [(1, 2)]
    gold3 = [(2, 1, 1, 1), (2, 1, 1, 2), (2, 1, 1, 3), 
             (2, 1, 2, 1), (2, 1, 2, 2), (2, 1, 2, 3), 
             (2, 1, 3, 1), (2, 1, 3, 2), (2, 1, 3, 3), 
             (2, 1, 4, 1), (2, 1, 4, 2), (2, 1, 4, 3),
             (1, 1, 1, 1), (1, 1, 1, 2), (1, 1, 1, 3), 
             (1, 1, 2, 1), (1, 1, 2, 2), (1, 1, 2, 3), 
             (1, 1, 3, 1), (1, 1, 3, 2), (1, 1, 3, 3), 
             (1, 1, 4, 1), (1, 1, 4, 2), (1, 1, 4, 3)]
    gold4 = [(2, 1, 1, 1), (2, 1, 1, 2), (2, 1, 1, 3), (2, 1, 1, 4),
             (2, 1, 2, 1), (2, 1, 2, 2), (2, 1, 2, 3), (2, 1, 2, 4),
             (2, 1, 3, 1), (2, 1, 3, 2), (2, 1, 3, 3), (2, 1, 3, 4)]    
    # check test1
    assert(test1.ordered_expr == set(gold1))
    assert(test2.ordered_expr == set(gold2))
    assert(test3.ordered_expr == set(gold3))
    assert(test4.ordered_expr == set(gold4))

def test_explicit_set_difference():
    x = CategoricalVar("x", range(1,5))
    y = CategoricalVar("y", range(1,5))
    z = CategoricalVar("z", range(1,4))

    a_expr = [(1, 2), (2, 1), (3, 3), (3, 4)]
    b_expr = [(2, 2), (1, 2), (3, 4)]
    c_expr = [(2, 3), (1, 2)]

    # basic, without reorder issue
    a_set = ExplicitSet([x, y], a_expr)
    b_set = ExplicitSet([x, y], b_expr)
    ret_set = a_set.difference(b_set)
    gold = set([(2, 1), (3, 3)])
    assert(gold == ret_set.ordered_expr)
    assert([x, y] == ret_set.ordered_vars)

    a_set = ExplicitSet([y, x], a_expr)
    b_set = ExplicitSet([x, y], b_expr)
    c_set = ExplicitSet([y, z], c_expr)
    ret_set = a_set.difference(b_set)
    gold = set([(1, 2), (3, 3), (3, 4)])
    assert(gold == ret_set.ordered_expr)
    assert([y, x] == ret_set.ordered_vars)
    
    ret_set = a_set.difference(c_set)
    gold = set([(1, 2, 1), (2, 1, 1), (3, 3, 1), (3, 4, 3), (1, 2, 3), (3, 3, 3), (3, 4, 2), (2, 1, 2), (3, 4, 1), (3, 3, 2)])
    assert(gold == ret_set.ordered_expr)
    assert([y, x, z] == ret_set.ordered_vars)

def test_explicit_set_union():
    x = CategoricalVar("x", range(1,5))
    y = CategoricalVar("y", range(1,5))
    z = CategoricalVar("z", range(1,4))

    a_expr = [(1, 2), (2, 1), (3, 3), (3, 4)]
    b_expr = [(2, 2), (1, 2), (3, 4)]
    c_expr = [(2, 3), (1, 2)]   

    a_set = ExplicitSet([y, x], a_expr)
    b_set = ExplicitSet([x, y], b_expr)
    c_set = ExplicitSet([y, z], c_expr)
    ret_set = a_set.union(b_set)
    gold = set([(1, 2), (2, 1), (3, 4), (4, 3), (3, 3), (2, 2)])
    assert(gold == ret_set.ordered_expr)
    assert([y, x] == ret_set.ordered_vars)
    
    ret_set = a_set.union(c_set)
    gold = set([(1, 2, 1), (1, 2, 2), (1, 2, 3),
                (2, 1, 1), (2, 1, 2), (2, 1, 3),
                (3, 3, 1), (3, 3, 2), (3, 3, 3),
                (3, 4, 1), (3, 4, 2), (3, 4, 3),
                (2, 1, 3), (2, 2, 3), (2, 3, 3), (2, 4, 3),
                (1, 1, 2), (1, 2, 2), (1, 3, 2), (1, 4, 2)
                ])
    assert(gold == ret_set.ordered_expr)
    assert([y, x, z] == ret_set.ordered_vars)

if __name__ == "__main__":
    test_explicit_set()
    test_explicit_set_iter()
    test_explicit_set_sample()