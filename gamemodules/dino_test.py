import pygame
from pygame import transform


class Dino(pygame.sprite.Sprite):
    def __init__(self, position: tuple, path):
        pygame.sprite.Sprite.__init__(self)
        self.gap = 50
        self.forward = True
        self.x = position[0]
        self.y = position[1]
        self.travel = 0
        self.animation_images = {}
        self.animation_frame = 0
        self.image = pygame.Surface((
            100, 100))
        self.load_animation(path)
        # self.image.fill((255, 255, 255))
        # self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.update_image(1)

    def update_image(self, x_dir):
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        if self.forward:
            self.image.blit(transform.flip(transform.scale(
                            self.animation_images[f"{self.animation_name}_{self.animation_frame}"], (100, 100)), True, False), (0, 0))

        else:
            self.image.blit(transform.scale(
                self.animation_images[f"{self.animation_name}_{self.animation_frame}"], (100, 100)), (0, 0))

    def update(self, x_dir, x: float, y: float, angle: float, rising: bool, falling: bool, jump_height: float, ceiling: float, y_dir: int):
        if x_dir < 0:
            self.forward = False
        if x_dir > 0:
            self.forward = True
        self.travel += x_dir
        if y_dir == 0:
            if self.travel >= 10:
                self.animation_frame += 1
                self.travel = 0
            if self.travel <= -10:
                self.animation_frame += 1
                self.travel = 0
            if self.animation_frame == 11:
                self.animation_frame = 0
        # if self.animation_frame == -1:
        #     self.animation_frame = 10

        self.x = x
        self.y = y
        self.rect.topleft = (x, y)
        self.update_image(x_dir)

    def load_animation(self, path):
        self.animation_name = path.split("/")[-1]
        for n in range(11):
            image_id = f"{self.animation_name}_{str(n)}"
            image_path = f"{path}/{image_id}.png"
            animation_image = pygame.image.load(image_path).convert_alpha()
            self.animation_images[image_id] = animation_image.copy()
