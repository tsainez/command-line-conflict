# Maps

Maps define the playable area and the units that are initially on it. All maps inherit from the `Map` class in `command_line_conflict/maps/base.py`.

## SimpleMap

This is the default map. It's a simple, open map with no obstacles.

## WallMap

This map has a horizontal wall with a gap in the middle. It's a good map for testing pathfinding, as ground units will have to go around the wall to reach the other side. Air units, on the other hand, can fly right over it.
