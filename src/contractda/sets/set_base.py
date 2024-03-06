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
    def union(set1, set2):
        pass

    @abstractmethod
    def intersect(set1, set2):
        pass

    @abstractmethod
    def difference(set1, set2):
        pass

    @abstractmethod
    def complement(set1, set2):
        pass

    @abstractmethod
    def project(set1):
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