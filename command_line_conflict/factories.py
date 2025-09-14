"""A collection of factory functions for creating game entities."""
from .game_state import GameState
from .components.position import Position
from .components.renderable import Renderable
from .components.movable import Movable
from .components.health import Health
from .components.attack import Attack
from .components.vision import Vision
from .components.flee import Flee
from .components.selectable import Selectable
from .components.owner import Owner
from .components.factory import Factory
from .components.production import Production
from .components.harvester import Harvester


def create_factory(game_state: GameState, x: float, y: float, player_id: int) -> int:
    """Creates a new factory unit."""
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Position(x, y))
    game_state.add_component(entity_id, Renderable(icon="F"))
    game_state.add_component(entity_id, Health(hp=200, max_hp=200))
    game_state.add_component(entity_id, Vision(vision_range=5))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Factory())
    game_state.add_component(entity_id, Production(production_list=["Chassis", "Rover"]))
    game_state.add_component(entity_id, Owner(player_id))
    return entity_id


def create_chassis(game_state: GameState, x: float, y: float, player_id: int) -> int:
    """Creates a new chassis unit.

    Args:
        game_state: The current state of the game.
        x: The x-coordinate where the unit will be created.
        y: The y-coordinate where the unit will be created.

    Returns:
        The entity ID of the newly created unit.
    """
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Position(x, y))
    game_state.add_component(entity_id, Renderable(icon="C"))
    game_state.add_component(entity_id, Movable(speed=2))
    game_state.add_component(entity_id, Health(hp=80, max_hp=80))
    game_state.add_component(
        entity_id, Attack(attack_damage=10, attack_range=1, attack_speed=1.0)
    )
    game_state.add_component(entity_id, Vision(vision_range=5))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Owner(player_id))
    return entity_id


def create_rover(game_state: GameState, x: float, y: float, player_id: int) -> int:
    """Creates a new rover unit."""
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Position(x, y))
    game_state.add_component(entity_id, Renderable(icon="R"))
    game_state.add_component(entity_id, Movable(speed=2.5))
    game_state.add_component(entity_id, Health(hp=60, max_hp=60))
    game_state.add_component(
        entity_id, Attack(attack_damage=15, attack_range=5, attack_speed=1.0)
    )
    game_state.add_component(entity_id, Vision(vision_range=5))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Owner(player_id))
    return entity_id


def create_arachnotron(game_state: GameState, x: float, y: float, player_id: int) -> int:
    """Creates a new arachnotron unit."""
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Position(x, y))
    game_state.add_component(entity_id, Renderable(icon="A"))
    game_state.add_component(entity_id, Movable(speed=1.8, can_fly=True))
    game_state.add_component(entity_id, Health(hp=120, max_hp=120))
    game_state.add_component(
        entity_id, Attack(attack_damage=20, attack_range=6, attack_speed=1.0)
    )
    game_state.add_component(entity_id, Vision(vision_range=6))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Owner(player_id))
    return entity_id


def create_observer(game_state: GameState, x: float, y: float, player_id: int) -> int:
    """Creates a new observer unit."""
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Position(x, y))
    game_state.add_component(entity_id, Renderable(icon="O"))
    game_state.add_component(entity_id, Movable(speed=4, can_fly=True))
    game_state.add_component(entity_id, Health(hp=40, max_hp=40))
    game_state.add_component(entity_id, Vision(vision_range=15))
    game_state.add_component(entity_id, Flee(flees_from_enemies=True))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Owner(player_id))
    return entity_id


def create_immortal(game_state: GameState, x: float, y: float, player_id: int) -> int:
    """Creates a new immortal unit."""
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Position(x, y))
    game_state.add_component(entity_id, Renderable(icon="I"))
    game_state.add_component(entity_id, Movable(speed=2))
    game_state.add_component(
        entity_id, Health(hp=150, max_hp=150, health_regen_rate=2.0)
    )
    game_state.add_component(
        entity_id, Attack(attack_damage=25, attack_range=7, attack_speed=1.0)
    )
    game_state.add_component(entity_id, Vision(vision_range=7))
    game_state.add_component(entity_id, Flee(flee_health_threshold=0.2))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Owner(player_id))
    return entity_id


def create_extractor(game_state: GameState, x: float, y: float, player_id: int) -> int:
    """Creates a new extractor unit."""
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Position(x, y))
    game_state.add_component(entity_id, Renderable(icon="E"))
    game_state.add_component(entity_id, Movable(speed=1.5))
    game_state.add_component(entity_id, Health(hp=50, max_hp=50))
    game_state.add_component(entity_id, Vision(vision_range=5))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Harvester())
    game_state.add_component(entity_id, Owner(player_id))
    return entity_id
