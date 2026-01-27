import math
import os

import pygame

from command_line_conflict import config
from command_line_conflict.camera import Camera
from command_line_conflict.logger import log
from command_line_conflict.maps.base import Map
from command_line_conflict.ui.file_dialog import FileDialog


class EditorScene:
    """Manages the map editor scene."""

    def __init__(self, game):
        """Initializes the EditorScene.

        Args:
            game: The main game object.
        """
        self.game = game
        self.font = game.font

        # Load custom map if exists, else create new
        self.map_path = os.path.join("command_line_conflict", "maps", "custom", "custom_map.json")
        try:
            self.map = Map.load_from_file(self.map_path)
            log.info(f"Loaded map from {self.map_path}")
        except FileNotFoundError:
            self.map = Map(width=40, height=30)
            log.info("Created new blank map")
        except (IOError, ValueError) as e:
            log.error(f"Error loading map: {e}")
            self.map = Map(width=40, height=30)

        self.camera = Camera()
        self.camera_movement = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }

        self.mode = "WALL"  # WALL, ERASE

        # UI Font - try to use game font if possible, or default
        self.ui_font = pygame.font.SysFont("arial", 24)
        self.tooltip_font = pygame.font.SysFont("arial", 16)

        self.file_dialog = None
        self.mouse_pos = (0, 0)
        self.hover_grid_pos = None

        self.buttons = [
            {
                "text": "Save",
                "rect": pygame.Rect(10, 10, 80, 40),
                "action": self.open_save_dialog,
                "tooltip": "Save Map (S)",
            },
            {
                "text": "Load",
                "rect": pygame.Rect(100, 10, 80, 40),
                "action": self.open_load_dialog,
                "tooltip": "Load Map (L)",
            },
            {
                "text": "Menu",
                "rect": pygame.Rect(190, 10, 80, 40),
                "action": self._return_to_menu,
                "tooltip": "Return to Menu (ESC)",
            },
        ]

    def handle_event(self, event):
        """Handles user input."""
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            # Simple UI area check (top 60 pixels)
            if event.pos[1] < 60:
                # Check for button hover
                hovering_button = False
                for btn in self.buttons:
                    if btn["rect"].collidepoint(event.pos):
                        hovering_button = True
                        break

                if hovering_button:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.hover_grid_pos = None
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
                gx, gy = self.camera.screen_to_grid(event.pos[0], event.pos[1])
                if 0 <= gx < self.map.width and 0 <= gy < self.map.height:
                    self.hover_grid_pos = (gx, gy)
                else:
                    self.hover_grid_pos = None

        if self.file_dialog and self.file_dialog.active:
            result = self.file_dialog.handle_event(event)
            if result:
                if self.file_dialog.mode == "save":
                    self._perform_save(result)
                elif self.file_dialog.mode == "load":
                    self._perform_load(result)
                self.file_dialog = None
            elif not self.file_dialog.active:
                self.file_dialog = None
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.camera_movement["up"] = True
            elif event.key == pygame.K_DOWN:
                self.camera_movement["down"] = True
            elif event.key == pygame.K_LEFT:
                self.camera_movement["left"] = True
            elif event.key == pygame.K_RIGHT:
                self.camera_movement["right"] = True
            elif event.key == pygame.K_s:
                self.open_save_dialog()
            elif event.key == pygame.K_l:
                self.open_load_dialog()
            elif event.key == pygame.K_ESCAPE:
                self._return_to_menu()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.camera_movement["up"] = False
            elif event.key == pygame.K_DOWN:
                self.camera_movement["down"] = False
            elif event.key == pygame.K_LEFT:
                self.camera_movement["left"] = False
            elif event.key == pygame.K_RIGHT:
                self.camera_movement["right"] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check UI first
                ui_clicked = False
                if event.pos[1] < 60:
                    for btn in self.buttons:
                        if btn["rect"].collidepoint(event.pos):
                            btn["action"]()
                            ui_clicked = True
                            break

                if not ui_clicked:
                    self.handle_click(event.pos)
            elif event.button == 4:  # Scroll up
                self.camera.zoom_in(0.1)
            elif event.button == 5:  # Scroll down
                self.camera.zoom_out(0.1)

    def _return_to_menu(self):
        self.game.scene_manager.switch_to("menu")

    def handle_click(self, screen_pos):
        grid_x, grid_y = self.camera.screen_to_grid(screen_pos[0], screen_pos[1])

        # Toggle wall
        if self.map.is_blocked(grid_x, grid_y):
            if (grid_x, grid_y) in self.map.walls:
                self.map.walls.remove((grid_x, grid_y))
        else:
            if 0 <= grid_x < self.map.width and 0 <= grid_y < self.map.height:
                self.map.add_wall(grid_x, grid_y)

    def update(self, dt):
        """Updates camera."""
        if self.camera_movement["up"]:
            self.camera.move(0, -config.CAMERA_SPEED * dt)
        if self.camera_movement["down"]:
            self.camera.move(0, config.CAMERA_SPEED * dt)
        if self.camera_movement["left"]:
            self.camera.move(-config.CAMERA_SPEED * dt, 0)
        if self.camera_movement["right"]:
            self.camera.move(config.CAMERA_SPEED * dt, 0)

    def draw(self, screen):
        """Draws the editor."""
        screen.fill((0, 0, 0))

        # Draw grid
        self._draw_grid(screen)

        # Draw map
        self.map.draw(screen, self.font, self.camera)

        # Draw UI
        self._draw_ui(screen)

        # Draw Tooltip
        if self.hover_grid_pos:
            self._draw_tooltip(screen)

        if self.file_dialog:
            self.file_dialog.draw()

    def _draw_tooltip(self, screen):
        gx, gy = self.hover_grid_pos
        tooltip_text = f"({gx}, {gy})"
        surf = self.tooltip_font.render(tooltip_text, True, (255, 255, 255))
        bg_rect = surf.get_rect(topleft=(self.mouse_pos[0] + 15, self.mouse_pos[1] + 15))

        # Add a small background for readability
        padding = 4
        bg_rect.inflate_ip(padding * 2, padding * 2)
        pygame.draw.rect(screen, (0, 0, 0, 200), bg_rect)
        pygame.draw.rect(screen, (100, 100, 100), bg_rect, 1)

        screen.blit(surf, (bg_rect.x + padding, bg_rect.y + padding))

    def _draw_grid(self, screen):
        grid_size = int(config.GRID_SIZE * self.camera.zoom)
        if grid_size > 0:
            width, height = self.game.screen.get_size()
            start_x = (math.floor(self.camera.x) - self.camera.x) * grid_size
            start_y = (math.floor(self.camera.y) - self.camera.y) * grid_size

            for x in range(int(start_x), width, grid_size):
                pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, height))
            for y in range(int(start_y), height, grid_size):
                pygame.draw.line(screen, (40, 40, 40), (0, y), (width, y))

    def _draw_ui(self, screen):
        # Draw background bar
        pygame.draw.rect(screen, (30, 30, 30), (0, 0, self.game.screen.get_width(), 60))
        pygame.draw.line(screen, (100, 100, 100), (0, 60), (self.game.screen.get_width(), 60))

        # Draw buttons
        for btn in self.buttons:
            color = (60, 60, 60)
            if btn["rect"].collidepoint(self.mouse_pos):
                color = (80, 80, 80)

            pygame.draw.rect(screen, color, btn["rect"])
            pygame.draw.rect(screen, (150, 150, 150), btn["rect"], 1)

            text_surf = self.ui_font.render(btn["text"], True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=btn["rect"].center)
            screen.blit(text_surf, text_rect)

            # Draw tooltip if hovered
            if btn["rect"].collidepoint(self.mouse_pos) and btn.get("tooltip"):
                tooltip_surf = self.tooltip_font.render(btn["tooltip"], True, (255, 255, 200))
                screen.blit(tooltip_surf, (btn["rect"].right + 10, btn["rect"].centery - 10))

        # Status info on the right
        status = f"Left Click: Toggle Wall | Map: {self.map.width}x{self.map.height} | Walls: {len(self.map.walls)}"
        status_surf = self.ui_font.render(status, True, (200, 200, 200))
        screen.blit(status_surf, (self.game.screen.get_width() - status_surf.get_width() - 10, 20))

    def open_save_dialog(self):
        """Opens the save map dialog."""
        initial_dir = os.path.join("command_line_conflict", "maps", "custom")
        self.file_dialog = FileDialog(self.game.screen, self.ui_font, "Save Map", initial_dir, mode="save")
        # Stop camera movement
        self.camera_movement = {k: False for k in self.camera_movement}

    def open_load_dialog(self):
        """Opens the load map dialog."""
        initial_dir = os.path.join("command_line_conflict", "maps", "custom")
        self.file_dialog = FileDialog(self.game.screen, self.ui_font, "Load Map", initial_dir, mode="load")
        # Stop camera movement
        self.camera_movement = {k: False for k in self.camera_movement}

    def _perform_save(self, file_path):
        try:
            self.map.save_to_file(file_path)
            self.map_path = file_path
            log.info(f"Map saved to {file_path}.")
        except (IOError, ValueError) as e:
            log.error(f"Failed to save map: {e}")

    def _perform_load(self, file_path):
        try:
            self.map = Map.load_from_file(file_path)
            self.map_path = file_path
            log.info(f"Map loaded from {file_path}.")
        except (IOError, ValueError) as e:
            log.error(f"Failed to load map: {e}")
