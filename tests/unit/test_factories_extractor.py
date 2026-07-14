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
from command_line_conflict.game_state import GameState


def test_create_extractor(game_state: GameState):
    """Test creating an extractor unit."""
    x, y = 15.0, 25.0
    player_id = 1

    entity_id = factories.create_extractor(game_state, x, y, player_id, is_human=True)

    # Check that entity was created
    assert entity_id is not None

    # Check Position
    pos = game_state.get_component(entity_id, Position)
    assert pos is not None
    assert pos.x == x
    assert pos.y == y

    # Check Renderable
    render = game_state.get_component(entity_id, Renderable)
    assert render is not None
    assert render.icon == "E"

    # Check Movable
    movable = game_state.get_component(entity_id, Movable)
    assert movable is not None
    assert movable.speed == 1.5
    assert movable.intelligent is True

    # Check Health
    health = game_state.get_component(entity_id, Health)
    assert health is not None
    assert health.hp == 50
    assert health.max_hp == 50

    # Check Detection
    detection = game_state.get_component(entity_id, Detection)
    assert detection is not None
    assert detection.detection_range == 5

    # Check Vision
    vision = game_state.get_component(entity_id, Vision)
    assert vision is not None
    assert vision.vision_range == 5

    # Check Selectable
    selectable = game_state.get_component(entity_id, Selectable)
    assert selectable is not None

    # Check Player
    player = game_state.get_component(entity_id, Player)
    assert player is not None
    assert player.player_id == player_id
    assert player.is_human is True

    # Check UnitIdentity
    identity = game_state.get_component(entity_id, UnitIdentity)
    assert identity is not None
    assert identity.name == "extractor"
