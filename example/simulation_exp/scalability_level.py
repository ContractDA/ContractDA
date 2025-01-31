from contractda.vars import Var, RealVar, IntVar
from contractda.sets import FOLClauseSet
import random
import time

operator_expression = [">=", ">", "<", "<=", "==", "!="]
operator_clause = ["&&", "||", "->"]

def random_generation_test(depth: int, n_var: int, variables:list = None):
    # Randomly generate a FOL clause with needed depth
    if variables is None:
        variables = []
        for i in range(n_var):
            v_name = f"v_{i}"
            variables.append(RealVar(v_name))

    return variables, _generate_with_depth(depth=depth, variables=variables)

def _generate_with_depth(depth: int, variables: list[Var]):
    if depth == 1:
        # randomly pick an variable
        v_random = random.choice(variables).id
        operator = random.choice(operator_expression)
        operand = random.uniform(0, 100)
        return f"{v_random} {operator} {operand}"
    
    operator = random.choice(operator_clause)
    c1 = _generate_with_depth(depth - 1, variables=variables)
    c2 = _generate_with_depth(depth - 1, variables=variables)
    if operator == "!":
        return f"{operator} ({c2})"
    else:
        return f"({c1}) {operator} ({c2})"


if __name__ == "__main__":
    random.seed(10)

    times = []
    for level in range(3, 15):
        total_time = 0
        for r in range(10):
            vs, c1 = random_generation_test(level, 100)
            #print(level, c1)
            
            clause = FOLClauseSet(vars=vs, expr=c1)
        
            start_time = time.perf_counter()
            examples = clause.generate_boundary_set_linear()
            end_time = time.perf_counter()
            print(level, r, end_time-start_time)
            total_time += end_time-start_time
            print(len(examples))
        times.append(total_time/10.0)
        print(f"finish level{level}, time:", total_time/10.0)

    print(times)
        # for i in in1:
        #     print(i)
        # for o in ex1:
        #     print(o)
        
