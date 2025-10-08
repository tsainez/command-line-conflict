from command_line_conflict.components.builder import Builder


def test_builder_initialization():
    """Tests that a Builder component can be initialized."""
    builder = Builder(build_types=["unit_factory"])
    assert builder.build_types == ["unit_factory"]
    assert builder.build_target is None
    assert builder.build_progress == 0.0