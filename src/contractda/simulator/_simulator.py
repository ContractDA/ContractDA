from contractda.contracts import ContractBase
from contractda.design import System
from contractda.logger._logger import LOG
from typing import Callable, Any, Type
from contractda.sets import FOLClauseSet, SetBase, ClauseSet
from contractda.vars import Var
#from contractda.sets._parsers._expression_parser import fol_exp_parser

# to be removed


class Stimulus(object):
    """class that represents the behaviors

    the behavior is set as a dictionary that maps a :py:class:`~contract.contracts.Var` to a value
    """
    def __init__(self, stimulus_map: dict[Var, Any]):
        self._map: dict[Var, Any] = stimulus_map

    @property
    def var_val_map(self) -> dict[Var, Any]:
        return self._map
    
    @property 
    def value(self, var: Var) -> Any:
        if var in self.var_val_map:
            return self.var_val_map[var]
        else:
            LOG.error(f"Variable {var.id} not found!")
            return None
    
    def __str__(self):
        ret = ""
        for var, val in self.var_val_map.items():
            ret += f"{var.id}: {val}, "
        return ret
        
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
    def __init__(self, clause_set: ClauseSet, clause_objective: list[Var]):
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
        behavior_set = _create_set_from_behavior(sample=behavior.var_val_map, set_type=type(self._clause_set))
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
                    constrained_set = behavior_set.generate_var_val_lt_constraint_set(self._obj[0], max_val)
                else:
                    constrained_set = behavior_set.generate_var_val_gt_constraint_set(self._obj[0], max_val)
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

    def _check_evaluation_uniqueness(self, behavior_set: SetBase, val: Any) -> list[Any]:
        uniqueness_set = behavior_set.generate_var_val_equivalence_constraint_set(var = self._obj[0], val = val)
        solver_set = self.objective_set.intersect(behavior_set).intersect(uniqueness_set)
        if solver_set.is_satifiable():
            return False
        else:
            return True

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
        self._set_type: Type[SetBase] = type(self._contract.environment)
        self._options = options

        self._behavior_history: list[Stimulus] = []
        
    def simulate(self, stimulus: Stimulus, environement: SetBase = None,  num_unique_simulations: int = 1) -> list[Stimulus]:
        """Simulate the contract using the stimulus

        :param Stimulus stimulus: the behaviors provided by the environment
        :param int num_unique_simulations: number of unique simulation needed for the stimulus
        """
        # TODO: Return a set or a stimulus?
        set_type = type(self._contract.environment)
        env_set = _create_set_from_behavior(stimulus.var_val_map, set_type=self._set_type)
        
        # self._contract.assumption
        # check if the stimulus always satisfy the assumption
        # check if stimulus has elements in not A
        if not self._contract.check_environment_satisfy(env_set):
            LOG.error("Contract Assumption is violated")
            # still return a behavior? must be careful as CB contract allow more behaviors!
            return 
        
        ret: list[Stimulus] = []
        constraint = None
        for i in range(num_unique_simulations):
            behavior = self._simulate_with_environment(env_set=env_set, constraint=constraint)
            if behavior is None:
                LOG.warn(f"Insufficient behavior to reach {num_unique_simulations} behaviors ({len(ret)} generated)")
                break
            # TODO: update constraints
            newconstraint = _create_set_from_behavior(behavior.var_val_map, set_type=self._set_type).complement()
            if constraint is None:
                constraint = newconstraint
            else:
                constraint = constraint.intersect(newconstraint)
            ret.append(behavior)


        
        return ret


    def _simulate_with_environment(self, env_set: SetBase, constraint: SetBase = None):
        """Generate a behavior based on the environment and constraint, assuming the env_set is a proper environment"""
        behavior_set = env_set.intersect(self._contract.implementation)
        if constraint is not None:
            behavior_set = behavior_set.intersect(constraint)
        try:
            sat, sample = behavior_set.sample()
        except Exception as e:
            sat = False

        if sat:
            return Stimulus(sample)
        else:
            return None

    def _check_behavior_uniqueness(self, found_behavior: Stimulus, env_set: SetBase):
        """Check if the behavior is unique given the environment and an already found behavior, assuming env_set is a subset of the proper environment for the contract
        
        """
        #check if there is other behaviors
        sample_set = _create_set_from_behavior(found_behavior.var_val_map, set_type=self._set_type)

        behavior_set = env_set.intersect(self._contract.implementation)
        check_set = behavior_set.intersect(sample_set.complement())
        if check_set.is_satifiable():
            LOG.debug(f"Multiple behavior exist!")
            #ret, sample = check_set.sample()
            return False
        else:
            return True

            



    def evaluate(self, stimulus: Stimulus, evaluator: Evaluator = None, check_unique = False):
        if evaluator is None:
            evaluator = self._evaluator
        if evaluator is None:
            raise Exception("No evaluator defined!")
        
        
        env_set = _create_set_from_behavior(stimulus.var_val_map, set_type=self._set_type)
        # check if the stimulus always satisfy the assumption
        # check if stimulus has elements in not A
        if not self._contract.check_environment_satisfy(env_set):
            LOG.error("Contract Assumption is violated")
            # still return a behavior?
            return
        
        behavior_set = env_set.intersect(self._contract.implementation)
        obj_vals = evaluator.evaluate(behavior_set=behavior_set)
        if check_unique:
            pass

        return obj_vals
    
    def _check_evaluate_uniqueness(self, found_value: Any, env_set: SetBase):
        pass
    
    def evaluate_range(self, stimulus: Stimulus, evaluator: Evaluator = None):
        if evaluator is None:
            evaluator = self._evaluator
        if evaluator is None:
            raise Exception("No evaluator defined!")
        
        env_set = _create_set_from_behavior(stimulus.var_val_map, self._set_type)
        # check if the stimulus always satisfy the assumption
        # check if stimulus has elements in not A
        if not self._contract.check_environment_satisfy(env_set):
            LOG.error("Contract Assumption is violated")
            # still return a behavior?
            return
        
        behavior_set = env_set.intersect(self._contract.implementation)
        max_vals = evaluator.evaluate_max(behavior_set=behavior_set)
        min_vals = evaluator.evaluate_max(behavior_set=behavior_set, minimum=True)

        return max_vals, min_vals


        

    

            
def _create_set_from_behavior(behavior: dict, set_type: Type[ClauseSet] = FOLClauseSet):
    stimulus_set = None
    for var, val in behavior.items():
        eq_set = set_type.generate_var_val_equivalence_constraint_set(var = var, val = val)
        if stimulus_set is None:
            stimulus_set = eq_set
        else:
            stimulus_set = stimulus_set.intersect(eq_set)
    return stimulus_set


