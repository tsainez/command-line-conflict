from command_line_conflict import factories
from command_line_conflict.components.dead import Dead
from command_line_conflict.components.health import Health
from command_line_conflict.components.position import Position
from command_line_conflict.components.resource_deposit import ResourceDeposit
from command_line_conflict.components.unit_identity import UnitIdentity
from command_line_conflict.systems.health_system import HealthSystem
from command_line_conflict.systems.resource_system import ResourceSystem


def test_game_state_resources_initialization(game_state):
    """Verify that GameState correctly initializes the resources dictionary."""
    assert hasattr(game_state, "resources")
    assert game_state.resources[1] == 0
    assert game_state.resources[2] == 0


def test_create_scrap(game_state):
    """Verify that create_scrap creates an entity with expected components."""
    scrap_id = factories.create_scrap(game_state, 10.0, 15.0, amount=75)

    pos = game_state.get_component(scrap_id, Position)
    assert pos is not None
    assert pos.x == 10.0
    assert pos.y == 15.0

    identity = game_state.get_component(scrap_id, UnitIdentity)
    assert identity is not None
    assert identity.name == "scrap"

    deposit = game_state.get_component(scrap_id, ResourceDeposit)
    assert deposit is not None
    assert deposit.amount == 75


def test_neutral_death_spawns_scrap(game_state):
    """Verify that when a neutral unit dies, a scrap entity is spawned at its location."""
    # Create neutral unit (Player 0)
    neutral_id = factories.create_wildlife(game_state, 5.0, 5.0)

    health = game_state.get_component(neutral_id, Health)
    assert health is not None

    # Reduce health to 0
    health.hp = 0

    # Run health system
    health_system = HealthSystem()
    health_system.update(game_state, 0.1)

    # Verify that the neutral unit is now marked dead
    assert game_state.get_component(neutral_id, Dead) is not None

    # Verify that a scrap entity was created at (5.0, 5.0)
    scrap_entities = game_state.get_entities_with_component(ResourceDeposit)
    assert len(scrap_entities) == 1

    scrap_id = list(scrap_entities)[0]
    pos = game_state.get_component(scrap_id, Position)
    assert pos.x == 5.0
    assert pos.y == 5.0

    deposit = game_state.get_component(scrap_id, ResourceDeposit)
    assert deposit.amount == 50


def test_resource_system_collects_scrap(game_state):
    """Verify that player units occupying the same cell collect scrap resources."""
    # Create a scrap entity at (3.0, 4.0)
    scrap_id = factories.create_scrap(game_state, 3.0, 4.0, amount=50)

    # Create a player unit at (3.0, 4.0)
    factories.create_chassis(game_state, 3.0, 4.0, player_id=1, is_human=True)

    # Run ResourceSystem
    resource_system = ResourceSystem()
    resource_system.update(game_state, 0.1)

    # Verify scrap entity was removed/consumed
    assert scrap_id not in game_state.entities

    # Verify resources updated for Player 1
    assert game_state.resources[1] == 50


def test_resource_system_ignores_dead_units(game_state):
    """Verify that dead player units do not collect scrap."""
    scrap_id = factories.create_scrap(game_state, 3.0, 4.0, amount=50)

    # Create a dead player unit at (3.0, 4.0)
    player_unit_id = factories.create_chassis(game_state, 3.0, 4.0, player_id=1, is_human=True)
    game_state.add_component(player_unit_id, Dead())

    # Run ResourceSystem
    resource_system = ResourceSystem()
    resource_system.update(game_state, 0.1)

    # Verify scrap entity was not consumed
    assert scrap_id in game_state.entities
    assert game_state.resources[1] == 0


def test_resource_system_ignores_neutral_units(game_state):
    """Verify that neutral units (Player 0) do not collect scrap."""
    scrap_id = factories.create_scrap(game_state, 3.0, 4.0, amount=50)

    # Create a neutral unit (Player 0) at (3.0, 4.0)
    factories.create_wildlife(game_state, 3.0, 4.0)

    # Run ResourceSystem
    resource_system = ResourceSystem()
    resource_system.update(game_state, 0.1)

    # Verify scrap entity was not consumed
    assert scrap_id in game_state.entities


class MockGame:
    def __init__(self):
        from unittest.mock import MagicMock

        self.music_manager = MagicMock()
        self.steam = MagicMock()
        self.font = MagicMock()
        self.screen = MagicMock()


def test_train_chassis_at_factory(game_state):
    """Verify that training a chassis at a factory deducts scrap and spawns a chassis."""
    from command_line_conflict.scenes.game import GameScene

    mock_game = MockGame()
    scene = GameScene(mock_game)
    scene.game_state = game_state
    scene.current_player_id = 1

    # Create factory
    factory_id = factories.create_rover_factory(game_state, 10.0, 10.0, player_id=1, is_human=True)

    # 1. Test when resources are insufficient
    game_state.resources[1] = 40
    scene._train_chassis_at_factory(factory_id)

    # Verify no chassis spawned and resources unchanged
    chassis_entities = [
        eid
        for eid in game_state.get_entities_with_component(UnitIdentity)
        if game_state.get_component(eid, UnitIdentity).name == "chassis"
    ]
    assert len(chassis_entities) == 0
    assert game_state.resources[1] == 40

    # 2. Test when resources are sufficient
    game_state.resources[1] = 60
    scene._train_chassis_at_factory(factory_id)

    # Verify chassis spawned and resources deducted
    chassis_entities = [
        eid
        for eid in game_state.get_entities_with_component(UnitIdentity)
        if game_state.get_component(eid, UnitIdentity).name == "chassis"
    ]
    assert len(chassis_entities) == 1
    assert game_state.resources[1] == 10  # 60 - 50


def test_settings_scene_mute_audio():
    """Verify that toggling Mute Audio toggles both config values and stops/plays music."""
    from command_line_conflict import config
    from command_line_conflict.scenes.settings import SettingsScene

    mock_game = MockGame()
    # Ensure config starts enabled
    config.SOUND_ENABLED = True
    config.MUSIC_ENABLED = True

    scene = SettingsScene(mock_game)

    # Toggling mute on
    scene._trigger_option("Mute Audio")
    assert not config.SOUND_ENABLED
    assert not config.MUSIC_ENABLED
    mock_game.music_manager.stop.assert_called_once()

    # Toggling mute off
    scene._trigger_option("Mute Audio")
    assert config.SOUND_ENABLED
    assert config.MUSIC_ENABLED
    mock_game.music_manager.play.assert_called_with("music/menu_theme.ogg")


def test_research_arachnotron_at_factory(game_state):
    """Verify that researching arachnotron at a Rover factory requires 6 chassis and 100 scrap."""
    from command_line_conflict.campaign_manager import CampaignManager
    from command_line_conflict.scenes.game import GameScene

    mock_game = MockGame()
    scene = GameScene(mock_game)
    scene.game_state = game_state
    scene.campaign_manager = CampaignManager()
    scene.game_state.campaign_manager = scene.campaign_manager
    scene.current_player_id = 1

    # Ensure locked at start
    if "arachnotron" in scene.campaign_manager.unlocked_units:
        scene.campaign_manager.unlocked_units.remove("arachnotron")

    factory_id = factories.create_rover_factory(game_state, 10.0, 10.0, player_id=1, is_human=True)

    # 1. Test when resources are sufficient but chassis count is insufficient (less than 6)
    game_state.resources[1] = 150
    # Spawn 3 chassis
    for i in range(3):
        factories.create_chassis(game_state, 5.0 + i, 5.0, player_id=1, is_human=True)

    scene._research_arachnotron_at_factory(factory_id)
    assert "arachnotron" not in scene.campaign_manager.unlocked_units
    assert game_state.resources[1] == 150

    # 2. Test when chassis count is sufficient (6) but scrap is insufficient (less than 100)
    # Spawn 3 more chassis (total 6)
    for i in range(3):
        factories.create_chassis(game_state, 8.0 + i, 5.0, player_id=1, is_human=True)

    game_state.resources[1] = 50
    scene._research_arachnotron_at_factory(factory_id)
    assert "arachnotron" not in scene.campaign_manager.unlocked_units
    assert game_state.resources[1] == 50

    # 3. Test when both requirements are met
    game_state.resources[1] = 120
    scene._research_arachnotron_at_factory(factory_id)
    assert "arachnotron" in scene.campaign_manager.unlocked_units
    assert game_state.resources[1] == 20  # 120 - 100


def test_train_chassis_refused_when_factory_surrounded(game_state):
    """A fully surrounded factory must refuse to train (and not charge).

    Regression test: the old fallback spawned the unit ON the factory tile,
    where ProductionSystem would instantly transform it for free.
    """
    from command_line_conflict.scenes.game import GameScene

    mock_game = MockGame()
    scene = GameScene(mock_game)
    scene.game_state = game_state
    scene.current_player_id = 1

    factory_id = factories.create_rover_factory(game_state, 10.0, 10.0, player_id=1, is_human=True)

    # Block all 8 neighboring tiles with live units.
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            factories.create_rover(game_state, 10.0 + dx, 10.0 + dy, player_id=1, is_human=True)

    game_state.resources[1] = 100
    scene._train_chassis_at_factory(factory_id)

    chassis_entities = [
        eid
        for eid in game_state.get_entities_with_component(UnitIdentity)
        if game_state.get_component(eid, UnitIdentity).name == "chassis"
    ]
    assert len(chassis_entities) == 0
    assert game_state.resources[1] == 100  # No charge on refusal


def test_train_rover_refused_when_factory_surrounded(game_state):
    """A surrounded Arachnotron Factory must not spawn a rover on its own tile.

    Regression test: an on-factory rover would be transformed into a free
    Arachnotron by ProductionSystem, bypassing the 120-scrap cost.
    """
    from command_line_conflict.scenes.game import GameScene

    mock_game = MockGame()
    scene = GameScene(mock_game)
    scene.game_state = game_state
    scene.current_player_id = 1

    factory_id = factories.create_arachnotron_factory(game_state, 15.0, 15.0, player_id=1, is_human=True)

    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            factories.create_chassis(game_state, 15.0 + dx, 15.0 + dy, player_id=1, is_human=True)

    game_state.resources[1] = 100
    scene._train_rover_at_factory(factory_id)

    rovers = [
        eid
        for eid in game_state.get_entities_with_component(UnitIdentity)
        if game_state.get_component(eid, UnitIdentity).name == "rover"
    ]
    assert len(rovers) == 0
    assert game_state.resources[1] == 100  # No charge on refusal


def test_r_key_fires_single_action_with_mixed_selection(game_state):
    """With a chassis AND an Arachnotron Factory selected, one R keypress
    must only build a Rover Factory (construction consumes the key), not
    also train a Rover — the old behavior double-spent scrap.
    """
    from unittest.mock import MagicMock

    import pygame

    from command_line_conflict.components.selectable import Selectable
    from command_line_conflict.scenes.game import GameScene

    mock_game = MockGame()
    scene = GameScene(mock_game)
    scene.game_state = game_state
    scene.current_player_id = 1
    scene.campaign_manager = MagicMock()
    scene.campaign_manager.is_unit_unlocked.return_value = True

    chassis_id = factories.create_chassis(game_state, 10.0, 10.0, player_id=1, is_human=True)
    game_state.get_component(chassis_id, Selectable).is_selected = True

    arach_factory_id = factories.create_arachnotron_factory(game_state, 20.0, 20.0, player_id=1, is_human=True)
    game_state.get_component(arach_factory_id, Selectable).is_selected = True

    game_state.resources[1] = 1000

    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))

    # The chassis was consumed to build a Rover Factory...
    assert chassis_id not in game_state.entities
    rover_factories = [
        eid
        for eid in game_state.get_entities_with_component(UnitIdentity)
        if game_state.get_component(eid, UnitIdentity).name == "rover_factory"
    ]
    assert len(rover_factories) == 1

    # ...and the Arachnotron Factory did NOT also train a Rover.
    rovers = [
        eid
        for eid in game_state.get_entities_with_component(UnitIdentity)
        if game_state.get_component(eid, UnitIdentity).name == "rover"
    ]
    assert len(rovers) == 0
    # Only the 100-scrap factory build was charged, not 100 + 80.
    assert game_state.resources[1] == 900


def test_arachnotron_factory_production(game_state):
    """Verify Rover and Arachnotron training at Arachnotron Factory."""
    from command_line_conflict.scenes.game import GameScene

    mock_game = MockGame()
    scene = GameScene(mock_game)
    scene.game_state = game_state
    scene.current_player_id = 1

    factory_id = factories.create_arachnotron_factory(game_state, 15.0, 15.0, player_id=1, is_human=True)

    # 1. Test train Rover with insufficient scrap (needs 80)
    game_state.resources[1] = 50
    scene._train_rover_at_factory(factory_id)

    rovers = [
        eid
        for eid in game_state.get_entities_with_component(UnitIdentity)
        if game_state.get_component(eid, UnitIdentity).name == "rover"
    ]
    assert len(rovers) == 0
    assert game_state.resources[1] == 50

    # 2. Test train Rover with sufficient scrap
    game_state.resources[1] = 100
    scene._train_rover_at_factory(factory_id)

    rovers = [
        eid
        for eid in game_state.get_entities_with_component(UnitIdentity)
        if game_state.get_component(eid, UnitIdentity).name == "rover"
    ]
    assert len(rovers) == 1
    assert game_state.resources[1] == 20  # 100 - 80

    # 3. Test train Arachnotron with insufficient adjacent rover (even if scrap is sufficient)
    rover_id = rovers[0]
    game_state.update_entity_position(rover_id, 20.0, 20.0)

    game_state.resources[1] = 200
    scene._train_arachnotron_at_factory(factory_id)

    arachnotrons = [
        eid
        for eid in game_state.get_entities_with_component(UnitIdentity)
        if game_state.get_component(eid, UnitIdentity).name == "arachnotron"
    ]
    assert len(arachnotrons) == 0
    assert game_state.resources[1] == 200

    # 4. Test train Arachnotron with adjacent rover and sufficient scrap
    game_state.update_entity_position(rover_id, 15.0, 14.0)

    scene._train_arachnotron_at_factory(factory_id)

    arachnotrons = [
        eid
        for eid in game_state.get_entities_with_component(UnitIdentity)
        if game_state.get_component(eid, UnitIdentity).name == "arachnotron"
    ]
    assert len(arachnotrons) == 1
    assert rover_id not in game_state.entities
    assert game_state.resources[1] == 80  # 200 - 120
