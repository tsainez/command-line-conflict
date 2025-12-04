import random
import unittest
from unittest.mock import MagicMock

from command_line_conflict.maps.base import TERRAIN_HIGH_GROUND, TERRAIN_NORMAL, TERRAIN_ROUGH
from command_line_conflict.game_state import GameState
from command_line_conflict.components.movable import Movable
from command_line_conflict.components.position import Position
from command_line_conflict.components.attack import Attack
from command_line_conflict.components.health import Health
from command_line_conflict.systems.movement_system import MovementSystem
from command_line_conflict.systems.combat_system import CombatSystem

class TestTerrainMechanics(unittest.TestCase):
    def setUp(self):
        self.mock_map = MagicMock()
        self.game_state = GameState(game_map=self.mock_map)
        self.game_state.map.get_terrain.return_value = TERRAIN_NORMAL
        self.game_state.map.find_path.side_effect = lambda start, end, can_fly=False, extra_obstacles=None: [end]

    def test_movement_slow_on_rough_terrain(self):
        """Test that units move slower on rough terrain."""
        system = MovementSystem()

        # Create an entity
        entity_id = self.game_state.create_entity()
        movable = Movable(speed=10)
        position = Position(0, 0)
        self.game_state.add_component(entity_id, movable)
        self.game_state.add_component(entity_id, position)

        # Set target
        movable.target_x = 10
        movable.target_y = 0
        movable.path = [(10, 0)]

        # Case 1: Normal Terrain
        self.game_state.map.get_terrain.return_value = TERRAIN_NORMAL
        system.update(self.game_state, dt=1.0)
        # Expected position change: speed * dt = 10 * 1 = 10
        # Actually logic is: step = min(dist, speed*dt)
        # dist is 10. step is 10. new pos should be 10.
        # Wait, I need to make sure I step less than full distance to measure speed.

        # Reset
        position.x = 0
        position.y = 0
        movable.target_x = 100 # Far away
        movable.path = [(100, 0)]

        system.update(self.game_state, dt=1.0)
        self.assertAlmostEqual(position.x, 10.0)

        # Case 2: Rough Terrain
        position.x = 0
        position.y = 0
        self.game_state.map.get_terrain.return_value = TERRAIN_ROUGH

        system.update(self.game_state, dt=1.0)
        # Expected: speed * 0.75 * dt = 7.5
        self.assertAlmostEqual(position.x, 7.5)

    def test_high_ground_miss_chance(self):
        """Test that attacks miss 50% of the time on high ground."""
        system = CombatSystem()

        # Create attacker (low ground)
        attacker = self.game_state.create_entity()
        self.game_state.add_component(attacker, Attack(attack_damage=10, attack_range=5, attack_speed=1))
        self.game_state.add_component(attacker, Position(0, 0))
        self.game_state.add_component(attacker, Movable(speed=0))

        # Create defender (high ground)
        defender = self.game_state.create_entity()
        self.game_state.add_component(defender, Health(hp=100, max_hp=100))
        self.game_state.add_component(defender, Position(4, 0)) # Within range 5

        # Set attacker target
        self.game_state.get_component(attacker, Attack).attack_target = defender

        # Mock terrain
        def get_terrain_side_effect(x, y):
            if x == 0 and y == 0: return TERRAIN_NORMAL # Attacker
            if x == 4 and y == 0: return TERRAIN_HIGH_GROUND # Defender
            return TERRAIN_NORMAL

        self.game_state.map.get_terrain.side_effect = get_terrain_side_effect

        # Run many attacks to verify approx 50% miss rate
        hits = 0
        attempts = 1000

        # We need to control random for deterministic testing or use statistical assertion
        # But here I'll just rely on statistical average being reasonably close.
        # Or I can patch random.

        with unittest.mock.patch('random.random') as mock_random:
            # First, test miss (< 0.5)
            mock_random.return_value = 0.4
            # Reset HP
            self.game_state.get_component(defender, Health).hp = 100
            # Reset Cooldown
            self.game_state.get_component(attacker, Attack).attack_cooldown = 0

            system.update(self.game_state, dt=1.0)

            # Should have missed, HP should still be 100
            self.assertEqual(self.game_state.get_component(defender, Health).hp, 100)

            # Second, test hit (>= 0.5)
            mock_random.return_value = 0.6
            self.game_state.get_component(attacker, Attack).attack_cooldown = 0

            system.update(self.game_state, dt=1.0)

            # Should have hit, HP should be 90
            self.assertEqual(self.game_state.get_component(defender, Health).hp, 90)

    def test_no_miss_on_equal_ground(self):
        """Test that attacks do not miss on equal ground."""
        system = CombatSystem()

        attacker = self.game_state.create_entity()
        self.game_state.add_component(attacker, Attack(attack_damage=10, attack_range=5, attack_speed=1))
        self.game_state.add_component(attacker, Position(0, 0))
        self.game_state.add_component(attacker, Movable(speed=0))

        defender = self.game_state.create_entity()
        self.game_state.add_component(defender, Health(hp=100, max_hp=100))
        self.game_state.add_component(defender, Position(4, 0))

        self.game_state.get_component(attacker, Attack).attack_target = defender

        # Both on Normal Terrain
        self.game_state.map.get_terrain.return_value = TERRAIN_NORMAL

        with unittest.mock.patch('random.random') as mock_random:
            mock_random.return_value = 0.1 # Even with low random value, should not miss

            system.update(self.game_state, dt=1.0)
            self.assertEqual(self.game_state.get_component(defender, Health).hp, 90)

if __name__ == '__main__':
    unittest.main()
