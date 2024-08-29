

class Design():
    def __init__(self, name):
        """A design consists of systems in multiple levels
        Any operation in the design level will be reflected recursively to all the systems in the design
        """
        self._name 
        self._system = None # the actual system for this design
        self._spec = []
        self._obj = []

    def set_specification(self):
        pass