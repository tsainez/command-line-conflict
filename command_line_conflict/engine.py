import os  # TODO: Remove unused import.
from pathlib import Path

import pygame

from . import config
from .logger import log
from .maps import Map
from .music import MusicManager
from .scenes.defeat import DefeatScene
from .scenes.editor import EditorScene
from .scenes.game import GameScene
from .scenes.menu import MenuScene
from .scenes.settings import SettingsScene
from .scenes.victory import VictoryScene
from .steam_integration import SteamIntegration


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
            "editor": EditorScene(game),
            "victory": VictoryScene(game),
            "defeat": DefeatScene(game),
        }
        self.current_scene = self.scenes["menu"]
        log.debug("SceneManager initialized with scenes: %s", list(self.scenes.keys()))

    def switch_to(self, scene_name):
        """Switches the active scene.

        Args:
            scene_name: The name of the scene to switch to.
        """
        log.debug(f"Switching scene to: {scene_name}")
        if scene_name == "game":
            self.scenes["game"] = GameScene(self.game)
        elif scene_name == "editor":
            self.scenes["editor"] = EditorScene(self.game)
        self.current_scene = self.scenes[scene_name]

    def handle_event(self, event):
        """Passes events to the current scene's event handler.

        Args:
            event: The pygame event to handle.
        """
        self.current_scene.handle_event(event)

    def update(self, dt):
        """Updates the current scene.

        Args:
            dt: The time elapsed since the last frame.
        """
        self.current_scene.update(dt)

    def draw(self, screen):
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
        log.debug("Pygame initialized")
        self.screen = pygame.display.set_mode(
            (config.SCREEN["width"], config.SCREEN["height"])
        )
        pygame.display.set_caption("ASCII RTS")
        log.debug(
            f"Screen created with resolution: {config.SCREEN['width']}x{config.SCREEN['height']}"
        )
        self.clock = pygame.time.Clock()
        self.running = True

        # Prefer the bundled DejaVu font for rendering path arrows
        font_dir = Path(__file__).resolve().parent / "fonts"
        bundled = font_dir / "DejaVuSansMono.ttf"
        self.font = None
        if bundled.exists():
            try:
                self.font = pygame.font.Font(str(bundled), 16)
                log.debug(f"Loaded bundled font: {bundled}")
            except Exception as e:
                log.warning(f"Failed to load bundled font: {e}")
                self.font = None
        else:
            log.debug("Bundled font not found.")

        self.music_manager = MusicManager()
        self.steam = SteamIntegration()
        self.steam.unlock_achievement("GAME_START")

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
                log.debug(f"Loaded system font: {font_path}")
            else:
                # Final fallback to generic monospace and ASCII graphics
                self.font = pygame.font.SysFont("monospace", 16)
                log.warning("No suitable font found, using generic monospace.")

        self.scene_manager = SceneManager(self)

    def run(self) -> None:
        """Starts and runs the main game loop."""
        log.info("Game starting...")
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0
            self.steam.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    log.info("Quit event received. Stopping game loop...")
                    self.running = False
                self.scene_manager.handle_event(event)
            self.scene_manager.update(dt)
            self.scene_manager.draw(self.screen)
            pygame.display.flip()
        log.info("Game loop finished. Quitting...")
        pygame.quit()


def main(game_map: Map | None = None) -> None:
    """Initializes and runs the game.

    Args:
        game_map: An optional map object to start the game with.
    """
    Game(game_map).run()


if __name__ == "__main__":
    main()
