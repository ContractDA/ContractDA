
class Context():
    """Class Context: Management of all the objects in the program"""
    def __init__(self):
        self._context_name = "global"
        self._system_mgr = None
        self._contract_mgr = None

    def report(self):
        print("Report Context")

global_context = Context()
