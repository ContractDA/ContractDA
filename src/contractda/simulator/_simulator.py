from contractda.contracts import ContractBase
from contractda.design import System
from contractda.logger._logger import LOG
from typing import Callable
from contractda.sets import FOLClauseSet

# to be removed


class Stimulus(object):
    """class that represents the behaviors"""
    def __init__(self, stimulus_map: dict):
        self._map = stimulus_map

    @property
    def var_val_map(self) -> dict:
        return self._map
        


class Simulator(object):
    """wrapper class for performing simulation"""
    def __init__(self, evaluator: Callable = None, options: dict = None, contract: ContractBase = None, system: System = None ):
        if system is None and contract is None:
            err_msg = "Need at least one system or contract"
            LOG.error(err_msg)
            raise Exception(err_msg)
        if system is None:
            self._contract = contract
        else:
            self._contract = system._get_single_system_contract()
        self._contract = contract
        self._evaluator = evaluator
        self._options = options
        
    def simulate(self, stimulus: Stimulus):

        eq_sets = []
        stimulus_set = None

        for var, val in stimulus.var_val_map.items():
            eq_set = FOLClauseSet.generate_var_val_equivalence_constraint_set(var = var, val = val)
            if stimulus_set is None:
                stimulus_set = eq_set
            stimulus_set = stimulus_set.intersect(eq_set)

        self._contract.assumption
        # check if the stimulus always satisfy the assumption
        # check if stimulus has elements in not A
        if stimulus_set.intersect(self._contract.assumption.complement()).is_satifiable():
            LOG.error("Contract Assumption is violated")
            return
        
        behavior_set = stimulus_set.intersect(self._contract.guarantee)
        ret, sample = behavior_set.sample()
        for var, val in sample.items():
            LOG.debug(f"{var.id}: {val}")

            


        pass


