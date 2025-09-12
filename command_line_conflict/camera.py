import pygame

from . import config


class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.zoom = 1.0

    def apply(self, rect):
        return rect.move(self.x, self.y).inflate(self.zoom, self.zoom)

    def screen_to_world(self, screen_x, screen_y):
        world_x = (screen_x - self.x) / self.zoom
        world_y = (screen_y - self.y) / self.zoom
        return int(world_x), int(world_y)

    def world_to_screen(self, world_x, world_y):
        screen_x = world_x * self.zoom + self.x
        screen_y = world_y * self.zoom + self.y
        return int(screen_x), int(screen_y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.zoom *= 1.1
            elif event.button == 5:  # Scroll down
                self.zoom /= 1.1

        self.zoom = max(0.5, min(self.zoom, 2.0))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x += config.CAMERA_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x -= config.CAMERA_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y += config.CAMERA_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y -= config.CAMERA_SPEED
