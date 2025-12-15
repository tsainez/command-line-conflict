
import unittest
from unittest.mock import MagicMock, patch
import pygame
from command_line_conflict.scenes.game import GameScene
from command_line_conflict import config

class TestGameSceneCamera(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock()
        self.mock_game.font = MagicMock()
        self.mock_game.screen = MagicMock()
        self.mock_game.music_manager = MagicMock()

        # Mock InputManager
        self.mock_game.input_manager = MagicMock()
        self.mock_game.input_manager.get_key.side_effect = lambda action: {
            "camera_up": pygame.K_UP,
            "camera_down": pygame.K_DOWN,
            "camera_left": pygame.K_LEFT,
            "camera_right": pygame.K_RIGHT,
            "build_rover_factory": pygame.K_r,
            "build_arachnotron_factory": pygame.K_a,
            "hold_position": pygame.K_h,
            "pause": pygame.K_p,
            "toggle_reveal_map": pygame.K_F1,
            "toggle_god_mode": pygame.K_F2,
            "switch_player": pygame.K_TAB,
            "menu": pygame.K_ESCAPE,
        }.get(action, 0)

        # Patch factories to avoid actual game state complexity
        with patch('command_line_conflict.scenes.game.factories') as mock_factories:
            with patch('command_line_conflict.scenes.game.SimpleMap'):
                with patch('command_line_conflict.scenes.game.FogOfWar'):
                    with patch('command_line_conflict.scenes.game.RenderingSystem'):
                         with patch('command_line_conflict.scenes.game.UISystem'):
                            with patch('command_line_conflict.scenes.game.ChatSystem') as mock_chat:
                                self.scene = GameScene(self.mock_game)
                                self.scene.chat_system.handle_event.return_value = False

    def test_wasd_does_not_control_camera(self):
        # W key (Up) should NOT work
        event_w_down = MagicMock(type=pygame.KEYDOWN, key=pygame.K_w)
        self.scene.handle_event(event_w_down)
        self.assertFalse(self.scene.camera_movement["up"], "W should NOT trigger camera up")

        # A key (Left) should NOT work
        event_a_down = MagicMock(type=pygame.KEYDOWN, key=pygame.K_a)
        self.scene.handle_event(event_a_down)
        self.assertFalse(self.scene.camera_movement["left"], "A should NOT trigger camera left")

    def test_arrow_keys_control_camera(self):
        # UP key
        event_up_down = MagicMock(type=pygame.KEYDOWN, key=pygame.K_UP)
        self.scene.handle_event(event_up_down)
        self.assertTrue(self.scene.camera_movement["up"], "Arrow UP should trigger camera up")

        event_up_up = MagicMock(type=pygame.KEYUP, key=pygame.K_UP)
        self.scene.handle_event(event_up_up)
        self.assertFalse(self.scene.camera_movement["up"])

    def test_middle_mouse_drag(self):
        # Initial camera position
        initial_x = self.scene.camera.x
        initial_y = self.scene.camera.y

        # 1. Mouse Button Down (Middle Button = 2)
        start_pos = (100, 100)
        event_down = MagicMock(type=pygame.MOUSEBUTTONDOWN, button=2, pos=start_pos)
        self.scene.handle_event(event_down)

        # Verify drag started (we need to inspect internal state or behavior)
        # Assuming internal state `self.drag_start` or similar is set.
        # But we can only verify behavior via updates or subsequent events.
        # Let's verify that a subsequent MOUSEMOTION moves the camera.

        # 2. Mouse Motion while dragging
        end_pos = (150, 120) # Moved right 50, down 20
        # When dragging camera, moving mouse right usually moves camera left (drag the world) OR moves camera right (push the edge).
        # Standard RTS drag: Click and drag the map. If I pull mouse right, map moves right, so camera moves left.
        # Delta: +50x, +20y.
        # Camera move: -50x, -20y (converted to grid coordinates).

        # Note: Pygame MOUSEMOTION has `rel` (relative movement).
        event_motion = MagicMock(type=pygame.MOUSEMOTION, pos=end_pos, rel=(50, 20), buttons=(0, 1, 0)) # Middle button pressed?
        # Actually `buttons` tuple is (left, middle, right) usually. Wait, button 2 is middle.

        self.scene.handle_event(event_motion)

        # Check if camera moved.
        # We need to know the scale. `screen_to_grid` uses zoom.
        # If I drag 50 pixels right, the camera x should decrease by (50 / GRID_SIZE / ZOOM).
        # Assuming we implement "drag map" style.

        self.assertNotEqual(self.scene.camera.x, initial_x, "Camera X should have changed after drag")
        self.assertNotEqual(self.scene.camera.y, initial_y, "Camera Y should have changed after drag")

        # 3. Mouse Button Up (Middle Button = 2)
        event_up = MagicMock(type=pygame.MOUSEBUTTONUP, button=2, pos=end_pos)
        self.scene.handle_event(event_up)

        # 4. Mouse Motion AFTER release
        current_x = self.scene.camera.x
        event_motion_after = MagicMock(type=pygame.MOUSEMOTION, pos=(200, 200), rel=(50, 80), buttons=(0, 0, 0))
        self.scene.handle_event(event_motion_after)

        self.assertEqual(self.scene.camera.x, current_x, "Camera should not move after drag release")
