import pytest
from contractda.design import Port, VarType, PortDirection

@pytest.fixture
def example_ports():
    return [Port(port_name="port1", port_type=VarType.REAL, direction="INOUT"),
            Port(port_name="port2", port_type=VarType.REAL, direction=PortDirection.OUTPUT),
            Port(port_name="port3", port_type="INTEGER", direction="INPUT"),
            Port(port_name="port4", port_type="BOOL", direction=PortDirection.INOUT),
            ]
@pytest.fixture
def example_port_json():
    return [
        {
            "port_name": "port5",
            "port_type": "INTEGER",
            "direction": "INPUT"
        },
        {
            "port_name": "port6",
            "port_type": "BOOL",
            "direction": "INPUT"
        },
        {
            "port_name": "port7",
            "port_type": "REAL",
            "direction": "OUTPUT"
        },
    ]

def test_port_name(example_ports):
    assert(example_ports[0].port_name == "port1")
    assert(example_ports[1].port_name == "port2")
    assert(example_ports[2].port_name == "port3")
    assert(example_ports[3].port_name == "port4")

    assert(example_ports[0].level_name == "port1")
    assert(example_ports[1].level_name == "port2")
    assert(example_ports[2].level_name == "port3")
    assert(example_ports[3].level_name == "port4")

    assert(example_ports[0].hier_name == "port1")
    assert(example_ports[1].hier_name == "port2")
    assert(example_ports[2].hier_name == "port3")
    assert(example_ports[3].hier_name == "port4")

def test_port_type(example_ports):
    assert(example_ports[0].port_type == VarType.REAL)
    assert(example_ports[1].port_type == VarType.REAL)
    assert(example_ports[2].port_type == VarType.INTEGER)
    assert(example_ports[3].port_type == VarType.BOOL)

def test_direction(example_ports):
    assert(example_ports[0].direction == PortDirection.INOUT)
    assert(example_ports[1].direction == PortDirection.OUTPUT)
    assert(example_ports[2].direction == PortDirection.INPUT)
    assert(example_ports[3].direction == PortDirection.INOUT)

def test_str(example_ports):
    str(example_ports[0])
    str(example_ports[1])
    str(example_ports[2])
    str(example_ports[3])

def test__create_var_using_hier_name(example_ports):
    var = Port._create_var_using_hier_name(example_ports[0])
    assert(var.id == example_ports[0].hier_name)
    assert(var._var_type == example_ports[0].port_type)

def test__level_name_by_instance_name(example_ports):
    instance_name = "Test_instance"
    ret_name = example_ports[0]._level_name_by_instance_name(instance_name=instance_name)
    assert(ret_name == f"{instance_name}.{example_ports[0].port_name}")

def test_report(example_ports):
    example_ports[0].report()
    example_ports[1].report()
    example_ports[2].report()
    example_ports[3].report()

def test_from_dict(example_port_json):
    for example in example_port_json:
        ex_port = Port.from_dict(example)
        assert(ex_port.port_name == example["port_name"])
        assert(ex_port.port_type == VarType[example["port_type"]] )
        assert(ex_port.direction == PortDirection[example["direction"]] )

        export_dict = ex_port.to_dict()
        assert(len(export_dict) == len(example))
        for key in export_dict.keys():
            export_dict[key] == example[key]

def test_from_dict_fail():
    obj1 = {
            "port_name": "port5",
            "direction": "INPUT"
    }
    obj2 = {
            "port_type": "INTEGER",
            "direction": "INPUT"
    }
    obj3 = {
            "port_name": "port5",
            "port_type": "INTEGER",
    }
    assert(Port.from_dict(obj1) == None)
    assert(Port.from_dict(obj2) == None)
    assert(Port.from_dict(obj3) == None)
