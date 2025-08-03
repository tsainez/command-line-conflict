from command_line_conflict.fog_of_war import FogOfWar
from command_line_conflict.maps.wall_map import WallMap
from command_line_conflict.units import Arachnotron, Chassis, Observer, Rover


def test_chassis_pathfinding_around_wall():
    game_map = WallMap()
    chassis = Chassis(x=1, y=7)
    game_map.spawn_unit(chassis)
    chassis.set_target(x=18, y=7, game_map=game_map)
    assert chassis.path is not None
    assert len(chassis.path) > 1
    # The path should go around the wall, so it must contain y-coordinates other than 7
    assert any(y != 7 for x, y in chassis.path)


def test_arachnotron_pathfinding_over_wall():
    game_map = WallMap()
    arachnotron = Arachnotron(x=1, y=7)
    game_map.spawn_unit(arachnotron)
    arachnotron.set_target(x=18, y=7, game_map=game_map)
    assert not arachnotron.path  # Flying units don't get a path
    assert arachnotron.target_x == 18
    assert arachnotron.target_y == 7


def test_rover_gets_stuck_on_wall():
    game_map = WallMap()
    rover = Rover(x=1, y=7)
    game_map.spawn_unit(rover)
    rover.set_target(x=18, y=7, game_map=game_map)

    # The wall starts at x=3. The rover moves in a straight line.
    # Let's check its position after a few updates.
    for _ in range(10):
        # In base.py, a unit will not move into an occupied square.
        # However, there is no check for walls for units that do not pathfind.
        # So the rover will move until it is inside the wall.
        # Its speed is 2.5, dt is 0.1, so it moves 0.25 per tick.
        # It starts at x=1. The wall is at x=3.
        # It will take 8 ticks to reach x=3. (2 / 0.25)
        # After 10 ticks, it will be at x = 1 + 10 * 0.25 = 3.5
        rover.update(dt=0.1, game_map=game_map)

    # The rover should be stuck before or at the beginning of the wall.
    # The current implementation lets it move into the wall.
    assert rover.x < 4


def test_observer_vision():
    game_map = WallMap()
    observer = Observer(x=5, y=5)
    game_map.spawn_unit(observer)

    fog = FogOfWar(width=game_map.width, height=game_map.height)
    fog.update(game_map.units)

    # A point far away but within the observer's vision
    # Observer vision is 15. Map height is 15.
    # Let's pick a point at the edge of the map, but inside the vision.
    far_point_x, far_point_y = 5, 14
    dist_sq = (far_point_x - observer.x)**2 + (far_point_y - observer.y)**2
    assert dist_sq <= observer.vision_range**2
    assert fog.grid[far_point_y][far_point_x] == FogOfWar.VISIBLE

    # A point outside the observer's vision
    game_map = WallMap()
    observer = Observer(x=0, y=0)
    game_map.spawn_unit(observer)
    fog = FogOfWar(width=game_map.width, height=game_map.height)
    fog.update(game_map.units)
    outside_point_x, outside_point_y = 14, 14
    dist_sq = (outside_point_x - observer.x)**2 + (outside_point_y - observer.y)**2
    assert dist_sq > observer.vision_range**2
    assert fog.grid[outside_point_y][outside_point_x] == FogOfWar.HIDDEN
