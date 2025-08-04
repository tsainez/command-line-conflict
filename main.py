import argparse

from command_line_conflict.engine import main
from command_line_conflict.maps import SimpleMap, WallMap

if __name__ == "__main__":
    maps = {"simple": SimpleMap, "wall": WallMap}
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--map",
        choices=maps.keys(),
        default="simple",
        help="The map to play on.",
    )
    args = parser.parse_args()
    main(maps[args.map]())
