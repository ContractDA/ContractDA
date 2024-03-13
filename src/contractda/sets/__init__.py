""" 
The :mod:`contract.sets` module defines a base class for set object as described extensively in :class:`~contract.sets.SetBase`.

.. rubric:: Classes

.. autosummary::
    :toctree: 
    :template: class.rst

    ~contractda.sets.ExplicitSet
    ~contractda.sets.ClauseSet
    ~contractda.sets.FOLClauseSet
    ~contractda.sets.SetBase
"""

from contractda.sets._explicit_set import ExplicitSet
from contractda.sets._clause_set import ClauseSet
from contractda.sets._fol_clause_set import FOLClauseSet
from contractda.sets._base import SetBase

__all__ = [
    "ExplicitSet",
    "ClauseSet",
    "FOLClauseSet",
#    "LTLClause"
    "SetBase",
]