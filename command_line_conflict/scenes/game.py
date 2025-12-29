import math
from types import SimpleNamespace

import pygame

from command_line_conflict import config, factories
from command_line_conflict.camera import Camera
from command_line_conflict.campaign_manager import CampaignManager
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.health import Health
from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.components.vision import Vision
from command_line_conflict.fog_of_war import FogOfWar
from command_line_conflict.game_state import GameState
from command_line_conflict.logger import log
from command_line_conflict.maps import SimpleMap
from command_line_conflict.maps.factory_battle_map import FactoryBattleMap
from command_line_conflict.systems.ai_system import AISystem
from command_line_conflict.systems.chat_system import ChatSystem
from command_line_conflict.systems.combat_system import CombatSystem
from command_line_conflict.systems.confetti_system import ConfettiSystem
from command_line_conflict.systems.corpse_removal_system import CorpseRemovalSystem
from command_line_conflict.systems.flee_system import FleeSystem
from command_line_conflict.systems.health_system import HealthSystem
from command_line_conflict.systems.movement_system import MovementSystem
from command_line_conflict.systems.production_system import ProductionSystem
from command_line_conflict.systems.rendering_system import RenderingSystem
from command_line_conflict.systems.selection_system import SelectionSystem
from command_line_conflict.systems.sound_system import SoundSystem
from command_line_conflict.systems.spawn_system import SpawnSystem
from command_line_conflict.systems.ui_system import UISystem
from command_line_conflict.systems.wander_system import WanderSystem


class UnitView:
    """A simple object to satisfy the FogOfWar interface."""

    def __init__(self, x, y, vision_range):
        self.x = x
        self.y = y
        self.vision_range = vision_range


class GameScene:
    """Manages the main gameplay scene, including entities, systems, and events."""

    def __init__(self, game):
        """Initializes the GameScene.

        Args:
            game: The main game object, providing access to the screen, font,
                  and scene manager.
        """
        self.game = game
        self.font = game.font
        self.game_state = GameState(FactoryBattleMap())
        self.fog_of_war = FogOfWar(self.game_state.map.width, self.game_state.map.height)
        self.selection_start = None
        self.paused = False
        self.current_player_id = 1

        # Cheats
        self.cheats = {
            "reveal_map": False,
            "god_mode": False,
        }

        # Fog of War
        self.fog_of_war = FogOfWar(self.game_state.map.width, self.game_state.map.height)

        # Camera
        self.camera = Camera()
        self.camera_movement = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }
        self.drag_start_pos = None  # For middle mouse drag
        self.camera_start_pos = None

        # Initialize systems
        self.campaign_manager = CampaignManager()
        self.movement_system = MovementSystem()
        self.rendering_system = RenderingSystem(self.game.screen, self.font, self.camera)
        self.combat_system = CombatSystem()
        self.flee_system = FleeSystem()
        self.health_system = HealthSystem()
        self.selection_system = SelectionSystem()
        self.ui_system = UISystem(self.game.screen, self.font, self.camera)
        self.chat_system = ChatSystem(self.game.screen, self.font)
        # Pass the cheats dictionary by reference so UISystem can see changes
        self.ui_system.cheats = self.cheats
        self.corpse_removal_system = CorpseRemovalSystem()
        self.ai_system = AISystem()
        self.confetti_system = ConfettiSystem()
        self.production_system = ProductionSystem(self.campaign_manager)

        # Current Mission ID - In a full game this would be passed from a mission select screen
        self.current_mission_id = "mission_1"

        self.sound_system = SoundSystem()
        self.wander_system = WanderSystem()
        self.spawn_system = SpawnSystem(spawn_interval=5.0)  # Spawn every 5 seconds
        self._create_initial_units()

        self.has_player_2_opponent = any(
            c.get(Player) and c.get(Player).player_id == 2 for _, c in self.game_state.entities.items()
        )

        # Start game music
        # Assuming the music file is in the root or a music folder
        # For now using a placeholder path
        self.game.music_manager.play("music/game_theme.ogg")

        if config.DEBUG:
            cheats_list = [
                "Debug Cheats:",
                "F1: Toggle Reveal Map",
                "F2: Toggle God Mode",
                "TAB: Switch Player",
                "1-6: Spawn Units",
            ]
            for cheat in cheats_list:
                log.info(cheat)

    def _create_initial_units(self):
        """Creates the starting units for each player."""
        if hasattr(self.game_state.map, "create_initial_units"):
            self.game_state.map.create_initial_units(self.game_state)
        else:
            # Fallback for maps without custom spawn logic
            # Player 1 units (human)
            for i in range(3):
                factories.create_chassis(self.game_state, 10 + i * 2, 10, player_id=1, is_human=True)
            # Player 2 units (AI) - Mission 1: Single Rover in center
            factories.create_rover(self.game_state, 20, 15, player_id=2, is_human=False)

    def handle_event(self, event):
        """Handles user input and other events for the game scene.

        This includes mouse clicks for selection and movement, as well as
        keyboard shortcuts for creating units and quitting the game.

        Args:
            event: The pygame event to handle.
        """
        # Pass event to chat system first
        if self.chat_system.handle_event(event):
            return

        log.debug(f"Handling event: {event}")

        # Handle construction hotkeys if a chassis is selected
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_r, pygame.K_a):
                self._handle_construction(event.key)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.selection_start = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.selection_start:
            x1, y1 = self.selection_start
            x2, y2 = event.pos
            # If the mouse moved less than 5 pixels, it's a click
            if (x2 - x1) ** 2 + (y2 - y1) ** 2 < 25:
                mods = pygame.key.get_mods()
                shift_pressed = mods & pygame.KMOD_SHIFT
                grid_pos = self.camera.screen_to_grid(event.pos[0], event.pos[1])
                log.debug(f"Click selection at {grid_pos}. Shift: {shift_pressed}")
                self.selection_system.handle_click_selection(self.game_state, grid_pos, shift_pressed, self.current_player_id)
            else:
                log.debug(f"Drag selection from {self.selection_start} to {event.pos}")
                mods = pygame.key.get_mods()
                shift_pressed = mods & pygame.KMOD_SHIFT
                grid_start = self.camera.screen_to_grid(self.selection_start[0], self.selection_start[1])
                grid_end = self.camera.screen_to_grid(event.pos[0], event.pos[1])
                self.selection_system.update(
                    self.game_state,
                    grid_start,
                    grid_end,
                    shift_pressed,
                    self.current_player_id,
                )
            self.selection_start = None
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            grid_x, grid_y = self.camera.screen_to_grid(event.pos[0], event.pos[1])
            log.debug(f"Right-click move command at grid coordinates: {(grid_x, grid_y)}")
            # Add visual feedback (green ripple)
            self.ui_system.add_click_effect(grid_x, grid_y, (0, 255, 0))

            for entity_id, components in self.game_state.entities.items():
                selectable = components.get(Selectable)
                if selectable and selectable.is_selected:
                    log.info(f"Moving entity {entity_id} to {(grid_x, grid_y)}")
                    # Moving clears hold position
                    from command_line_conflict.components.movable import Movable

                    movable = components.get(Movable)
                    if movable:
                        movable.hold_position = False

                    self.movement_system.set_target(self.game_state, entity_id, grid_x, grid_y)
                    attack = components.get(Attack)
                    if attack:
                        attack.attack_target = None
        elif event.type == pygame.KEYDOWN:
            # Camera movement
            if event.key == pygame.K_UP:
                self.camera_movement["up"] = True
            elif event.key == pygame.K_DOWN:
                self.camera_movement["down"] = True
            elif event.key == pygame.K_LEFT:
                self.camera_movement["left"] = True
            elif event.key == pygame.K_RIGHT:
                self.camera_movement["right"] = True
            else:
                if config.DEBUG:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        mx, my = pygame.mouse.get_pos()
                        gx, gy = self.camera.screen_to_grid(mx, my)
                        if event.key == pygame.K_1:
                            factories.create_extractor(
                                self.game_state,
                                gx,
                                gy,
                                player_id=self.current_player_id,
                                is_human=True,
                            )
                        elif event.key == pygame.K_2:
                            factories.create_chassis(
                                self.game_state,
                                gx,
                                gy,
                                player_id=self.current_player_id,
                                is_human=True,
                            )
                        elif event.key == pygame.K_3:
                            factories.create_rover(
                                self.game_state,
                                gx,
                                gy,
                                player_id=self.current_player_id,
                                is_human=True,
                            )
                        elif event.key == pygame.K_4:
                            factories.create_arachnotron(
                                self.game_state,
                                gx,
                                gy,
                                player_id=self.current_player_id,
                                is_human=True,
                            )
                        elif event.key == pygame.K_5:
                            factories.create_observer(
                                self.game_state,
                                gx,
                                gy,
                                player_id=self.current_player_id,
                                is_human=True,
                            )
                        elif event.key == pygame.K_6:
                            factories.create_immortal(
                                self.game_state,
                                gx,
                                gy,
                                player_id=self.current_player_id,
                                is_human=True,
                            )

                    # Debug cheats
                    if event.key == pygame.K_F1:
                        self.cheats["reveal_map"] = not self.cheats["reveal_map"]
                        status = "Enabled" if self.cheats["reveal_map"] else "Disabled"
                        log.info(f"Cheat 'Reveal Map' toggled: {self.cheats['reveal_map']}")
                        self.chat_system.add_message(f"Cheat: Map Reveal {status}", (255, 0, 255))
                    elif event.key == pygame.K_F2:
                        self.cheats["god_mode"] = not self.cheats["god_mode"]
                        status = "Enabled" if self.cheats["god_mode"] else "Disabled"
                        log.info(f"Cheat 'God Mode' toggled: {self.cheats['god_mode']}")
                        self.chat_system.add_message(f"Cheat: God Mode {status}", (255, 0, 255))
                    elif event.key == pygame.K_TAB:
                        # Switch sides
                        self.selection_system.clear_selection(self.game_state)
                        if self.current_player_id == 1:
                            self.current_player_id = 2
                        else:
                            self.current_player_id = 1
                        log.info(f"Switched to player {self.current_player_id}")
                        self.chat_system.add_message(f"Switched to player {self.current_player_id}", (255, 0, 255))

                if event.key == pygame.K_h:
                    # Hold Position
                    self.chat_system.add_message("Hold Position command issued", (255, 255, 0))
                    from command_line_conflict.components.movable import Movable

                    for entity_id, components in self.game_state.entities.items():
                        selectable = components.get(Selectable)
                        if selectable and selectable.is_selected:
                            movable = components.get(Movable)
                            if movable:
                                movable.hold_position = True
                                movable.path = []
                                movable.target_x = None
                                movable.target_y = None
                                log.info(f"Entity {entity_id} holding position")

                elif event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    self.paused = not self.paused
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
        # Camera zoom (mouse wheel) and middle mouse drag
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.camera.zoom_in(0.1)
            elif event.button == 5:  # Scroll down
                self.camera.zoom_out(0.1)
            elif event.button == 2:  # Middle mouse click (start drag)
                self.drag_start_pos = event.pos
                self.camera_start_pos = (self.camera.x, self.camera.y)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:  # Middle mouse release (end drag)
                self.drag_start_pos = None
                self.camera_start_pos = None
        elif event.type == pygame.MOUSEMOTION:
            if self.drag_start_pos and self.camera_start_pos:
                # Middle mouse drag logic
                dx = event.pos[0] - self.drag_start_pos[0]
                dy = event.pos[1] - self.drag_start_pos[1]

                # Convert screen delta to grid delta
                # When dragging the "world", if I move mouse RIGHT (positive dx),
                # the camera should move LEFT (decrease x) to "pull" the world.

                grid_dx = dx / (config.GRID_SIZE * self.camera.zoom)
                grid_dy = dy / (config.GRID_SIZE * self.camera.zoom)

                self.camera.x = self.camera_start_pos[0] - grid_dx
                self.camera.y = self.camera_start_pos[1] - grid_dy

    def _handle_construction(self, key):
        """Handles building construction requests."""
        # Find selected chassis
        selected_chassis_ids = []
        for entity_id, components in self.game_state.entities.items():
            selectable = components.get(Selectable)
            # I need to get UnitIdentity from components
            identity = components.get(factories.UnitIdentity)

            if selectable and selectable.is_selected:
                if identity and identity.name == "chassis":
                    selected_chassis_ids.append(entity_id)

        if not selected_chassis_ids:
            return

        # Simple logic: First selected chassis builds the factory
        builder_id = selected_chassis_ids[0]
        pos = self.game_state.get_component(builder_id, factories.Position)
        player = self.game_state.get_component(builder_id, factories.Player)

        if not pos or not player:
            return

        # Check unlock requirements and build
        if key == pygame.K_r:  # Build Rover Factory
            # Check if Rover is unlocked (implied requirement for Rover Factory)
            if self.campaign_manager.is_unit_unlocked("rover"):
                log.info("Building Rover Factory")
                self.game_state.remove_entity(builder_id)
                factories.create_rover_factory(self.game_state, pos.x, pos.y, player.player_id, player.is_human)
                self.game.steam.unlock_achievement("BUILDER")
            else:
                log.info("Rover tech not unlocked!")

        elif key == pygame.K_a:  # Build Arachnotron Factory
            if self.campaign_manager.is_unit_unlocked("arachnotron"):
                log.info("Building Arachnotron Factory")
                self.game_state.remove_entity(builder_id)
                factories.create_arachnotron_factory(self.game_state, pos.x, pos.y, player.player_id, player.is_human)
                self.game.steam.unlock_achievement("BUILDER")
            else:
                log.info("Arachnotron tech not unlocked!")

    def _update_camera(self, dt):
        """Updates the camera position based on user input."""
        if self.camera_movement["up"]:
            self.camera.move(0, -config.CAMERA_SPEED * dt)
        if self.camera_movement["down"]:
            self.camera.move(0, config.CAMERA_SPEED * dt)
        if self.camera_movement["left"]:
            self.camera.move(-config.CAMERA_SPEED * dt, 0)
        if self.camera_movement["right"]:
            self.camera.move(config.CAMERA_SPEED * dt, 0)

    def update(self, dt):
        """Updates the state of all game systems.

        Args:
            dt: The time elapsed since the last frame.
        """
        self.chat_system.update(dt)

        if self.paused:
            return

        # God Mode Cheat
        if self.cheats["god_mode"]:
            for _, components in self.game_state.entities.items():
                player = components.get(Player)
                health = components.get(Health)
                if player and player.is_human and health:
                    health.hp = health.max_hp

        self._update_camera(dt)
        self.health_system.update(self.game_state, dt)
        self.flee_system.update(self.game_state, dt)
        self.ai_system.update(self.game_state)
        self.wander_system.update(self.game_state, dt)
        self.combat_system.update(self.game_state, dt)
        self.confetti_system.update(self.game_state, dt)
        self.movement_system.update(self.game_state, dt)
        self.production_system.update(self.game_state, dt)
        self.corpse_removal_system.update(self.game_state, dt)
        self.sound_system.update(self.game_state)

        # Clear event queue after all systems have processed events
        self.game_state.event_queue.clear()
        self.spawn_system.update(self.game_state, dt)

        # Update Fog of War
        vision_units = []
        for entity_id, components in self.game_state.entities.items():
            pos = components.get(Position)
            vis = components.get(Vision)
            player = components.get(Player)
            if pos and vis and player and player.is_human:
                vision_units.append(SimpleNamespace(x=pos.x, y=pos.y, vision_range=vis.vision_range))
        self.fog_of_war.update(vision_units)

        if self.check_win_condition():
            self.game.scene_manager.switch_to("victory")
        elif self.check_loss_condition():
            self.game.scene_manager.switch_to("defeat")

    def check_win_condition(self) -> bool:
        """Checks if the player has won the level.

        Returns:
            True if the win condition is met, False otherwise.
        """
        enemy_count = 0
        for _, components in self.game_state.entities.items():
            player = components.get(Player)
            if player and not player.is_human:
                if self.has_player_2_opponent and player.player_id == config.NEUTRAL_PLAYER_ID:
                    continue
                if Health in components:
                    enemy_count += 1

        if enemy_count == 0:
            log.info("Victory! Mission Complete.")
            self.game.steam.unlock_achievement("VICTORY")
            # Trigger victory sound (note: scene switch might cut it off if SoundSystem isn't persistent or updated)
            # Since SoundSystem is part of GameScene, and we switch scene, we should ideally play it in the new scene
            # or ensure the sound continues. For now, we emit the event.
            # But wait, if we switch immediately, update won't process events.
            # However, GameScene.update processes systems then checks win.
            # So the event might be lost if we don't process it.
            # Actually, SoundSystem.update is called BEFORE check_win_condition in update().
            # So if we add event here, it won't be processed until NEXT frame's SoundSystem.update.
            # But next frame we are in VictoryScene.
            # So we should play it directly via self.sound_system.play_sound("victory") to ensure it starts.
            self.sound_system.play_sound("victory")
            self.campaign_manager.complete_mission(self.current_mission_id)
            return True
        return False

    def check_loss_condition(self) -> bool:
        """Checks if the player has lost the level.

        Returns:
            True if the loss condition is met, False otherwise.
        """
        player_entity_count = 0
        for _, components in self.game_state.entities.items():
            player = components.get(Player)
            if player and player.is_human:
                # Check for any player-controlled entity (unit or building)
                if Health in components:
                    player_entity_count += 1

        if player_entity_count == 0:
            log.info("Defeat! Mission Failed.")
            self.game.steam.unlock_achievement("DEFEAT")
            self.sound_system.play_sound("defeat")
            return True
        return False

    def draw(self, screen):
        """Draws the entire game scene.

        This includes the background grid, the map, all entities, and the UI.

        Args:
            screen: The pygame screen surface to draw on.
        """
        screen.fill((0, 0, 0))

        # Draw grid lines with camera and zoom
        grid_size = int(config.GRID_SIZE * self.camera.zoom)
        if grid_size > 0:
            width, height = self.game.screen.get_size()
            start_x = (math.floor(self.camera.x) - self.camera.x) * grid_size
            start_y = (math.floor(self.camera.y) - self.camera.y) * grid_size

            for x in range(int(start_x), width, grid_size):
                pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, height))
            for y in range(int(start_y), height, grid_size):
                pygame.draw.line(screen, (40, 40, 40), (0, y), (width, y))

        self.game_state.map.draw(screen, self.font, camera=self.camera)
        self.rendering_system.draw(self.game_state, self.paused)

        if not self.cheats["reveal_map"]:
            self.fog_of_war.draw(screen, self.camera)

        self.chat_system.draw()
        self.ui_system.draw(self.game_state, self.paused, self.current_player_id)

        # Highlight selected units
        if self.selection_start:
            x1, y1 = self.selection_start
            x2, y2 = pygame.mouse.get_pos()
            min_x, max_x = sorted((x1, x2))
            min_y, max_y = sorted((y1, y2))
            rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
            overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
            overlay.fill((0, 255, 0, 60))
            screen.blit(overlay, rect.topleft)
            pygame.draw.rect(screen, (0, 255, 0), rect, 1)
