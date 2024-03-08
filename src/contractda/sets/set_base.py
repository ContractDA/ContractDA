from abc import ABC, abstractmethod
from typing import Callable




class SetBase(ABC):
    """
    Base class for different set objects
    """

    def __init__(self):
        pass

    ######################
    #   Set Operation
    ######################
    @abstractmethod
    def union(self, set2):
        pass

    @abstractmethod
    def intersect(self, set2):
        pass

    @abstractmethod
    def difference(self, set2):
        pass

    @abstractmethod
    def complement(self):
        pass

    @abstractmethod
    def project(self, vars, is_refine = True):
        pass
    ######################
    #   Extraction
    ######################
    @abstractmethod
    def sample(self):
        """
        Sample an element in the set
        """
        pass

    @abstractmethod
    def __iter__(self):
        pass
    
    @abstractmethod
    def __next__(self):
        pass