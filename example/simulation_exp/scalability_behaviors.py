from contractda.vars import Var, RealVar, IntVar
from contractda.sets import FOLClauseSet
from contractda.contracts import AGContract
from contractda.simulator import Simulator
import random
import time
from matplotlib import pyplot as plt

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


def draw_fig():
    plt.rcParams['text.usetex'] = True
    t = [0.04192322699964279, 0.044321294997644145, 0.05218311299904599, 0.06607821400029934, 0.08702132200050983, 0.12131853000028059, 0.1654990459974215, 0.34955407999950694, 0.6971476190010435, 1.2612670069975138, 2.643466642999556, 5.781236349001119, 13.726289706002717, 28.396860518998437, 64.27351459700003, 145.7506383709988, 285.8922719700022]
    x = [i for i in range(1, 18)]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), constrained_layout=True)
    axes[0].plot(x, t, marker='o', linestyle='-', color='r', label='t')
    fontsize = 16
    axes[0].legend(fontsize=fontsize)
    axes[0].set_ylim(0, 300)
    axes[0].set_xlim(0, 18)
    axes[0].set_ylabel("Execution time (s)", fontsize=fontsize)
    axes[0].set_xlabel("$2^n$ clauses", fontsize=fontsize)
    #axes[0].show()
    axes[0].minorticks_on()
    axes[0].tick_params(axis='x',labelsize=fontsize)
    axes[0].tick_params(axis='y',labelsize=fontsize)
    tick_positions = [i for i in range(1, 18, 2)]
    axes[0].set_xticks(tick_positions)
    tick_labels = [f"$2^{{ {int(pos)-1} }}$" for pos in tick_positions]
    axes[0].set_xticklabels(tick_labels, fontsize=fontsize)
    # Customize minor ticks (remove labels but keep ticks visible)
    axes[0].tick_params(axis='y', which='minor', length=4, color='gray', labelbottom=False)
    for i, j in zip(x, t):
        axes[0].text(i, j + 3, f'{j:.2f}', fontsize=9, ha='center', va='bottom', color='blue')
    axes[0].grid(True)

    x = [2**i for i in range(1, 18)]
    axes[1].plot(x, t, marker='o', linestyle='-', color='r', label='t')
    axes[1].legend(fontsize=fontsize)
    # # axes[1].set_xlim(0, 18)
    # axes[1].set_yscale("log")
    # axes[1].set_xscale("log")
    axes[1].set_ylabel("Execution time (s)", fontsize=fontsize)
    axes[1].set_xlabel("\# clauses", fontsize=fontsize)
    # axes[1].set_xticks(tick_positions)
    # axes[1].set_xticklabels(tick_labels, fontsize=fontsize)
    # #axes[0].show()
    axes[1].minorticks_on()
    axes[1].tick_params(axis='x',labelsize=fontsize)
    axes[1].tick_params(axis='y',labelsize=fontsize)
    # # Customize minor ticks (remove labels but keep ticks visible)
    axes[1].tick_params(axis='y', which='minor', length=4, color='gray', labelbottom=False)
    axes[1].grid(True)

    plt.savefig('behavior_scalability.pdf')

if __name__ == "__main__":
    draw_fig()
    # random.seed(10)

    # n_var = 100
    # variables = []
    # for i in range(n_var):
    #     v_name = f"v_{i}"
    #     variables.append(RealVar(v_name))

    # n_assumption_vs = 10
    # assumption_vs = variables[:10]

    # n_behaviors = [i for i in range(1, 18)]
    # times = []

    # for n_behavior in n_behaviors:

    #     vs1, c1 = random_generation_test(n_behavior, 0, variables=assumption_vs)
    #     vs2, c2 = random_generation_test(n_behavior, 0, variables=variables)

    #     assumption = FOLClauseSet(assumption_vs, c1)
    #     guarantee = FOLClauseSet(variables, c2)
    #     cont1 = AGContract(vars=variables, assumption=assumption, guarantee=guarantee)
    #     print(n_behavior, cont1)
    #     simulator = Simulator(contract=cont1)
    #     print(n_behavior)
    #     simulate_stimulus, violated_stimulus,_ = simulator.auto_simulate(max_depth=1, produce_env_only=True)
    
    #     print(n_behavior)
    #     start_time = time.perf_counter()
    #     ret = simulator.simulate(stimulus=simulate_stimulus[0])
    #     end_time = time.perf_counter()
    #     print(ret[0])
    #     times.append(end_time-start_time)

    # print(times)




        


