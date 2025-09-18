from .. import config
from ..components.player import Player
from ..components.position import Position
from ..components.selectable import Selectable
from ..game_state import GameState

# TODO: Integrate logger for debug mode. Currently not used.


class SelectionSystem:
    """Handles entity selection via mouse clicks and drag-to-select."""

    def update(
        self,
        game_state: GameState,
        grid_start: tuple[int, int] | None,
        grid_end: tuple[int, int],
    ) -> None:
        """Processes a drag-to-select action.

        This method is called when a selection box is being drawn. It selects
        all selectable entities within the rectangular area defined by the
        selection start and current mouse position.

        Args:
            game_state: The current state of the game.
            grid_start: The (x, y) grid coordinates where the selection
                        drag started. If None, no action is taken.
            grid_end: The current (x, y) grid coordinates of the mouse.
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
            if not selectable or not player or not player.is_human:
                continue

            position = components.get(Position)
            if not position:
                continue

            ux = int(position.x)
            uy = int(position.y)
            if sx <= ux <= ex and sy <= uy <= ey:
                selectable.is_selected = True
            else:
                selectable.is_selected = False

    def handle_click_selection(
        self, game_state: GameState, grid_pos: tuple[int, int], shift_pressed: bool
    ) -> None:
        """Handles entity selection from a single mouse click.

        This method updates the selection based on a click. It can select a
        single unit, add/remove a unit from the selection (with shift), or
        deselect all units if the click is on an empty tile.

        Args:
            game_state: The current state of the game.
            grid_pos: The (x, y) grid coordinates of the mouse click.
            shift_pressed: True if the shift key was held during the click.
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
                and player.is_human
            ):
                if components.get(Selectable):
                    clicked_entity_id = entity_id
                    break

        if clicked_entity_id != -1:
            if shift_pressed:
                selectable = game_state.get_component(clicked_entity_id, Selectable)
                if selectable:
                    selectable.is_selected = not selectable.is_selected
            else:
                for entity_id, components in game_state.entities.items():
                    selectable = components.get(Selectable)
                    if selectable:
                        selectable.is_selected = entity_id == clicked_entity_id
        elif not shift_pressed:
            for entity_id, components in game_state.entities.items():
                selectable = components.get(Selectable)
                if selectable:
                    selectable.is_selected = False
