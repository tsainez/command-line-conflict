import math
import os
import pygame

try:
    import tkinter as tk
    from tkinter import filedialog

    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False

from command_line_conflict import config
from command_line_conflict.camera import Camera
from command_line_conflict.maps.base import Map
from command_line_conflict.logger import log


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
        self.map_path = os.path.join(
            "command_line_conflict", "maps", "custom", "custom_map.json"
        )
        try:
            self.map = Map.load_from_file(self.map_path)
            log.info(f"Loaded map from {self.map_path}")
        except FileNotFoundError:
            self.map = Map(width=40, height=30)
            log.info("Created new blank map")
        except Exception as e:
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

    def handle_event(self, event):
        """Handles user input."""
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
                self.save_map()
            elif event.key == pygame.K_l:
                self.load_map()
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
        text = f"Editor Mode | Left Click: Toggle Wall | S: Save | L: Load | ESC: Menu"
        surf = self.ui_font.render(text, True, (255, 255, 255))
        screen.blit(surf, (10, 10))

        status = f"Map: {self.map.width}x{self.map.height} | Walls: {len(self.map.walls)}"
        surf2 = self.ui_font.render(status, True, (200, 200, 200))
        screen.blit(surf2, (10, 30))

    def save_map(self):
        """Opens a file dialog (or console input) to save the map."""
        # Default directory
        initial_dir = os.path.join("command_line_conflict", "maps", "custom")
        if not os.path.exists(initial_dir):
            os.makedirs(initial_dir)

        file_path = None
        use_console = not HAS_TKINTER

        if HAS_TKINTER:
            try:
                root = tk.Tk()
                root.withdraw()  # Hide the main window
                file_path = filedialog.asksaveasfilename(
                    initialdir=initial_dir,
                    title="Save Map",
                    filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
                    defaultextension=".json",
                )
                root.destroy()
            except Exception as e:
                log.error(f"Tkinter error: {e}. Falling back to console.")
                print(f"Tkinter error: {e}")
                use_console = True

        if use_console and not file_path:
            print("\n--- Save Map ---")
            print(f"Default directory: {initial_dir}")
            try:
                name = input(
                    "Enter filename (e.g. mymap.json) or blank to cancel: "
                ).strip()
                if name:
                    # Security: sanitize filename to prevent path traversal
                    name = os.path.basename(name)
                    file_path = os.path.join(initial_dir, name)
                    if not file_path.endswith(".json"):
                        file_path += ".json"
            except EOFError:
                pass

        if file_path:
            try:
                self.map.save_to_file(file_path)
                self.map_path = file_path  # Update current path
                log.info(f"Map saved to {file_path}.")
                print(f"Map saved to {file_path}.")
            except Exception as e:
                log.error(f"Failed to save map: {e}")

    def load_map(self):
        """Opens a file dialog (or console input) to load a map."""
        initial_dir = os.path.join("command_line_conflict", "maps", "custom")
        if not os.path.exists(initial_dir):
            os.makedirs(initial_dir)

        file_path = None
        use_console = not HAS_TKINTER

        if HAS_TKINTER:
            try:
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename(
                    initialdir=initial_dir,
                    title="Load Map",
                    filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
                )
                root.destroy()
            except Exception as e:
                log.error(f"Tkinter error: {e}. Falling back to console.")
                print(f"Tkinter error: {e}")
                use_console = True

        if use_console and not file_path:
            print("\n--- Load Map ---")
            print(f"Directory: {initial_dir}")
            # List files
            try:
                files = [f for f in os.listdir(initial_dir) if f.endswith(".json")]
                if not files:
                    print("No maps found in custom folder.")
                else:
                    print("Available maps:")
                    for f in files:
                        print(f" - {f}")
            except OSError:
                pass

            try:
                name = input("Enter filename to load or blank to cancel: ").strip()
                if name:
                    # Security: sanitize filename to prevent path traversal
                    name = os.path.basename(name)
                    file_path = os.path.join(initial_dir, name)
                    if not file_path.endswith(".json"):
                        file_path += ".json"
            except EOFError:
                pass

        if file_path:
            try:
                self.map = Map.load_from_file(file_path)
                self.map_path = file_path
                log.info(f"Map loaded from {file_path}.")
                print(f"Map loaded from {file_path}.")
            except Exception as e:
                log.error(f"Failed to load map: {e}")
                print(f"Failed to load map: {e}")
