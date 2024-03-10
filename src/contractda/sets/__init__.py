""" 
The :mod:`contract.sets` module defines a base class for set object as described extensively in :class:`~contract.sets.SetBase`.

.. rubric:: Classes

.. autosummary::
    :toctree: 
    :template: class.rst

    ~contractda.sets.ExplicitSet
    ~contractda.sets.ClauseSet
    ~contractda.sets.SetBase
    ~contractda.sets.Var
    ~contractda.sets.IntVar
    ~contractda.sets.BoolVar
    ~contractda.sets.CategoricalVar
"""

from contractda.sets._explicit_set import ExplicitSet
from contractda.sets._clause_set import ClauseSet
from contractda.sets._base import SetBase
from contractda.sets._var import Var, IntVar, BoolVar, RealVar, CategoricalVar

__all__ = [
    "ExplicitSet",
    "ClauseSet",
    "SetBase",
    "Var",
    "IntVar",
    "BoolVar",
    "RealVar",
    "CategoricalVar",
]