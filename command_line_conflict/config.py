import pygame

from .units import (
    Arachnotron,
    Chassis,
    Extractor,
    Immortal,
    Observer,
    Rover,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
FPS = 60

KEY_BINDINGS = {
    pygame.K_1: Extractor,
    pygame.K_2: Chassis,
    pygame.K_3: Rover,
    pygame.K_4: Arachnotron,
    pygame.K_5: Observer,
    pygame.K_6: Immortal,
}
