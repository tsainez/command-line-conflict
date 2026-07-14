import math
from types import SimpleNamespace

import pygame

from command_line_conflict import config, factories
from command_line_conflict.camera import Camera
from command_line_conflict.campaign_manager import CampaignManager
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.dead import Dead
from command_line_conflict.components.health import Health
from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.components.unit_identity import UnitIdentity
from command_line_conflict.components.vision import Vision
from command_line_conflict.fog_of_war import FogOfWar
from command_line_conflict.game_state import GameState
from command_line_conflict.logger import log
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
from command_line_conflict.systems.resource_system import ResourceSystem
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

        # Lifecycle flags used by SceneManager/MenuScene to decide whether
        # this scene can be resumed after ESC-ing out to the menu.
        # mission_started flips once the scene actually runs a frame (a
        # freshly constructed, never-entered scene is not "in progress");
        # mission_over flips when the win/loss condition fires.
        self.mission_started = False
        self.mission_over = False

        self.win_loss_check_timer = 0.0

        # Cheats
        self.cheats = {
            "reveal_map": False,
            "god_mode": False,
        }

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
        self.hovered_entity_id = None
        self._wave_cache = {}

        # Initialize systems
        self.campaign_manager = CampaignManager()
        self.game_state.campaign_manager = self.campaign_manager
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
        self.resource_system = ResourceSystem()

        # Current Mission ID - In a full game this would be passed from a mission select screen
        self.current_mission_id = "mission_1"

        self.sound_system = SoundSystem()
        self.wander_system = WanderSystem()
        self.spawn_system = SpawnSystem(spawn_interval=5.0)  # Spawn every 5 seconds
        self._create_initial_units()

        player_entities = [self.game_state.entities.get(eid) for eid in self.game_state.get_entities_with_component(Player)]
        self.has_player_2_opponent = any(c and c.get(Player) and c.get(Player).player_id == 2 for c in player_entities)

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

        # R and A are context-sensitive hotkeys shared between two actions:
        #   - Chassis selected:            R/A = build a factory (consumes the chassis).
        #   - Arachnotron Factory selected: R/A = train a Rover / Arachnotron.
        # Construction takes priority and consumes the keypress. Without the
        # early return, a mixed selection (chassis + factory) would trigger
        # BOTH actions from a single keypress and double-spend scrap.
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_r, pygame.K_a):
                if self._handle_construction(event.key):
                    return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.selection_start = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.selection_start:
            x1, y1 = self.selection_start
            x2, y2 = event.pos
            # If the mouse moved less than 5 pixels, it's a click
            dx = x2 - x1
            dy = y2 - y1
            if dx * dx + dy * dy < 25:
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
            log.debug(f"Right-click command at grid coordinates: {(grid_x, grid_y)}")

            # Check if there is an enemy at the target location
            target_enemy_id = None
            entities_at_pos = self.game_state.get_entities_at_position(grid_x, grid_y)
            for eid in entities_at_pos:
                # Filter for live enemies
                if self.game_state.get_component(eid, Dead):
                    continue
                player = self.game_state.get_component(eid, Player)
                if player and player.player_id != self.current_player_id:
                    target_enemy_id = eid
                    break

            if target_enemy_id:
                # Attack Command
                log.info(f"Attack command issued on entity {target_enemy_id}")
                # Visual feedback (red ripple)
                self.ui_system.add_click_effect(grid_x, grid_y, (255, 0, 0))

                for entity_id in self.game_state.get_entities_with_component(Selectable):
                    components = self.game_state.entities.get(entity_id)
                    if not components:
                        continue

                    selectable = components.get(Selectable)
                    if selectable and selectable.is_selected:
                        attack = components.get(Attack)
                        if attack:
                            attack.attack_target = target_enemy_id
                            # Clear move target if attacking? CombatSystem handles closing distance.
                            # But if we were moving elsewhere, we should stop?
                            # CombatSystem will update position if needed.
                            # We should probably clear explicit move path so it doesn't wander off.
                            from command_line_conflict.components.movable import Movable

                            movable = components.get(Movable)
                            if movable:
                                movable.path = []
                                movable.target_x = None
                                movable.target_y = None
                                movable.hold_position = False
            else:
                # Move Command
                log.info(f"Move command issued to {(grid_x, grid_y)}")
                # Visual feedback (green ripple)
                self.ui_system.add_click_effect(grid_x, grid_y, (0, 255, 0))

                for entity_id in self.game_state.get_entities_with_component(Selectable):
                    components = self.game_state.entities.get(entity_id)
                    if not components:
                        continue

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
                    if config.DEBUG:
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
                            # Security: Gated side-switching feature behind config.DEBUG to prevent unauthorized access
                            self.selection_system.clear_selection(self.game_state)
                            if self.current_player_id == 1:
                                self.current_player_id = 2
                            else:
                                self.current_player_id = 1
                            log.info(f"Switched to player {self.current_player_id}")
                            self.chat_system.add_message(f"Switched to player {self.current_player_id}", (255, 0, 255))

                if event.key == pygame.K_c:
                    selected_factories = []
                    for entity_id in self.game_state.get_entities_with_component(Selectable):
                        components = self.game_state.entities.get(entity_id)
                        if not components:
                            continue
                        selectable = components.get(Selectable)
                        identity = components.get(UnitIdentity)
                        player = components.get(Player)
                        if player and player.player_id == self.current_player_id:
                            if selectable and selectable.is_selected:
                                if identity and (
                                    "factory" in identity.name or identity.name in ("rover_factory", "arachnotron_factory")
                                ):
                                    selected_factories.append(entity_id)

                    if selected_factories:
                        self._train_chassis_at_factory(selected_factories[0])

                if event.key == pygame.K_t:
                    selected_rover_factories = []
                    for entity_id in self.game_state.get_entities_with_component(Selectable):
                        components = self.game_state.entities.get(entity_id)
                        if not components:
                            continue
                        selectable = components.get(Selectable)
                        identity = components.get(UnitIdentity)
                        player = components.get(Player)
                        if player and player.player_id == self.current_player_id:
                            if selectable and selectable.is_selected:
                                if identity and identity.name == "rover_factory":
                                    selected_rover_factories.append(entity_id)

                    if selected_rover_factories:
                        self._research_arachnotron_at_factory(selected_rover_factories[0])

                if event.key == pygame.K_r:
                    selected_arachnotron_factories = []
                    for entity_id in self.game_state.get_entities_with_component(Selectable):
                        components = self.game_state.entities.get(entity_id)
                        if not components:
                            continue
                        selectable = components.get(Selectable)
                        identity = components.get(UnitIdentity)
                        player = components.get(Player)
                        if player and player.player_id == self.current_player_id:
                            if selectable and selectable.is_selected:
                                if identity and identity.name == "arachnotron_factory":
                                    selected_arachnotron_factories.append(entity_id)

                    if selected_arachnotron_factories:
                        self._train_rover_at_factory(selected_arachnotron_factories[0])

                if event.key == pygame.K_a:
                    selected_arachnotron_factories = []
                    for entity_id in self.game_state.get_entities_with_component(Selectable):
                        components = self.game_state.entities.get(entity_id)
                        if not components:
                            continue
                        selectable = components.get(Selectable)
                        identity = components.get(UnitIdentity)
                        player = components.get(Player)
                        if player and player.player_id == self.current_player_id:
                            if selectable and selectable.is_selected:
                                if identity and identity.name == "arachnotron_factory":
                                    selected_arachnotron_factories.append(entity_id)

                    if selected_arachnotron_factories:
                        self._train_arachnotron_at_factory(selected_arachnotron_factories[0])

                if event.key == pygame.K_h:
                    # Hold Position
                    self.chat_system.add_message("Hold Position command issued", (255, 255, 0))
                    from command_line_conflict.components.movable import Movable

                    for entity_id in self.game_state.get_entities_with_component(Selectable):
                        components = self.game_state.entities.get(entity_id)
                        if not components:
                            continue

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
            self._update_cursor(event.pos)
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

    def _update_cursor(self, screen_pos: tuple[int, int]) -> None:
        """Updates the mouse cursor based on what is under the mouse."""
        self.hovered_entity_id = None
        # Check if over UI panel (bottom 100px)
        panel_height = 100
        if screen_pos[1] > config.SCREEN_HEIGHT - panel_height:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            return

        grid_x, grid_y = self.camera.screen_to_grid(screen_pos[0], screen_pos[1])
        entity_ids = self.game_state.get_entities_at_position(grid_x, grid_y)

        cursor_set = False
        for entity_id in entity_ids:
            # We must filter out dead entities, or cursors will react to corpses
            if self.game_state.get_component(entity_id, Dead):
                continue

            self.hovered_entity_id = entity_id
            player = self.game_state.get_component(entity_id, Player)
            if player:
                if player.player_id != self.current_player_id and player.player_id != config.NEUTRAL_PLAYER_ID:
                    # Enemy
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
                    cursor_set = True
                    break
                if player.player_id == self.current_player_id:
                    # Friendly
                    if self.game_state.get_component(entity_id, Selectable):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        cursor_set = True
                        break

        if not cursor_set:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def _handle_construction(self, key) -> bool:
        """Handles building construction requests.

        Returns:
            True if a chassis was selected and the keypress was consumed
            (even if the build was refused, e.g. insufficient scrap), False
            if no builder was selected and the key should fall through to
            other handlers (factory training shares the R/A keys).
        """
        # Find selected chassis
        selected_chassis_ids = []
        for entity_id in self.game_state.get_entities_with_component(Selectable):
            components = self.game_state.entities.get(entity_id)
            if not components:
                continue

            selectable = components.get(Selectable)
            identity = components.get(UnitIdentity)

            if selectable and selectable.is_selected:
                if identity and identity.name == "chassis":
                    selected_chassis_ids.append(entity_id)

        if not selected_chassis_ids:
            return False

        # Simple logic: First selected chassis builds the factory
        builder_id = selected_chassis_ids[0]
        pos = self.game_state.get_component(builder_id, Position)
        player = self.game_state.get_component(builder_id, Player)

        if not pos or not player:
            return True

        # Check unlock requirements and build
        if key == pygame.K_r:  # Build Rover Factory
            # Check if Rover is unlocked (implied requirement for Rover Factory)
            if not self.campaign_manager.is_unit_unlocked("rover"):
                log.info("Rover tech not unlocked!")
                self.chat_system.add_message("Rover tech not unlocked!", (255, 0, 0))
                return True

            cost = 100
            player_resources = self.game_state.resources.get(player.player_id, 0)
            if player_resources < cost:
                log.info(f"Insufficient scrap! Need {cost}, have {player_resources}.")
                self.chat_system.add_message(f"Insufficient scrap! Need {cost}, have {player_resources}.", (255, 0, 0))
                return True

            log.info("Building Rover Factory")
            self.game_state.resources[player.player_id] = player_resources - cost
            self.game_state.remove_entity(builder_id)
            factories.create_rover_factory(self.game_state, pos.x, pos.y, player.player_id, player.is_human)
            self.game.steam.unlock_achievement("BUILDER")

        elif key == pygame.K_a:  # Build Arachnotron Factory
            if not self.campaign_manager.is_unit_unlocked("arachnotron"):
                log.info("Arachnotron tech not unlocked!")
                self.chat_system.add_message("Arachnotron tech not unlocked!", (255, 0, 0))
                return True

            cost = 150
            player_resources = self.game_state.resources.get(player.player_id, 0)
            if player_resources < cost:
                log.info(f"Insufficient scrap! Need {cost}, have {player_resources}.")
                self.chat_system.add_message(f"Insufficient scrap! Need {cost}, have {player_resources}.", (255, 0, 0))
                return True

            log.info("Building Arachnotron Factory")
            self.game_state.resources[player.player_id] = player_resources - cost
            self.game_state.remove_entity(builder_id)
            factories.create_arachnotron_factory(self.game_state, pos.x, pos.y, player.player_id, player.is_human)
            self.game.steam.unlock_achievement("BUILDER")

        return True

    def _find_free_adjacent_tile(self, center_pos: Position) -> "tuple[float, float] | None":
        """Finds a walkable, unoccupied tile in the 8 cells around a position.

        Returns:
            (x, y) of the first free neighboring tile, or None if all eight
            neighbors are blocked. Callers must treat None as "do not spawn"
            rather than spawning on the center tile itself — see the exploit
            notes in the training methods below.
        """
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            nx, ny = int(center_pos.x + dx), int(center_pos.y + dy)
            if self.game_state.map.is_walkable(nx, ny) and not self.game_state.is_position_occupied(nx, ny):
                return float(nx), float(ny)
        return None

    def _train_chassis_at_factory(self, factory_id):
        """Trains a chassis at the selected factory."""
        cost = 50
        player_resources = self.game_state.resources.get(self.current_player_id, 0)
        if player_resources < cost:
            log.info(f"Insufficient scrap to train Chassis! Need {cost}, have {player_resources}.")
            self.chat_system.add_message(f"Insufficient scrap! Need {cost}, have {player_resources}.", (255, 0, 0))
            return

        factory_pos = self.game_state.get_component(factory_id, Position)
        player = self.game_state.get_component(factory_id, Player)
        if not factory_pos or not player:
            return

        # Find a free adjacent tile to spawn the chassis. Never fall back to
        # the factory's own tile: ProductionSystem transforms any input unit
        # standing on a factory (chassis -> rover here) at zero scrap cost,
        # so an on-factory spawn would silently upgrade the unit for free.
        spawn_pos = self._find_free_adjacent_tile(factory_pos)
        if spawn_pos is None:
            self.chat_system.add_message("No open tile next to the factory to deploy a Chassis!", (255, 0, 0))
            return
        spawn_x, spawn_y = spawn_pos

        # Spend resources
        self.game_state.resources[self.current_player_id] = player_resources - cost

        # Spawn unit
        factories.create_chassis(self.game_state, spawn_x, spawn_y, player_id=player.player_id, is_human=player.is_human)

        log.info(f"Trained Chassis at ({spawn_x}, {spawn_y}) for player {player.player_id}")
        self.chat_system.add_message("Chassis trained successfully.", (0, 255, 0))

        # Sound effect
        self.game_state.add_event({"type": "sound", "data": {"name": "spawn_unit"}})

        # Floating text at factory position
        self.game_state.add_event(
            {
                "type": "visual_effect",
                "subtype": "floating_text",
                "x": factory_pos.x,
                "y": factory_pos.y,
                "text": "+Chassis",
                "color": (0, 255, 0),
            }
        )

    def _research_arachnotron_at_factory(self, factory_id):
        """Researches Arachnotron tech at the selected Rover Factory."""
        if self.campaign_manager.is_unit_unlocked("arachnotron"):
            self.chat_system.add_message("Arachnotron tech is already unlocked!", (255, 255, 0))
            return

        # Count chassis
        chassis_count = 0
        from command_line_conflict.components.dead import Dead
        from command_line_conflict.components.player import Player
        from command_line_conflict.components.unit_identity import UnitIdentity

        for eid in self.game_state.get_entities_with_component(UnitIdentity):
            components = self.game_state.entities[eid]
            ident = components.get(UnitIdentity)
            if ident and ident.name == "chassis":
                plyr = components.get(Player)
                if plyr and plyr.player_id == self.current_player_id and Dead not in components:
                    chassis_count += 1

        cost = 100
        player_resources = self.game_state.resources.get(self.current_player_id, 0)

        # Verify chassis requirement
        if chassis_count < 6:
            self.chat_system.add_message(f"Research requirements not met! Need 6 Chassis (have {chassis_count}).", (255, 0, 0))
            return

        # Verify scrap requirement
        if player_resources < cost:
            self.chat_system.add_message(f"Insufficient scrap! Need {cost}, have {player_resources}.", (255, 0, 0))
            return

        # Deduct cost
        self.game_state.resources[self.current_player_id] = player_resources - cost

        # Unlock Arachnotron tech for THIS MATCH ONLY. This mutates the
        # in-memory set on the scene's CampaignManager; it is deliberately not
        # saved to disk (save_progress only persists completed_missions, and
        # _update_unlocks would discard it anyway). A new GameScene starts
        # with the research locked again. See the DESIGN NOTE above
        # MISSION_REWARDS in campaign_manager.py before changing this.
        self.campaign_manager.unlocked_units.add("arachnotron")

        log.info(f"Arachnotron tech researched by player {self.current_player_id}")
        self.chat_system.add_message(
            "Arachnotron research complete! Arachnotron Factories can now be constructed.", (0, 255, 0)
        )

        # Visual and sound effect
        self.game_state.add_event({"type": "sound", "data": {"name": "spawn_unit"}})
        factory_pos = self.game_state.get_component(factory_id, Position)
        if factory_pos:
            self.game_state.add_event(
                {
                    "type": "visual_effect",
                    "subtype": "floating_text",
                    "x": factory_pos.x,
                    "y": factory_pos.y,
                    "text": "RESEARCH COMPLETE",
                    "color": (255, 215, 0),
                }
            )

    def _train_rover_at_factory(self, factory_id):
        """Trains a rover at the selected Arachnotron Factory."""
        cost = 80
        player_resources = self.game_state.resources.get(self.current_player_id, 0)
        if player_resources < cost:
            self.chat_system.add_message(
                f"Insufficient scrap to train Rover! Need {cost}, have {player_resources}.", (255, 0, 0)
            )
            return

        factory_pos = self.game_state.get_component(factory_id, Position)
        player = self.game_state.get_component(factory_id, Player)
        if not factory_pos or not player:
            return

        # Find a free adjacent tile to spawn the rover. Never fall back to the
        # factory's own tile: this is an Arachnotron Factory whose input unit
        # is "rover", so ProductionSystem would instantly convert an
        # on-factory rover into a free Arachnotron, bypassing the 120-scrap
        # cost and the adjacent-rover training requirement.
        spawn_pos = self._find_free_adjacent_tile(factory_pos)
        if spawn_pos is None:
            self.chat_system.add_message("No open tile next to the factory to deploy a Rover!", (255, 0, 0))
            return
        spawn_x, spawn_y = spawn_pos

        # Spend resources
        self.game_state.resources[self.current_player_id] = player_resources - cost

        # Spawn unit
        factories.create_rover(
            self.game_state,
            spawn_x,
            spawn_y,
            player_id=player.player_id,
            is_human=player.is_human,
        )

        log.info(f"Trained Rover at ({spawn_x}, {spawn_y}) for player {player.player_id}")
        self.chat_system.add_message("Rover trained successfully.", (0, 255, 0))

        # Sound effect
        self.game_state.add_event({"type": "sound", "data": {"name": "spawn_unit"}})

        # Floating text
        self.game_state.add_event(
            {
                "type": "visual_effect",
                "subtype": "floating_text",
                "x": factory_pos.x,
                "y": factory_pos.y,
                "text": "+Rover",
                "color": (0, 255, 0),
            }
        )

    def _train_arachnotron_at_factory(self, factory_id):
        """Trains an arachnotron at the selected Arachnotron Factory, consuming an adjacent rover."""
        cost = 120
        player_resources = self.game_state.resources.get(self.current_player_id, 0)
        if player_resources < cost:
            self.chat_system.add_message(
                f"Insufficient scrap to train Arachnotron! Need {cost}, have {player_resources}.", (255, 0, 0)
            )
            return

        factory_pos = self.game_state.get_component(factory_id, Position)
        player = self.game_state.get_component(factory_id, Player)
        if not factory_pos or not player:
            return

        # Find an adjacent friendly rover
        from command_line_conflict.components.dead import Dead
        from command_line_conflict.components.player import Player as PlayerComponent
        from command_line_conflict.components.unit_identity import UnitIdentity

        rover_to_consume = None
        rover_x, rover_y = 0.0, 0.0

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            nx, ny = int(factory_pos.x + dx), int(factory_pos.y + dy)
            cell_entities = self.game_state.get_entities_at_position(nx, ny)
            for ceid in cell_entities:
                if ceid == factory_id:
                    continue
                ident = self.game_state.get_component(ceid, UnitIdentity)
                plyr = self.game_state.get_component(ceid, PlayerComponent)
                is_dead = self.game_state.get_component(ceid, Dead) is not None
                if ident and ident.name == "rover" and plyr and plyr.player_id == self.current_player_id and not is_dead:
                    rover_to_consume = ceid
                    rover_pos = self.game_state.get_component(ceid, Position)
                    if rover_pos:
                        rover_x, rover_y = rover_pos.x, rover_pos.y
                    break
            if rover_to_consume is not None:
                break

        if rover_to_consume is None:
            self.chat_system.add_message("Requires a friendly Rover in an adjacent tile!", (255, 0, 0))
            return

        # Spend resources
        self.game_state.resources[self.current_player_id] = player_resources - cost

        # Remove the consumed rover
        self.game_state.remove_entity(rover_to_consume)

        # Spawn Arachnotron at the consumed rover's position
        spawn_x = rover_x
        spawn_y = rover_y

        factories.create_arachnotron(
            self.game_state,
            spawn_x,
            spawn_y,
            player_id=player.player_id,
            is_human=player.is_human,
        )

        log.info(f"Trained Arachnotron at ({spawn_x}, {spawn_y}) by consuming rover {rover_to_consume}")
        self.chat_system.add_message("Arachnotron trained successfully.", (0, 255, 0))

        # Sound effect
        self.game_state.add_event({"type": "sound", "data": {"name": "spawn_unit"}})

        # Floating text
        self.game_state.add_event(
            {
                "type": "visual_effect",
                "subtype": "floating_text",
                "x": spawn_x,
                "y": spawn_y,
                "text": "+Arachnotron",
                "color": (255, 215, 0),
            }
        )

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
        self.mission_started = True
        self.chat_system.update(self.game_state, dt)

        if self.paused:
            return

        # God Mode Cheat
        if self.cheats["god_mode"]:
            for entity_id in self.game_state.get_entities_with_component(Player):
                components = self.game_state.entities.get(entity_id)
                if not components:
                    continue

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
        self.resource_system.update(self.game_state, dt)
        # NOTE: ProductionSystem still grants FREE walk-in transformations
        # (unit standing on a factory tile becomes the factory's output),
        # which bypasses the scrap prices charged by the training hotkeys.
        # See the DESIGN NOTE on ProductionSystem before rebalancing costs.
        self.production_system.update(self.game_state, dt)
        self.corpse_removal_system.update(self.game_state, dt)
        self.sound_system.update(self.game_state)

        # Process visual events
        for event in self.game_state.event_queue:
            if event.get("type") == "visual_effect":
                if event.get("subtype") == "floating_text":
                    self.ui_system.add_floating_text(event["x"], event["y"], event["text"], event["color"])

        # Clear event queue after all systems have processed events
        self.game_state.event_queue.clear()
        self.spawn_system.update(self.game_state, dt)

        # Update Fog of War
        vision_units = []
        # Optimization: Iterate only over entities with Vision component
        # This avoids iterating over non-combat entities (walls, minerals, etc.)
        for entity_id in self.game_state.get_entities_with_component(Vision):
            components = self.game_state.entities.get(entity_id)
            if not components:
                continue

            player = components.get(Player)
            if not player or not player.is_human:
                continue

            pos = components.get(Position)
            vis = components.get(Vision)
            if pos and vis:
                vision_units.append(SimpleNamespace(x=pos.x, y=pos.y, vision_range=vis.vision_range))
        self.fog_of_war.update(vision_units)

        self.win_loss_check_timer += dt
        if self.win_loss_check_timer >= 0.5:
            self.win_loss_check_timer = 0.0
            if self.check_win_condition():
                self.game.scene_manager.switch_to("victory")
            elif self.check_loss_condition():
                self.game.scene_manager.switch_to("defeat")

    def check_win_condition(self) -> bool:
        """Checks if the player has won the level.

        Returns:
            True if the win condition is met, False otherwise.
        """
        for entity_id in self.game_state.get_entities_with_component(Player):
            components = self.game_state.entities.get(entity_id)
            if not components:
                continue

            player = components.get(Player)
            if player and not player.is_human:
                if self.has_player_2_opponent and player.player_id == config.NEUTRAL_PLAYER_ID:
                    continue
                if Health in components:
                    return False

        log.info("Victory! Mission Complete.")
        self.mission_over = True
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

    def check_loss_condition(self) -> bool:
        """Checks if the player has lost the level.

        Returns:
            True if the loss condition is met, False otherwise.
        """
        for entity_id in self.game_state.get_entities_with_component(Player):
            components = self.game_state.entities.get(entity_id)
            if not components:
                continue

            player = components.get(Player)
            if player and player.is_human:
                # Check for any player-controlled entity (unit or building)
                if Health in components:
                    return False

        log.info("Defeat! Mission Failed.")
        self.mission_over = True
        self.game.steam.unlock_achievement("DEFEAT")
        self.sound_system.play_sound("defeat")
        return True

    def draw(self, screen):
        """Draws the entire game scene.

        This includes the background ocean, the map area, all entities, and the UI.

        Args:
            screen: The pygame screen surface to draw on.
        """
        # Deep dark blue background for the ocean
        screen.fill((0, 15, 35))

        grid_size = int(config.GRID_SIZE * self.camera.zoom)
        width, height = self.game.screen.get_size()

        if grid_size > 0:
            map_width = self.game_state.map.width
            map_height = self.game_state.map.height
            if not isinstance(map_width, (int, float)):
                map_width = 0
            if not isinstance(map_height, (int, float)):
                map_height = 0

            # 1. Draw solid black rectangle for the map area
            map_left = int(-self.camera.x * grid_size)
            map_top = int(-self.camera.y * grid_size)
            map_width_px = map_width * grid_size
            map_height_px = map_height * grid_size
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(map_left, map_top, map_width_px, map_height_px))

            # 2. Draw animated wave characters in the out-of-bounds area
            col_start = math.floor(self.camera.x)
            row_start = math.floor(self.camera.y)
            cols_count = math.ceil(width / grid_size) + 1
            rows_count = math.ceil(height / grid_size) + 1

            col_end = col_start + cols_count
            row_end = row_start + rows_count
            time_ms = pygame.time.get_ticks()

            for r in range(row_start, row_end):
                for c in range(col_start, col_end):
                    # Only draw outside the map boundaries
                    if 0 <= c < map_width and 0 <= r < map_height:
                        continue

                    # Animation frame changes every 400ms, offset by coordinates for movement
                    char_idx = (c + r + time_ms // 400) % 4
                    wave_surf = self._get_wave_surface(char_idx, grid_size)

                    draw_x = int((c - self.camera.x) * grid_size)
                    draw_y = int((r - self.camera.y) * grid_size)
                    screen.blit(wave_surf, (draw_x, draw_y))

            # 3. Draw grid lines *only* within the map boundaries
            map_right = map_left + map_width_px
            map_bottom = map_top + map_height_px

            # Vertical lines
            for col in range(map_width + 1):
                x = int((col - self.camera.x) * grid_size)
                if 0 <= x <= width:
                    y_start = max(0, map_top)
                    y_end = min(height, map_bottom)
                    if y_start < y_end:
                        pygame.draw.line(screen, (40, 40, 40), (x, y_start), (x, y_end))

            # Horizontal lines
            for row in range(map_height + 1):
                y = int((row - self.camera.y) * grid_size)
                if 0 <= y <= height:
                    x_start = max(0, map_left)
                    x_end = min(width, map_right)
                    if x_start < x_end:
                        pygame.draw.line(screen, (40, 40, 40), (x_start, y), (x_end, y))

        self.game_state.map.draw(screen, self.font, camera=self.camera)
        self.rendering_system.draw(self.game_state, self.paused)

        if not self.cheats["reveal_map"]:
            self.fog_of_war.draw(screen, self.camera)

        self.chat_system.draw()
        self.ui_system.draw(self.game_state, self.paused, self.current_player_id)

        if self.hovered_entity_id is not None:
            self.ui_system.draw_tooltip(self.game_state, self.hovered_entity_id, pygame.mouse.get_pos())

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

    def _get_wave_surface(self, char_idx, grid_size):
        """Pre-renders and scales wave characters to avoid runtime font overhead."""
        cache_key = (char_idx, grid_size)
        if cache_key not in self._wave_cache:
            char = ["~", " ", "-", "."][char_idx]
            surf = self.font.render(char, True, (0, 100, 180))
            try:
                surf = pygame.transform.scale(surf, (grid_size, grid_size))
            except TypeError:
                # If surf is a mock object (e.g. in tests), keep the mock as is
                pass
            self._wave_cache[cache_key] = surf
        return self._wave_cache[cache_key]
