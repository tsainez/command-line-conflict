import pytest
from command_line_conflict.maps import Map
from command_line_conflict.units import (
    Arachnotron,
    Chassis,
    Extractor,
    Immortal,
    Observer,
    Rover,
)


@pytest.mark.parametrize(
    "unit_class, expected_stats",
    [
        (Chassis, {"max_hp": 80, "attack_damage": 10, "attack_range": 1, "speed": 2}),
        (Rover, {"max_hp": 60, "attack_damage": 15, "attack_range": 5, "speed": 2.5}),
        (
            Arachnotron,
            {
                "max_hp": 120,
                "attack_damage": 20,
                "attack_range": 6,
                "speed": 1.8,
                "can_fly": True,
            },
        ),
        (
            Observer,
            {
                "max_hp": 40,
                "attack_damage": 0,
                "attack_range": 0,
                "speed": 4,
                "vision_range": 15,
                "flees_from_enemies": True,
            },
        ),
        (
            Immortal,
            {
                "max_hp": 150,
                "attack_damage": 25,
                "attack_range": 7,
                "speed": 2,
                "health_regen_rate": 2.0,
                "flee_health_threshold": 0.2,
            },
        ),
        (
            Extractor,
            {"max_hp": 50, "attack_damage": 0, "attack_range": 0, "speed": 1.5},
        ),
    ],
)
def test_unit_stat_initialization(unit_class, expected_stats):
    unit = unit_class(0, 0)
    for stat, value in expected_stats.items():
        assert getattr(unit, stat) == value


def test_immortal_health_regeneration():
    game_map = Map()
    immortal = Immortal(0, 0)
    game_map.spawn_unit(immortal)
    immortal.hp = 100
    immortal.update(dt=1.0, game_map=game_map)
    assert immortal.hp == 102  # 100 + 2.0 * 1.0


def test_immortal_health_regeneration_stops_at_max_health():
    game_map = Map()
    immortal = Immortal(0, 0)
    game_map.spawn_unit(immortal)
    immortal.hp = immortal.max_hp - 1
    immortal.update(dt=1.0, game_map=game_map)
    assert immortal.hp == immortal.max_hp


def test_rover_set_target_no_pathfinding():
    rover = Rover(0, 0)
    rover.set_target(10, 10)
    assert rover.path == []
    assert rover.target_x == 10
    assert rover.target_y == 10


def test_unit_can_attack_target():
    game_map = Map()
    attacker = Chassis(0, 0)
    target = Chassis(1, 0)
    game_map.spawn_unit(attacker)
    game_map.spawn_unit(target)

    attacker.attack_target = target
    initial_target_hp = target.hp

    # Attacker is in range, so it should attack
    attacker.update(dt=1.0, game_map=game_map)

    assert target.hp < initial_target_hp
    assert target.hp == initial_target_hp - attacker.attack_damage


def test_unit_pursues_target():
    game_map = Map()
    attacker = Chassis(0, 0)
    target = Chassis(10, 0)  # Out of range
    game_map.spawn_unit(attacker)
    game_map.spawn_unit(target)

    attacker.attack_target = target
    initial_attacker_x = attacker.x

    attacker.update(dt=1.0, game_map=game_map)

    assert attacker.x > initial_attacker_x
    assert target.hp == target.max_hp  # No damage dealt as target is out of range


def test_unit_stops_to_attack():
    game_map = Map()
    attacker = Chassis(0, 0)
    target = Chassis(2, 0)  # Just outside melee range
    game_map.spawn_unit(attacker)
    game_map.spawn_unit(target)

    attacker.attack_target = target
    attacker.update(dt=1.0, game_map=game_map)  # Move towards target

    # Now attacker should be in range
    assert abs(attacker.x - target.x) <= attacker.attack_range

    initial_target_hp = target.hp
    attacker.update(dt=1.0, game_map=game_map)  # Attack
    assert target.hp < initial_target_hp


def test_unit_with_zero_attack_cannot_attack():
    game_map = Map()
    attacker = Extractor(0, 0)
    target = Chassis(1, 0)
    game_map.spawn_unit(attacker)
    game_map.spawn_unit(target)

    attacker.attack_target = target
    initial_target_hp = target.hp
    attacker.update(dt=1.0, game_map=game_map)

    assert target.hp == initial_target_hp


def test_unit_clears_dead_target():
    game_map = Map()
    attacker = Chassis(0, 0)
    target = Chassis(1, 0)
    game_map.spawn_unit(attacker)
    game_map.spawn_unit(target)

    attacker.attack_target = target
    target.hp = 0
    attacker.update(dt=1.0, game_map=game_map)

    assert attacker.attack_target is None


def test_observer_flees_from_enemy():
    game_map = Map()
    observer = Observer(0, 0)
    enemy = Chassis(5, 0)  # Within vision range
    game_map.spawn_unit(observer)
    game_map.spawn_unit(enemy)

    initial_observer_x = observer.x
    observer.update(dt=1.0, game_map=game_map)

    assert observer.is_fleeing
    assert observer.x < initial_observer_x  # Should move away from enemy


def test_immortal_flees_when_health_is_low():
    game_map = Map()
    immortal = Immortal(0, 0)
    enemy = Chassis(5, 0)
    game_map.spawn_unit(immortal)
    game_map.spawn_unit(enemy)

    immortal.hp = immortal.max_hp * 0.1  # Below 20% threshold
    initial_immortal_x = immortal.x
    immortal.update(dt=1.0, game_map=game_map)

    assert immortal.is_fleeing
    assert immortal.x < initial_immortal_x


def test_immortal_does_not_flee_when_health_is_high():
    game_map = Map()
    immortal = Immortal(0, 0)
    enemy = Chassis(5, 0)
    game_map.spawn_unit(immortal)
    game_map.spawn_unit(enemy)

    immortal.hp = immortal.max_hp * 0.3  # Above 20% threshold
    immortal.update(dt=1.0, game_map=game_map)

    assert not immortal.is_fleeing


def test_fleeing_unit_does_not_attack():
    game_map = Map()
    immortal = Immortal(0, 0)
    enemy = Chassis(1, 0)
    game_map.spawn_unit(immortal)
    game_map.spawn_unit(enemy)

    immortal.hp = immortal.max_hp * 0.1  # Low health to trigger fleeing
    initial_enemy_hp = enemy.hp
    immortal.update(dt=1.0, game_map=game_map)

    assert immortal.is_fleeing
    assert enemy.hp == initial_enemy_hp
