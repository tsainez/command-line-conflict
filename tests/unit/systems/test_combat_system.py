from command_line_conflict.components.attack import Attack
from command_line_conflict.components.confetti import Confetti
from command_line_conflict.components.health import Health
from command_line_conflict.components.position import Position
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.simple_map import SimpleMap
from command_line_conflict.systems.combat_system import CombatSystem


def test_combat_system_creates_confetti_on_ranged_attack():
    # Arrange
    game_state = GameState(game_map=SimpleMap())
    combat_system = CombatSystem()

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
    confetti_found = False
    for entity_id, components in game_state.entities.items():
        if components.get(Confetti):
            confetti_found = True
            confetti_pos = components.get(Position)
            assert confetti_pos.x == 3
            assert confetti_pos.y == 3
            break
    assert confetti_found, "Confetti should have been created"


def test_melee_attack_deals_damage():
    # Arrange
    game_state = GameState(game_map=SimpleMap())
    combat_system = CombatSystem()

    attacker_id = game_state.create_entity()
    game_state.add_component(attacker_id, Position(0, 0))
    attack_component = Attack(attack_damage=10, attack_range=1, attack_speed=1.0)
    game_state.add_component(attacker_id, attack_component)

    target_id = game_state.create_entity()
    game_state.add_component(target_id, Position(1, 0))
    initial_hp = 100
    game_state.add_component(target_id, Health(hp=initial_hp, max_hp=100))

    game_state.entities[attacker_id][Attack].attack_target = target_id

    # Act
    combat_system.update(game_state, dt=1.0)

    # Assert
    target_health = game_state.get_component(target_id, Health)
    assert target_health.hp == initial_hp - attack_component.attack_damage

    confetti_found = False
    for entity_id, components in game_state.entities.items():
        if components.get(Confetti):
            confetti_found = True
            break
    assert not confetti_found, "Confetti should not be created for melee attacks"