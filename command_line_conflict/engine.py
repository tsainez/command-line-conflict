import os
from pathlib import Path

import pygame

from . import config
from .logger import (  # TODO: Expand logger usage, specifically for when in debug mode.
    log,
)
from .maps import Map
from .music import MusicManager
from .scenes.game import GameScene
from .scenes.menu import MenuScene
from .scenes.settings import SettingsScene


class SceneManager:
    """Manages the different scenes (e.g., menu, game, settings) in the game."""

    def __init__(self, game):
        """Initializes the SceneManager.

        Args:
            game: The main game object.
        """
        self.game = game
        self.scenes = {
            "menu": MenuScene(game),
            "settings": SettingsScene(game),
            "game": GameScene(game),
        }
        self.current_scene = self.scenes["menu"]

    def switch_to(self, scene_name: str) -> None:
        """Switches the active scene.

        Args:
            scene_name: The name of the scene to switch to (e.g., "game", "menu").
        """
        if scene_name == "game":
            self.scenes["game"] = GameScene(self.game)
        self.current_scene = self.scenes[scene_name]

    def handle_event(self, event: pygame.event.Event) -> None:
        """Passes events to the current scene's event handler.

        Args:
            event: The pygame event to handle.
        """
        self.current_scene.handle_event(event)

    def update(self, dt: float) -> None:
        """Updates the current scene.

        Args:
            dt: The time elapsed since the last frame in seconds.
        """
        self.current_scene.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the current scene to the screen.

        Args:
            screen: The pygame screen surface to draw on.
        """
        self.current_scene.draw(screen)


class Game:
    """The main game engine, responsible for the game loop and managing scenes."""

    def __init__(self, game_map: Map | None = None) -> None:
        """Initializes the game engine.

        This sets up pygame, the screen, the clock, and the scene manager.
        It also handles font loading.

        Args:
            game_map: An optional map object to start the game with.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(
            (config.SCREEN["width"], config.SCREEN["height"])
        )
        pygame.display.set_caption("ASCII RTS")
        self.clock = pygame.time.Clock()
        self.running = True

        # Prefer the bundled DejaVu font for rendering path arrows
        font_dir = Path(__file__).resolve().parent / "fonts"
        bundled = font_dir / "DejaVuSansMono.ttf"
        self.font = None
        if bundled.exists():
            try:
                self.font = pygame.font.Font(str(bundled), 16)
            except Exception:
                self.font = None

        self.music_manager = MusicManager()

        if self.font is None:
            # Try common system fonts
            candidates = [
                "dejavusansmono",
                "couriernew",
                "menlo",
                "consolas",
            ]
            font_path = None
            for name in candidates:
                font_path = pygame.font.match_font(name)
                if font_path:
                    break

            if font_path:
                self.font = pygame.font.Font(font_path, 16)
            else:
                # Final fallback to generic monospace and ASCII graphics
                self.font = pygame.font.SysFont("monospace", 16)

        self.scene_manager = SceneManager(self)

    def run(self) -> None:
        """Starts and runs the main game loop."""
        log.info("Game starting...")
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.scene_manager.handle_event(event)
            self.scene_manager.update(dt)
            self.scene_manager.draw(self.screen)
            pygame.display.flip()
        pygame.quit()


def main(game_map: Map | None = None) -> None:
    """Initializes and runs the game.

    Args:
        game_map: An optional map object to start the game with.
    """
    Game(game_map).run()


if __name__ == "__main__":
    main()
