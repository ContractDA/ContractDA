from contractda.sets.explicit_set import ExplicitSet

def test_explicit_set():
    eset = ExplicitSet(["x", "y", "z"], [(1, 2, 3), (2, 3, 4), (1, 3, 5)])
    print(eset)

def test_explicit_set_iter():
    eset = ExplicitSet(["x", "y", "z"], [(1, 2, 3), (2, 3, 4), (1, 3, 5)])
    for e in eset:
        print(e)

def test_explicit_set_sample():
    eset = ExplicitSet(["x", "y", "z"], [(1, 2, 3), (2, 3, 4), (1, 3, 5)])
    print(eset.sample())

if __name__ == "__main__":
    test_explicit_set()
    test_explicit_set_iter()
    test_explicit_set_sample()