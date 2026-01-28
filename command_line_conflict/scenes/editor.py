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
        self.ui_font = pygame.font.SysFont("arial", 20)
        self.tooltip_font = pygame.font.SysFont("arial", 16)

        self.file_dialog = None
        self.mouse_pos = (0, 0)
        self.hover_grid_pos = None

        # Define buttons
        start_x = 10
        start_y = 10
        btn_width = 80
        btn_height = 30
        spacing = 10

        self.buttons = [
            {
                "label": "Save",
                "rect": pygame.Rect(start_x, start_y, btn_width, btn_height),
                "action": self.open_save_dialog,
                "tooltip": "Save Map (S)"
            },
            {
                "label": "Load",
                "rect": pygame.Rect(start_x + btn_width + spacing, start_y, btn_width, btn_height),
                "action": self.open_load_dialog,
                "tooltip": "Load Map (L)"
            },
            {
                "label": "Menu",
                "rect": pygame.Rect(start_x + (btn_width + spacing) * 2, start_y, btn_width, btn_height),
                "action": lambda: self.game.scene_manager.switch_to("menu"),
                "tooltip": "Return to Menu (ESC)"
            }
        ]
        self.hovered_button_index = None

    def handle_event(self, event):
        """Handles user input."""
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            self.hovered_button_index = None

            # Check for button hover first
            for i, btn in enumerate(self.buttons):
                if btn["rect"].collidepoint(event.pos):
                    self.hovered_button_index = i
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    return

            # Simple UI area check (top 60 pixels)
            if event.pos[1] < 60:
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
                self.game.scene_manager.switch_to("menu")
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
                # Check buttons
                clicked_btn = False
                for btn in self.buttons:
                    if btn["rect"].collidepoint(event.pos):
                        btn["action"]()
                        clicked_btn = True
                        break

                if not clicked_btn and not (self.file_dialog and self.file_dialog.active):
                    # Only edit map if not clicking UI
                    if event.pos[1] >= 60:
                        self.handle_click(event.pos)

            elif event.button == 4:  # Scroll up
                self.camera.zoom_in(0.1)
            elif event.button == 5:  # Scroll down
                self.camera.zoom_out(0.1)

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
        if self.file_dialog:
            self.file_dialog.update(dt)

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
        if self.hover_grid_pos and not self.hovered_button_index:
            self._draw_tooltip(screen)
        elif self.hovered_button_index is not None:
             self._draw_button_tooltip(screen)

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

    def _draw_button_tooltip(self, screen):
        btn = self.buttons[self.hovered_button_index]
        if "tooltip" not in btn:
            return

        surf = self.tooltip_font.render(btn["tooltip"], True, (255, 255, 255))
        bg_rect = surf.get_rect(topleft=(self.mouse_pos[0] + 10, self.mouse_pos[1] + 20))

        # Keep tooltip on screen
        if bg_rect.right > config.SCREEN_WIDTH:
            bg_rect.right = config.SCREEN_WIDTH - 10

        padding = 4
        bg_rect.inflate_ip(padding * 2, padding * 2)
        pygame.draw.rect(screen, (0, 0, 0, 220), bg_rect)
        pygame.draw.rect(screen, (150, 150, 150), bg_rect, 1)

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
        # Draw buttons
        for i, btn in enumerate(self.buttons):
            color = (70, 70, 70)
            if i == self.hovered_button_index:
                color = (100, 100, 100)

            pygame.draw.rect(screen, color, btn["rect"])
            pygame.draw.rect(screen, (200, 200, 200), btn["rect"], 1)

            text_surf = self.ui_font.render(btn["label"], True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=btn["rect"].center)
            screen.blit(text_surf, text_rect)

        # Draw status text below buttons
        status_y = 50
        text = "Editor Mode | Left Click: Toggle Wall"
        surf = self.ui_font.render(text, True, (255, 255, 255))
        screen.blit(surf, (10, status_y))

        status = f"Map: {self.map.width}x{self.map.height} | Walls: {len(self.map.walls)}"
        surf2 = self.ui_font.render(status, True, (200, 200, 200))
        screen.blit(surf2, (10, status_y + 25))

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
