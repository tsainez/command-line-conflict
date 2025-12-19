from ..components.floating_text import FloatingText
from ..components.position import Position
from ..game_state import GameState


class FloatingTextSystem:
    """Handles the lifecycle and movement of floating text."""

    def update(self, game_state: GameState, dt: float) -> None:
        """Updates floating text entities.

        Args:
            game_state: The current state of the game.
            dt: The time elapsed since the last frame.
        """
        for entity_id, components in list(game_state.entities.items()):
            text_comp = components.get(FloatingText)
            if not text_comp:
                continue

            # Update lifetime
            text_comp.lifetime -= dt
            if text_comp.lifetime <= 0:
                game_state.remove_entity(entity_id)
                continue

            # Move text up
            position = components.get(Position)
            if position:
                new_y = position.y - (text_comp.speed * dt)
                game_state.update_entity_position(entity_id, position.x, new_y)
