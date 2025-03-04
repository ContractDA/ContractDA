from contractda.sets import Clause, ClauseSet, FOLClauseSet
from contractda.vars import Var

from typing import Type

class DesignExpression():
    """Design Expression: Class for defining constraints and objective
    For example: sys.a <= 5 as a constraints (environment for performing simulation)
    or sys.x + sys.y == obj as an objective function
    
    """

    def __init__(self, expr:str, clause_type: Type[ClauseSet] = FOLClauseSet, aux_vars: list[Var] = None):
        self._aux_vars: list[Var] 
        if aux_vars is not None:
            self._aux_vars = aux_vars
        else:
            self._aux_vars = []

        self._clause_type: Type[ClauseSet] = clause_type
        self._expr: str = expr

    def get_clause_set(self, design_vars: list[Var]):
        """Accept design vars to form the propert clause set"""
        all_vars = design_vars + self._aux_vars
        clause_set = self._clause_type(vars=all_vars, expr=self._expr)
        return clause_set
    
    @property
    def aux_vars(self) -> list[Var]:
        return self._aux_vars

