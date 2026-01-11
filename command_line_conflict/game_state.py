from typing import Any, Optional

from . import config
from .components.position import Position
from .logger import log
from .maps.base import Map


class GameState:
    """Manages all game state, including entities, components, and the map."""

    def __init__(self, game_map: Map) -> None:
        """Initializes the GameState.

        Args:
            game_map: The game map object.
        """
        if config.DEBUG:
            log.debug("GameState initialized")

        self.map = game_map
        self.entities: dict[int, dict] = {}
        self.next_entity_id = 0
        self.event_queue: list[dict[str, Any]] = []
        # Spatial hashing for O(1) lookups
        self.spatial_map: dict[tuple[int, int], set[int]] = {}
        # Component index for O(1) entity lookup by component type
        self.component_index: dict[type, set[int]] = {}

    def _add_to_spatial_map(self, entity_id: int, x: int, y: int) -> None:
        pos = (x, y)
        if pos not in self.spatial_map:
            self.spatial_map[pos] = set()
        self.spatial_map[pos].add(entity_id)

    def _remove_from_spatial_map(self, entity_id: int, x: int, y: int) -> None:
        pos = (x, y)
        if pos in self.spatial_map:
            self.spatial_map[pos].discard(entity_id)
            if not self.spatial_map[pos]:
                del self.spatial_map[pos]

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

        # Update component index
        if component_type not in self.component_index:
            self.component_index[component_type] = set()
        self.component_index[component_type].add(entity_id)

        if isinstance(component, Position):
            self._add_to_spatial_map(entity_id, int(component.x), int(component.y))
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

    def get_entities_with_component(self, component_type) -> set[int]:
        """Returns a set of entity IDs that have the specified component type.

        Args:
            component_type: The type of component to look for.

        Returns:
            A set of entity IDs.
        """
        return self.component_index.get(component_type, set())

    def remove_component(self, entity_id: int, component_type) -> None:
        """Removes a component from an entity.

        Args:
            entity_id: The ID of the entity.
            component_type: The type of the component to remove.
        """
        if component_type in self.entities[entity_id]:
            component = self.entities[entity_id][component_type]

            # Update component index
            if component_type in self.component_index:
                self.component_index[component_type].discard(entity_id)

            if isinstance(component, Position):
                self._remove_from_spatial_map(entity_id, int(component.x), int(component.y))
            del self.entities[entity_id][component_type]
            if config.DEBUG:
                log.debug(f"Removed component {component_type.__name__} from entity {entity_id}")

    def remove_entity(self, entity_id: int) -> None:
        """Removes an entity and all its components from the game.

        Args:
            entity_id: The ID of the entity to remove.
        """
        if entity_id in self.entities:
            # Update component index
            for component_type in self.entities[entity_id]:
                if component_type in self.component_index:
                    self.component_index[component_type].discard(entity_id)

            position = self.entities[entity_id].get(Position)
            if position:
                self._remove_from_spatial_map(entity_id, int(position.x), int(position.y))
            del self.entities[entity_id]
            if config.DEBUG:
                log.debug(f"Removed entity {entity_id}")

    def update_entity_position(self, entity_id: int, x: float, y: float) -> None:
        """Updates the position of an entity and the spatial map.

        Args:
            entity_id: The ID of the entity to move.
            x: The new x-coordinate.
            y: The new y-coordinate.
        """
        position = self.get_component(entity_id, Position)
        if position:
            old_ix, old_iy = int(position.x), int(position.y)
            new_ix, new_iy = int(x), int(y)

            if old_ix != new_ix or old_iy != new_iy:
                self._remove_from_spatial_map(entity_id, old_ix, old_iy)
                self._add_to_spatial_map(entity_id, new_ix, new_iy)

            position.x = x
            position.y = y

    def get_entities_at_position(self, x: int, y: int) -> list[int]:
        """Returns a list of entity IDs at a given position.

        Optimized with spatial hashing O(1).
        """
        return list(self.spatial_map.get((x, y), []))

    def is_position_occupied(self, x: int, y: int, exclude_entity_id: Optional[int] = None) -> bool:
        """Checks if a position is occupied by any entity.

        This method is optimized to avoid creating a list of entities.
        It checks the spatial map directly.

        Args:
            x: The x-coordinate.
            y: The y-coordinate.
            exclude_entity_id: An optional entity ID to exclude from the check
                (e.g., the entity moving).

        Returns:
            True if the position is occupied, False otherwise.
        """
        entities = self.spatial_map.get((x, y))
        if not entities:
            return False

        if exclude_entity_id is None:
            return True

        # If there are entities and we need to exclude one, we check if
        # there are any *other* entities.
        if len(entities) > 1:
            return True

        # If there is exactly one entity, check if it is the excluded one
        return exclude_entity_id not in entities
