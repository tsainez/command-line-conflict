import pytest
from unittest.mock import MagicMock, patch
from command_line_conflict.systems.ui_system import UISystem
from command_line_conflict.systems.combat_system import CombatSystem
from command_line_conflict.components.health import Health
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.position import Position
from command_line_conflict.components.movable import Movable
from command_line_conflict.components.unit_identity import UnitIdentity
from command_line_conflict import config

class TestFloatingText:
    @pytest.fixture
    def mock_camera(self):
        camera = MagicMock()
        camera.x = 0
        camera.y = 0
        camera.zoom = 1.0
        return camera

    @pytest.fixture
    def ui_system(self, mock_camera):
        screen = MagicMock()
        font = MagicMock()
        return UISystem(screen, font, mock_camera)

    def test_add_floating_text(self, ui_system):
        with patch("pygame.time.get_ticks", return_value=1000):
            ui_system.add_floating_text(10, 20, "15", (255, 0, 0))

        assert len(ui_system.floating_texts) == 1
        item = ui_system.floating_texts[0]
        assert item["x"] == 10
        assert item["y"] == 20
        assert item["text"] == "15"
        assert item["color"] == (255, 0, 0)
        assert item["start_time"] == 1000
        assert item["duration"] == 1000

    def test_draw_floating_texts_renders_and_expires(self, ui_system):
        # Setup: Add one active text and one that will expire
        with patch("pygame.time.get_ticks", return_value=1000):
            ui_system.add_floating_text(10, 10, "Active", (255, 255, 255))
            ui_system.add_floating_text(20, 20, "Expired", (255, 255, 255))

            # Manually expire the second one by setting start_time to 0
            # Current time will be 1500, so elapsed 1500 > 1000
            ui_system.floating_texts[1]["start_time"] = 0

        # Run draw with time = 1500 (500ms elapsed since add for "Active")
        with patch("pygame.time.get_ticks", return_value=1500):
            ui_system._draw_floating_texts()

        assert len(ui_system.floating_texts) == 1
        assert ui_system.floating_texts[0]["text"] == "Active"

        # Verify blit was called for the active one
        ui_system.screen.blit.assert_called()

    def test_combat_system_emits_visual_event(self, game_state):
        combat_system = CombatSystem()

        # Create attacker
        attacker = game_state.create_entity()
        game_state.add_component(attacker, Position(10, 10))
        game_state.add_component(attacker, Attack(attack_damage=10, attack_range=2, attack_speed=1))
        game_state.add_component(attacker, Movable(speed=1))
        game_state.add_component(attacker, UnitIdentity(name="Attacker"))

        # Create target
        target = game_state.create_entity()
        game_state.add_component(target, Position(11, 10)) # Distance 1
        game_state.add_component(target, Health(hp=100, max_hp=100))
        game_state.add_component(target, UnitIdentity(name="Target"))

        # Set target
        attack_comp = game_state.get_component(attacker, Attack)
        attack_comp.attack_target = target

        # Update combat system
        combat_system.update(game_state, 1.0)

        # Check event queue
        visual_events = [e for e in game_state.event_queue if e.get("type") == "visual_effect"]
        assert len(visual_events) == 1
        event = visual_events[0]
        assert event["subtype"] == "floating_text"
        assert event["text"] == "10"
        assert event["x"] == 11
        assert event["y"] == 10
        assert event["color"] == (255, 50, 50)
