from contractda.design import DesignLevelManager

class Context():
    """Class Context: Management of all the objects in the shell"""
    def __init__(self):
        self._context_name = "global"
        self._design_mgr: DesignLevelManager =  DesignLevelManager()
        self._contract_mgr = None

    def report(self):
        print("Report Context")

global_context = Context()
