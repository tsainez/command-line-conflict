import logging
from unittest.mock import MagicMock

import pytest

from command_line_conflict.camera import Camera
from command_line_conflict.components.health import Health
from command_line_conflict.components.position import Position
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.systems.ui_system import UISystem


class TestUILogging:

    @pytest.fixture
    def ui_system(self):
        screen = MagicMock()
        font = MagicMock()
        camera = Camera()
        return UISystem(screen, font, camera)

    def test_initialization_log(self, caplog):
        """Test that UISystem logs initialization."""
        caplog.set_level(logging.DEBUG, logger="Command Line Conflict")

        screen = MagicMock()
        font = MagicMock()
        camera = Camera()

        UISystem(screen, font, camera)

        assert "UISystem initialized" in caplog.text

    def test_selection_change_log(self, ui_system, game_state, caplog):
        """Test that UISystem logs when selection changes."""
        caplog.set_level(logging.DEBUG, logger="Command Line Conflict")

        # Initial draw - no selection
        ui_system.draw(game_state, paused=False)
        assert "UI: Selection changed. Count: 0" in caplog.text

        caplog.clear()

        # Add a selected entity
        entity_id = game_state.create_entity()
        selectable = Selectable()
        selectable.is_selected = True
        game_state.add_component(entity_id, selectable)
        game_state.add_component(entity_id, Position(10, 10))
        game_state.add_component(entity_id, Health(100, 100))

        ui_system.draw(game_state, paused=False)
        assert "UI: Selection changed. Count: 1" in caplog.text

        caplog.clear()

        # Draw again - no change
        ui_system.draw(game_state, paused=False)
        assert "UI: Selection changed" not in caplog.text

        # Deselect
        game_state.get_component(entity_id, Selectable).is_selected = False
        ui_system.draw(game_state, paused=False)
        assert "UI: Selection changed. Count: 0" in caplog.text

    def test_cheat_change_log(self, ui_system, game_state, caplog):
        """Test that UISystem logs when active cheats change."""
        caplog.set_level(logging.DEBUG, logger="Command Line Conflict")

        # Inject cheats dict
        cheats = {"reveal_map": False, "god_mode": False}
        ui_system.cheats = cheats

        # Initial draw
        ui_system.draw(game_state, paused=False)
        # Should log count 0
        assert "UI: Active cheats count changed to 0" in caplog.text

        caplog.clear()

        # Enable a cheat
        cheats["reveal_map"] = True
        ui_system.draw(game_state, paused=False)
        assert "UI: Active cheats count changed to 1" in caplog.text

        caplog.clear()

        # Draw again - no change
        ui_system.draw(game_state, paused=False)
        assert "UI: Active cheats count changed" not in caplog.text

        # Disable cheat
        cheats["reveal_map"] = False
        ui_system.draw(game_state, paused=False)
        assert "UI: Active cheats count changed to 0" in caplog.text
