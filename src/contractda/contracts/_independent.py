import copy

from contractda.contracts._contract_base import ContractBase
from contractda.sets import SetBase, FOLClauseSet, ExplicitSet
from contractda.vars import Var
from contractda.solvers import SolverInterface
from contractda.sets._fol_lan import name_remap
from contractda.contracts._agcontract import AGContract
from contractda.logger._logger import LOG

class IndependentAlgo():

    def __init__(system, sub1, sub2):
        pass