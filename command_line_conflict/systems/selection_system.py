from ..game_state import GameState
from ..components.selectable import Selectable
from ..components.position import Position
from .. import config


class SelectionSystem:
    """Handles entity selection via mouse clicks and drag-to-select."""

    def update(
        self,
        game_state: GameState,
        selection_start: tuple[int, int] | None,
        mouse_pos: tuple[int, int],
    ) -> None:
        """Processes a drag-to-select action.

        This method is called when a selection box is being drawn. It selects
        all selectable entities within the rectangular area defined by the
        selection start and current mouse position.

        Args:
            game_state: The current state of the game.
            selection_start: The (x, y) pixel coordinates where the selection
                             drag started. If None, no action is taken.
            mouse_pos: The current (x, y) pixel coordinates of the mouse.
        """
        if not selection_start:
            return

        x1, y1 = selection_start
        x2, y2 = mouse_pos
        sx, ex = sorted((x1 // config.GRID_SIZE, x2 // config.GRID_SIZE))
        sy, ey = sorted((y1 // config.GRID_SIZE, y2 // config.GRID_SIZE))

        for entity_id, components in game_state.entities.items():
            selectable = components.get(Selectable)
            if not selectable:
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
        self, game_state: GameState, mouse_pos: tuple[int, int], shift_pressed: bool
    ) -> None:
        """Handles entity selection from a single mouse click.

        This method updates the selection based on a click. It can select a
        single unit, add/remove a unit from the selection (with shift), or
        deselect all units if the click is on an empty tile.

        Args:
            game_state: The current state of the game.
            mouse_pos: The (x, y) pixel coordinates of the mouse click.
            shift_pressed: True if the shift key was held during the click.
        """
        gx = mouse_pos[0] // config.GRID_SIZE
        gy = mouse_pos[1] // config.GRID_SIZE

        clicked_entity_id = -1
        for entity_id, components in game_state.entities.items():
            position = components.get(Position)
            if position and int(position.x) == gx and int(position.y) == gy:
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
