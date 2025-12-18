import json
import os
import unittest
from unittest.mock import MagicMock, patch

from command_line_conflict.campaign_manager import MISSION_REWARDS, CampaignManager
from command_line_conflict.components.factory import Factory
from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
from command_line_conflict.components.unit_identity import UnitIdentity
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.simple_map import SimpleMap
from command_line_conflict.systems.production_system import ProductionSystem

# Mock factories to avoid importing pygame logic during tests if possible,
# or just ensure mock_pygame is active.
# Since we import factories in production_system, we should be careful.
# But existing tests use factories, so it should be fine with the conftest.


class TestCampaignManager(unittest.TestCase):
    def setUp(self):
        self.save_file = "test_save_game.json"
        if os.path.exists(self.save_file):
            os.remove(self.save_file)
        self.manager = CampaignManager(self.save_file)

    def tearDown(self):
        if os.path.exists(self.save_file):
            os.remove(self.save_file)

    def test_initial_state(self):
        self.assertIn("chassis", self.manager.unlocked_units)
        # Assuming rover requires 1 mission, it should not be unlocked yet
        self.assertNotIn("rover", self.manager.unlocked_units)

    def test_unlock_progression(self):
        # Rover needs mission_1
        self.manager.complete_mission("mission_1")
        self.assertIn("rover", self.manager.unlocked_units)
        self.assertNotIn("arachnotron", self.manager.unlocked_units)

        # Arachnotron needs mission_2
        self.manager.complete_mission("mission_2")
        self.assertIn("arachnotron", self.manager.unlocked_units)

    def test_persistence(self):
        self.manager.complete_mission("mission_1")
        self.manager.save_progress()

        new_manager = CampaignManager(self.save_file)
        self.assertIn("mission_1", new_manager.completed_missions)
        self.assertIn("rover", new_manager.unlocked_units)


class TestProductionSystem(unittest.TestCase):
    def setUp(self):
        self.map = SimpleMap()
        self.game_state = GameState(self.map)
        self.campaign_manager = MagicMock()
        self.system = ProductionSystem(self.campaign_manager)

    def test_production_unlocked(self):
        # Setup: Unlocked rover
        self.campaign_manager.is_unit_unlocked.return_value = True

        # Create Factory: Input Chassis -> Output Rover
        factory_id = self.game_state.create_entity()
        self.game_state.add_component(factory_id, Position(10, 10))
        self.game_state.add_component(factory_id, Factory("chassis", "rover"))
        self.game_state.add_component(factory_id, Player(1, True))

        # Create Unit: Chassis at same location
        unit_id = self.game_state.create_entity()
        self.game_state.add_component(unit_id, Position(10, 10))
        self.game_state.add_component(unit_id, UnitIdentity("chassis"))
        self.game_state.add_component(unit_id, Player(1, True))

        # Run Update
        with patch.dict(
            "command_line_conflict.factories.UNIT_NAME_TO_FACTORY",
            {"rover": MagicMock()},
        ) as mock_dict:
            mock_create_rover = mock_dict["rover"]
            self.system.update(self.game_state, 0.1)

            # Check unit removed
            self.assertNotIn(unit_id, self.game_state.entities)

            # Check factory remains
            self.assertIn(factory_id, self.game_state.entities)

            # Check new unit created
            mock_create_rover.assert_called_once()
            # args: game_state, x, y, player_id, is_human
            args, _ = mock_create_rover.call_args
            self.assertEqual(args[1], 10)
            self.assertEqual(args[2], 10)

    def test_production_locked(self):
        # Setup: Locked rover
        self.campaign_manager.is_unit_unlocked.return_value = False

        # Create Factory
        factory_id = self.game_state.create_entity()
        self.game_state.add_component(factory_id, Position(10, 10))
        self.game_state.add_component(factory_id, Factory("chassis", "rover"))
        self.game_state.add_component(factory_id, Player(1, True))

        # Create Unit
        unit_id = self.game_state.create_entity()
        self.game_state.add_component(unit_id, Position(10, 10))
        self.game_state.add_component(unit_id, UnitIdentity("chassis"))
        self.game_state.add_component(unit_id, Player(1, True))

        # Run Update
        with patch("command_line_conflict.factories.create_rover") as mock_create_rover:
            self.system.update(self.game_state, 0.1)

            # Check unit NOT removed
            self.assertIn(unit_id, self.game_state.entities)

            # Check new unit NOT created
            mock_create_rover.assert_not_called()

    def test_wrong_input_type(self):
        self.campaign_manager.is_unit_unlocked.return_value = True

        # Factory expects Chassis
        factory_id = self.game_state.create_entity()
        self.game_state.add_component(factory_id, Position(10, 10))
        self.game_state.add_component(factory_id, Factory("chassis", "rover"))
        self.game_state.add_component(factory_id, Player(1, True))

        # Unit is Rover (can't process rover in rover factory usually, or just wrong input)
        unit_id = self.game_state.create_entity()
        self.game_state.add_component(unit_id, Position(10, 10))
        self.game_state.add_component(unit_id, UnitIdentity("rover"))
        self.game_state.add_component(unit_id, Player(1, True))

        self.system.update(self.game_state, 0.1)
        self.assertIn(unit_id, self.game_state.entities)

    def test_player_ownership_mismatch(self):
        self.campaign_manager.is_unit_unlocked.return_value = True

        # Factory owned by Player 1
        factory_id = self.game_state.create_entity()
        self.game_state.add_component(factory_id, Position(10, 10))
        self.game_state.add_component(factory_id, Factory("chassis", "rover"))
        self.game_state.add_component(factory_id, Player(1, True))

        # Unit owned by Player 2
        unit_id = self.game_state.create_entity()
        self.game_state.add_component(unit_id, Position(10, 10))
        self.game_state.add_component(unit_id, UnitIdentity("chassis"))
        self.game_state.add_component(unit_id, Player(2, False))

        self.system.update(self.game_state, 0.1)
        self.assertIn(unit_id, self.game_state.entities)
