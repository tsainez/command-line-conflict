import pytest
from unittest.mock import MagicMock, patch, ANY
import pygame

from command_line_conflict import config
from command_line_conflict.scenes.game import GameScene
from command_line_conflict.components.player import Player
from command_line_conflict.components.health import Health
from command_line_conflict.components.position import Position
from command_line_conflict.components.vision import Vision
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.components.unit_identity import UnitIdentity
from command_line_conflict.components.attack import Attack

@pytest.fixture
def mock_game():
    game = MagicMock()
    game.screen = MagicMock()
    game.screen.get_size.return_value = (800, 600)
    game.font = MagicMock()
    game.music_manager = MagicMock()
    game.scene_manager = MagicMock()
    game.steam = MagicMock()
    return game

@pytest.fixture
def game_scene(mock_game):
    with patch('command_line_conflict.scenes.game.GameState') as MockGameState, \
         patch('command_line_conflict.scenes.game.FogOfWar') as MockFogOfWar, \
         patch('command_line_conflict.scenes.game.Camera') as MockCamera, \
         patch('command_line_conflict.scenes.game.CampaignManager') as MockCampaignManager, \
         patch('command_line_conflict.scenes.game.MovementSystem') as MockMovementSystem, \
         patch('command_line_conflict.scenes.game.RenderingSystem') as MockRenderingSystem, \
         patch('command_line_conflict.scenes.game.CombatSystem') as MockCombatSystem, \
         patch('command_line_conflict.scenes.game.FleeSystem') as MockFleeSystem, \
         patch('command_line_conflict.scenes.game.HealthSystem') as MockHealthSystem, \
         patch('command_line_conflict.scenes.game.SelectionSystem') as MockSelectionSystem, \
         patch('command_line_conflict.scenes.game.UISystem') as MockUISystem, \
         patch('command_line_conflict.scenes.game.ChatSystem') as MockChatSystem, \
         patch('command_line_conflict.scenes.game.CorpseRemovalSystem') as MockCorpseRemovalSystem, \
         patch('command_line_conflict.scenes.game.AISystem') as MockAISystem, \
         patch('command_line_conflict.scenes.game.ConfettiSystem') as MockConfettiSystem, \
         patch('command_line_conflict.scenes.game.ProductionSystem') as MockProductionSystem, \
         patch('command_line_conflict.scenes.game.SoundSystem') as MockSoundSystem, \
         patch('command_line_conflict.scenes.game.WanderSystem') as MockWanderSystem, \
         patch('command_line_conflict.scenes.game.SpawnSystem') as MockSpawnSystem:

        # Setup GameState behavior
        mock_game_state_instance = MockGameState.return_value
        mock_game_state_instance.map = MagicMock()
        mock_game_state_instance.map.width = 100
        mock_game_state_instance.map.height = 100
        mock_game_state_instance.entities = {}
        mock_game_state_instance.event_queue = []

        # Mock get_entities_with_component to use the entities dict
        def get_entities_with_component_side_effect(component_type):
            result = set()
            for entity_id, components in mock_game_state_instance.entities.items():
                if component_type in components:
                    result.add(entity_id)
            return result
        mock_game_state_instance.get_entities_with_component.side_effect = get_entities_with_component_side_effect

        scene = GameScene(mock_game)

        # Attach mocked systems to the scene instance for assertion convenience
        scene.mock_game_state = mock_game_state_instance
        scene.mock_campaign_manager = MockCampaignManager.return_value
        scene.mock_ui_system = MockUISystem.return_value
        scene.mock_selection_system = MockSelectionSystem.return_value
        scene.mock_movement_system = MockMovementSystem.return_value
        scene.mock_chat_system = MockChatSystem.return_value
        scene.mock_sound_system = MockSoundSystem.return_value
        scene.mock_fog_of_war = MockFogOfWar.return_value
        scene.mock_combat_system = MockCombatSystem.return_value
        scene.mock_health_system = MockHealthSystem.return_value
        scene.mock_flee_system = MockFleeSystem.return_value
        scene.mock_ai_system = MockAISystem.return_value
        scene.mock_wander_system = MockWanderSystem.return_value
        scene.mock_confetti_system = MockConfettiSystem.return_value
        scene.mock_production_system = MockProductionSystem.return_value
        scene.mock_corpse_removal_system = MockCorpseRemovalSystem.return_value
        scene.mock_spawn_system = MockSpawnSystem.return_value
        scene.rendering_system = MockRenderingSystem.return_value # GameScene stores it in self.rendering_system

        return scene

class TestGameSceneInit:
    def test_init_initializes_systems(self, game_scene):
        assert game_scene.game_state is not None
        assert game_scene.fog_of_war is not None
        assert game_scene.camera is not None
        assert game_scene.campaign_manager is not None
        assert game_scene.movement_system is not None
        assert game_scene.rendering_system is not None
        assert game_scene.combat_system is not None
        assert game_scene.flee_system is not None
        assert game_scene.health_system is not None
        assert game_scene.selection_system is not None
        assert game_scene.ui_system is not None
        assert game_scene.chat_system is not None
        assert game_scene.corpse_removal_system is not None
        assert game_scene.ai_system is not None
        assert game_scene.confetti_system is not None
        assert game_scene.production_system is not None
        assert game_scene.sound_system is not None
        assert game_scene.wander_system is not None
        assert game_scene.spawn_system is not None

    def test_init_plays_music(self, game_scene, mock_game):
        mock_game.music_manager.play.assert_called_with("music/game_theme.ogg")

    def test_init_creates_initial_units_fallback(self, mock_game):
         with patch('command_line_conflict.scenes.game.GameState') as MockGameState, \
              patch('command_line_conflict.scenes.game.factories') as mock_factories, \
              patch('command_line_conflict.scenes.game.FactoryBattleMap') as MockMap, \
              patch('command_line_conflict.scenes.game.FogOfWar'), \
              patch('command_line_conflict.scenes.game.Camera'), \
              patch('command_line_conflict.scenes.game.CampaignManager'), \
              patch('command_line_conflict.scenes.game.MovementSystem'), \
              patch('command_line_conflict.scenes.game.RenderingSystem'), \
              patch('command_line_conflict.scenes.game.CombatSystem'), \
              patch('command_line_conflict.scenes.game.FleeSystem'), \
              patch('command_line_conflict.scenes.game.HealthSystem'), \
              patch('command_line_conflict.scenes.game.SelectionSystem'), \
              patch('command_line_conflict.scenes.game.UISystem'), \
              patch('command_line_conflict.scenes.game.ChatSystem'), \
              patch('command_line_conflict.scenes.game.CorpseRemovalSystem'), \
              patch('command_line_conflict.scenes.game.AISystem'), \
              patch('command_line_conflict.scenes.game.ConfettiSystem'), \
              patch('command_line_conflict.scenes.game.ProductionSystem'), \
              patch('command_line_conflict.scenes.game.SoundSystem'), \
              patch('command_line_conflict.scenes.game.WanderSystem'), \
              patch('command_line_conflict.scenes.game.SpawnSystem'):

            mock_game_state_instance = MockGameState.return_value
            # Ensure map does NOT have create_initial_units
            mock_map_instance = MockMap.return_value
            del mock_map_instance.create_initial_units
            mock_game_state_instance.map = mock_map_instance
            mock_game_state_instance.map.width = 100
            mock_game_state_instance.map.height = 100

            GameScene(mock_game)

            # Check if fallback factories were called
            # 3 chassis for player 1
            assert mock_factories.create_chassis.call_count == 3
            # 1 rover for player 2
            mock_factories.create_rover.assert_called_once()

class TestGameSceneHandleEvent:
    def test_handle_event_chat_system_consumes_event(self, game_scene):
        event = MagicMock()
        game_scene.mock_chat_system.handle_event.return_value = True

        game_scene.handle_event(event)

        # Verify no other processing happened (e.g. selection system not called)
        game_scene.mock_selection_system.handle_click_selection.assert_not_called()

    def test_handle_event_click_selection(self, game_scene):
        game_scene.mock_chat_system.handle_event.return_value = False
        game_scene.camera.screen_to_grid.return_value = (10, 10)

        # Mouse down
        event_down = MagicMock()
        event_down.type = pygame.MOUSEBUTTONDOWN
        event_down.button = 1
        event_down.pos = (100, 100)
        game_scene.handle_event(event_down)

        assert game_scene.selection_start == (100, 100)

        # Mouse up (click)
        event_up = MagicMock()
        event_up.type = pygame.MOUSEBUTTONUP
        event_up.button = 1
        event_up.pos = (102, 102) # Moved slightly

        with patch('pygame.key.get_mods', return_value=0):
            game_scene.handle_event(event_up)

        game_scene.mock_selection_system.handle_click_selection.assert_called_once_with(
            game_scene.game_state, (10, 10), 0, game_scene.current_player_id
        )
        assert game_scene.selection_start is None

    def test_handle_event_drag_selection(self, game_scene):
        game_scene.mock_chat_system.handle_event.return_value = False
        game_scene.camera.screen_to_grid.side_effect = [(5, 5), (10, 10)]

        # Mouse down
        event_down = MagicMock()
        event_down.type = pygame.MOUSEBUTTONDOWN
        event_down.button = 1
        event_down.pos = (50, 50)
        game_scene.handle_event(event_down)

        # Mouse up (drag)
        event_up = MagicMock()
        event_up.type = pygame.MOUSEBUTTONUP
        event_up.button = 1
        event_up.pos = (200, 200) # Moved significantly

        with patch('pygame.key.get_mods', return_value=0):
            game_scene.handle_event(event_up)

        game_scene.mock_selection_system.update.assert_called_once_with(
            game_scene.game_state, (5, 5), (10, 10), 0, game_scene.current_player_id
        )

    def test_handle_event_right_click_move(self, game_scene):
        game_scene.mock_chat_system.handle_event.return_value = False
        game_scene.camera.screen_to_grid.return_value = (15, 20)

        # Setup selected entity
        entity_id = 1
        components = {
            Selectable: MagicMock(is_selected=True),
            # Need to mock Attack to test attack target clearing
            Attack: MagicMock(attack_target=123)
        }

        # Mock get_component behavior or entities dict
        # The code iterates game_state.entities.items()
        game_scene.game_state.entities = {entity_id: components}

        # Mock component retrieval
        def get_component(ent_id, comp_type):
            return components.get(comp_type)
        game_scene.game_state.get_component.side_effect = get_component

        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 3
        event.pos = (300, 400)

        game_scene.handle_event(event)

        game_scene.mock_ui_system.add_click_effect.assert_called_with(15, 20, (0, 255, 0))
        game_scene.mock_movement_system.set_target.assert_called_with(
            game_scene.game_state, entity_id, 15, 20
        )
        assert components[Attack].attack_target is None

    def test_handle_event_camera_keys(self, game_scene):
        game_scene.mock_chat_system.handle_event.return_value = False

        keys = {
            pygame.K_UP: "up",
            pygame.K_DOWN: "down",
            pygame.K_LEFT: "left",
            pygame.K_RIGHT: "right"
        }

        for key, direction in keys.items():
            # Key down
            event_down = MagicMock()
            event_down.type = pygame.KEYDOWN
            event_down.key = key
            game_scene.handle_event(event_down)
            assert game_scene.camera_movement[direction] is True

            # Key up
            event_up = MagicMock()
            event_up.type = pygame.KEYUP
            event_up.key = key
            game_scene.handle_event(event_up)
            assert game_scene.camera_movement[direction] is False

    def test_handle_event_cheats(self, game_scene):
        game_scene.mock_chat_system.handle_event.return_value = False
        config.DEBUG = True

        # F1 Reveal Map
        event_f1 = MagicMock()
        event_f1.type = pygame.KEYDOWN
        event_f1.key = pygame.K_F1
        with patch('pygame.key.get_mods', return_value=0):
            game_scene.handle_event(event_f1)
        assert game_scene.cheats["reveal_map"] is True

        # F2 God Mode
        event_f2 = MagicMock()
        event_f2.type = pygame.KEYDOWN
        event_f2.key = pygame.K_F2
        with patch('pygame.key.get_mods', return_value=0):
            game_scene.handle_event(event_f2)
        assert game_scene.cheats["god_mode"] is True

class TestGameSceneUpdate:
    def test_update_paused(self, game_scene):
        game_scene.paused = True
        game_scene.update(0.1)

        # Systems should not update when paused
        game_scene.mock_movement_system.update.assert_not_called()
        game_scene.mock_combat_system.update.assert_not_called()

        # Chat system ALWAYS updates
        game_scene.mock_chat_system.update.assert_called_once()

    def test_update_running(self, game_scene):
        game_scene.paused = False
        dt = 0.1

        game_scene.update(dt)

        game_scene.mock_chat_system.update.assert_called_with(game_scene.game_state, dt)
        game_scene.mock_health_system.update.assert_called_with(game_scene.game_state, dt)
        game_scene.mock_flee_system.update.assert_called_with(game_scene.game_state, dt)
        game_scene.mock_ai_system.update.assert_called_with(game_scene.game_state)
        game_scene.mock_wander_system.update.assert_called_with(game_scene.game_state, dt)
        game_scene.mock_combat_system.update.assert_called_with(game_scene.game_state, dt)
        game_scene.mock_confetti_system.update.assert_called_with(game_scene.game_state, dt)
        game_scene.mock_movement_system.update.assert_called_with(game_scene.game_state, dt)
        game_scene.mock_production_system.update.assert_called_with(game_scene.game_state, dt)
        game_scene.mock_corpse_removal_system.update.assert_called_with(game_scene.game_state, dt)
        game_scene.mock_sound_system.update.assert_called_with(game_scene.game_state)
        game_scene.mock_spawn_system.update.assert_called_with(game_scene.game_state, dt)

    def test_update_win_condition(self, game_scene, mock_game):
        # Setup no enemies
        game_scene.game_state.entities = {
            1: {Player: MagicMock(player_id=1, is_human=True), Health: MagicMock()}
        }

        game_scene.update(0.1)

        mock_game.scene_manager.switch_to.assert_called_with("victory")
        mock_game.steam.unlock_achievement.assert_called_with("VICTORY")
        game_scene.mock_campaign_manager.complete_mission.assert_called_with(game_scene.current_mission_id)

    def test_update_loss_condition(self, game_scene, mock_game):
        # Setup no player units
        game_scene.game_state.entities = {
            2: {Player: MagicMock(player_id=2, is_human=False), Health: MagicMock()}
        }

        game_scene.update(0.1)

        mock_game.scene_manager.switch_to.assert_called_with("defeat")
        mock_game.steam.unlock_achievement.assert_called_with("DEFEAT")

    def test_update_fog_of_war(self, game_scene):
        # Setup units with vision
        game_scene.game_state.entities = {
            1: {
                Position: MagicMock(x=10, y=10),
                Vision: MagicMock(vision_range=5),
                Player: MagicMock(is_human=True)
            },
            2: {
                Position: MagicMock(x=20, y=20),
                Vision: MagicMock(vision_range=3),
                Player: MagicMock(is_human=False) # Should be ignored
            }
        }

        game_scene.update(0.1)

        # Verify fog of war updated with only human units
        assert game_scene.mock_fog_of_war.update.call_count == 1
        call_args = game_scene.mock_fog_of_war.update.call_args[0][0]
        assert len(call_args) == 1
        assert call_args[0].x == 10
        assert call_args[0].y == 10
        assert call_args[0].vision_range == 5

class TestGameSceneDraw:
    def test_draw(self, game_scene):
        screen = MagicMock()
        game_scene.draw(screen)

        game_scene.game_state.map.draw.assert_called()
        game_scene.rendering_system.draw.assert_called()
        game_scene.mock_fog_of_war.draw.assert_called()
        game_scene.chat_system.draw.assert_called()
        game_scene.ui_system.draw.assert_called()
