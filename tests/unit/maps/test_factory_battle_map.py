from command_line_conflict.components.factory import Factory
from command_line_conflict.components.player import Player
from command_line_conflict.components.unit_identity import UnitIdentity
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.factory_battle_map import FactoryBattleMap


def test_factory_battle_map_default_dimensions():
    game_map = FactoryBattleMap()
    assert game_map.width == 60
    assert game_map.height == 40


def test_factory_battle_map_has_walls():
    game_map = FactoryBattleMap()
    assert len(game_map.walls) > 0
    for x, y in game_map.walls:
        assert 0 <= x < game_map.width
        assert 0 <= y < game_map.height


def test_factory_battle_map_create_initial_units_spawns_human_player():
    game_map = FactoryBattleMap()
    state = GameState(game_map)

    game_map.create_initial_units(state)

    human_units = [
        eid
        for eid, comps in state.entities.items()
        if (player := comps.get(Player)) and player.is_human and player.player_id == 1
    ]
    assert len(human_units) > 0


def test_factory_battle_map_create_initial_units_spawns_enemy_factories():
    game_map = FactoryBattleMap()
    state = GameState(game_map)

    game_map.create_initial_units(state)

    factory_names = set()
    for _, comps in state.entities.items():
        player = comps.get(Player)
        identity = comps.get(UnitIdentity)
        factory = comps.get(Factory)
        if player and not player.is_human and player.player_id == 2 and factory and identity:
            factory_names.add(identity.name)

    assert "rover_factory" in factory_names
    assert "arachnotron_factory" in factory_names
