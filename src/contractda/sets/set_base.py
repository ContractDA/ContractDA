from abc import ABC, abstractmethod
from typing import Callable

class SetBase(ABC):
    """
    Class for defining sets
    
    """

    def __init__(self):
        pass

    ######################
    #   Set Operation
    ######################
    @abstractmethod
    @staticmethod 
    def union(set1, set2):
        pass

    @abstractmethod
    @staticmethod 
    def intersect(set1, set2):
        pass

    @abstractmethod
    @staticmethod 
    def difference(set1, set2):
        pass

    @abstractmethod
    @staticmethod 
    def complement(set1, set2):
        pass

    @abstractmethod
    @staticmethod 
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