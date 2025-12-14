"""A collection of factory functions for creating game entities."""

from . import config
from .components.attack import Attack
from .components.confetti import Confetti
from .components.detection import Detection
from .components.factory import Factory
from .components.flee import Flee
from .components.health import Health
from .components.movable import Movable
from .components.player import Player
from .components.position import Position
from .components.renderable import Renderable
from .components.selectable import Selectable
from .components.unit_identity import UnitIdentity
from .components.vision import Vision
from .components.wander import Wander
from .game_state import GameState
from .logger import log

# TODO: Create a map with factories for the player to fight against.


def create_chassis(
    game_state: GameState, x: float, y: float, player_id: int, is_human: bool = False
) -> int:
    """Creates a new chassis unit.
    Args:
        game_state: The current state of the game.
        x: The x-coordinate where the unit will be created.
        y: The y-coordinate where the unit will be created.
        player_id: The ID of the player who owns this unit.
        is_human: True if the player is human-controlled.
    Returns:
        The entity ID of the newly created unit.
    """
    entity_id = game_state.create_entity()
    if config.DEBUG:
        log.debug(
            f"Created chassis (ID: {entity_id}) at ({x}, {y}) for player {player_id}"
        )
    game_state.add_component(entity_id, Position(x, y))
    color = config.PLAYER_COLORS.get(player_id, (255, 255, 255))
    game_state.add_component(entity_id, Renderable(icon="C", color=color))
    game_state.add_component(entity_id, Movable(speed=2, intelligent=False))
    game_state.add_component(entity_id, Health(hp=80, max_hp=80))
    game_state.add_component(
        entity_id, Attack(attack_damage=10, attack_range=1, attack_speed=1.0)
    )
    game_state.add_component(entity_id, Detection(detection_range=1))
    game_state.add_component(entity_id, Vision(vision_range=5))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Player(player_id=player_id, is_human=is_human))
    game_state.add_component(entity_id, UnitIdentity(name="chassis"))
    return entity_id


def create_wildlife(
    game_state: GameState, x: float, y: float
) -> int:
    """Creates a new wildlife unit (Neutral).
    Args:
        game_state: The current state of the game.
        x: The x-coordinate where the unit will be created.
        y: The y-coordinate where the unit will be created.
    Returns:
        The entity ID of the newly created unit.
    """
    entity_id = game_state.create_entity()
    if config.DEBUG:
        log.debug(f"Created wildlife (ID: {entity_id}) at ({x}, {y})")
    game_state.add_component(entity_id, Position(x, y))
    color = config.PLAYER_COLORS.get(config.NEUTRAL_PLAYER_ID, (128, 128, 128))
    game_state.add_component(entity_id, Renderable(icon="w", color=color))
    game_state.add_component(entity_id, Movable(speed=1.0, intelligent=False))
    game_state.add_component(entity_id, Health(hp=40, max_hp=40))
    game_state.add_component(
        entity_id, Attack(attack_damage=8, attack_range=1, attack_speed=0.8)
    )
    game_state.add_component(entity_id, Vision(vision_range=4))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Player(player_id=config.NEUTRAL_PLAYER_ID, is_human=False))
    game_state.add_component(entity_id, Wander(wander_radius=5, move_interval=4.0))
    return entity_id


def create_confetti(game_state: GameState, x: float, y: float) -> int:
    """Creates a new confetti effect.
    Args:
        game_state: The current state of the game.
        x: The x-coordinate where the effect will be created.
        y: The y-coordinate where the effect will be created.
    Returns:
        The entity ID of the newly created effect.
    """
    entity_id = game_state.create_entity()
    if config.DEBUG:
        log.debug(f"Created confetti (ID: {entity_id}) at ({x}, {y})")
    game_state.add_component(entity_id, Position(x, y))
    game_state.add_component(entity_id, Renderable(icon="*"))
    game_state.add_component(entity_id, Confetti(lifetime=0.5))
    return entity_id


def create_rover(
    game_state: GameState, x: float, y: float, player_id: int, is_human: bool = False
) -> int:
    """Creates a new rover unit.
    Args:
        game_state: The current state of the game.
        x: The x-coordinate where the unit will be created.
        y: The y-coordinate where the unit will be created.
        player_id: The ID of the player who owns this unit.
        is_human: True if the player is human-controlled.
    Returns:
        The entity ID of the newly created unit.
    """
    entity_id = game_state.create_entity()
    if config.DEBUG:
        log.debug(
            f"Created rover (ID: {entity_id}) at ({x}, {y}) for player {player_id}"
        )
    game_state.add_component(entity_id, Position(x, y))
    color = config.PLAYER_COLORS.get(player_id, (255, 255, 255))
    game_state.add_component(entity_id, Renderable(icon="R", color=color))
    game_state.add_component(entity_id, Movable(speed=2.5, intelligent=True))
    game_state.add_component(entity_id, Health(hp=60, max_hp=60))
    game_state.add_component(
        entity_id, Attack(attack_damage=15, attack_range=5, attack_speed=1.0)
    )
    game_state.add_component(entity_id, Detection(detection_range=5))
    game_state.add_component(entity_id, Vision(vision_range=5))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Player(player_id=player_id, is_human=is_human))
    game_state.add_component(entity_id, UnitIdentity(name="rover"))
    return entity_id


def create_arachnotron(
    game_state: GameState, x: float, y: float, player_id: int, is_human: bool = False
) -> int:
    """Creates a new arachnotron unit.
    Args:
        game_state: The current state of the game.
        x: The x-coordinate where the unit will be created.
        y: The y-coordinate where the unit will be created.
        player_id: The ID of the player who owns this unit.
        is_human: True if the player is human-controlled.
    Returns:
        The entity ID of the newly created unit.
    """
    entity_id = game_state.create_entity()
    if config.DEBUG:
        log.debug(
            f"Created arachnotron (ID: {entity_id}) at ({x}, {y}) for player {player_id}"
        )
    game_state.add_component(entity_id, Position(x, y))
    color = config.PLAYER_COLORS.get(player_id, (255, 255, 255))
    game_state.add_component(entity_id, Renderable(icon="A", color=color))
    game_state.add_component(
        entity_id, Movable(speed=1.8, can_fly=True, intelligent=True)
    )
    game_state.add_component(entity_id, Health(hp=120, max_hp=120))
    game_state.add_component(
        entity_id, Attack(attack_damage=20, attack_range=6, attack_speed=1.0)
    )
    game_state.add_component(entity_id, Detection(detection_range=6))
    game_state.add_component(entity_id, Vision(vision_range=6))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Player(player_id=player_id, is_human=is_human))
    game_state.add_component(entity_id, UnitIdentity(name="arachnotron"))
    return entity_id


def create_observer(
    game_state: GameState, x: float, y: float, player_id: int, is_human: bool = False
) -> int:
    """Creates a new observer unit.
    Args:
        game_state: The current state of the game.
        x: The x-coordinate where the unit will be created.
        y: The y-coordinate where the unit will be created.
        player_id: The ID of the player who owns this unit.
        is_human: True if the player is human-controlled.
    Returns:
        The entity ID of the newly created unit.
    """
    entity_id = game_state.create_entity()
    if config.DEBUG:
        log.debug(
            f"Created observer (ID: {entity_id}) at ({x}, {y}) for player {player_id}"
        )
    game_state.add_component(entity_id, Position(x, y))
    color = config.PLAYER_COLORS.get(player_id, (255, 255, 255))
    game_state.add_component(entity_id, Renderable(icon="O", color=color))
    game_state.add_component(
        entity_id, Movable(speed=4, can_fly=True, intelligent=True)
    )
    game_state.add_component(entity_id, Health(hp=40, max_hp=40))
    game_state.add_component(entity_id, Detection(detection_range=15))
    game_state.add_component(entity_id, Vision(vision_range=15))
    game_state.add_component(entity_id, Flee(flees_from_enemies=True))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Player(player_id=player_id, is_human=is_human))
    game_state.add_component(entity_id, UnitIdentity(name="observer"))
    return entity_id


def create_immortal(
    game_state: GameState, x: float, y: float, player_id: int, is_human: bool = False
) -> int:
    """Creates a new immortal unit.
    Args:
        game_state: The current state of the game.
        x: The x-coordinate where the unit will be created.
        y: The y-coordinate where the unit will be created.
        player_id: The ID of the player who owns this unit.
        is_human: True if the player is human-controlled.
    Returns:
        The entity ID of the newly created unit.
    """
    entity_id = game_state.create_entity()
    if config.DEBUG:
        log.debug(
            f"Created immortal (ID: {entity_id}) at ({x}, {y}) for player {player_id}"
        )
    game_state.add_component(entity_id, Position(x, y))
    color = config.PLAYER_COLORS.get(player_id, (255, 255, 255))
    game_state.add_component(entity_id, Renderable(icon="I", color=color))
    game_state.add_component(entity_id, Movable(speed=2, intelligent=True))
    game_state.add_component(
        entity_id, Health(hp=150, max_hp=150, health_regen_rate=2.0)
    )
    game_state.add_component(
        entity_id, Attack(attack_damage=25, attack_range=7, attack_speed=1.0)
    )
    game_state.add_component(entity_id, Detection(detection_range=7))
    game_state.add_component(entity_id, Vision(vision_range=7))
    game_state.add_component(entity_id, Flee(flee_health_threshold=0.2))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Player(player_id=player_id, is_human=is_human))
    game_state.add_component(entity_id, UnitIdentity(name="immortal"))
    return entity_id


def create_extractor(
    game_state: GameState, x: float, y: float, player_id: int, is_human: bool = False
) -> int:
    """Creates a new extractor unit.
    Args:
        game_state: The current state of the game.
        x: The x-coordinate where the unit will be created.
        y: The y-coordinate where the unit will be created.
        player_id: The ID of the player who owns this unit.
        is_human: True if the player is human-controlled.
    Returns:
        The entity ID of the newly created unit.
    """
    entity_id = game_state.create_entity()
    if config.DEBUG:
        log.debug(
            f"Created extractor (ID: {entity_id}) at ({x}, {y}) for player {player_id}"
        )
    game_state.add_component(entity_id, Position(x, y))
    color = config.PLAYER_COLORS.get(player_id, (255, 255, 255))
    game_state.add_component(entity_id, Renderable(icon="E", color=color))
    game_state.add_component(entity_id, Movable(speed=1.5, intelligent=True))
    game_state.add_component(entity_id, Health(hp=50, max_hp=50))
    game_state.add_component(entity_id, Detection(detection_range=5))
    game_state.add_component(entity_id, Vision(vision_range=5))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Player(player_id=player_id, is_human=is_human))
    game_state.add_component(entity_id, UnitIdentity(name="extractor"))
    return entity_id


def create_rover_factory(
    game_state: GameState, x: float, y: float, player_id: int, is_human: bool = False
) -> int:
    """Creates a factory that converts Chassis to Rovers.

    Args:
        game_state: The current state of the game.
        x: The x-coordinate where the unit will be created.
        y: The y-coordinate where the unit will be created.
        player_id: The ID of the player who owns this unit.
        is_human: True if the player is human-controlled.
    Returns:
        The entity ID of the newly created unit.
    """
    entity_id = game_state.create_entity()
    if config.DEBUG:
        log.debug(
            f"Created rover_factory (ID: {entity_id}) at ({x}, {y}) for player {player_id}"
        )
    game_state.add_component(entity_id, Position(x, y))
    color = config.PLAYER_COLORS.get(player_id, (255, 255, 255))
    game_state.add_component(entity_id, Renderable(icon="F", color=color))
    game_state.add_component(entity_id, Health(hp=200, max_hp=200))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Player(player_id=player_id, is_human=is_human))
    game_state.add_component(entity_id, Factory(input_unit="chassis", output_unit="rover"))
    game_state.add_component(entity_id, UnitIdentity(name="rover_factory"))
    return entity_id


def create_arachnotron_factory(
    game_state: GameState, x: float, y: float, player_id: int, is_human: bool = False
) -> int:
    """Creates a factory that converts Rovers to Arachnotrons.

    Args:
        game_state: The current state of the game.
        x: The x-coordinate where the unit will be created.
        y: The y-coordinate where the unit will be created.
        player_id: The ID of the player who owns this unit.
        is_human: True if the player is human-controlled.
    Returns:
        The entity ID of the newly created unit.
    """
    entity_id = game_state.create_entity()
    if config.DEBUG:
        log.debug(
            f"Created arachnotron_factory (ID: {entity_id}) at ({x}, {y}) for player {player_id}"
        )
    game_state.add_component(entity_id, Position(x, y))
    color = config.PLAYER_COLORS.get(player_id, (255, 255, 255))
    game_state.add_component(entity_id, Renderable(icon="f", color=color))
    game_state.add_component(entity_id, Health(hp=300, max_hp=300))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Player(player_id=player_id, is_human=is_human))
    game_state.add_component(entity_id, Factory(input_unit="rover", output_unit="arachnotron"))
    game_state.add_component(entity_id, UnitIdentity(name="arachnotron_factory"))
    return entity_id


UNIT_NAME_TO_FACTORY = {
    "chassis": create_chassis,
    "rover": create_rover,
    "arachnotron": create_arachnotron,
    "observer": create_observer,
    "immortal": create_immortal,
    "extractor": create_extractor,
}
