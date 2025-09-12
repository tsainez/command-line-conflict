from .maps.base import Map


class GameState:
    """
    A container for all the state of the game.
    """

    def __init__(self, game_map: Map) -> None:
        self.map = game_map
        self.entities: dict[int, dict] = {}
        self.next_entity_id = 0

    def create_entity(self) -> int:
        entity_id = self.next_entity_id
        self.entities[entity_id] = {}
        self.next_entity_id += 1
        return entity_id

    def add_component(self, entity_id: int, component) -> None:
        component_type = type(component)
        self.entities[entity_id][component_type] = component

    def get_component(self, entity_id: int, component_type):
        return self.entities[entity_id].get(component_type)

    def remove_component(self, entity_id: int, component_type) -> None:
        if component_type in self.entities[entity_id]:
            del self.entities[entity_id][component_type]

    def remove_entity(self, entity_id: int) -> None:
        if entity_id in self.entities:
            del self.entities[entity_id]
