from ..components.dead import Dead
from ..components.movable import Movable
from ..components.player import Player
from ..components.position import Position
from ..components.selectable import Selectable
from ..game_state import GameState
from ..logger import log


class ControlGroupSystem:
    """Manages numbered control groups of selected entities (RTS-style hotkeys).

    Conventions mirrored from genre staples like StarCraft:
      - Ctrl+<number> assigns the current selection to a control group,
        replacing whatever was previously bound to that number.
      - <number> alone recalls a group, replacing the current selection.
      - A group may hold any number of units, but at most one building
        (a stationary, non-Movable entity such as a factory). Assigning a
        selection containing several buildings keeps only the first one.
    """

    def __init__(self) -> None:
        # player_id -> {group_number: set(entity_id)}
        self._groups: dict[int, dict[int, set[int]]] = {}

    @staticmethod
    def _is_building(components: dict) -> bool:
        """Stationary (non-Movable) entities are treated as buildings."""
        return Movable not in components

    def assign_group(self, game_state: GameState, group_number: int, player_id: int) -> set[int]:
        """Binds the current selection (owned by player_id) to a control group.

        Returns:
            The set of entity IDs actually assigned to the group (empty if
            nothing was selected).
        """
        selected = []
        for entity_id in game_state.get_entities_with_component(Selectable):
            components = game_state.entities.get(entity_id)
            if not components:
                continue

            selectable = components.get(Selectable)
            player = components.get(Player)
            if selectable and selectable.is_selected and player and player.player_id == player_id:
                selected.append((entity_id, components))

        group: set[int] = set()
        building_assigned = False
        skipped_buildings = 0
        for entity_id, components in selected:
            if self._is_building(components):
                if building_assigned:
                    skipped_buildings += 1
                    continue
                building_assigned = True
            group.add(entity_id)

        if not group:
            return group

        self._groups.setdefault(player_id, {})[group_number] = group
        log.debug(f"Player {player_id} assigned {len(group)} entities to control group {group_number}")
        if skipped_buildings:
            log.debug(f"Control group {group_number}: only one building allowed, skipped {skipped_buildings}")

        return group

    def get_group_entities(self, game_state: GameState, group_number: int, player_id: int) -> list[int]:
        """Returns the still-alive entity IDs bound to a group, pruning any that are gone."""
        player_groups = self._groups.get(player_id)
        if not player_groups or group_number not in player_groups:
            return []

        bound_ids = player_groups[group_number]
        alive_ids = []
        stale_ids = []
        for entity_id in bound_ids:
            components = game_state.entities.get(entity_id)
            if not components or components.get(Dead) or not components.get(Selectable):
                stale_ids.append(entity_id)
                continue
            alive_ids.append(entity_id)

        if stale_ids:
            bound_ids.difference_update(stale_ids)

        return alive_ids

    def select_group(self, game_state: GameState, group_number: int, player_id: int) -> list[int]:
        """Selects every entity bound to a group, replacing the current selection.

        Returns:
            The entity IDs newly selected (empty if the group has no members).
        """
        entity_ids = self.get_group_entities(game_state, group_number, player_id)
        if not entity_ids:
            return entity_ids

        target_ids = set(entity_ids)
        for entity_id in game_state.get_entities_with_component(Selectable):
            components = game_state.entities.get(entity_id)
            if not components:
                continue

            player = components.get(Player)
            if not player or player.player_id != player_id:
                continue

            selectable = components.get(Selectable)
            if selectable:
                selectable.is_selected = entity_id in target_ids

        log.debug(f"Player {player_id} selected control group {group_number} ({len(entity_ids)} entities)")
        return entity_ids

    @staticmethod
    def get_center_position(game_state: GameState, entity_ids: list[int]) -> "tuple[float, float] | None":
        """Returns the centroid (x, y) of the given entities' positions, or None if none have one."""
        total_x = 0.0
        total_y = 0.0
        count = 0
        for entity_id in entity_ids:
            position = game_state.get_component(entity_id, Position)
            if position:
                total_x += position.x
                total_y += position.y
                count += 1

        if count == 0:
            return None

        return total_x / count, total_y / count
