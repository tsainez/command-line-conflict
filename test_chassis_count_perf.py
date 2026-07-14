import time
from command_line_conflict.game_state import GameState
from command_line_conflict.maps.base import Map
from command_line_conflict.components.unit_identity import UnitIdentity
from command_line_conflict.components.player import Player
from command_line_conflict.components.dead import Dead
import pygame
import os

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
pygame.init()

game_map = Map(100, 100)
game_state = GameState(game_map)
current_player_id = 1

for i in range(1000):
    eid = game_state.create_entity()
    game_state.add_component(eid, UnitIdentity("chassis"))
    game_state.add_component(eid, Player(current_player_id, is_human=True))

for i in range(1000):
    eid = game_state.create_entity()
    game_state.add_component(eid, UnitIdentity("arachnotron"))
    game_state.add_component(eid, Player(current_player_id, is_human=True))

def benchmark_old():
    start = time.time()
    for _ in range(1000):
        chassis_count = 0
        for eid in game_state.get_entities_with_component(UnitIdentity):
            ent_components = game_state.entities.get(eid)
            if not ent_components:
                continue
            ident = ent_components.get(UnitIdentity)
            plyr = ent_components.get(Player)
            is_dead = ent_components.get(Dead) is not None
            if ident and ident.name == "chassis" and plyr and plyr.player_id == current_player_id and not is_dead:
                chassis_count += 1
    end = time.time()
    return end - start

def benchmark_fast_fail():
    start = time.time()
    for _ in range(1000):
        chassis_count = 0
        for eid in game_state.get_entities_with_component(UnitIdentity):
            comps = game_state.entities[eid]
            ident = comps.get(UnitIdentity)
            if ident and ident.name == "chassis":
                plyr = comps.get(Player)
                if plyr and plyr.player_id == current_player_id and Dead not in comps:
                    chassis_count += 1
    end = time.time()
    return end - start

print(f"Old approach time: {benchmark_old():.5f}s")
print(f"Fast fail time: {benchmark_fast_fail():.5f}s")
