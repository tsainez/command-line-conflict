from command_line_conflict.scenes.game import GameScene
from command_line_conflict.maps.mission_one import MissionOne
from command_line_conflict.engine import Game

def test_launch_mission_one():
    """Tests that the first campaign mission can be launched without crashing."""
    game = Game()
    game.scene_manager.scenes["game"] = GameScene(game, MissionOne())
    game.scene_manager.switch_to("game")
    assert isinstance(game.scene_manager.current_scene, GameScene)
    assert isinstance(game.scene_manager.current_scene.game_state.map, MissionOne)
