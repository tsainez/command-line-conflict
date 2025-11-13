"""A collection of factory functions for creating game entities."""

from . import config
from .components.attack import Attack
from .components.confetti import Confetti
from .components.detection import Detection
from .components.flee import Flee
from .components.health import Health
from .components.movable import Movable
from .components.player import Player
from .components.position import Position
from .components.renderable import Renderable
from .components.selectable import Selectable
from .components.vision import Vision
from .components.harvester import Harvester
from .components.production import Production
from .components.building import Building
from .components.mineral import Mineral
from .game_state import GameState

# TODO: Integrate logger for debug mode. Currently not used.
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
    game_state.add_component(entity_id, Harvester())
    return entity_id


def create_mineral_patch(game_state: GameState, x: float, y: float) -> int:
    """Creates a new mineral patch.
    Args:
        game_state: The current state of the game.
        x: The x-coordinate where the patch will be created.
        y: The y-coordinate where the patch will be created.
    Returns:
        The entity ID of the newly created patch.
    """
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Position(x, y))
    game_state.add_component(entity_id, Renderable(icon="M", color=(255, 255, 0)))
    game_state.add_component(entity_id, Mineral(amount=1000))
    return entity_id


def create_unit_factory(
    game_state: GameState, x: float, y: float, player_id: int, is_human: bool = False
) -> int:
    """Creates a new unit factory.
    Args:
        game_state: The current state of the game.
        x: The x-coordinate where the building will be created.
        y: The y-coordinate where the building will be created.
        player_id: The ID of the player who owns this building.
        is_human: True if the player is human-controlled.
    Returns:
        The entity ID of the newly created building.
    """
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Position(x, y))
    color = config.PLAYER_COLORS.get(player_id, (255, 255, 255))
    game_state.add_component(entity_id, Renderable(icon="F", color=color))
    game_state.add_component(entity_id, Health(hp=300, max_hp=300))
    game_state.add_component(entity_id, Vision(vision_range=8))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Player(player_id=player_id, is_human=is_human))
    game_state.add_component(entity_id, Building())
    game_state.add_component(entity_id, Production())
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
    game_state.add_component(entity_id, Position(x, y))
    color = config.PLAYER_COLORS.get(player_id, (255, 255, 255))
    game_state.add_component(entity_id, Renderable(icon="E", color=color))
    game_state.add_component(entity_id, Movable(speed=1.5, intelligent=True))
    game_state.add_component(entity_id, Health(hp=50, max_hp=50))
    game_state.add_component(entity_id, Detection(detection_range=5))
    game_state.add_component(entity_id, Vision(vision_range=5))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Player(player_id=player_id, is_human=is_human))
    return entity_id
