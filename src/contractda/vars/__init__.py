""" 
The :mod:`contract.sets` module defines a base class for set object as described extensively in :class:`~contract.sets.SetBase`.

.. rubric:: Classes

.. autosummary::
    :toctree: 
    :template: class.rst

    ~contractda.vars.Var
    ~contractda.vars.IntVar
    ~contractda.vars.BoolVar
    ~contractda.vars.CategoricalVar
    ~contractda.vars.VarType
"""

from contractda.vars._var import Var, IntVar, BoolVar, RealVar, CategoricalVar, VarType

__all__ = [
    "Var",
    "IntVar",
    "BoolVar",
    "RealVar",
    "CategoricalVar",
    "VarType"
]