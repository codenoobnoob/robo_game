from pygame import sprite, Vector2, Surface
from gamemodules.settings import *

# only static object tested. Continue Development


class Drawable_Object(sprite.Sprite):
    def __init__(self, image: object, position: tuple, layer: int):
        sprite.Sprite.__init__(self)
        self.vec = Vector2((position[0], position[1]))
        self.image = image
        self.rect = Surface.get_rect(self.image)
        self.rect.topleft = self.vec
        self._layer = layer

    def update(self, other: object):
        self.vec += other
        self.rect.topleft = self.vec


class Static_Object(Drawable_Object):
    def __init__(self, image: object, position: tuple, layer: int, scale: int):
        super().__init__(image, (position[0]*scale, position[1]*scale), layer)


class Level_Object(Static_Object):
    def __init__(self, image: object, position: tuple, layer: int, scale: int, friction=0):
        super()._init_(image, position, layer, scale)
        self.penetrable = penetrable
        self.friction = friction


class Background_object(Static_Object):
    def __init__(self, image: object, position: tuple, layer: int, scale: int, bg_speed: float):
        super()._init_(image, position, layer, scale)
        self.bg_speed = bg_speed


class Moving_Object(Drawable_Object):
    def __init__(self, image: object, position: tuple, layer: int, movement=None):
        super().__init__(image, position, layer)
        if movement:
            movement.set_vec(self.vec)

    def update(self, world_move: Vector2, own_move: Vector2):
        self.vec -= other


class Background_object(Moving_Object):
    def __init__(self, image: object, position: tuple, layer: int, movement, bg_speed: float):
        super().__init__(image, position, layer, movement=movement)
        self.bg_speed = bg_speed


class Following_object(Moving_Object):
    def __init__(self, image: object, position: tuple, layer: int, movement):
        super().__init__(image, position, layer, movement=movement)


class Linear_move_object(Moving_Object):
    def __init__(self, image: object, position: tuple, layer: int, movement):
        super().__init__(image, position, layer, movement=movement)


class Linear_ease_object(Moving_Object):
    def __init__(self, image: object, position: tuple, layer: int, movement):
        super().__init__(image, position, layer, movement=movement)


class Player(sprite.Sprite):
    def __init__(self, image: object):
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = Vector2(WIDTH/2, HEIGHT/2)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.faceright = True
        self.update()

    def jump(self):
        self.vel.y = -20

    def update(self, controls_vec: Vector2):
        self.acc.update(0, GRAVITY)
        if abs(self.vel.x) < SPEED:
            self.acc.x = controls_vec.x*ACCELERATION*FRICTION

            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
        else:
            self.pos += self.vel

        self.rect.midbottom = self.pos
