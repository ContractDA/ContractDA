from contractda.design._module import Module
from contractda.design._connections import ModuleConnection
from contractda.design._port import VarType, PortDirection, Port
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
            "description": "x = a+b+c+d"
        }
    }
}

json_obj2 = {
    "name": "C2",
    "type": "AG",
    "content": {
        "assumption": {
            "set_type": "FOL",
            "description": "a >= 0"
        },
        "guarantee": {
            "set_type": "FOL",
            "description": "x = a + b"
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
            "description": "x = a + b"
        }
    }
}

if __name__ == "__main__":
    p_a = Port(port_name="a", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_b = Port(port_name="b", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_c = Port(port_name="c", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_d = Port(port_name="d", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_x = Port(port_name="x", port_type=VarType.REAL, direction=PortDirection.OUTPUT)

    sys = Module(name="test_sys", ports=[p_a, p_b, p_c, p_d, p_x], contracts=[SystemContract.from_dict(json_obj1)])

    p_1a = Port(port_name="a", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_1b = Port(port_name="b", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_1x = Port(port_name="x", port_type=VarType.REAL, direction=PortDirection.OUTPUT)
    p_2a = Port(port_name="a", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_2b = Port(port_name="b", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_2x = Port(port_name="x", port_type=VarType.REAL, direction=PortDirection.OUTPUT)

    adder1 = Module(name="adder1", ports=[p_1a, p_1b, p_1x], contracts=[SystemContract.from_dict(json_obj2)])
    adder2 = Module(name="adder2", ports=[p_2a, p_2b, p_2x], contracts=[SystemContract.from_dict(json_obj3)])

    sys.add_submodule(submodule=adder1, instance_name="add1")
    sys.add_submodule(submodule=adder1, instance_name="add2")
    sys.add_submodule(submodule=adder2, instance_name="add3")


    conn1 = ModuleConnection(name="net1", terminals=[sys.ports["a"], p_1a], instance_names=["test_sys", "add1"])
    conn2 = ModuleConnection(name="net2", terminals=[sys.ports["b"], p_1b], instance_names=["test_sys", "add1"])
    conn3 = ModuleConnection(name="net3", terminals=[p_1x, p_1a], instance_names=["add1", "add2"])
    conn4 = ModuleConnection(name="net4", terminals=[sys.ports["c"], p_1b], instance_names=["test_sys", "add2"])
    conn5 = ModuleConnection(name="net5", terminals=[p_1x, p_2a], instance_names=["add2", "add3"])
    conn6 = ModuleConnection(name="net6", terminals=[sys.ports["d"], p_2b], instance_names=["test_sys", "add3"])
    conn7 = ModuleConnection(name="net7", terminals=[p_2x, sys.ports["x"]], instance_names=["add3", "test_sys"])

    sys.add_connection(conn1)
    sys.add_connection(conn2)
    sys.add_connection(conn3)
    sys.add_connection(conn4)
    sys.add_connection(conn5)





    sys.report()
    for submodule in sys.submodules.values():
        submodule.report()

    json_obj = sys.to_dict()
    print(json_obj)
    print(" read json obj")
    newsys = Module.from_dict(dict_obj=json_obj, modules={"adder1":adder1, "adder2": adder2})
    newsys.report()
    print(newsys.to_dict())


    with open("./example/design_files/simple_module_adder1.json", "w") as file:
        json.dump(adder1.to_dict(), file, indent=4)
    with open("./example/design_files/simple_module_adder2.json", "w") as file:
        json.dump(adder1.to_dict(), file, indent=4)
    with open("./example/design_files/simple_module_sys.json", "w") as file:
        json.dump(newsys.to_dict(), file, indent=4)