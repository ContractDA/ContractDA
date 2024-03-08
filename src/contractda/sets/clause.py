from abc import ABC, abstractmethod

class Clause(ABC):
    """Base Class for Clause
    
    A Clause is a description that express the set implicitly through a condition.

    Given an assignment of the values to the variables, the values is in the set if the condition evaluates to true.
    """

    def __init__(self):
        pass