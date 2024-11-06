from contractda.contracts import ContractBase
from contractda.design import System
from contractda.logger._logger import LOG
from typing import Callable, Any
from contractda.sets import FOLClauseSet, SetBase
from contractda.vars import Var
#from contractda.sets._parsers._expression_parser import fol_exp_parser

# to be removed


class Stimulus(object):
    """class that represents the behaviors"""
    def __init__(self, stimulus_map: dict):
        self._map = stimulus_map

    @property
    def var_val_map(self) -> dict:
        return self._map
        
# class ObjectiveExpression(object):
#     def __init__(self, expr:str):
#         self._expr = fol_exp_parser.parse(expr)
    
#     def create_constraint():
#         pass


class Evaluator(object):
    """Class that wraps the evaluation function"""
    def __init__(self):
            pass

    def evaluate(self, behavior: Stimulus, behavior_set: SetBase):
        pass

class ClauseEvaluator(Evaluator):
    """Class for evaluation using clause to represent objectives"""
    def __init__(self, clause_set: FOLClauseSet, clause_objective: list[Var]):
        self._clause_set = clause_set
        self._obj = clause_objective

    @property
    def objective_set(self):
        return self._clause_set

    def evaluate(self, behavior: Stimulus = None, behavior_set: SetBase = None):
        if behavior is not None and behavior_set is not None:
            err_msg = "Cannot set both behavior and behavior_set arguments!"
            LOG.error(err_msg)
            raise Exception(err_msg)
        
        if behavior is None and behavior_set is None:
            err_msg = "Need behavior or behavior_set to evaluate the behavior"
            LOG.error(err_msg)
            raise Exception(err_msg) 

        if behavior is not None:
            return self._evaluate_by_behavior(behavior=behavior)
        else:
            ret, _ = self._evaluate_by_behavior_set(behavior_set=behavior_set)
            return ret
    
    def _evaluate_by_behavior(self, behavior: Stimulus) -> list[Any]:
        behavior_set = _create_set_from_behavior(sample=behavior.var_val_map)
        sat, sample = self._clause_set.intersect(behavior_set).sample()
        if not sat:
            err_msg = "Cannot evaluate as the objective function does not have solution"
            LOG.error(err_msg)
            raise Exception(err_msg)
        
        # ret = []
        # for var, val in sample.items():
        #     if var in sample:
        #         ret.append(var)
        #     else:
        #         # any values
        return [sample[var] for var in self._obj]
    
    def evaluate_max(self, behavior_set: SetBase, minimum = False):
        if len(self._obj) != 1:
            LOG.error("Multi-objective undefined!")
            return 
        
        sat = True
        max_val = None
        while sat:
            if max_val is not None:
                if minimum:
                    constrained_set = FOLClauseSet.generate_var_val_lt_constraint_set(self._obj[0], max_val)
                else:
                    constrained_set = FOLClauseSet.generate_var_val_gt_constraint_set(self._obj[0], max_val)
                new_behavior_set = behavior_set.intersect(constrained_set)
            else:
                new_behavior_set = behavior_set

            try:
                vals, sample =  self._evaluate_by_behavior_set(behavior_set=new_behavior_set)
                max_val = vals[0]
            except Exception as e:
                sat = False

        return [max_val]


    def _evaluate_by_behavior_set(self, behavior_set: SetBase) -> list[Any]:
        solver_set = self.objective_set.intersect(behavior_set)
        sat, sample = solver_set.sample()
        if not sat:
            err_msg = "Cannot evaluate as the objective function does not have solution"
            LOG.error(err_msg)
            raise Exception(err_msg)
    
        return [sample[var] for var in self._obj], sample 

class CallableEvaluator(Evaluator):
    def __init__(self, callable_func: Callable[[Stimulus], list[Any]]):
        self._func = callable_func

    def evaluate(self, behavior: Stimulus):
        ret = self._func(behavior)
        return ret
   



class Simulator(object):
    """wrapper class for performing simulation"""
    def __init__(self, evaluator: Evaluator = None, options: dict = None, contract: ContractBase = None, system: System = None ):
        if system is None and contract is None:
            err_msg = "Need at least one system or contract"
            LOG.error(err_msg)
            raise Exception(err_msg)
        if system is None:
            self._contract = contract
        else:
            self._contract = system._get_single_system_contract()
        self._contract: ContractBase = contract
        self._evaluator: Evaluator = evaluator
        self._options = options
        
    def simulate(self, stimulus: Stimulus):
        env_set = _create_set_from_behavior(stimulus.var_val_map)

        self._contract.assumption
        # check if the stimulus always satisfy the assumption
        # check if stimulus has elements in not A
        if env_set.intersect(self._contract.assumption.complement()).is_satifiable():
            LOG.error("Contract Assumption is violated")
            # still return a behavior?
            return
        
        behavior_set = env_set.intersect(self._contract.guarantee)
        ret, sample = behavior_set.sample()
        for var, val in sample.items():
            LOG.debug(f"{var.id}: {val}")

        #check if there is other behaviors
        sample_set = _create_set_from_behavior(sample)
        check_set = behavior_set.intersect(sample_set.complement())
        if check_set.is_satifiable():
            LOG.debug(f"Multiple behavior exist!")
            ret, sample = check_set.sample()
            for var, val in sample.items():
                LOG.debug(f"{var.id}: {val}")

    def evaluate(self, stimulus: Stimulus, evaluator: Evaluator = None):
        if evaluator is None:
            evaluator = self._evaluator
        if evaluator is None:
            raise Exception("No evaluator defined!")
        
        env_set = _create_set_from_behavior(stimulus.var_val_map)
        # check if the stimulus always satisfy the assumption
        # check if stimulus has elements in not A
        if env_set.intersect(self._contract.assumption.complement()).is_satifiable():
            LOG.error("Contract Assumption is violated")
            # still return a behavior?
            return
        
        behavior_set = env_set.intersect(self._contract.guarantee)
        obj_vals = self._evaluator.evaluate(behavior_set=behavior_set)

        return obj_vals
    
    def evaluate_range(self, stimulus: Stimulus, evaluator: Evaluator = None):
        if evaluator is None:
            evaluator = self._evaluator
        if evaluator is None:
            raise Exception("No evaluator defined!")
        
        env_set = _create_set_from_behavior(stimulus.var_val_map)
        # check if the stimulus always satisfy the assumption
        # check if stimulus has elements in not A
        if env_set.intersect(self._contract.assumption.complement()).is_satifiable():
            LOG.error("Contract Assumption is violated")
            # still return a behavior?
            return
        
        behavior_set = env_set.intersect(self._contract.guarantee)
        max_vals = self._evaluator.evaluate_max(behavior_set=behavior_set)
        min_vals = self._evaluator.evaluate_max(behavior_set=behavior_set, minimum=True)

        return max_vals, min_vals


        

    

            
def _create_set_from_behavior(behavior: dict):
    stimulus_set = None
    for var, val in behavior.items():
        eq_set = FOLClauseSet.generate_var_val_equivalence_constraint_set(var = var, val = val)
        if stimulus_set is None:
            stimulus_set = eq_set
        else:
            stimulus_set = stimulus_set.intersect(eq_set)
    return stimulus_set


