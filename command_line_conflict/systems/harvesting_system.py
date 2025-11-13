from ..components.harvester import Harvester
from ..components.mineral import Mineral
from ..components.position import Position
from ..components.building import Building
from ..components.player import Player

class HarvestingSystem:
    """A system that handles the logic of harvesting minerals."""

    def update(self, game_state):
        """Updates the harvesting state of all harvesters.
        Args:
            game_state: The current state of the game.
        """
        for entity_id, components in game_state.entities.items():
            harvester = components.get(Harvester)
            if harvester:
                position = components.get(Position)
                player = components.get(Player)

                # If the harvester is full, find the nearest friendly building to return to
                if harvester.carrying >= harvester.capacity:
                    nearest_building = self._find_nearest_building(game_state, position, player.player_id)
                    if nearest_building:
                        game_state.get_component(entity_id, "Movable").target_x = nearest_building.x
                        game_state.get_component(entity_id, "Movable").target_y = nearest_building.y

                # If the harvester is at a mineral patch, harvest it
                entities_at_position = game_state.get_entities_at_position(int(position.x), int(position.y))
                for other_entity_id in entities_at_position:
                    mineral = game_state.get_component(other_entity_id, Mineral)
                    if mineral:
                        amount_to_harvest = min(harvester.capacity - harvester.carrying, mineral.amount)
                        harvester.carrying += amount_to_harvest
                        mineral.amount -= amount_to_harvest
                        if mineral.amount <= 0:
                            game_state.remove_entity(other_entity_id)

                # If the harvester is at a friendly building, drop off the minerals
                if harvester.carrying > 0:
                    entities_at_position = game_state.get_entities_at_position(int(position.x), int(position.y))
                    for other_entity_id in entities_at_position:
                        building = game_state.get_component(other_entity_id, Building)
                        building_player = game_state.get_component(other_entity_id, Player)
                        if building and building_player.player_id == player.player_id:
                            # For now, just destroy the minerals. We'll add them to the player's resources later.
                            harvester.carrying = 0

    def _find_nearest_building(self, game_state, position, player_id):
        """Finds the nearest friendly building to a given position."""
        nearest_building = None
        min_dist = float("inf")
        for entity_id, components in game_state.entities.items():
            building = components.get(Building)
            building_player = components.get(Player)
            if building and building_player.player_id == player_id:
                building_position = components.get(Position)
                dist = (position.x - building_position.x) ** 2 + (position.y - building_position.y) ** 2
                if dist < min_dist:
                    min_dist = dist
                    nearest_building = building_position
        return nearest_building
