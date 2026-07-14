import pytest

from command_line_conflict.components.factory import Factory


def test_factory_valid_units():
    f = Factory("chassis", "rover")
    assert f.input_unit == "chassis"
    assert f.output_unit == "rover"


def test_factory_invalid_input_unit():
    with pytest.raises(ValueError):
        Factory("invalid", "rover")


def test_factory_invalid_output_unit():
    with pytest.raises(ValueError):
        Factory("chassis", "invalid")
