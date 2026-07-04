from command_line_conflict import factories
from command_line_conflict.components.vision import Vision


def test_rover_factory_has_vision(game_state):
    """Friendly buildings must clear their own fog of war."""
    factory_id = factories.create_rover_factory(game_state, 10.0, 10.0, player_id=1, is_human=True)
    vision = game_state.get_component(factory_id, Vision)
    assert vision is not None
    assert vision.vision_range >= 3


def test_arachnotron_factory_has_vision(game_state):
    factory_id = factories.create_arachnotron_factory(game_state, 10.0, 10.0, player_id=1, is_human=True)
    vision = game_state.get_component(factory_id, Vision)
    assert vision is not None
    assert vision.vision_range >= 3
