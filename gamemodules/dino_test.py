from pygame import Vector2, sprite, transform, Surface, image
from pygame.math import Vector2

# working class for animation objects. Maybe implement a (step setter) to set the speed of the animation. (or break apart into smaller bits, not very generic at the moment)


class Dino(sprite.Sprite):
    def __init__(self, position: tuple, animation_name: str, animation_images: dict, size: tuple):
        sprite.Sprite.__init__(self)
        self.gap = 50
        self.forward = True
        self.size = size
        self.vec = Vector2()
        self.vec.update((position[0], position[1]))
        # self.x = position[0]
        # self.y = position[1]
        self.travel = 0
        self.image_count = len(animation_images)
        self.animation_images = animation_images
        self.animation_name = animation_name
        self.animation_frame = 0
        self.image = Surface(size)
        # self.image.fill((255, 255, 255))
        # self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.vec
        self.update_image()

    def update_image(self):
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        if self.forward:
            self.image.blit(transform.flip(transform.scale(
                            self.animation_images[f"{self.animation_name}_{self.animation_frame}"], self.size), True, False), (0, 0))

        else:
            self.image.blit(transform.scale(
                self.animation_images[f"{self.animation_name}_{self.animation_frame}"], self.size), (0, 0))

    def update(self, vector: object):
        x_dir = vector.x
        y_dir = vector.y
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
            if self.animation_frame == self.image_count:
                self.animation_frame = 0

        self.vec += vector
        self.rect.topleft = self.vec
        self.update_image()
