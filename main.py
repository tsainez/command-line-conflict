import pygame
from pygame.locals import *

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
FPS = 60
# units per second
UNIT_SPEED = 2

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ASCII RTS")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 16)


class Unit:
    """A very simple unit that can move around the grid."""

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.target_x = self.x
        self.target_y = self.y
        self.selected = False

    def update(self, dt):
        """Move the unit toward its target."""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = (dx * dx + dy * dy) ** 0.5
        if dist < 0.01:
            return
        step = UNIT_SPEED * dt
        if step > dist:
            step = dist
        self.x += step * dx / dist
        self.y += step * dy / dist

    def draw(self, surf):
        color = (0, 255, 0) if self.selected else (255, 255, 255)
        ch = font.render("U", True, color)
        surf.blit(ch, (int(self.x) * GRID_SIZE, int(self.y) * GRID_SIZE))


units = [Unit(5, 5), Unit(10, 10), Unit(15, 5)]
selection_start = None
running = True

while running:
    dt = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            # left click starts selection
            selection_start = event.pos
            for u in units:
                u.selected = False
        elif event.type == MOUSEBUTTONUP and event.button == 1 and selection_start:
            # finalize selection rectangle
            x1, y1 = selection_start
            x2, y2 = event.pos
            selection_start = None
            min_x, max_x = sorted((x1, x2))
            min_y, max_y = sorted((y1, y2))
            for u in units:
                ux = u.x * GRID_SIZE
                uy = u.y * GRID_SIZE
                if min_x <= ux <= max_x and min_y <= uy <= max_y:
                    u.selected = True
        elif event.type == MOUSEBUTTONDOWN and event.button == 3:
            # right click issues move command
            grid_x = event.pos[0] // GRID_SIZE
            grid_y = event.pos[1] // GRID_SIZE
            for u in units:
                if u.selected:
                    u.target_x = grid_x
                    u.target_y = grid_y

    for u in units:
        u.update(dt)

    screen.fill((0, 0, 0))

    # draw grid
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (SCREEN_WIDTH, y))

    # draw units
    for u in units:
        u.draw(screen)

    pygame.display.flip()

pygame.quit()
