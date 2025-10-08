from command_line_conflict.components.factory import Factory


def test_factory_initialization():
    """Tests that a Factory component can be initialized."""
    factory = Factory(unit_types=["chassis", "extractor"], production_time=5.0)
    assert factory.unit_types == ["chassis", "extractor"]
    assert factory.production_time == 5.0
    assert factory.production_queue == []
    assert factory.production_progress == 0.0