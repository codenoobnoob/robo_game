import pygame

# Not tested or used yet


class Camera(pygame.sprite.Sprite):
    def __init__(self, vector: object, width: int, height: int):
        pygame.sprite.Sprite().__init__(self)
        self.vec = pygame.Vector2()
        self.vec.update((0, 0))
        self.rect = pygame.rect(0, 0, width, height)
        self.rect.topleft = self.vec

    def update(self, other: object):
        self.vec += other
