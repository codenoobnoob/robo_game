from gamemodules.settings import ADVANCE, HEIGHT, WIDTH
from pygame.sprite import Group
from settings import *
import pygame
from pygame.math import Vector2

# Not tested or used yet


class Camera:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.pos = Vector2(WIDTH/2, HEIGHT/2)
        self.rect = pygame.rect(0, 0, width, height)
        self.rect.center = self.pos
        self.gamesections = pygame.sprite.Group()
        self.acc = Vector2(0, 0)
        self.vel = Vector2(0, 0)

    def update(self, player: object):
        if abs(self.pos.x-player.pos.x) >= ADVANCE or abs(self.pos.y-player.pos.y) >= ADVANCE:
            self.acc
        # here what happens if the camera is ADVANCE pixels behind or before player.

    def get_drawlist(self):
        draw_list = []
        gamesections = pygame.sprite.spritecollide(
            self.rect, self.gamesections)
        for gamesection in gamesections:
            draw_list.extend(pygame.sprite.spritecollide(
                self.rect, gamesection.group, False))

        return draw_list

    def add_gamesection(self, all_objects: list):
        for vec in [(0, 0.5), (0, 1), (0.5, 0.5), (0.5, 1)]:
            x = WORLDSIZE_X * vec[0]
            y = WORLDSIZE_Y * vec[1] + HEIGHT
            self.gamesections.add(GameSection(x, y))

        for item in self.gamesections.sprites():
            collitions = pygame.sprite.spritecollide(item, all_objects, False)
            item.add_objects(collitions)


class GameSection(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite().__init__(self)
        self.group = pygame.sprite.Group()
        self.rect = pygame.rect(x, y, WORLDSIZE[0]/2, WORLDSIZE[1]/2)

    def add_objects(self, objects: list):
        self.group.add(objects)
