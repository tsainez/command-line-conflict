import pygame

from ..components.environmental import Environmental
from ..components.player import Player
from ..components.position import Position
from ..components.vision import Vision
from ..components.light import Light


class FogOfWarSystem:
    """A system that manages the fog of war."""

    def __init__(self, screen, camera):
        """Initializes the FogOfWarSystem.
        Args:
            screen: The pygame screen surface to draw on.
            camera: The camera object for view/zoom.
        """
        self.screen = screen
        self.camera = camera
        self.visible_tiles = set()

    def update(self, game_state):
        """Updates the set of visible tiles.
        Args:
            game_state: The current state of the game.
        """
        self.visible_tiles.clear()
        environmental = None
        for entity_id, components in game_state.entities.items():
            if Environmental in components:
                environmental = components.get(Environmental)
                break

        if not environmental or not environmental.fog_of_war:
            return

        for entity_id, components in game_state.entities.items():
            player = components.get(Player)
            if player and player.player_id == 1:
                position = components.get(Position)
                vision = components.get(Vision)
                light = components.get(Light)

                if position and vision:
                    radius = vision.vision_range
                    if not environmental.is_day and light:
                        radius += light.radius

                    for x in range(int(position.x) - radius, int(position.x) + radius + 1):
                        for y in range(int(position.y) - radius, int(position.y) + radius + 1):
                            if (x - position.x) ** 2 + (y - position.y) ** 2 <= radius ** 2:
                                self.visible_tiles.add((x, y))

    def draw(self, game_state):
        """Draws the fog of war.
        Args:
            game_state: The current state of the game.
        """
        environmental = None
        for entity_id, components in game_state.entities.items():
            if Environmental in components:
                environmental = components.get(Environmental)
                break

        if not environmental or not environmental.fog_of_war:
            return

        for x in range(game_state.map.width):
            for y in range(game_state.map.height):
                if (x, y) not in self.visible_tiles:
                    cam_x = (x - self.camera.x) * self.camera.zoom * 16
                    cam_y = (y - self.camera.y) * self.camera.zoom * 16
                    surface = pygame.Surface((16 * self.camera.zoom, 16 * self.camera.zoom), pygame.SRCALPHA)
                    pygame.draw.rect(surface, (0, 0, 0, 200), surface.get_rect())
                    self.screen.blit(surface, (cam_x, cam_y))
