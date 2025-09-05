from ..game_state import GameState
from ..components.selectable import Selectable
from ..components.position import Position
from .. import config


class SelectionSystem:
    """
    This system is responsible for selecting entities.
    """

    def update(
        self, game_state: GameState, selection_start: tuple[int, int] | None, mouse_pos: tuple[int, int]
    ) -> None:
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
