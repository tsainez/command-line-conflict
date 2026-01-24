from unittest.mock import MagicMock, patch
import pytest
import pygame

from command_line_conflict.components.attack import Attack
from command_line_conflict.components.health import Health
from command_line_conflict.components.position import Position
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.base import Map
from command_line_conflict.systems.combat_system import CombatSystem
from command_line_conflict.systems.ui_system import UISystem
from command_line_conflict.camera import Camera

class TestCombatFeedback:
    @pytest.fixture
    def game_state(self):
        game_map = MagicMock(spec=Map)
        return GameState(game_map)

    @pytest.fixture
    def ui_system(self):
        pygame.init()
        screen = MagicMock()
        font = MagicMock()
        camera = Camera()
        return UISystem(screen, font, camera)

    def test_combat_system_emits_floating_text_event(self, game_state):
        combat_system = CombatSystem()

        # Setup attacker and target
        attacker_id = game_state.create_entity()
        game_state.add_component(attacker_id, Position(0, 0))
        game_state.add_component(attacker_id, Attack(attack_damage=10, attack_range=5, attack_speed=1.0))

        target_id = game_state.create_entity()
        game_state.add_component(target_id, Position(3, 3))
        game_state.add_component(target_id, Health(hp=100, max_hp=100))

        game_state.entities[attacker_id][Attack].attack_target = target_id

        # Act
        combat_system.update(game_state, dt=1.0)

        # Assert
        events = list(game_state.event_queue)
        floating_text_events = [
            e for e in events
            if e.get("type") == "visual_effect" and e.get("subtype") == "floating_text"
        ]

        assert len(floating_text_events) == 1
        event_data = floating_text_events[0]["data"]
        assert event_data["text"] == "10"
        assert event_data["x"] == 3
        assert event_data["y"] == 3
        assert event_data["color"] == (255, 0, 0)

    def test_ui_system_consumes_floating_text_event(self, game_state, ui_system):
        # Setup event
        event = {
            "type": "visual_effect",
            "subtype": "floating_text",
            "data": {
                "text": "15",
                "x": 10,
                "y": 20,
                "color": (255, 0, 0)
            }
        }
        game_state.add_event(event)

        # Act
        ui_system.update(game_state)

        # Assert
        assert len(ui_system.floating_texts) == 1
        text_data = ui_system.floating_texts[0]
        assert text_data["text"] == "15"
        assert text_data["x"] == 10
        assert text_data["y"] == 20
        assert text_data["color"] == (255, 0, 0)
        assert text_data["duration"] == 1000

    def test_ui_system_draws_floating_text(self, game_state, ui_system):
        # Setup floating text
        ui_system.floating_texts.append({
            "text": "100",
            "x": 5,
            "y": 5,
            "color": (255, 0, 0),
            "time": pygame.time.get_ticks(),
            "duration": 1000
        })

        # We mock the font render to ensure it returns a surface we can check calls on,
        # or just ensure no crash.
        # Since we passed a mock font to UISystem, default self.font is mock.
        # But _get_text_surface might use self.small_font which is created internally.

        # Act
        # We need to ensure _get_text_surface works.
        # UISystem.__init__ creates fonts. If pygame is headless, this might fail unless mocked.
        # But fixture called pygame.init().

        ui_system.draw(game_state, paused=False)

        # Assert
        # Verify blit was called.
        # Floating text drawing calls screen.blit
        assert ui_system.screen.blit.called
