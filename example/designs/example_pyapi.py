from contractda.design._system import System
from contractda.design._connections import Connection, Port
from contractda.design._port import VarType, PortDirection
from contractda.design._design import Design
from contractda.design_api._design_mgr import DesignLevelManager
#from contractda.design._contracts import AGSystemContract

if __name__ == "__main__":
    # describe system
    p_a = Port(port_name="a", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_b = Port(port_name="b", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_c = Port(port_name="c", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_x = Port(port_name="x", port_type=VarType.REAL, direction=PortDirection.OUTPUT)
    p_1a = Port(port_name="a", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_1b = Port(port_name="b", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_1t1 = Port(port_name="t1", port_type=VarType.REAL, direction=PortDirection.OUTPUT)
    p_2c = Port(port_name="c", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_2d = Port(port_name="d", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_2t2 = Port(port_name="t2", port_type=VarType.REAL, direction=PortDirection.OUTPUT)

    sub1 = System(system_name="sub1", ports=[p_1a, p_1b, p_1t1], contracts=None)
    sub2 = System(system_name="sub2", ports=[p_2c, p_2d, p_2t2], contracts=None)

    sys = System(system_name="test_sys", ports=[p_a, p_b, p_c, p_x], contracts=None)
    sys.add_subsystem(sub1)
    sys.add_subsystem(sub2)

    conn1 = Connection(name="net1", terminals=[p_a, p_1a])
    conn2 = Connection(name="net2", terminals=[p_b, p_1b])
    conn3 = Connection(name="net3", terminals=[p_c, p_2c])
    conn4 = Connection(name="net4", terminals=[p_x, p_2t2])
    conn5 = Connection(name="net5", terminals=[p_1t1, p_2d])

    sys.add_connection(conn1)
    sys.add_connection(conn2)
    sys.add_connection(conn3)
    sys.add_connection(conn4)
    sys.add_connection(conn5)



    sys.report()
    for subsystem in sys.subsystems.values():
        subsystem.report()

    # set contracts
    #sys.set_contract_ag(assumption="a > 0", guarantee="x = a + b + c", language="FOL")# use port name
    #sub1.set_contract_ag(assumption="a > 0", guarantee="t1 = a + b", language="FOL")# use port name
    #sub2.set_contract_ag(assumption="true", guarantee="t2 = c + d", language="FOL")# use port name

    # let the user do whatever he likes to define, using minimal check to accerlate construction
    # call manager before performing task
    mgr = DesignLevelManager()
    mgr.compile_system(sys)
    sys.add_connection(conn1)
    sys.add_connection(conn2)
    sys.add_connection(conn3)
    sys.add_subsystem(sub1)

    #mgr.check_system_validity(sys) # check if there is connection error or problem in using it recursively
    #mgr.verify_system(sys)
