from command_line_conflict.components.building import Building


def test_building_initialization():
    """Tests that a Building component can be initialized."""
    building = Building()
    assert isinstance(building, Building)