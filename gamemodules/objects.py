from pygame import sprite, Vector2, Surface

# only static object tested. Continue Development


class Drawable_Object(sprite.Sprite):
    def __init__(self, image: object, position: tuple):
        sprite.Sprite.__init__(self)
        self.vec = Vector2()
        self.vec.update((position[0], position[1]))
        self.image = image
        self.rect = Surface.get_rect(self.image)
        self.rect.topleft = self.vec

    def update(self, other: object):
        self.vec += other
        self.rect.topleft = self.vec


class Static_Object(Drawable_Object):
    def __init__(self, image: object, position: tuple, scale: int):
        super().__init__(image, (position[0]*scale, position[1]*scale))


class Level_Object(Static_Object):
    def __init__(self, image: object, position: tuple, scale: int, friction=0):
        super()._init_(image, position, scale)
        self.penetrable = penetrable
        self.friction = friction


class Background_object(Static_Object):
    def __init__(self, image: object, position: tuple, scale: int, bg_speed: float):
        super()._init_(image, position, scale)
        self.bg_speed = bg_speed

    def update(self, other):
        self.vec -= other*self.bg_speed


class Moving_Object(Drawable_Object):
    def __init__(self, image: object, position: tuple, movement=None):
        super().__init__(image, position)
        if movement:
            movement.set_vec(self.vec)

    def update(self, move: Vector2, movement: Vector2):
        self.vec -= other


class Following_object(Moving_Object):
    def __init__(self, image: object, position: tuple, movement):
        super().__init__(image, position, movement=movement)


class Linear_move_object(Moving_Object):
    def __init__(self, image: object, position: tuple, movement):
        super().__init__(image, position, movement=movement)


class Linear_ease_object(Moving_Object):
    def __init__(self, image: object, position: tuple, movement):
        super().__init__(image, position, movement=movement)
