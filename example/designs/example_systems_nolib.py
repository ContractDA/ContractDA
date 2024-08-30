from contractda.design._system import System, LibSystem
from contractda.design._connections import Connection, Port
from contractda.design._port import VarType, PortDirection
from contractda.design._system_contracts import SystemContract
import json

json_obj1 = {
    "name": "C1",
    "type": "AG",
    "content": {
        "assumption": {
            "set_type": "FOL",
            "description": "a >= 0"
        },
        "guarantee": {
            "set_type": "FOL",
            "description": "x = a+b+c"
        }
    }
}

json_obj2 = {
    "name": "C2",
    "type": "AG",
    "content": {
        "assumption": {
            "set_type": "FOL",
            "description": "a1 >= 0"
        },
        "guarantee": {
            "set_type": "FOL",
            "description": "t1 = a1 + b"
        }
    }
}


json_obj3 = {
    "name": "C3",
    "type": "AG",
    "content": {
        "assumption": {
            "set_type": "FOL",
            "description": "true"
        },
        "guarantee": {
            "set_type": "FOL",
            "description": "t2 = c + d"
        }
    }
}

if __name__ == "__main__":
    p_a = Port(port_name="a", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_b = Port(port_name="b", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_c = Port(port_name="c", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_x = Port(port_name="x", port_type=VarType.REAL, direction=PortDirection.OUTPUT)

    sys = System(system_name="test_sys", ports=[p_a, p_b, p_c, p_x], contracts=[SystemContract.from_dict(json_obj1)])

    p_1a = Port(port_name="a1", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_1b = Port(port_name="b", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_1t1 = Port(port_name="t1", port_type=VarType.REAL, direction=PortDirection.OUTPUT)
    p_2c = Port(port_name="c", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_2d = Port(port_name="d", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_2t2 = Port(port_name="t2", port_type=VarType.REAL, direction=PortDirection.OUTPUT)

    sub1 = System(system_name="sub1", ports=[p_1a, p_1b, p_1t1], contracts=[SystemContract.from_dict(json_obj2)])
    sub2 = System(system_name="sub2", ports=[p_2c, p_2d, p_2t2], contracts=[SystemContract.from_dict(json_obj3)])


    conn1 = Connection(name="net1", terminals=[sys.ports["a"], p_1a])
    conn2 = Connection(name="net2", terminals=[sys.ports["b"], p_1b])
    conn3 = Connection(name="net3", terminals=[sys.ports["c"], p_2c])
    conn4 = Connection(name="net4", terminals=[sys.ports["x"], p_2t2])
    conn5 = Connection(name="net5", terminals=[p_1t1, p_2d])

    sys.add_connection(conn1)
    sys.add_connection(conn2)
    sys.add_connection(conn3)
    sys.add_connection(conn4)
    sys.add_connection(conn5)



    sys.add_subsystem(sub1)
    sys.add_subsystem(sub2)

    sys.report()
    for subsystem in sys.subsystems.values():
        subsystem.report()

    json_obj = sys.to_dict()
    print(json_obj)
    print(" read json obj")
    newsys = System.from_dict(dict_obj=json_obj)
    newsys.report()
    print(newsys.to_dict())


    with open("./example/design_files/simple_design.json", "w") as file:
        json.dump(newsys.to_dict(), file, indent=4)
