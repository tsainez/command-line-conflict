from .components.position import Position
from .logger import log
from .maps.base import Map
from . import config


class GameState:
    """Manages all game state, including entities, components, and the map."""

    def __init__(self, game_map: Map) -> None:
        """Initializes the GameState.

        Args:
            game_map: The game map object.
        """
        self.map = game_map
        self.entities: dict[int, dict] = {}
        self.next_entity_id = 0
        self.event_queue = []
        if config.DEBUG:
            log.debug("GameState initialized")

    def add_event(self, event: dict) -> None:
        """Adds an event to the event queue.

        Args:
            event: A dictionary representing the event.
        """
        self.event_queue.append(event)
        if config.DEBUG:
            log.debug(f"Event added: {event}")

    def create_entity(self) -> int:
        """Creates a new entity and returns its ID."""
        entity_id = self.next_entity_id
        self.entities[entity_id] = {}
        self.next_entity_id += 1
        if config.DEBUG:
            log.debug(f"Created entity: {entity_id}")
        return entity_id

    def add_component(self, entity_id: int, component) -> None:
        """Adds a component to an entity.

        Args:
            entity_id: The ID of the entity.
            component: The component instance to add.
        """
        component_type = type(component)
        self.entities[entity_id][component_type] = component
        if config.DEBUG:
            log.debug(f"Added component {component_type.__name__} to entity {entity_id}")

    def get_component(self, entity_id: int, component_type):
        """Gets a component from an entity.

        Args:
            entity_id: The ID of the entity.
            component_type: The type of the component to get.

        Returns:
            The component instance, or None if the entity does not have the
            component.
        """
        return self.entities[entity_id].get(component_type)

    def remove_component(self, entity_id: int, component_type) -> None:
        """Removes a component from an entity.

        Args:
            entity_id: The ID of the entity.
            component_type: The type of the component to remove.
        """
        if component_type in self.entities[entity_id]:
            del self.entities[entity_id][component_type]
            if config.DEBUG:
                log.debug(f"Removed component {component_type.__name__} from entity {entity_id}")

    def remove_entity(self, entity_id: int) -> None:
        """Removes an entity and all its components from the game.

        Args:
            entity_id: The ID of the entity to remove.
        """
        if entity_id in self.entities:
            del self.entities[entity_id]
            if config.DEBUG:
                log.debug(f"Removed entity {entity_id}")

    def get_entities_at_position(self, x: int, y: int) -> list[int]:
        """Returns a list of entity IDs at a given position."""
        entities_at_pos = []
        for entity_id, components in self.entities.items():
            position = components.get(Position)
            if position and int(position.x) == x and int(position.y) == y:
                entities_at_pos.append(entity_id)
        return entities_at_pos
