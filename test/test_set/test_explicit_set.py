from contractda.sets.explicit_set import ExplicitSet
import pytest

@pytest.fixture
def basic_values():
    return [(1, 2, 3), (2, 3, 4), (1, 3, 5)]

@pytest.fixture
def basic_var_list():
    return ["x", "y", "z"]

@pytest.fixture
def basic_explicit_set(basic_var_list, basic_values):
    eset = ExplicitSet(basic_var_list, basic_values)
    return eset

def test_explicit_set(basic_explicit_set):
    print(basic_explicit_set)

def test_explicit_set_iter(basic_explicit_set, basic_values):
    for e, value in zip(basic_explicit_set, basic_values):
        assert(e == value)

def test_explicit_set_sample(basic_explicit_set, basic_values):
    assert(basic_explicit_set.sample() in basic_values)

if __name__ == "__main__":
    test_explicit_set()
    test_explicit_set_iter()
    test_explicit_set_sample()