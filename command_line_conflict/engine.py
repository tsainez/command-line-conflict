import os
from pathlib import Path

import pygame

from . import config
from .logger import log
from .maps import Map
from .scenes.menu import MenuScene
from .scenes.settings import SettingsScene
from .scenes.game import GameScene


class SceneManager:
    def __init__(self, game):
        self.game = game
        self.scenes = {
            "menu": MenuScene(game),
            "settings": SettingsScene(game),
            "game": GameScene(game),
        }
        self.current_scene = self.scenes["menu"]

    def switch_to(self, scene_name):
        if scene_name == "game":
            self.scenes["game"] = GameScene(self.game)
        self.current_scene = self.scenes[scene_name]

    def handle_event(self, event):
        self.current_scene.handle_event(event)

    def update(self, dt):
        self.current_scene.update(dt)

    def draw(self, screen):
        self.current_scene.draw(screen)


class Game:
    """Main game engine."""

    def __init__(self, game_map: Map | None = None) -> None:
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
    """Helper to launch the game with a given map."""
    Game(game_map).run()


if __name__ == "__main__":
    main()
