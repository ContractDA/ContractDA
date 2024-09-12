import pytest
from contractda.design import Port, VarType, PortDirection
from contractda.design import Connection

@pytest.fixture
def example_ports():
    return [Port(port_name="port1", port_type=VarType.REAL, direction="INOUT"),
            Port(port_name="port2", port_type=VarType.REAL, direction=PortDirection.OUTPUT),
            Port(port_name="port3", port_type="INTEGER", direction="INPUT"),
            Port(port_name="port4", port_type="BOOL", direction=PortDirection.INOUT),
            ]

@pytest.fixture
def example_connection(example_ports):
    return Connection(name="net1", terminals=example_ports)

def test_name(example_connection):
    assert(example_connection.name == "net1")
    assert(example_connection.hier_name == "net1")

def test_str(example_connection):
    str(example_connection)

def test_terminals(example_connection, example_ports):
    assert(len(example_connection.terminals) == len(example_ports))
    for term in example_connection.terminals:
        assert(term in example_ports)

def test_report(example_connection):
    example_connection.report()







    