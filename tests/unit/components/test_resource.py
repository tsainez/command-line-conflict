from command_line_conflict.components.resource import Resource


def test_resource_initialization():
    """Tests that a Resource component can be initialized with default values."""
    resource = Resource()
    assert resource.resource_type == "minerals"
    assert resource.amount == 10000


def test_resource_initialization_with_custom_values():
    """Tests that a Resource component can be initialized with custom values."""
    resource = Resource(resource_type="gas", amount=5000)
    assert resource.resource_type == "gas"
    assert resource.amount == 5000