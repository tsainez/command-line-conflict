import pytest
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
    immortal = Immortal(0, 0)
    immortal.hp = 100
    immortal.update(dt=1.0)
    assert immortal.hp == 102  # 100 + 2.0 * 1.0


def test_immortal_health_regeneration_stops_at_max_health():
    immortal = Immortal(0, 0)
    immortal.hp = immortal.max_hp - 1
    immortal.update(dt=1.0)
    assert immortal.hp == immortal.max_hp


def test_rover_set_target_no_pathfinding():
    rover = Rover(0, 0)
    rover.set_target(10, 10)
    assert rover.path == []
    assert rover.target_x == 10
    assert rover.target_y == 10
