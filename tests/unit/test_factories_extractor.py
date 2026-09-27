import pytest
from command_line_conflict import factories
from command_line_conflict.components.position import Position
from command_line_conflict.components.renderable import Renderable
from command_line_conflict.components.movable import Movable
from command_line_conflict.components.health import Health
from command_line_conflict.components.detection import Detection
from command_line_conflict.components.vision import Vision
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.components.player import Player
from command_line_conflict.components.unit_identity import UnitIdentity


def test_create_extractor(game_state):
    """Verify that create_extractor creates an entity with expected components."""
    extractor_id = factories.create_extractor(game_state, 10.0, 15.0, player_id=1, is_human=True)

    pos = game_state.get_component(extractor_id, Position)
    assert pos is not None
    assert pos.x == 10.0
    assert pos.y == 15.0

    renderable = game_state.get_component(extractor_id, Renderable)
    assert renderable is not None
    assert renderable.icon == "E"

    movable = game_state.get_component(extractor_id, Movable)
    assert movable is not None
    assert movable.speed == 1.5
    assert movable.intelligent is True

    health = game_state.get_component(extractor_id, Health)
    assert health is not None
    assert health.hp == 50
    assert health.max_hp == 50

    detection = game_state.get_component(extractor_id, Detection)
    assert detection is not None
    assert detection.detection_range == 5

    vision = game_state.get_component(extractor_id, Vision)
    assert vision is not None
    assert vision.vision_range == 5

    selectable = game_state.get_component(extractor_id, Selectable)
    assert selectable is not None

    player = game_state.get_component(extractor_id, Player)
    assert player is not None
    assert player.player_id == 1
    assert player.is_human is True

    identity = game_state.get_component(extractor_id, UnitIdentity)
    assert identity is not None
    assert identity.name == "extractor"
