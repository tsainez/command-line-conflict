from ..components.player import Player
from ..components.position import Position
from ..components.selectable import Selectable
from ..game_state import GameState
from ..logger import log


class SelectionSystem:
    """Handles entity selection via mouse clicks and drag-to-select."""

    def clear_selection(self, game_state: GameState) -> None:
        """Deselects all entities.

        Args:
            game_state: The current state of the game.
        """
        count = 0
        for entity_id, components in game_state.entities.items():
            selectable = components.get(Selectable)
            if selectable and selectable.is_selected:
                selectable.is_selected = False
                count += 1

        if count > 0:
            log.debug(f"Cleared selection of {count} entities.")

    def update(
        self,
        game_state: GameState,
        grid_start: tuple[int, int] | None,
        grid_end: tuple[int, int],
        shift_pressed: bool = False,
        current_player_id: int = 1,
    ) -> None:
        """Processes a drag-to-select action.

        This method is called when a drag selection event is completed.
        It selects all selectable entities within the rectangular area.
        If shift is pressed, it adds to the selection. Otherwise, it replaces the selection.

        Args:
            game_state: The current state of the game.
            grid_start: The (x, y) grid coordinates where the selection
                        drag started. If None, no action is taken.
            grid_end: The current (x, y) grid coordinates of the mouse.
            shift_pressed: True if the shift key was held during the drag.
            current_player_id: The ID of the player currently controlling the game.
        """
        if not grid_start:
            return

        x1, y1 = grid_start
        x2, y2 = grid_end
        sx, ex = sorted((x1, x2))
        sy, ey = sorted((y1, y2))

        for entity_id, components in game_state.entities.items():
            selectable = components.get(Selectable)
            player = components.get(Player)

            # Check if the unit belongs to the current player
            if not selectable or not player or player.player_id != current_player_id:
                continue

            position = components.get(Position)
            if not position:
                continue

            ux = int(position.x)
            uy = int(position.y)
            if sx <= ux <= ex and sy <= uy <= ey:
                selectable.is_selected = True
            elif not shift_pressed:
                selectable.is_selected = False

        selected_count = 0
        for entity_id, components in game_state.entities.items():
            selectable = components.get(Selectable)
            player = components.get(Player)
            if selectable and selectable.is_selected and player and player.player_id == current_player_id:
                selected_count += 1

        if selected_count > 0:
            log.debug(f"Drag selection complete. Total selected: {selected_count}")
        elif not shift_pressed:
            log.debug("Drag selection cleared all units.")

    def handle_click_selection(
        self,
        game_state: GameState,
        grid_pos: tuple[int, int],
        shift_pressed: bool,
        current_player_id: int = 1,
    ) -> None:
        """Handles entity selection from a single mouse click.

        This method updates the selection based on a click. It can select a
        single unit, add/remove a unit from the selection (with shift), or
        deselect all units if the click is on an empty tile.

        Args:
            game_state: The current state of the game.
            grid_pos: The (x, y) grid coordinates of the mouse click.
            shift_pressed: True if the shift key was held during the click.
            current_player_id: The ID of the player currently controlling the game.
        """
        gx, gy = grid_pos

        clicked_entity_id = -1
        for entity_id, components in game_state.entities.items():
            position = components.get(Position)
            player = components.get(Player)
            if (
                position
                and int(position.x) == gx
                and int(position.y) == gy
                and player
                and player.player_id == current_player_id
            ):
                if components.get(Selectable):
                    clicked_entity_id = entity_id
                    break

        if clicked_entity_id != -1:
            if shift_pressed:
                selectable = game_state.get_component(clicked_entity_id, Selectable)
                if selectable:
                    selectable.is_selected = not selectable.is_selected
                    status = "selected" if selectable.is_selected else "deselected"
                    log.debug(f"Shift-clicked unit {clicked_entity_id}: {status}")
            else:
                for entity_id, components in game_state.entities.items():
                    selectable = components.get(Selectable)
                    # Deselect other units unless they are the one clicked
                    if selectable:
                        selectable.is_selected = entity_id == clicked_entity_id
                log.debug(f"Selected unit {clicked_entity_id}")
        elif not shift_pressed:
            log.debug("Clicked on empty space, clearing selection")
            self.clear_selection(game_state)
