from unittest.mock import MagicMock

import pygame

from command_line_conflict import config
from command_line_conflict.components.factory import Factory
from command_line_conflict.components.movable import Movable
from command_line_conflict.components.player import Player
from command_line_conflict.components.position import Position
from command_line_conflict.components.selectable import Selectable
from command_line_conflict.scenes.game import NUMBER_KEY_TO_GROUP, GameScene


class MockGame:
    def __init__(self):
        self.screen = MagicMock()
        self.screen.get_size.return_value = (800, 600)
        self.font = MagicMock()
        self.music_manager = MagicMock()
        self.scene_manager = MagicMock()
        self.steam = MagicMock()


def _keydown(key):
    return pygame.event.Event(pygame.KEYDOWN, {"key": key})


def _make_selected_unit(game_state, x, y, player_id=1):
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Position(x, y))
    game_state.add_component(entity_id, Movable(speed=1.0))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Player(player_id=player_id, is_human=True))
    game_state.entities[entity_id][Selectable].is_selected = True
    return entity_id


def _make_selected_building(game_state, x, y, player_id=1):
    entity_id = game_state.create_entity()
    game_state.add_component(entity_id, Position(x, y))
    game_state.add_component(entity_id, Factory(input_unit="chassis", output_unit="rover"))
    game_state.add_component(entity_id, Selectable())
    game_state.add_component(entity_id, Player(player_id=player_id, is_human=True))
    game_state.entities[entity_id][Selectable].is_selected = True
    return entity_id


def test_at_least_ten_control_groups_are_addressable():
    # 1-9 and 0 (bound to the 10th group) must all be distinct group numbers.
    assert len(NUMBER_KEY_TO_GROUP) >= 10
    assert len(set(NUMBER_KEY_TO_GROUP.values())) >= 10
    assert NUMBER_KEY_TO_GROUP[pygame.K_0] == 10


def test_ctrl_number_assigns_selection_to_group(mocker):
    game = MockGame()
    scene = GameScene(game)
    game_state = scene.game_state
    unit_id = _make_selected_unit(game_state, 3, 3)

    mocker.patch("pygame.key.get_mods", return_value=pygame.KMOD_CTRL)
    scene.handle_event(_keydown(pygame.K_1))

    assert scene.control_group_system.select_group(game_state, 1, scene.current_player_id) == [unit_id]


def test_number_alone_recalls_group_selection(mocker):
    game = MockGame()
    scene = GameScene(game)
    game_state = scene.game_state
    unit_id = _make_selected_unit(game_state, 3, 3)

    mocker.patch("pygame.key.get_mods", return_value=pygame.KMOD_CTRL)
    scene.handle_event(_keydown(pygame.K_1))

    # Deselect, then recall via a plain (no-Ctrl) press of the same key.
    game_state.entities[unit_id][Selectable].is_selected = False
    mocker.patch("pygame.key.get_mods", return_value=0)
    scene.handle_event(_keydown(pygame.K_1))

    assert game_state.entities[unit_id][Selectable].is_selected is True


def test_only_one_building_survives_group_assignment(mocker):
    game = MockGame()
    scene = GameScene(game)
    game_state = scene.game_state
    building_a = _make_selected_building(game_state, 0, 0)
    building_b = _make_selected_building(game_state, 1, 1)
    unit_id = _make_selected_unit(game_state, 2, 2)

    mocker.patch("pygame.key.get_mods", return_value=pygame.KMOD_CTRL)
    scene.handle_event(_keydown(pygame.K_2))

    group = scene.control_group_system.select_group(game_state, 2, scene.current_player_id)
    assert unit_id in group
    assert building_a in group
    assert building_b not in group
    assert len(group) == 2


def test_double_tap_group_key_centers_camera(mocker):
    game = MockGame()
    scene = GameScene(game)
    game_state = scene.game_state
    _make_selected_unit(game_state, 30, 40)

    mocker.patch("pygame.key.get_mods", return_value=pygame.KMOD_CTRL)
    scene.handle_event(_keydown(pygame.K_3))

    mocker.patch("pygame.key.get_mods", return_value=0)
    mocker.patch("pygame.time.get_ticks", return_value=1000)
    scene.handle_event(_keydown(pygame.K_3))  # first recall: no snap yet
    initial_camera_x = scene.camera.x
    initial_camera_y = scene.camera.y

    mocker.patch("pygame.time.get_ticks", return_value=1000 + config.CONTROL_GROUP_DOUBLE_TAP_MS - 1)
    scene.handle_event(_keydown(pygame.K_3))  # second recall within the window: snap

    grid_size = config.GRID_SIZE * scene.camera.zoom
    screen_w, screen_h = game.screen.get_size()
    assert scene.camera.x != initial_camera_x
    assert scene.camera.x == 30 - (screen_w / grid_size) / 2
    assert scene.camera.y == 40 - (screen_h / grid_size) / 2
    assert initial_camera_y == 0  # sanity: camera really did start at the default origin


def test_slow_second_press_does_not_center_camera(mocker):
    game = MockGame()
    scene = GameScene(game)
    game_state = scene.game_state
    _make_selected_unit(game_state, 30, 40)

    mocker.patch("pygame.key.get_mods", return_value=pygame.KMOD_CTRL)
    scene.handle_event(_keydown(pygame.K_4))

    mocker.patch("pygame.key.get_mods", return_value=0)
    mocker.patch("pygame.time.get_ticks", return_value=1000)
    scene.handle_event(_keydown(pygame.K_4))

    mocker.patch("pygame.time.get_ticks", return_value=1000 + config.CONTROL_GROUP_DOUBLE_TAP_MS + 1)
    scene.handle_event(_keydown(pygame.K_4))

    assert scene.camera.x == 0
    assert scene.camera.y == 0


def test_debug_ctrl_shift_number_spawns_unit_instead_of_assigning_group(mocker):
    mocker.patch("command_line_conflict.config.DEBUG", True)
    game = MockGame()
    scene = GameScene(game)
    game_state = scene.game_state

    mocker.patch("pygame.mouse.get_pos", return_value=(40, 40))
    mocker.patch("pygame.key.get_mods", return_value=pygame.KMOD_CTRL | pygame.KMOD_SHIFT)

    entity_count_before = len(game_state.entities)
    scene.handle_event(_keydown(pygame.K_2))  # Ctrl+Shift+2 -> debug-spawn a chassis

    assert len(game_state.entities) == entity_count_before + 1
    # Nothing should have been bound to control group 2 by this spawn shortcut.
    assert not scene.control_group_system.select_group(game_state, 2, scene.current_player_id)


def test_plain_ctrl_number_still_assigns_group_in_debug_mode(mocker):
    mocker.patch("command_line_conflict.config.DEBUG", True)
    game = MockGame()
    scene = GameScene(game)
    game_state = scene.game_state
    unit_id = _make_selected_unit(game_state, 5, 5)

    mocker.patch("pygame.key.get_mods", return_value=pygame.KMOD_CTRL)
    scene.handle_event(_keydown(pygame.K_5))

    assert scene.control_group_system.select_group(game_state, 5, scene.current_player_id) == [unit_id]
