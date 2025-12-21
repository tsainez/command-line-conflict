from command_line_conflict import factories
from command_line_conflict.campaign_manager import CampaignManager
from command_line_conflict.components.factory import Factory
from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
from command_line_conflict.components.unit_identity import UnitIdentity
from command_line_conflict.logger import log


class ProductionSystem:
    """System that handles unit production via factories."""

    def __init__(self, campaign_manager: CampaignManager):
        self.campaign_manager = campaign_manager

    def update(self, game_state, dt):
        """Checks for units entering factories and handles transformation.

        Args:
            game_state: The current state of the game.
            dt: Delta time (unused for this check, but required by interface).
        """
        # Find all entities with Factory component
        factory_entities = []
        for entity_id, components in game_state.entities.items():
            if Factory in components and Position in components:
                factory_entities.append((entity_id, components))

        if not factory_entities:
            return

        # Check for overlap with input units
        # Iterate over a copy of entities to avoid modification issues if we delete
        # entities while iterating (though create_entity creates a new ID, best be safe)
        all_entities = list(game_state.entities.items())

        for unit_id, unit_components in all_entities:
            unit_pos = unit_components.get(Position)
            unit_identity = unit_components.get(UnitIdentity)
            unit_player = unit_components.get(Player)

            if not unit_pos or not unit_identity:
                continue

            for factory_id, factory_components in factory_entities:
                # Don't let a factory consume itself (though it shouldn't match input_unit usually)
                if unit_id == factory_id:
                    continue

                factory = factory_components[Factory]
                factory_pos = factory_components[Position]
                factory_player = factory_components.get(Player)

                # Check player ownership compatibility (can only use own factories)
                if unit_player and factory_player and unit_player.player_id != factory_player.player_id:
                    continue

                # Check Position Overlap
                # Using simple integer grid comparison as movement snaps to grid or close enough
                if int(unit_pos.x) == int(factory_pos.x) and int(unit_pos.y) == int(factory_pos.y):

                    # Check Input Type Match
                    if unit_identity.name == factory.input_unit:

                        # Check Campaign Unlock
                        if self.campaign_manager.is_unit_unlocked(factory.output_unit):
                            self._transform_unit(game_state, unit_id, unit_player, factory, factory_pos)
                            break  # Consumed unit, stop checking factories for this unit
                        # Optional: Feedback that tech is not unlocked

    def _transform_unit(
        self, game_state, input_unit_id, input_player, factory, position
    ):  # pylint: disable=too-many-arguments
        """Performs the transformation from input unit to output unit."""
        log.info(f"Transforming unit {input_unit_id} ({factory.input_unit}) into {factory.output_unit}")

        # Remove input unit
        game_state.remove_entity(input_unit_id)

        # Create output unit
        factory_func = factories.UNIT_NAME_TO_FACTORY.get(factory.output_unit)
        if not factory_func:
            log.error(f"No factory function found for unit type: {factory.output_unit}")
            return

        # Preserve player ownership and human status
        player_id = input_player.player_id if input_player else 1
        is_human = input_player.is_human if input_player else True

        factory_func(
            game_state,
            position.x,
            position.y,
            player_id=player_id,
            is_human=is_human,
        )
